# HTTP client of the fleet steward: retries, rate limits, Retry-After, redirects and the path guard.
# A real steward.Github runs against the scripted seams steward.urlopen and steward.time.sleep;
# no test opens a socket.

import contextlib
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
import functools
import http.client
import io
import json
import os
from pathlib import Path
import socket
import tempfile
import time
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError
import urllib.request
import urllib.response

from test_github_fleet_steward import FakeGitHub, encoded, repo, steward

API = "https://api.github.com"  # the only host a request may go to
TOKEN = "unit-test-token-0123456789"
ROUTE = "/user/repos"
PATH = ROUTE + "?affiliation=owner&per_page=100&page=2"
ISSUES = "/repos/o/r/issues"
ELSEWHERE = "https://elsewhere.example/collect"


class FakeResponse:
    """The part of http.client.HTTPResponse a client may touch: context manager, read(), close()."""

    status = 200

    def __init__(self, body=b"", read_error=None):
        self._body, self._read_error = io.BytesIO(body), read_error
        self.headers = http.client.HTTPMessage()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return False

    def close(self):
        pass

    def read(self, amt=None):
        if self._read_error is not None:
            raise self._read_error.with_traceback(None)
        return self._body.read(amt)


def reply(body=b"", read_error=None):
    """A step for `replay`: every call it serves gets a fresh 200 response."""
    return functools.partial(FakeResponse, body, read_error)


def replay(*steps):
    """Stand-in for urlopen that acts out `steps` in order and then repeats the last one for ever.

    A step is an exception to raise from urlopen itself, or a `reply(...)`.
    """
    queue = list(steps)

    def urlopen(request, timeout=None):
        step = queue.pop(0) if len(queue) > 1 else queue[0]
        if isinstance(step, BaseException):
            raise step.with_traceback(None)
        return step()

    return urlopen


def http_date(**from_now):
    """An HTTP-date (always GMT) that lies `from_now` away, e.g. http_date(seconds=30)."""
    return format_datetime(datetime.now(timezone.utc) + timedelta(**from_now), usegmt=True)


@contextlib.contextmanager
def far_from_utc():
    """Give the process a local time zone nine hours from UTC, so local-time arithmetic cannot pass by luck."""
    tzset = getattr(time, "tzset", lambda: None)  # absent on Windows
    try:
        with patch.dict(os.environ, {"TZ": "Asia/Tokyo"}):
            tzset()
            yield
    finally:
        tzset()


ANSWER = reply(b'{"login": "octocat"}')
PARSED = {"login": "octocat"}

# What http.client raises for a malformed request target: its text repeats the query string.
ECHOED_TARGET = http.client.InvalidURL(f"URL can't contain control characters. {PATH!r} (found at least ' ')")

# Ways a response can fail without an HTTP status.
TRANSIENT_FAILURES = (
    ("no answer in time", TimeoutError("timed out")),
    ("connection reset", ConnectionResetError(54, "Connection reset by peer")),
    ("server hung up", http.client.RemoteDisconnected("Remote end closed connection without response")),
    ("body cut short", reply(read_error=http.client.IncompleteRead(b'{"login": "oc', 7))),
    ("stalled in the middle of the body", reply(read_error=TimeoutError("timed out"))),
    ("truncated JSON", reply(b'{"login": "oc')),
    ("request target echoed in the error", ECHOED_TARGET),
)


class OfflineTestCase(unittest.TestCase):
    """No test may dial out: a client that slips past the seams fails here instead of reaching GitHub."""

    def setUp(self):
        for owner, name in ((socket, "getaddrinfo"), (socket.socket, "connect")):
            blocked = AssertionError("test tried to use the network")
            self.enterContext(patch.object(owner, name, side_effect=blocked))


class HttpClientCase(OfflineTestCase):
    """A real steward.Github whose seams steward.urlopen and steward.time.sleep are mocks."""

    def setUp(self):
        super().setUp()
        self.enterContext(far_from_utc())
        self.opened = self.enterContext(patch.object(steward, "urlopen"))
        self.slept = self.enterContext(patch.object(steward.time, "sleep"))
        self.api = steward.Github(TOKEN)
        self.script(ANSWER)

    def script(self, *steps):
        """Start a new scenario in which urlopen acts out `steps` (see `replay`)."""
        self.opened.reset_mock()
        self.slept.reset_mock()
        self.opened.side_effect = replay(*steps)

    def sleeps(self):
        return [call.args[0] for call in self.slept.call_args_list]

    def http_error(self, code, headers=None):
        """What urllib raises for a non-2xx answer; closed again when the test ends."""
        message = http.client.HTTPMessage()
        for name, value in (headers or {}).items():
            message[name] = value
        error = HTTPError(API + PATH, code, "status text", message, io.BytesIO())
        self.addCleanup(error.close)
        return error

    def assertLeaksNothing(self, error):
        """No error message contains the token or the query string."""
        for secret in (TOKEN, "affiliation", "per_page"):
            self.assertNotIn(secret, str(error))

    def raised(self, expected, method, path, **kwargs):
        """Make a request that must raise `expected` and return the error, already checked for leaks."""
        with self.assertRaises(expected) as caught:
            self.api.request(method, path, **kwargs)
        self.assertLeaksNothing(caught.exception)
        return caught.exception


class TransientFailureTests(HttpClientCase):
    """A stalled or dropped answer is retried for reads, never for writes."""

    def test_get_retries_after_a_transient_failure_and_returns_the_parsed_body(self):
        for label, failure in TRANSIENT_FAILURES:
            with self.subTest(label):
                self.script(failure, ANSWER)
                self.assertEqual(self.api.request("GET", PATH), PARSED)
                self.assertEqual(self.opened.call_count, 2)
                self.assertEqual(self.sleeps(), [1])

    def test_get_gives_up_after_three_transient_failures_with_a_runtime_error(self):
        for label, failure in TRANSIENT_FAILURES:
            with self.subTest(label):
                self.script(failure)
                error = self.raised(RuntimeError, "GET", PATH)
                self.assertEqual(self.opened.call_count, 3)
                self.assertEqual(self.sleeps(), [1, 2])
                self.assertNotIsInstance(error, steward.RateLimitError)

    def test_three_attempts_are_shared_by_failures_of_different_kinds(self):
        self.script(TimeoutError("timed out"), self.http_error(502), reply(b'{"login": "oc'))
        self.raised(RuntimeError, "GET", PATH)
        self.assertEqual(self.opened.call_count, 3)
        self.assertEqual(self.sleeps(), [1, 2])

    def test_write_is_sent_once_and_reports_outcome_unknown_when_the_transport_fails(self):
        unreachable = URLError(ConnectionRefusedError(61, "Connection refused"))
        for label, failure in TRANSIENT_FAILURES + (("unreachable host", unreachable),):
            with self.subTest(label):
                self.script(failure)
                error = self.raised(RuntimeError, "POST", ISSUES, payload={"title": "Review"})
                self.assertEqual(self.opened.call_count, 1)
                self.assertEqual(self.sleeps(), [])
                self.assertIn("outcome unknown", str(error))

    def test_get_retries_an_unreachable_host_with_backoff_before_giving_up(self):
        unreachable = URLError(ConnectionRefusedError(61, "Connection refused"))
        self.script(unreachable, ANSWER)
        self.assertEqual(self.api.request("GET", PATH), PARSED)
        self.assertEqual(self.sleeps(), [1])
        self.script(unreachable)
        self.raised(RuntimeError, "GET", PATH)
        self.assertEqual(self.opened.call_count, 3)
        self.assertEqual(self.sleeps(), [1, 2])


class ServerErrorTests(HttpClientCase):
    """Retryable statuses are retried for reads only."""

    def test_get_gives_up_on_a_persistent_server_error_after_three_attempts(self):
        for code in (429, 500, 502, 503, 504):
            with self.subTest(code=code):
                self.script(self.http_error(code))
                error = self.raised(RuntimeError, "GET", PATH)
                self.assertEqual(str(error), f"GitHub HTTP {code} for GET {ROUTE}")
                self.assertEqual(self.opened.call_count, 3)
                self.assertEqual(self.sleeps(), [1, 2])

    def test_write_is_never_retried_after_a_retryable_status(self):
        for method in ("POST", "PATCH"):
            for code, headers in ((502, {}), (503, {}), (429, {}), (403, {"Retry-After": "1"})):
                with self.subTest(method=method, code=code):
                    self.script(self.http_error(code, headers))
                    error = self.raised(RuntimeError, method, ISSUES, payload={"title": "Review"})
                    self.assertEqual(self.opened.call_count, 1)
                    self.assertEqual(self.sleeps(), [])
                    self.assertEqual(str(error), f"GitHub HTTP {code} for {method} {ISSUES}")


class RateLimitTests(HttpClientCase):
    """An exhausted primary rate limit is reported as such, at once."""

    RESET = datetime(2026, 11, 10, 12, 30, tzinfo=timezone.utc)

    def test_rate_limit_error_is_a_distinct_kind_of_runtime_error(self):
        self.assertTrue(issubclass(steward.RateLimitError, RuntimeError))
        self.assertIsNot(steward.RateLimitError, RuntimeError)

    def test_exhausted_rate_limit_raises_rate_limit_error_at_once_with_the_reset_time(self):
        reset = str(int(self.RESET.timestamp()))
        rows = (
            (403, {"x-ratelimit-remaining": "0", "x-ratelimit-reset": reset}),
            (429, {"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": reset}),
            (429, {"x-ratelimit-remaining": "0", "x-ratelimit-reset": reset, "Retry-After": "5"}),  # 2.3b before 2.3d
        )
        for code, headers in rows:
            with self.subTest(code=code, headers=sorted(headers)):
                self.script(self.http_error(code, headers))
                error = self.raised(RuntimeError, "GET", PATH)
                self.assertEqual(self.opened.call_count, 1)
                self.assertEqual(self.sleeps(), [])
                self.assertIn("rate limit", str(error))
                self.assertRegex(str(error), r"2026-11-10T12:30(:00)?(\+00:00|Z)")
                self.assertIsInstance(error, steward.RateLimitError)

    def test_exhausted_rate_limit_is_reported_even_without_a_usable_reset_time(self):
        for reset in ({}, {"x-ratelimit-reset": "soon"}, {"x-ratelimit-reset": "9" * 30}):
            with self.subTest(reset=reset):
                self.script(self.http_error(403, {"x-ratelimit-remaining": "0", **reset}))
                error = self.raised(RuntimeError, "GET", PATH)
                self.assertEqual(self.opened.call_count, 1)
                self.assertEqual(self.sleeps(), [])
                self.assertIn("rate limit", str(error))
                self.assertIsInstance(error, steward.RateLimitError)

    def test_forbidden_without_an_exhausted_limit_or_retry_after_fails_at_once_as_a_plain_error(self):
        for headers in ({}, {"x-ratelimit-remaining": "4999", "x-ratelimit-reset": "1794313800"}):
            with self.subTest(headers=headers):
                self.script(self.http_error(403, headers))
                error = self.raised(RuntimeError, "GET", PATH)
                self.assertIs(type(error), RuntimeError)
                self.assertEqual(str(error), f"GitHub HTTP 403 for GET {ROUTE}")
                self.assertEqual(self.opened.call_count, 1)
                self.assertEqual(self.sleeps(), [])

    def test_zero_budget_on_any_other_status_is_not_a_rate_limit_error(self):
        spent = {"x-ratelimit-remaining": "0"}
        self.script(self.http_error(404, spent))
        self.assertIsNone(self.api.request("GET", PATH, optional=True))
        for code, attempts in ((404, 1), (500, 3)):
            with self.subTest(code=code):
                self.script(self.http_error(code, spent))
                error = self.raised(RuntimeError, "GET", PATH)
                self.assertIs(type(error), RuntimeError)
                self.assertEqual(str(error), f"GitHub HTTP {code} for GET {ROUTE}")
                self.assertEqual(self.opened.call_count, attempts)


class RetryAfterTests(HttpClientCase):
    """The server's Retry-After is obeyed in both of its forms, or refused."""

    def test_delay_of_up_to_sixty_seconds_is_slept_exactly(self):
        for code, seconds in ((429, 1), (503, 20), (429, 30), (403, 60)):
            with self.subTest(code=code, seconds=seconds):
                self.script(self.http_error(code, {"Retry-After": str(seconds)}), ANSWER)
                self.assertEqual(self.api.request("GET", PATH), PARSED)
                self.assertEqual(self.sleeps(), [seconds])

    def test_http_date_is_converted_to_seconds_from_now(self):
        self.script(self.http_error(429, {"Retry-After": http_date(seconds=30)}), ANSWER)
        self.assertEqual(self.api.request("GET", PATH), PARSED)
        delays = self.sleeps()
        self.assertEqual(len(delays), 1, delays)
        self.assertTrue(20 <= delays[0] <= 31, delays)

    def test_http_date_in_the_past_waits_the_minimum_of_one_second(self):
        overdue = self.http_error(429, {"Retry-After": "Wed, 21 Oct 2015 07:28:00 GMT"})
        self.script(overdue, overdue, ANSWER)
        self.assertEqual(self.api.request("GET", PATH), PARSED)
        self.assertEqual(self.sleeps(), [1, 1])  # exponential back-off would have slept 1 and 2

    def test_unparseable_value_falls_back_to_exponential_backoff(self):
        for garbage in ("soon", "", "3 seconds"):
            with self.subTest(garbage=garbage):
                unparseable = self.http_error(503, {"Retry-After": garbage})
                self.script(unparseable, unparseable, ANSWER)
                self.assertEqual(self.api.request("GET", PATH), PARSED)
                self.assertEqual(self.sleeps(), [1, 2])

    def test_delay_above_sixty_seconds_raises_rate_limit_error_without_sleeping(self):
        rows = ((429, "61", "61"), (403, "3600", "3600"), (503, "120", "120"),
                (429, http_date(hours=1), r"35\d\d|360[01]"))
        for code, retry_after, seconds in rows:
            with self.subTest(code=code, retry_after=retry_after):
                self.script(self.http_error(code, {"Retry-After": retry_after}))
                error = self.raised(RuntimeError, "GET", PATH)
                self.assertEqual(self.opened.call_count, 1)
                self.assertEqual(self.sleeps(), [])
                self.assertRegex(str(error), seconds)
                self.assertIsInstance(error, steward.RateLimitError)


class RedirectStatusTests(HttpClientCase):
    """A redirect status is an error to report, never to retry."""

    def test_redirect_status_is_reported_at_once_as_a_redirect(self):
        for method, path in (("GET", PATH), ("POST", ISSUES)):
            for code in (301, 302, 303, 307, 308):
                with self.subTest(method=method, code=code):
                    self.script(self.http_error(code, {"Location": ELSEWHERE}))
                    error = self.raised(RuntimeError, method, path)
                    self.assertEqual(self.opened.call_count, 1)
                    self.assertEqual(self.sleeps(), [])
                    self.assertIn(str(code), str(error))
                    self.assertIn("redirect", str(error))
                    self.assertNotIsInstance(error, steward.RateLimitError)


def outgoing(method):
    """A request as the client builds it: bearer token, and a JSON body when it is a write."""
    return urllib.request.Request(API + ISSUES, method=method, data=b"{}" if method == "POST" else None,
                                  headers={"Authorization": "Bearer " + TOKEN})


def redirect_answer(code):
    """What an HTTPS transport hands urllib for a redirect: the status, a Location header, no body."""
    headers = http.client.HTTPMessage()
    headers["Location"] = ELSEWHERE
    answer = urllib.response.addinfourl(io.BytesIO(), headers, API + ISSUES, code)
    answer.msg = "Moved"
    return answer


class RedirectWiringTests(OfflineTestCase):
    """The real steward.urlopen is an opener that cannot follow a redirect."""

    def test_no_redirect_handler_declines_every_redirect(self):
        handler = steward.NoRedirectHandler()
        self.assertIsInstance(handler, urllib.request.HTTPRedirectHandler)
        for method in ("GET", "POST"):
            for code in (301, 302, 303, 307, 308):
                with self.subTest(method=method, code=code):
                    follow_up = handler.redirect_request(outgoing(method), io.BytesIO(), code, "Moved",
                                                         http.client.HTTPMessage(), ELSEWHERE)
                    self.assertIsNone(follow_up)

    def test_urlopen_is_the_open_method_of_an_opener_whose_redirect_handler_declines(self):
        opener = getattr(steward.urlopen, "__self__", None)
        self.assertIsInstance(opener, urllib.request.OpenerDirector)
        self.assertEqual(steward.urlopen, opener.open)
        redirect_handlers = [h for h in opener.handlers if isinstance(h, urllib.request.HTTPRedirectHandler)]
        self.assertTrue(redirect_handlers)
        for handler in redirect_handlers:
            self.assertIsInstance(handler, steward.NoRedirectHandler)

    def test_redirect_answer_is_never_followed_on_the_wire(self):
        for method, code in (("POST", 302), ("GET", 301), ("GET", 307)):
            with self.subTest(method=method, code=code):
                sent = []

                def https_open(handler, request):
                    sent.append((request.get_method(), request.full_url))
                    if len(sent) > 1:
                        self.fail(f"redirect followed: {request.get_method()} {request.full_url} "
                                  f"(body kept: {request.data is not None}, "
                                  f"Authorization sent: {request.has_header('Authorization')})")
                    return redirect_answer(code)

                # Only the HTTPS transport is replaced; proxies are bypassed so that it is always reached.
                with patch.object(urllib.request.HTTPSHandler, "https_open", https_open), \
                        patch.object(urllib.request, "proxy_bypass", return_value=True), \
                        self.assertRaises(HTTPError) as caught:
                    steward.urlopen(outgoing(method), timeout=5)
                caught.exception.close()
                self.assertEqual(caught.exception.code, code)
                self.assertEqual(sent, [(method, API + ISSUES)])


class PathGuardTests(HttpClientCase):
    """Dot segments are refused, names that merely contain dots are not."""

    def test_names_containing_dots_reach_urlopen(self):
        paths = (
            "/repos/o/a..b/contents/README..md",
            "/repos/o/.github/contents/..env",
            "/repos/o/r/issues?labels=a..b&since=..&next=//c",  # the guard looks at the part before "?"
        )
        for path in paths:
            with self.subTest(path=path):
                self.script(ANSWER)
                self.assertEqual(self.api.request("GET", path), PARSED)
                self.assertEqual([call.args[0].full_url for call in self.opened.call_args_list], [API + path])

    def test_single_dot_segment_is_refused_before_any_request(self):
        for path in ("/repos/o/./x", "/repos/o/r/.", "/./user", "/repos/o/r/contents/.?ref=main"):
            with self.subTest(path=path):
                self.script(ANSWER)
                with self.assertRaises(ValueError) as caught:
                    self.api.request("GET", path)
                self.assertEqual(str(caught.exception), "Invalid GitHub API path")
                self.opened.assert_not_called()

    def test_traversal_and_malformed_paths_are_refused_before_any_request(self):
        paths = ("/repos/o/../x", "/repos/o/r/..", "/repos/o/r/contents/..?ref=main", "//x", "/repos//x",
                 "repos/x", "", "https://elsewhere.example/x", "/a#b")
        for path in paths:
            with self.subTest(path=path):
                self.script(ANSWER)
                with self.assertRaises(ValueError) as caught:
                    self.api.request("GET", path)
                self.assertEqual(str(caught.exception), "Invalid GitHub API path")
                self.opened.assert_not_called()


class UnchangedBehaviourTests(HttpClientCase):
    """Behaviour the hardening must keep: the urlopen seam, optional 404, empty bodies and clean error messages."""

    def test_get_hands_urlopen_one_authenticated_request_and_its_timeout(self):
        self.assertEqual(steward.Github(TOKEN, timeout=7).get(PATH), PARSED)
        self.assertEqual(self.opened.call_count, 1)
        call = self.opened.call_args
        self.assertEqual((len(call.args), call.kwargs), (1, {"timeout": 7}))
        request = call.args[0]
        self.assertEqual((request.get_method(), request.full_url), ("GET", API + PATH))
        self.assertEqual(request.get_header("Authorization"), "Bearer " + TOKEN)
        self.assertIsNone(request.data)

    def test_post_sends_its_payload_once_as_json(self):
        self.script(reply(b'{"number": 7}'))
        self.assertEqual(self.api.post(ISSUES, {"title": "Review"}), {"number": 7})
        self.assertEqual(self.opened.call_count, 1)
        request = self.opened.call_args.args[0]
        self.assertEqual((request.get_method(), request.full_url), ("POST", API + ISSUES))
        self.assertEqual(json.loads(request.data), {"title": "Review"})
        self.assertEqual(request.get_header("Content-type"), "application/json")

    def test_optional_404_returns_none_and_required_404_raises(self):
        missing = self.http_error(404)
        self.script(missing)
        self.assertIsNone(self.api.request("GET", PATH, optional=True))
        self.assertEqual((self.opened.call_count, self.sleeps()), (1, []))
        self.script(missing)
        error = self.raised(RuntimeError, "GET", PATH)
        self.assertEqual(str(error), f"GitHub HTTP 404 for GET {ROUTE}")
        self.assertEqual((self.opened.call_count, self.sleeps()), (1, []))

    def test_empty_body_returns_none(self):
        self.script(reply(b""))
        self.assertIsNone(self.api.request("GET", PATH))
        self.assertEqual(self.opened.call_count, 1)

    def test_error_messages_never_contain_the_token_or_the_query_string(self):
        failures = (
            ("forbidden", self.http_error(403)),
            ("not found", self.http_error(404)),
            ("server error on every attempt", self.http_error(500)),
            ("unreachable host", URLError(ConnectionRefusedError(61, "Connection refused"))),
        )
        for label, failure in failures:
            with self.subTest(label):
                self.script(failure)
                with self.assertRaises(RuntimeError) as caught:
                    self.api.request("GET", PATH)
                self.assertLeaksNothing(caught.exception)


class StalledScanTests(HttpClientCase):
    """End to end: a real scan through the real client, in which one answer stalls once."""

    LISTING = "/users/borjamoskv/repos?sort=full_name&direction=asc&per_page=100&page=1"
    CONTENTS = "/repos/borjamoskv/alpha/contents"

    def test_scan_completes_when_one_response_stalls_once(self):
        account = FakeGitHub({
            self.LISTING: [repo("alpha")],
            self.CONTENTS: [{"name": "README.md", "type": "file"}],
            self.CONTENTS + "/README.md": encoded("# Alpha\n"),
        })
        undisturbed = json.loads(json.dumps(steward.inspect_repo(account, repo("alpha"), {"alpha": "alpha"})))
        self.assertEqual((undisturbed["root_scanned"], undisturbed["errors"], undisturbed["files_checked"]),
                         (True, [], ["README.md"]))
        requested = []

        def urlopen(request, timeout=None):
            """Serve the fake account over HTTP: unknown paths are 404s and CONTENTS times out once."""
            path = request.selector
            requested.append(path)
            if path == self.CONTENTS and requested.count(path) == 1:
                raise TimeoutError("timed out")
            answer = account.get(path)
            if answer is None:
                raise self.http_error(404)
            return FakeResponse(json.dumps(answer).encode())

        self.opened.side_effect = urlopen
        out, err = io.StringIO(), io.StringIO()
        with tempfile.TemporaryDirectory() as tmp:
            reports = Path(tmp) / "reports"
            argv = ["scan", "--scope", "public", "--owner", "borjamoskv", "--workers", "1", "--out", str(reports)]
            with patch.object(steward, "auth_token", return_value=TOKEN), \
                    patch.object(steward.Path, "home", return_value=Path(tmp)), \
                    contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = steward.main(argv)
            self.assertEqual(code, 0, err.getvalue())
            inventory = json.loads((reports / "inventory.json").read_text(encoding="utf-8"))
        self.assertIn("[READ-ONLY] 1 repositories; 1 inspected", out.getvalue())
        self.assertEqual(requested.count(self.CONTENTS), 2)
        self.assertEqual(self.sleeps(), [1])
        self.assertEqual(inventory["inspections"], [undisturbed])  # the stall left no trace


if __name__ == "__main__":
    unittest.main()
