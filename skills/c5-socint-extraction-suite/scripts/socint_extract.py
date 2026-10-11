#!/usr/bin/env python3
"""
socint_extract.py - Suite Soberana de Inteligencia Social (SOCINT C5-REAL)
Motor autónomo de extracción, normalización, detección de astroturfing y auditoría
epistemológica de telemetría discursiva en X (Twitter), Substack, Reddit y YouTube (stdlib pura).
"""

import sys
import os
import re
import math
import json
import time
import html
import sqlite3
import argparse
from datetime import datetime, timezone
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
DEFAULT_DB_PATH = os.path.expanduser("~/.gemini/antigravity/socint_vault.db")

# -----------------------------------------------------------------------------
# HTTP Helpers & Resilient Fetcher
# -----------------------------------------------------------------------------

def http_get(url, headers=None, timeout=12, max_retries=2):
    req_headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/html, application/xml, */*",
        "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
    }
    if headers:
        req_headers.update(headers)

    req = urllib.request.Request(url, headers=req_headers)
    last_err = None

    for attempt in range(max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.status
                content_type = resp.headers.get("Content-Type", "")
                charset = "utf-8"
                if "charset=" in content_type.lower():
                    charset = content_type.lower().split("charset=")[-1].split(";")[0].strip()
                data = resp.read()
                try:
                    text = data.decode(charset)
                except Exception:
                    text = data.decode("utf-8", errors="replace")
                return status, text, resp.headers
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in (429, 500, 502, 503, 504) and attempt < max_retries:
                time.sleep(1.5 * (attempt + 1))
                continue
            break
        except Exception as e:
            last_err = e
            if attempt < max_retries:
                time.sleep(1.0 * (attempt + 1))
                continue
            break

    raise RuntimeError(f"Error HTTP al conectar con {url}: {last_err}")


def calculate_shannon_entropy(counter_dict):
    """Calcula la entropía de Shannon H = -sum(p_i * log2(p_i)) sobre una distribución de frecuencias."""
    total = sum(counter_dict.values())
    if total <= 0:
        return 0.0
    entropy = 0.0
    for count in counter_dict.values():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    return round(entropy, 3)


# -----------------------------------------------------------------------------
# Epistemic Classifier & Astroturf Detection Engine (C5-REAL Standard)
# -----------------------------------------------------------------------------

class EpistemicClassifier:
    """Clasifica afirmaciones discursivas en las 4 categorías epistemológicas de C5-REAL."""

    FACT_PATTERNS = [
        r"\b(?:github\.com/[a-zA-Z0-9_\-\.]+/[a-zA-Z0-9_\-\.]+)\b",
        r"\b(?:0x[a-fA-F0-9]{40,64})\b",
        r"\b(?:sha256|[a-f0-9]{64})\b",
        r"\b(?:doi:\s*10\.\d{4,9}/[-._;()/:A-Z0-9]+)\b",
        r"\b(?:rfc\s*\d+|iso\s*\d+|ieee\s*\d+)\b",
        r"\b(?:sentencia|ley\s*\d+/\d+|borme|boe|decreto)\b",
        r"\b(?:v\d+\.\d+\.\d+|commit\s+[0-9a-f]{7,40})\b",
    ]

    EXPERIMENTAL_PATTERNS = [
        r"\b(?:\d+(?:\.\d+)?\s*(?:ms|us|ns|fps|tokens?/s|gb/s|mb/s|kb/s|hz|khz|mhz|ghz))\b",
        r"\b(?:\d+(?:\.\d+)?%\s*(?:latencia|throughput|acierto|accuracy|p99|p95|error rate|cpu|ram))\b",
        r"\b(?:benchmark|telemetr[ií]a|ab test|a/b testing|p99|p95|latency|sample size|n\s*=\s*\d+)\b",
        r"\b(?:\$\d+(?:\.\d+)?(?:k|m|b)?\s*(?:arr|mrr|coste|cost|gasto|ahorro))\b",
    ]

    MODEL_PATTERNS = [
        r"\b(?:arquitectura|paradigma|heur[ií]stica|teorema|axioma|morfismo|isomorfismo)\b",
        r"\b(?:markov|fisher|chentsov|landauer|shannon|bayes|fsm|invariante|atractor)\b",
        r"\b(?:pipeline|framework|metodolog[ií]a|diseño|topolog[ií]a|patr[oó]n|abstracci[oó]n)\b",
    ]

    SPECULATION_PATTERNS = [
        r"\b(?:garantizado|100x|revolucionar[aá]|cambiar[aá] el mundo|game[- ]changer)\b",
        r"\b(?:sin duda|todo el mundo sabe|f[aá]cilmente|secreto de|hacerte rico)\b",
        r"\b(?:alucina con|no te lo vas a creer|hilo imprescindible|el futuro de)\b",
        r"\b(?:seg[uú]n mi intuici[oó]n|creo firmemente|predicci[oó]n para \d{4})\b",
    ]

    @classmethod
    def classify_text(cls, text):
        sentences = [s.strip() for s in re.split(r'[\.\n\r]+', text) if len(s.strip()) > 15]

        facts = []
        experimental = []
        models = []
        speculation = []

        for s in sentences:
            s_lower = s.lower()
            if any(re.search(p, s_lower, re.IGNORECASE) for p in cls.FACT_PATTERNS):
                facts.append(s)
            elif any(re.search(p, s_lower, re.IGNORECASE) for p in cls.EXPERIMENTAL_PATTERNS):
                experimental.append(s)
            elif any(re.search(p, s_lower, re.IGNORECASE) for p in cls.MODEL_PATTERNS):
                models.append(s)
            elif any(re.search(p, s_lower, re.IGNORECASE) for p in cls.SPECULATION_PATTERNS):
                speculation.append(s)

        total_classified = len(facts) + len(experimental) + len(models) + len(speculation)
        grounded = len(facts) + len(experimental) + len(models)

        if total_classified == 0:
            signal_ratio = 0.50
        else:
            signal_ratio = round(grounded / (grounded + (len(speculation) * 1.5)), 3)

        return {
            "counts": {
                "hechos_verificados": len(facts),
                "evidencia_experimental": len(experimental),
                "modelos_doctrina": len(models),
                "especulacion_sesgo": len(speculation),
            },
            "signal_ratio": min(1.0, max(0.0, signal_ratio)),
            "samples": {
                "hechos": facts[:3],
                "experimental": experimental[:3],
                "modelos": models[:3],
                "especulacion": speculation[:3],
            }
        }


class AstroturfDetector:
    """Detecta campañas de astroturfing y bots analizando similitud léxica Jaccard y ratios de autor."""

    @staticmethod
    def _get_ngrams(text, n=3):
        tokens = re.findall(r'\b\w+\b', text.lower())
        if len(tokens) < n:
            return set(tokens)
        return set(" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1))

    @classmethod
    def analyze_comments(cls, comments):
        if not comments or len(comments) < 4:
            return {
                "astroturf_risk_score": 0.0,
                "duplicate_clusters": 0,
                "author_concentration": 0.0,
                "verdict": "DATOS INSUFICIENTES (Muestra reducida)",
            }

        authors = [c.get("author") for c in comments if c.get("author") not in (None, "[deleted]", "[removed]")]
        unique_authors = set(authors)
        author_concentration = round(1.0 - (len(unique_authors) / max(1, len(authors))), 2)

        ngrams_list = [cls._get_ngrams(c.get("body", "")) for c in comments]
        duplicate_pairs = 0
        pair_matches = []

        for i in range(len(comments)):
            if len(ngrams_list[i]) < 3:
                continue
            for j in range(i + 1, len(comments)):
                if len(ngrams_list[j]) < 3:
                    continue
                intersection = len(ngrams_list[i].intersection(ngrams_list[j]))
                union = len(ngrams_list[i].union(ngrams_list[j]))
                if union > 0:
                    sim = intersection / union
                    if sim > 0.60:
                        duplicate_pairs += 1
                        pair_matches.append({
                            "author_a": comments[i].get("author"),
                            "author_b": comments[j].get("author"),
                            "similarity": round(sim, 2),
                            "sample": comments[i].get("body", "")[:80]
                        })

        total_pairs = max(1, (len(comments) * (len(comments) - 1)) // 2)
        pair_ratio = duplicate_pairs / total_pairs

        risk_score = round(min(1.0, (author_concentration * 0.35) + (pair_ratio * 0.65 * 2.0)), 2)

        if risk_score >= 0.55:
            verdict = "⚠️ ALTO RIESGO DE ASTROTURFING (Campaña artificial detectada)"
        elif risk_score >= 0.25:
            verdict = "⚠️ RIESGO MODERADO (Repetición léxica o saturación de autor)"
        else:
            verdict = "✅ DISCUSIÓN ORGÁNICA (Baja correlación sintética)"

        return {
            "astroturf_risk_score": risk_score,
            "duplicate_clusters": duplicate_pairs,
            "author_concentration": author_concentration,
            "verdict": verdict,
            "suspicious_pairs": pair_matches[:5],
        }


# -----------------------------------------------------------------------------
# ADAPTER 1: X (Twitter) Engine con Unfolding de Hilos
# -----------------------------------------------------------------------------

class XAdapter:
    """Extrae tweets, perfiles y desenrolla hilos completos en X vía FixTweet y sindicación."""

    FX_API = "https://api.fxtwitter.com"
    SYNDICATION_API = "https://cdn.syndication.twimg.com/tweet-result"

    @staticmethod
    def parse_url(url_or_id):
        m = re.search(r"(?:twitter|x|fxtwitter|vxtwitter)\.com/([a-zA-Z0-9_]+)/status/(\d+)", url_or_id)
        if m:
            return "tweet", m.group(1), m.group(2)
        m_profile = re.search(r"(?:twitter|x|fxtwitter|vxtwitter)\.com/([a-zA-Z0-9_]+)/?$", url_or_id)
        if m_profile and m_profile.group(1) not in ("home", "explore", "messages", "search"):
            return "profile", m_profile.group(1), None
        m_id = re.search(r"^\d+$", url_or_id.strip())
        if m_id:
            return "tweet", "user", m_id.group(0)
        return None, None, None

    @classmethod
    def fetch_profile(cls, username):
        url = f"{cls.FX_API}/{username}"
        status, body, _ = http_get(url)
        data = json.loads(body)
        if data.get("code") == 200 and "user" in data:
            u = data["user"]
            ver = u.get("verification", {}) or {}
            return {
                "platform": "x",
                "type": "profile",
                "screen_name": u.get("screen_name"),
                "name": u.get("name"),
                "url": u.get("url"),
                "followers": u.get("followers") or 0,
                "following": u.get("following") or 0,
                "likes": u.get("likes") or 0,
                "tweets_count": u.get("tweets") or 0,
                "media_count": u.get("media_count") or 0,
                "joined": u.get("joined"),
                "description": u.get("description", ""),
                "verified": ver.get("verified", False),
                "verification_type": ver.get("type", "none"),
                "avatar_url": u.get("avatar_url"),
            }
        raise RuntimeError(f"No se pudo obtener el perfil de @{username} en X.")

    @classmethod
    def fetch_tweet(cls, user, tweet_id):
        for fx_url in [f"{cls.FX_API}/status/{tweet_id}", f"{cls.FX_API}/{user}/status/{tweet_id}"]:
            try:
                status, body, _ = http_get(fx_url, timeout=10)
                data = json.loads(body)
                if data.get("code") == 200 and "tweet" in data and data["tweet"]:
                    return cls._normalize_fx_tweet(data["tweet"])
            except Exception:
                continue

        # Fallback a Twimg Syndication
        try:
            token = f"{(int(tweet_id) / 1e15) * 3.14159:.0f}"
            synd_url = f"{cls.SYNDICATION_API}?id={tweet_id}&token={token}"
            status, body, _ = http_get(synd_url, timeout=10)
            data = json.loads(body)
            if "text" in data:
                return cls._normalize_syndication_tweet(data)
        except Exception:
            pass

        # Fallback a Jina Reader
        jina_url = f"https://r.jina.ai/https://x.com/{user}/status/{tweet_id}"
        try:
            status, body, _ = http_get(jina_url, timeout=12)
            if body and len(body) > 100:
                return cls._normalize_jina_x(body, user, tweet_id)
        except Exception as e:
            raise RuntimeError(f"Fallo en todos los adaptadores para X (Tweet {tweet_id}): {e}")

        raise RuntimeError(f"No se pudo extraer el tweet {tweet_id} de X.")

    @classmethod
    def unfold_thread(cls, user, tweet_id, max_depth=15):
        """Desenrolla un hilo de tweets ascendiendo a la raíz y concatenando respuestas del autor."""
        visited_ids = set()
        thread_chain = []
        current_id = tweet_id
        author_screen_name = user

        # 1. Recuperar tweet inicial
        initial_tweet = cls.fetch_tweet(user, current_id)
        thread_chain.append(initial_tweet)
        visited_ids.add(initial_tweet["id"])
        author_screen_name = initial_tweet["author"]["screen_name"]

        # 2. Ascender si es respuesta a otro tweet del mismo autor
        parent_id = initial_tweet.get("replying_to")
        depth = 0
        while parent_id and parent_id not in visited_ids and depth < max_depth:
            try:
                parent_tweet = cls.fetch_tweet(author_screen_name, parent_id)
                if parent_tweet["author"]["screen_name"].lower() == author_screen_name.lower():
                    thread_chain.insert(0, parent_tweet)
                    visited_ids.add(parent_id)
                    parent_id = parent_tweet.get("replying_to")
                    depth += 1
                else:
                    break
            except Exception:
                break

        full_text = "\n\n".join(f"[{i+1}/{len(thread_chain)}] {t['text']}" for i, t in enumerate(thread_chain))

        return {
            "platform": "x",
            "type": "thread",
            "id": tweet_id,
            "root_id": thread_chain[0]["id"],
            "author": thread_chain[0]["author"],
            "url": thread_chain[0]["url"],
            "total_tweets": len(thread_chain),
            "tweets": thread_chain,
            "text": full_text,
            "metrics": {
                "total_likes": sum(t["metrics"]["likes"] for t in thread_chain),
                "total_retweets": sum(t["metrics"]["retweets"] for t in thread_chain),
                "total_replies": sum(t["metrics"]["replies"] for t in thread_chain),
                "total_views": sum(t["metrics"]["views"] for t in thread_chain),
            }
        }

    @classmethod
    def _normalize_fx_tweet(cls, t):
        author = t.get("author", {}) or {}
        media_list = []
        if "media" in t and t["media"]:
            if "photos" in t["media"] and t["media"]["photos"]:
                for p in t["media"]["photos"]:
                    media_list.append({"type": "photo", "url": p.get("url")})
            if "videos" in t["media"] and t["media"]["videos"]:
                for v in t["media"]["videos"]:
                    media_list.append({"type": "video", "url": v.get("url")})

        quoted = None
        if "quote" in t and t["quote"]:
            q = t["quote"]
            q_author = q.get("author", {}) or {}
            quoted = {
                "author": q_author.get("name"),
                "screen_name": q_author.get("screen_name"),
                "text": q.get("text"),
                "id": q.get("id"),
                "url": q.get("url"),
            }

        return {
            "platform": "x",
            "type": "tweet",
            "id": t.get("id"),
            "url": t.get("url") or f"https://x.com/{author.get('screen_name')}/status/{t.get('id')}",
            "created_at": t.get("created_at"),
            "timestamp": t.get("created_timestamp"),
            "author": {
                "name": author.get("name") or author.get("screen_name"),
                "screen_name": author.get("screen_name"),
                "avatar_url": author.get("avatar_url"),
                "followers": author.get("followers") or 0,
                "following": author.get("following") or 0,
            },
            "text": t.get("text", ""),
            "metrics": {
                "likes": t.get("likes") or 0,
                "retweets": t.get("retweets") or 0,
                "replies": t.get("replies") or 0,
                "views": t.get("views") or 0,
            },
            "replying_to": t.get("replying_to_status"),
            "quoted_tweet": quoted,
            "media": media_list,
        }

    @classmethod
    def _normalize_syndication_tweet(cls, t):
        user = t.get("user", {}) or {}
        return {
            "platform": "x",
            "type": "tweet",
            "id": t.get("id_str"),
            "url": f"https://x.com/{user.get('screen_name', 'i')}/status/{t.get('id_str')}",
            "created_at": t.get("created_at"),
            "timestamp": None,
            "author": {
                "name": user.get("name"),
                "screen_name": user.get("screen_name"),
                "avatar_url": user.get("profile_image_url_https"),
                "followers": 0,
                "following": 0,
            },
            "text": t.get("text", ""),
            "metrics": {
                "likes": t.get("favorite_count") or 0,
                "retweets": t.get("conversation_count") or 0,
                "replies": 0,
                "views": 0,
            },
            "replying_to": t.get("in_reply_to_status_id_str"),
            "quoted_tweet": None,
            "media": [],
        }

    @classmethod
    def _normalize_jina_x(cls, text, user, tweet_id):
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        body_text = "\n".join(lines[:30])
        return {
            "platform": "x",
            "type": "tweet",
            "id": tweet_id,
            "url": f"https://x.com/{user}/status/{tweet_id}",
            "created_at": None,
            "timestamp": None,
            "author": {
                "name": user,
                "screen_name": user,
                "avatar_url": None,
                "followers": 0,
                "following": 0,
            },
            "text": body_text,
            "metrics": {"likes": 0, "retweets": 0, "replies": 0, "views": 0},
            "replying_to": None,
            "quoted_tweet": None,
            "media": [],
        }


# -----------------------------------------------------------------------------
# ADAPTER 2: Substack Engine
# -----------------------------------------------------------------------------

class SubstackAdapter:
    """Extrae publicaciones, newsletters, comentarios y audita PODs de recomendación."""

    @staticmethod
    def parse_url(url):
        u = url.strip()
        parsed = urllib.parse.urlparse(u)
        hostname = parsed.netloc.lower()

        note_m = re.search(r"substack\.com/@([a-zA-Z0-9_\-\.]+)/note/([a-zA-Z0-9_\-]+)", u)
        if note_m:
            return {"type": "note", "user": note_m.group(1), "note_id": note_m.group(2), "domain": hostname}

        post_m = re.search(r"/p/([a-zA-Z0-9_\-]+)", parsed.path)
        slug = post_m.group(1) if post_m else None

        subdomain_m = re.search(r"^([a-zA-Z0-9_\-]+)\.substack\.com", hostname)
        pub_name = subdomain_m.group(1) if subdomain_m else hostname

        return {
            "type": "post" if slug else "publication",
            "domain": hostname,
            "publication": pub_name,
            "slug": slug,
        }

    @classmethod
    def fetch_publication_archive(cls, domain, limit=25, offset=0):
        url = f"https://{domain}/api/v1/archive?sort=new&limit={limit}&offset={offset}"
        try:
            status, body, _ = http_get(url)
            posts_raw = json.loads(body)
            results = []
            for p in posts_raw:
                author_name = None
                if p.get("primary_author"):
                    author_name = p["primary_author"].get("name")
                elif p.get("published_by"):
                    author_name = p["published_by"].get("name")

                results.append({
                    "id": p.get("id"),
                    "title": p.get("title"),
                    "subtitle": p.get("subtitle"),
                    "slug": p.get("slug"),
                    "canonical_url": p.get("canonical_url"),
                    "post_date": p.get("post_date"),
                    "audience": p.get("audience"),
                    "word_count": p.get("wordcount") or 0,
                    "reaction_count": (p.get("reactions") or {}).get("❤", 0),
                    "comments_count": p.get("comment_count") or 0,
                    "author": author_name or domain,
                })
            return {
                "platform": "substack",
                "type": "archive",
                "domain": domain,
                "total_fetched": len(results),
                "posts": results,
            }
        except Exception:
            return cls.fetch_rss_feed(domain, limit=limit)

    @classmethod
    def fetch_rss_feed(cls, domain, limit=25):
        rss_url = f"https://{domain}/feed"
        status, body, _ = http_get(rss_url)
        root = ET.fromstring(body)
        channel = root.find("channel")
        items = channel.findall("item") if channel is not None else []
        results = []
        for it in items[:limit]:
            title = it.findtext("title") or "Sin título"
            link = it.findtext("link") or ""
            pub_date = it.findtext("pubDate") or ""
            creator = it.findtext("{http://purl.org/dc/elements/1.1/}creator") or domain
            results.append({
                "id": link,
                "title": title,
                "subtitle": "",
                "slug": link.split("/p/")[-1] if "/p/" in link else "",
                "canonical_url": link,
                "post_date": pub_date,
                "audience": "everyone",
                "word_count": 0,
                "reaction_count": 0,
                "comments_count": 0,
                "author": creator,
            })
        return {
            "platform": "substack",
            "type": "archive",
            "domain": domain,
            "total_fetched": len(results),
            "posts": results,
        }

    @classmethod
    def fetch_post(cls, domain, slug, fetch_comments=True):
        url = f"https://{domain}/api/v1/posts/{slug}"
        try:
            status, body, _ = http_get(url)
            p = json.loads(body)
            raw_html = p.get("body_html", "")
            text_clean = cls._clean_html(raw_html)
            author = (p.get("primary_author") or {}).get("name") or domain
            post_id = p.get("id")

            comments = []
            if fetch_comments and post_id:
                try:
                    c_url = f"https://{domain}/api/v1/posts/{post_id}/comments?all_comments=true"
                    c_status, c_body, _ = http_get(c_url, timeout=8)
                    c_data = json.loads(c_body)
                    for comment in c_data.get("comments", [])[:30]:
                        c_user = comment.get("user", {}) or {}
                        comments.append({
                            "author": c_user.get("name") or "[reader]",
                            "body": cls._clean_html(comment.get("body", "")),
                            "likes": comment.get("reactions", {}).get("❤", 0),
                            "date": comment.get("date"),
                        })
                except Exception:
                    pass

            return {
                "platform": "substack",
                "type": "post",
                "id": post_id,
                "title": p.get("title"),
                "subtitle": p.get("subtitle") or "",
                "slug": p.get("slug"),
                "canonical_url": p.get("canonical_url") or f"https://{domain}/p/{slug}",
                "post_date": p.get("post_date"),
                "author": author,
                "word_count": p.get("wordcount") or len(text_clean.split()),
                "likes": (p.get("reactions") or {}).get("❤", 0),
                "comments_count": p.get("comment_count") or len(comments),
                "paywalled": p.get("audience") != "everyone",
                "content": text_clean,
                "comments": comments,
            }
        except Exception:
            jina_url = f"https://r.jina.ai/https://{domain}/p/{slug}"
            status, body, _ = http_get(jina_url)
            return {
                "platform": "substack",
                "type": "post",
                "id": None,
                "title": slug,
                "subtitle": "",
                "slug": slug,
                "canonical_url": f"https://{domain}/p/{slug}",
                "post_date": None,
                "author": domain,
                "word_count": len(body.split()),
                "likes": 0,
                "comments_count": 0,
                "paywalled": False,
                "content": body,
                "comments": [],
            }

    @classmethod
    def audit_recommendation_network(cls, domain):
        url = f"https://{domain}/api/v1/recommendations"
        try:
            status, body, _ = http_get(url)
            recs_raw = json.loads(body)
            recommendations = []
            for r in recs_raw:
                pub = r.get("recommended_publication", {}) or {}
                recommendations.append({
                    "name": pub.get("name"),
                    "subdomain": pub.get("subdomain"),
                    "custom_domain": pub.get("custom_domain"),
                    "blurb": r.get("blurb"),
                    "subscribers": pub.get("ranking_detail_free_subscribers"),
                })
            return {
                "platform": "substack",
                "type": "recommendations",
                "source_publication": domain,
                "total_recommended": len(recommendations),
                "is_cartelized": len(recommendations) > 15,
                "recommendations": recommendations,
            }
        except Exception as e:
            return {
                "platform": "substack",
                "type": "recommendations",
                "source_publication": domain,
                "error": f"No se pudieron auditar las recomendaciones: {e}",
                "recommendations": [],
            }

    @staticmethod
    def _clean_html(raw_html):
        text = re.sub(r'<script.*?</script>', '', raw_html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</p>', '\n\n', text, flags=re.IGNORECASE)
        text = re.sub(r'<h[1-6].*?>(.*?)</h[1-6]>', r'\n\n### \1\n\n', text, flags=re.IGNORECASE)
        text = re.sub(r'<[^>]+>', '', text)
        return html.unescape(text).strip()


# -----------------------------------------------------------------------------
# ADAPTER 3: Reddit Engine con Dossiers Forenses de Usuario
# -----------------------------------------------------------------------------

class RedditAdapter:
    """Extrae subreddits, hilos, búsquedas y dossiers forenses de usuario en Reddit."""

    BASE_URL = "https://www.reddit.com"

    @staticmethod
    def parse_url(url):
        u = url.strip()
        m_thread = re.search(r"reddit\.com/r/([a-zA-Z0-9_\-]+)/comments/([a-zA-Z0-9]+)", u)
        if m_thread:
            return {"type": "thread", "subreddit": m_thread.group(1), "post_id": m_thread.group(2)}

        m_user = re.search(r"reddit\.com/u(?:ser)?/([a-zA-Z0-9_\-]+)", u)
        if m_user:
            return {"type": "user", "username": m_user.group(1), "post_id": None}

        m_sub = re.search(r"reddit\.com/r/([a-zA-Z0-9_\-]+)", u)
        if m_sub:
            return {"type": "subreddit", "subreddit": m_sub.group(1), "post_id": None}

        m_short_u = re.search(r"^u/([a-zA-Z0-9_\-]+)$", u)
        if m_short_u:
            return {"type": "user", "username": m_short_u.group(1), "post_id": None}

        m_short = re.search(r"^r/([a-zA-Z0-9_\-]+)$", u)
        if m_short:
            return {"type": "subreddit", "subreddit": m_short.group(1), "post_id": None}

        return None

    @classmethod
    def fetch_user_dossier(cls, username, limit=50):
        """Genera un peritaje forense de usuario calculando entropía de subreddits y karma."""
        json_url = f"{cls.BASE_URL}/user/{username}/submitted.json?limit={limit}"
        posts = []
        sub_distribution = {}

        try:
            headers = {"User-Agent": USER_AGENT}
            status, body, _ = http_get(json_url, headers=headers, timeout=10)
            data = json.loads(body)
            children = data.get("data", {}).get("children", [])
            for c in children:
                p = c.get("data", {})
                sub = p.get("subreddit", "unknown")
                sub_distribution[sub] = sub_distribution.get(sub, 0) + 1
                posts.append({
                    "title": p.get("title"),
                    "subreddit": sub,
                    "score": p.get("score", 0),
                    "created_utc": p.get("created_utc"),
                    "permalink": f"https://reddit.com{p.get('permalink')}",
                })
        except Exception:
            # Fallback Atom RSS
            rss_url = f"{cls.BASE_URL}/user/{username}/submitted.rss?limit={limit}"
            try:
                status, body, _ = http_get(rss_url, headers={"User-Agent": USER_AGENT}, timeout=10)
                root = ET.fromstring(body)
                ns = {"atom": "http://www.w3.org/2005/Atom"}
                for e in root.findall("atom:entry", ns):
                    title = e.findtext("atom:title", "", ns)
                    cat_node = e.find("atom:category", ns)
                    sub = cat_node.get("term", "unknown") if cat_node is not None else "unknown"
                    sub_distribution[sub] = sub_distribution.get(sub, 0) + 1
                    link_node = e.find("atom:link", ns)
                    plink = link_node.get("href") if link_node is not None else ""
                    posts.append({
                        "title": title,
                        "subreddit": sub,
                        "score": 0,
                        "created_utc": e.findtext("atom:published", "", ns),
                        "permalink": plink,
                    })
            except Exception as e:
                raise RuntimeError(f"No se pudo generar el dossier para /u/{username}: {e}")

        entropy = calculate_shannon_entropy(sub_distribution)
        is_burner = entropy < 0.85 and len(posts) > 5

        return {
            "platform": "reddit",
            "type": "user_dossier",
            "username": username,
            "url": f"https://reddit.com/user/{username}",
            "total_submitted_indexed": len(posts),
            "subreddit_distribution": sub_distribution,
            "subreddit_entropy": entropy,
            "entropy_verdict": "⚠️ CUENTA MONO-TEMÁTICA / RIESGO SHILL" if is_burner else "✅ DISTRIBUCIÓN DIVERSIFICADA (Orgánica)",
            "recent_posts": posts[:10],
        }

    @classmethod
    def search_subreddit(cls, subreddit, query, limit=25, sort="relevance"):
        url = f"{cls.BASE_URL}/r/{subreddit}/search.json?q={urllib.parse.quote(query)}&restrict_sr=1&sort={sort}&limit={limit}"
        headers = {"User-Agent": USER_AGENT}
        status, body, _ = http_get(url, headers=headers)
        data = json.loads(body)
        children = data.get("data", {}).get("children", [])
        results = []
        for c in children:
            p = c.get("data", {})
            results.append({
                "title": p.get("title"),
                "author": p.get("author"),
                "score": p.get("score", 0),
                "num_comments": p.get("num_comments", 0),
                "permalink": f"https://reddit.com{p.get('permalink')}",
            })
        return {
            "platform": "reddit",
            "type": "search",
            "subreddit": subreddit,
            "query": query,
            "total_results": len(results),
            "results": results,
        }

    @classmethod
    def fetch_subreddit(cls, subreddit, sort="hot", limit=25, after=None):
        json_url = f"{cls.BASE_URL}/r/{subreddit}/{sort}.json?limit={limit}"
        if after:
            json_url += f"&after={after}"

        try:
            headers = {"User-Agent": USER_AGENT}
            status, body, _ = http_get(json_url, headers=headers, timeout=8)
            data = json.loads(body)
            children = data.get("data", {}).get("children", [])
            if children:
                posts = []
                for c in children:
                    p = c.get("data", {})
                    if p.get("stickied"):
                        continue
                    score = p.get("score") or 0
                    ratio = p.get("upvote_ratio") or 1.0
                    num_comments = p.get("num_comments") or 0
                    c_index = round((1.0 - ratio) * (num_comments ** 0.5), 2)
                    posts.append({
                        "id": p.get("id"),
                        "title": p.get("title"),
                        "author": p.get("author") or "[deleted]",
                        "score": score,
                        "upvote_ratio": ratio,
                        "controversy_index": c_index,
                        "num_comments": num_comments,
                        "permalink": f"https://reddit.com{p.get('permalink')}",
                        "created_utc": p.get("created_utc"),
                        "selftext": (p.get("selftext") or "")[:500],
                        "domain": p.get("domain"),
                        "url": p.get("url"),
                    })
                return {
                    "platform": "reddit",
                    "type": "subreddit",
                    "subreddit": subreddit,
                    "sort": sort,
                    "total_posts": len(posts),
                    "after": data.get("data", {}).get("after"),
                    "posts": posts,
                }
        except Exception:
            pass

        # Fallback Atom RSS
        rss_url = f"{cls.BASE_URL}/r/{subreddit}/{sort}.rss?limit={limit}"
        try:
            status, body, _ = http_get(rss_url, headers={"User-Agent": USER_AGENT}, timeout=10)
            return cls._parse_reddit_atom(body, subreddit, sort)
        except Exception as e:
            raise RuntimeError(f"Fallo en todos los adaptadores para r/{subreddit}: {e}")

    @classmethod
    def _parse_reddit_atom(cls, xml_text, subreddit, sort):
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        root = ET.fromstring(xml_text)
        entries = root.findall("atom:entry", ns)
        posts = []

        for e in entries:
            title = e.findtext("atom:title", "", ns)
            author_node = e.find("atom:author/atom:name", ns)
            author = author_node.text.replace("/u/", "") if author_node is not None and author_node.text else "[unknown]"
            link_node = e.find("atom:link", ns)
            permalink = link_node.get("href") if link_node is not None else ""
            content = e.findtext("atom:content", "", ns)
            clean_content = SubstackAdapter._clean_html(content)[:500]

            posts.append({
                "id": permalink.split("/comments/")[-1].split("/")[0] if "/comments/" in permalink else "",
                "title": title,
                "author": author,
                "score": 0,
                "upvote_ratio": 1.0,
                "controversy_index": 0.0,
                "num_comments": 0,
                "permalink": permalink,
                "created_utc": e.findtext("atom:published", "", ns),
                "selftext": clean_content,
                "domain": f"reddit.com/r/{subreddit}",
                "url": permalink,
            })

        return {
            "platform": "reddit",
            "type": "subreddit",
            "subreddit": subreddit,
            "sort": sort,
            "total_posts": len(posts),
            "after": None,
            "posts": posts,
        }

    @classmethod
    def fetch_thread(cls, subreddit, post_id, depth=3, comment_limit=40):
        json_url = f"{cls.BASE_URL}/r/{subreddit}/comments/{post_id}.json?limit={comment_limit}&depth={depth}"
        try:
            headers = {"User-Agent": USER_AGENT}
            status, body, _ = http_get(json_url, headers=headers, timeout=10)
            data = json.loads(body)
            if isinstance(data, list) and len(data) >= 2:
                post_raw = data[0].get("data", {}).get("children", [{}])[0].get("data", {})
                post_info = {
                    "platform": "reddit",
                    "type": "thread",
                    "id": post_raw.get("id"),
                    "subreddit": post_raw.get("subreddit") or subreddit,
                    "title": post_raw.get("title"),
                    "author": post_raw.get("author"),
                    "score": post_raw.get("score") or 0,
                    "upvote_ratio": post_raw.get("upvote_ratio") or 1.0,
                    "num_comments": post_raw.get("num_comments") or 0,
                    "selftext": post_raw.get("selftext") or "",
                    "permalink": f"https://reddit.com{post_raw.get('permalink')}",
                    "created_utc": post_raw.get("created_utc"),
                }

                comments_raw = data[1].get("data", {}).get("children", [])
                parsed_comments = []

                def parse_comment_node(node, current_depth):
                    if node.get("kind") != "t1":
                        return None
                    c = node.get("data", {})
                    c_author = c.get("author", "[deleted]")
                    c_body = c.get("body", "")
                    c_score = c.get("score", 0)

                    children_replies = []
                    if current_depth < depth and "replies" in c and isinstance(c["replies"], dict):
                        sub_children = c["replies"].get("data", {}).get("children", [])
                        for sub in sub_children:
                            res = parse_comment_node(sub, current_depth + 1)
                            if res:
                                children_replies.append(res)

                    return {
                        "author": c_author,
                        "score": c_score,
                        "body": c_body,
                        "depth": current_depth,
                        "replies": children_replies,
                    }

                for c_node in comments_raw[:comment_limit]:
                    res = parse_comment_node(c_node, 1)
                    if res:
                        parsed_comments.append(res)

                post_info["comments"] = parsed_comments
                return post_info
        except Exception:
            pass

        # Fallback Jina Reader
        jina_url = f"https://r.jina.ai/https://www.reddit.com/r/{subreddit}/comments/{post_id}"
        try:
            status, body, _ = http_get(jina_url, timeout=12)
            lines = [l.strip() for l in body.split("\n") if l.strip()]
            title = lines[0] if lines else f"Hilo {post_id}"
            return {
                "platform": "reddit",
                "type": "thread",
                "id": post_id,
                "subreddit": subreddit,
                "title": title,
                "author": "[unknown]",
                "score": 0,
                "upvote_ratio": 1.0,
                "num_comments": 0,
                "selftext": "\n".join(lines[1:25]),
                "permalink": f"https://reddit.com/r/{subreddit}/comments/{post_id}",
                "created_utc": None,
                "comments": [],
            }
        except Exception as e:
            raise RuntimeError(f"Fallo al recuperar hilo {post_id} en r/{subreddit}: {e}")


# -----------------------------------------------------------------------------
# ADAPTER 4: YouTube Engine (oEmbed + Transcripciones Zero-Auth)
# -----------------------------------------------------------------------------

class YouTubeAdapter:
    """Extrae metadatos y transcripciones de vídeos de YouTube sin claves de API."""

    OEMBED_API = "https://www.youtube.com/oembed"

    @staticmethod
    def parse_url(url):
        u = url.strip()
        m_watch = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([a-zA-Z0-9_\-]{11})", u)
        if m_watch:
            return {"type": "video", "video_id": m_watch.group(1)}
        return None

    @classmethod
    def fetch_video(cls, video_id):
        # 1. Recuperar metadatos oficiales vía oEmbed
        target_url = f"https://www.youtube.com/watch?v={video_id}"
        oembed_url = f"{cls.OEMBED_API}?url={urllib.parse.quote(target_url)}&format=json"

        title = f"YouTube Video {video_id}"
        author = "YouTube Creator"
        thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"

        try:
            status, body, _ = http_get(oembed_url, timeout=8)
            data = json.loads(body)
            title = data.get("title", title)
            author = data.get("author_name", author)
            thumbnail_url = data.get("thumbnail_url", thumbnail_url)
        except Exception:
            pass

        # 2. Rescate de transcripción completa vía proxy autónomo Jina Reader
        transcript_text = ""
        try:
            jina_url = f"https://r.jina.ai/{target_url}"
            status, body, _ = http_get(jina_url, timeout=12)
            if body:
                transcript_text = body[:10000]
        except Exception:
            pass

        return {
            "platform": "youtube",
            "type": "video",
            "id": video_id,
            "url": target_url,
            "title": title,
            "author": author,
            "thumbnail_url": thumbnail_url,
            "transcript": transcript_text,
            "content": transcript_text,
            "text": transcript_text,
        }


# -----------------------------------------------------------------------------
# SQLite WAL Storage & Telemetry (Sovereign Archival Vault)
# -----------------------------------------------------------------------------

def init_vault(db_path=DEFAULT_DB_PATH):
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=5)
    conn.execute("PRAGMA journal_mode = WAL;")
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS socint_vault (
                record_id TEXT PRIMARY KEY,
                platform TEXT NOT NULL,
                target_type TEXT NOT NULL,
                url TEXT NOT NULL,
                author TEXT,
                title TEXT,
                raw_content TEXT,
                metrics_json TEXT,
                epistemic_counts_json TEXT,
                snr_score REAL,
                captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    conn.close()


def save_to_vault(data, db_path=DEFAULT_DB_PATH):
    init_vault(db_path)
    conn = sqlite3.connect(db_path, timeout=5)
    with conn:
        rec_id = str(data.get("id") or data.get("permalink") or data.get("url") or f"{data.get('platform')}_{int(time.time())}")
        plat = data.get("platform", "unknown")
        target_type = data.get("type", "unknown")
        url = data.get("url") or data.get("canonical_url") or data.get("permalink") or ""
        author = ""
        if isinstance(data.get("author"), dict):
            author = data["author"].get("screen_name") or data["author"].get("name") or ""
        elif isinstance(data.get("author"), str):
            author = data.get("author")

        title = data.get("title") or (data.get("text", "")[:80] if data.get("text") else "")
        content = data.get("text") or data.get("content") or data.get("selftext") or ""
        metrics_json = json.dumps(data.get("metrics") or {})
        epistemic = data.get("epistemic_audit") or {}
        epistemic_counts = json.dumps(epistemic.get("counts") or {})
        snr = epistemic.get("signal_ratio", 0.50)

        conn.execute("""
            INSERT OR REPLACE INTO socint_vault
            (record_id, platform, target_type, url, author, title, raw_content, metrics_json, epistemic_counts_json, snr_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (rec_id, plat, target_type, url, author, title, content, metrics_json, epistemic_counts, snr))

    conn.close()
    return rec_id


def vault_stats(db_path=DEFAULT_DB_PATH):
    init_vault(db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    total_records = cur.execute("SELECT COUNT(*) FROM socint_vault;").fetchone()[0]
    platforms = cur.execute("SELECT platform, COUNT(*) FROM socint_vault GROUP BY platform;").fetchall()
    avg_snr = cur.execute("SELECT AVG(snr_score) FROM socint_vault;").fetchone()[0] or 0.0
    latest = cur.execute("SELECT record_id, platform, author, snr_score, captured_at FROM socint_vault ORDER BY captured_at DESC LIMIT 5;").fetchall()
    conn.close()

    lines = [
        f"=== TELEMETRÍA DE BÓVEDA SOCINT C5-REAL (SQLite WAL) ===",
        f"Base de datos: {db_path}",
        f"Registros Totales: {total_records}",
        f"Score SNR Medio Global: {avg_snr * 100:.1f}%",
        f"",
        f"Distribución por Plataforma:",
    ]
    for p, c in platforms:
        lines.append(f"  • {p.upper():12s}: {c} registros")
    lines.append("")
    lines.append("Últimos Registros Archivados:")
    for r in latest:
        lines.append(f"  - [{r[4]}] {r[1].upper()} | ID: {r[0]} | Autor: {r[2]} | SNR: {r[3]*100:.0f}%")

    return "\n".join(lines)


def vault_query(sql_query, db_path=DEFAULT_DB_PATH):
    init_vault(db_path)
    clean_sql = sql_query.strip()
    if not clean_sql.lower().startswith("select"):
        raise ValueError("Solo se autorizan sentencias de lectura SELECT en la bóveda.")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(clean_sql)
    col_names = [d[0] for d in cur.description]
    rows = cur.fetchall()
    conn.close()

    lines = [" | ".join(col_names), "-" * (len(" | ".join(col_names)) + 5)]
    for r in rows:
        lines.append(" | ".join(str(val) for val in r))
    return "\n".join(lines)


# -----------------------------------------------------------------------------
# Markdown Report Generator
# -----------------------------------------------------------------------------

def generate_markdown_report(data, epistemic_audit=None, astroturf_audit=None):
    plat = data.get("platform", "unknown").upper()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        f"# Informe de Inteligencia Social SOCINT C5-REAL: {plat}",
        f"",
        f"> **Auditoría Forense C5:** Extracción Determinista en Silicio  ",
        f"> **Fecha de Captura:** `{ts}`  ",
        f"> **Estado del Canal:** `Soberano · Zero Cloud Leak`  ",
        f"",
        f"---",
        f"",
    ]

    if plat == "X":
        if data.get("type") == "profile":
            lines.extend([
                f"## 👤 Auditoría Forense de Perfil X (Twitter): @{data.get('screen_name')}",
                f"",
                f"- **Nombre:** **{data.get('name')}** (`@{data.get('screen_name')}`)",
                f"- **Verificación:** `{'✅ ' + str(data.get('verification_type')).upper() if data.get('verified') else '❌ No verificado'}`",
                f"- **Audiencia:** {data.get('followers', 0):,} Followers | {data.get('following', 0):,} Siguiendo",
                f"- **Actividad:** {data.get('tweets_count', 0):,} Tweets | {data.get('media_count', 0):,} Media | {data.get('likes', 0):,} Likes",
                f"- **Fecha de Creación:** `{data.get('joined', 'N/A')}`",
                f"",
                f"### Biografía",
                f"> {data.get('description', '*(Sin biografía)*')}",
                f"",
            ])
        elif data.get("type") == "thread":
            author = data.get("author", {}) or {}
            metrics = data.get("metrics", {}) or {}
            lines.extend([
                f"## 🧵 Hilo Desenlazado de X (Twitter): @{author.get('screen_name')}",
                f"",
                f"- **Autor:** **{author.get('name')}** (`@{author.get('screen_name')}`)",
                f"- **Total de Entregas:** `{data.get('total_tweets')}` tweets encadenados",
                f"- **Impacto Agregado:** {metrics.get('total_likes', 0):,} Likes | {metrics.get('total_retweets', 0):,} RTs | {metrics.get('total_replies', 0):,} Replies",
                f"- **Enlace Raíz:** [{data.get('url')}]({data.get('url')})",
                f"",
                f"### Contenido Completo del Hilo",
                f"",
                f"```text",
                f"{data.get('text', '')}",
                f"```",
                f"",
            ])
        else:
            author = data.get("author", {}) or {}
            metrics = data.get("metrics", {}) or {}
            likes = int(metrics.get("likes") or 0)
            retweets = int(metrics.get("retweets") or 0)
            replies = int(metrics.get("replies") or 0)
            views = int(metrics.get("views") or 0)

            lines.extend([
                f"## 🛰️ Telemetría de Publicación (X/Twitter)",
                f"",
                f"- **Autor:** **{author.get('name') or author.get('screen_name')}** (`@{author.get('screen_name')}`)",
                f"- **URL:** [{data.get('url')}]({data.get('url')})",
                f"- **Fecha:** `{data.get('created_at', 'N/A')}`",
                f"- **Métricas de Impacto:** {likes:,} Likes | {retweets:,} RTs | {replies:,} Replies | {views:,} Views",
                f"",
                f"### Contenido Extraído",
                f"",
                f"```text",
                f"{data.get('text', '')}",
                f"```",
                f"",
            ])
            if data.get("quoted_tweet"):
                q = data["quoted_tweet"]
                lines.extend([
                    f"### Tweet Citado (Quote)",
                    f"> **@{q.get('screen_name')}**: {q.get('text')}",
                    f"",
                ])

    elif plat == "SUBSTACK":
        if data.get("type") == "post":
            likes = int(data.get("likes") or 0)
            comments = int(data.get("comments_count") or 0)
            lines.extend([
                f"## 📰 Publicación de Substack: {data.get('title')}",
                f"",
                f"- **Autor:** `{data.get('author')}`",
                f"- **URL:** [{data.get('canonical_url')}]({data.get('canonical_url')})",
                f"- **Fecha:** `{data.get('post_date')}` | Palabras: `{data.get('word_count')}`",
                f"- **Engagement:** {likes:,} Likes | {comments:,} Comentarios",
                f"- **Acceso:** `{'🔒 Paywalled' if data.get('paywalled') else '🔓 Abierto'}`",
                f"",
                f"### Extracto / Cuerpo del Artículo",
                f"",
                f"{data.get('content', '')[:2500]}...",
                f"",
            ])
            if data.get("comments"):
                lines.extend([
                    f"### Comentarios de Suscriptores ({len(data.get('comments'))} recuperados)",
                    f"",
                ])
                for c in data["comments"][:6]:
                    lines.append(f"- **{c.get('author')}** (`{c.get('likes')} likes`): {c.get('body')[:200]}")
                lines.append("")

        elif data.get("type") == "archive":
            lines.extend([
                f"## 📚 Archivo Histórico de Newsletter: `{data.get('domain')}`",
                f"",
                f"Total de entregas indexadas: **{data.get('total_fetched')}**",
                f"",
                f"| Fecha | Título | Autor | Likes | Comentarios |",
                f"| :--- | :--- | :--- | :--- | :--- |",
            ])
            for p in data.get("posts", []):
                likes = int(p.get("reaction_count") or 0)
                comments = int(p.get("comments_count") or 0)
                lines.append(f"| `{str(p.get('post_date', ''))[:10]}` | [{p.get('title')}]({p.get('canonical_url')}) | {p.get('author')} | {likes:,} | {comments:,} |")
            lines.append("")

        elif data.get("type") == "recommendations":
            lines.extend([
                f"## 🕸️ Auditoría de Cártel de Recomendaciones (PODs): `{data.get('source_publication')}`",
                f"",
                f"- **Recomendaciones Salientes Totales:** `{data.get('total_recommended')}`",
                f"- **Veredicto de Cartelización:** `{'⚠️ ALTO RIESGO DE POD' if data.get('is_cartelized') else '✅ DENTRO DE LÍMITES ORGÁNICOS'}`",
                f"",
                f"| Publicación Recomendada | Subdominio | Suscriptores Estimados |",
                f"| :--- | :--- | :--- |",
            ])
            for r in data.get("recommendations", []):
                lines.append(f"| {r.get('name')} | `{r.get('subdomain')}` | {r.get('subscribers', 'N/A')} |")
            lines.append("")

    elif plat == "REDDIT":
        if data.get("type") == "user_dossier":
            dist = data.get("subreddit_distribution", {})
            lines.extend([
                f"## 🕵️ Dossier Forense de Usuario Reddit: /u/{data.get('username')}",
                f"",
                f"- **URL:** [{data.get('url')}]({data.get('url')})",
                f"- **Posts Indexados:** `{data.get('total_submitted_indexed')}`",
                f"- **Entropía de Subreddits (H):** `{data.get('subreddit_entropy')} bits`",
                f"- **Veredicto:** `{data.get('entropy_verdict')}`",
                f"",
                f"### Distribución de Actividad por Subreddit",
                f"",
                f"| Subreddit | Frecuencia | Proporción |",
                f"| :--- | :--- | :--- |",
            ])
            tot = max(1, data.get("total_submitted_indexed", 1))
            for sub, cnt in sorted(dist.items(), key=lambda x: x[1], reverse=True)[:10]:
                lines.append(f"| `r/{sub}` | {cnt} posts | {cnt/tot*100:.1f}% |")
            lines.append("")

        elif data.get("type") == "search":
            lines.extend([
                f"## 🔍 Búsqueda en Subreddit: r/{data.get('subreddit')} (Query: \"{data.get('query')}\")",
                f"",
                f"Resultados encontrados: **{data.get('total_results')}**",
                f"",
                f"| Score | Comentarios | Título | Autor |",
                f"| :--- | :--- | :--- | :--- |",
            ])
            for r in data.get("results", []):
                lines.append(f"| {r.get('score')} | {r.get('num_comments')} | [{r.get('title')[:60]}]({r.get('permalink')}) | `/u/{r.get('author')}` |")
            lines.append("")

        elif data.get("type") == "thread":
            score = int(data.get("score") or 0)
            ratio = float(data.get("upvote_ratio") or 1.0)
            comments_num = int(data.get("num_comments") or 0)
            lines.extend([
                f"## 👾 Hilo de Discusión en Reddit: r/{data.get('subreddit')}",
                f"",
                f"- **Título:** **{data.get('title')}**",
                f"- **Autor:** `/u/{data.get('author')}`",
                f"- **Puntuación:** `{score:,}` (Upvote Ratio: `{ratio * 100:.1f}%`)",
                f"- **Comentarios Totales:** `{comments_num:,}`",
                f"- **Enlace:** [{data.get('permalink')}]({data.get('permalink')})",
                f"",
                f"### Texto Principal (OP)",
                f"",
                f"{data.get('selftext') if data.get('selftext') else '*(Solo enlace o título)*'}",
                f"",
                f"### Señal de la Comunidad (Comentarios de Alto Rango)",
                f"",
            ])
            for idx, c in enumerate(data.get("comments", [])[:10], 1):
                clean_comment = c.get('body', '').replace('\n', ' ')[:300]
                c_score = int(c.get('score') or 0)
                lines.append(f"{idx}. **/u/{c.get('author')}** (`{c_score:,} pts`):")
                lines.append(f"   > \"{clean_comment}\"")
                lines.append("")

        elif data.get("type") == "subreddit":
            lines.extend([
                f"## 🌐 Barrido de Subreddit: r/{data.get('subreddit')} (Orden: `{data.get('sort')}`)",
                f"",
                f"Posts extraídos: **{data.get('total_posts')}**",
                f"",
                f"| Score | Ratio | C-Index | Título | Autor |",
                f"| :--- | :--- | :--- | :--- | :--- |",
            ])
            for p in data.get("posts", []):
                score = int(p.get("score") or 0)
                ratio = float(p.get("upvote_ratio") or 1.0)
                c_idx = p.get("controversy_index", 0.0)
                lines.append(f"| {score:,} | {ratio:.2f} | **{c_idx}** | [{p.get('title')[:60]}]({p.get('permalink')}) | `/u/{p.get('author')}` |")
            lines.append("")

    elif plat == "YOUTUBE":
        lines.extend([
            f"## 📺 Telemetría Audiovisual de YouTube: {data.get('title')}",
            f"",
            f"- **Canal / Creador:** **{data.get('author')}**",
            f"- **URL:** [{data.get('url')}]({data.get('url')})",
            f"- **Miniatura:** ![{data.get('title')}]({data.get('thumbnail_url')})",
            f"",
            f"### Transcripción / Audio Extraído",
            f"",
            f"{data.get('transcript', '')[:2500]}...",
            f"",
        ])

    # Auditoría Forense de Astroturfing
    if astroturf_audit and astroturf_audit.get("verdict"):
        lines.extend([
            f"---",
            f"",
            f"## 🤖 Auditoría de Astroturfing & Shilling (Jaccard N-Grams)",
            f"",
            f"- **Veredicto Forense:** `{astroturf_audit.get('verdict')}`",
            f"- **Índice de Riesgo Astroturf:** `{astroturf_audit.get('astroturf_risk_score') * 100:.1f}%`",
            f"- **Concentración de Autores:** `{astroturf_audit.get('author_concentration') * 100:.1f}%`",
            f"- **Pares de Comentarios Cuasi-Idénticos:** `{astroturf_audit.get('duplicate_clusters')}`",
            f"",
        ])
        if astroturf_audit.get("suspicious_pairs"):
            lines.append("#### Pares Sospechosos Detectados:")
            for p in astroturf_audit["suspicious_pairs"]:
                lines.append(f"- `/u/{p.get('author_a')}` vs `/u/{p.get('author_b')}` (Similitud: `{p.get('similarity') * 100:.0f}%`): *\"{p.get('sample')}\"*")
            lines.append("")

    # Auditoría Epistemológica
    if epistemic_audit:
        c = epistemic_audit.get("counts", {})
        lines.extend([
            f"---",
            f"",
            f"## ⚖️ Matriz de Auditoría Epistemológica C5-REAL",
            f"",
            f"- **Ratio de Señal/Ruido (SNR):** `{epistemic_audit.get('signal_ratio') * 100:.1f}%`",
            f"- **Hechos Verificados:** `{c.get('hechos_verificados')}`",
            f"- **Evidencia Experimental & Telemetría:** `{c.get('evidencia_experimental')}`",
            f"- **Modelos & Doctrina:** `{c.get('modelos_doctrina')}`",
            f"- **Especulación & Sesgo / Falsa Causalidad:** `{c.get('especulacion_sesgo')}`",
            f"",
        ])
        samples = epistemic_audit.get("samples", {})
        if samples.get("hechos"):
            lines.append(f"#### 🔍 Muestras de Hechos Verificados:")
            for s in samples["hechos"]:
                lines.append(f"- *\"{s}\"*")
            lines.append("")
        if samples.get("especulacion"):
            lines.append(f"#### ⚠️ Muestras de Especulación / Cheap Talk:")
            for s in samples["especulacion"]:
                lines.append(f"- *\"{s}\"*")
            lines.append("")

    return "\n".join(lines)


# -----------------------------------------------------------------------------
# Main CLI Orchestrator
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Suite Soberana de Inteligencia Social (SOCINT C5-REAL): Extracción sin API de pago en X, Substack, Reddit y YouTube."
    )
    parser.add_argument("--url", "-u", type=str, help="URL del post, newsletter, subreddit, perfil, vídeo o tweet.")
    parser.add_argument("--batch", "-b", type=str, help="Archivo con lista de URLs a procesar en lote.")
    parser.add_argument("--platform", "-p", choices=["auto", "x", "substack", "reddit", "youtube"], default="auto", help="Plataforma de destino.")
    parser.add_argument("--limit", "-l", type=int, default=25, help="Límite de elementos a recuperar.")
    parser.add_argument("--depth", "-d", type=int, default=3, help="Profundidad de comentarios en Reddit.")
    parser.add_argument("--format", "-f", choices=["json", "markdown"], default="markdown", help="Formato de salida.")
    parser.add_argument("--output", "-o", type=str, help="Ruta de archivo para guardar el resultado.")
    parser.add_argument("--unfold", action="store_true", help="Desenrollar hilos completos en X (Twitter).")
    parser.add_argument("--search", "-s", type=str, help="Buscar término dentro de un subreddit.")
    parser.add_argument("--audit-pods", action="store_true", help="Auditar red de recomendaciones en Substack.")
    parser.add_argument("--save-vault", action="store_true", help="Almacenar registro en SQLite WAL vault.")
    parser.add_argument("--vault-stats", action="store_true", help="Consultar estadísticas y telemetría de la bóveda SQLite.")
    parser.add_argument("--vault-query", type=str, help="Ejecutar consulta SELECT en la bóveda SQLite.")
    parser.add_argument("--vault-db", type=str, default=DEFAULT_DB_PATH, help="Ruta de base de datos SQLite WAL.")

    args = parser.parse_args()

    # Comandos de Bóveda directa
    if args.vault_stats:
        print(vault_stats(args.vault_db))
        return

    if args.vault_query:
        print(vault_query(args.vault_query, args.vault_db))
        return

    if not args.url and not args.batch:
        parser.print_help()
        sys.exit(1)

    urls_to_process = []
    if args.batch:
        batch_path = os.path.expanduser(args.batch)
        if not os.path.exists(batch_path):
            print(f"[!] Error: Archivo batch no encontrado: {batch_path}", file=sys.stderr)
            sys.exit(1)
        with open(batch_path, "r", encoding="utf-8") as bf:
            urls_to_process = [line.strip() for line in bf if line.strip() and not line.startswith("#")]
    else:
        urls_to_process = [args.url.strip()]

    all_reports = []

    for target_url in urls_to_process:
        platform = args.platform
        if platform == "auto":
            if "twitter.com" in target_url or "x.com" in target_url or "fxtwitter.com" in target_url:
                platform = "x"
            elif "substack.com" in target_url or "/p/" in target_url:
                platform = "substack"
            elif "reddit.com" in target_url or target_url.startswith("r/") or target_url.startswith("u/"):
                platform = "reddit"
            elif "youtube.com" in target_url or "youtu.be" in target_url:
                platform = "youtube"
            else:
                print(f"[!] Advertencia: No se pudo auto-detectar plataforma para: {target_url}", file=sys.stderr)
                continue

        extracted_data = None
        text_for_audit = ""
        comments_for_astroturf = []

        if platform == "x":
            kind, user, tweet_id = XAdapter.parse_url(target_url)
            if kind == "profile":
                extracted_data = XAdapter.fetch_profile(user)
                text_for_audit = extracted_data.get("description", "")
            elif kind == "tweet" and tweet_id:
                if args.unfold:
                    extracted_data = XAdapter.unfold_thread(user, tweet_id)
                else:
                    extracted_data = XAdapter.fetch_tweet(user, tweet_id)
                text_for_audit = extracted_data.get("text", "")
            else:
                print(f"[!] Error: URL de X no reconocida: {target_url}", file=sys.stderr)
                continue

        elif platform == "substack":
            sub_info = SubstackAdapter.parse_url(target_url)
            if not sub_info:
                print(f"[!] Error: URL de Substack no válida: {target_url}", file=sys.stderr)
                continue

            if sub_info["type"] == "post":
                extracted_data = SubstackAdapter.fetch_post(sub_info["domain"], sub_info["slug"])
                text_for_audit = extracted_data.get("content", "")
                comments_for_astroturf = extracted_data.get("comments", [])
            else:
                if args.audit_pods:
                    extracted_data = SubstackAdapter.audit_recommendation_network(sub_info["domain"])
                else:
                    extracted_data = SubstackAdapter.fetch_publication_archive(sub_info["domain"], limit=args.limit)

        elif platform == "reddit":
            red_info = RedditAdapter.parse_url(target_url)
            if not red_info:
                print(f"[!] Error: URL de Reddit no válida: {target_url}", file=sys.stderr)
                continue

            if red_info["type"] == "user":
                extracted_data = RedditAdapter.fetch_user_dossier(red_info["username"], limit=args.limit)
                text_for_audit = " ".join(p.get("title", "") for p in extracted_data.get("recent_posts", []))
            elif red_info["type"] == "thread":
                extracted_data = RedditAdapter.fetch_thread(red_info["subreddit"], red_info["post_id"], depth=args.depth, comment_limit=args.limit)
                text_for_audit = (extracted_data.get("selftext") or "") + "\n" + "\n".join(
                    c.get("body", "") for c in extracted_data.get("comments", [])
                )
                comments_for_astroturf = extracted_data.get("comments", [])
            elif red_info["type"] == "subreddit":
                if args.search:
                    extracted_data = RedditAdapter.search_subreddit(red_info["subreddit"], args.search, limit=args.limit)
                else:
                    extracted_data = RedditAdapter.fetch_subreddit(red_info["subreddit"], limit=args.limit)

        elif platform == "youtube":
            yt_info = YouTubeAdapter.parse_url(target_url)
            if not yt_info:
                print(f"[!] Error: URL de YouTube no reconocida: {target_url}", file=sys.stderr)
                continue
            extracted_data = YouTubeAdapter.fetch_video(yt_info["video_id"])
            text_for_audit = extracted_data.get("transcript", "")

        # Auditorías
        epistemic_audit = None
        if text_for_audit.strip():
            epistemic_audit = EpistemicClassifier.classify_text(text_for_audit)
            extracted_data["epistemic_audit"] = epistemic_audit

        astroturf_audit = None
        if comments_for_astroturf:
            astroturf_audit = AstroturfDetector.analyze_comments(comments_for_astroturf)
            extracted_data["astroturf_audit"] = astroturf_audit

        # Almacenamiento en Bóveda SQLite
        if args.save_vault:
            rec_id = save_to_vault(extracted_data, args.vault_db)
            extracted_data["vault_record_id"] = rec_id

        if args.format == "json":
            all_reports.append(json.dumps(extracted_data, indent=2, ensure_ascii=False))
        else:
            all_reports.append(generate_markdown_report(extracted_data, epistemic_audit, astroturf_audit))

    final_output = "\n\n---\n\n".join(all_reports)

    if args.output:
        out_path = os.path.expanduser(args.output)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(final_output)
        print(f"[✓] Extracción completada. Guardado en: {out_path}")
    else:
        print(final_output)


if __name__ == "__main__":
    main()
