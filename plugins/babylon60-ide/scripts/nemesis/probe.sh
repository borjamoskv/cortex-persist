#!/bin/sh
# Runs under precisely the same OS policy as the verifier, before every job.
set -eu
src=$1
runtime=$2
out=$3
outside=$4
deny() {
    name=$1
    shift
    if "$@" >"$out/$name.stdout" 2>"$out/$name.stderr"; then
        printf 'FAIL %s\n' "$name"
        exit 1
    fi
    test -s "$out/$name.stderr"
    /usr/bin/grep -Eq 'Operation not permitted|Permission denied|Read-only file system' "$out/$name.stderr"
    printf 'DENIED %s\n' "$name"
}
printf allowed > "$out/allowed"
/usr/bin/touch "$out/positive"
/bin/chmod 600 "$out/positive"
/bin/ln "$out/positive" "$out/positive-link"
/bin/mv "$out/positive-link" "$out/positive-renamed"
/bin/rm "$out/positive-renamed" "$out/positive"
deny source-write /bin/sh -c 'printf bad > "$1"' sh "$src/canary"
deny source-create /usr/bin/touch "$src/created"
deny source-chmod /bin/chmod 000 "$src/canary"
deny source-delete /bin/rm "$src/canary"
deny source-rename /bin/mv "$src/canary" "$out/stolen"
deny source-hardlink /bin/ln "$src/canary" "$out/hardlink"
deny oracle-write /bin/sh -c 'printf bad > "$1"' sh "$src/oracle/probe.sh"
deny runtime-write /usr/bin/touch "$runtime/created"
deny outside-write /bin/sh -c 'printf bad > "$1"' sh "$outside"
deny outside-read /bin/cat "$outside"
/bin/ln -s "$src/canary" "$out/symlink"
deny symlink-write /bin/sh -c 'printf bad > "$1"' sh "$out/symlink"
deny grandchild-write /bin/sh -c '/bin/sh -c '\''printf bad > "$1"'\'' sh "$1"' sh "$src/canary"
deny detached-child-write /usr/bin/perl -MPOSIX -e 'my $p = fork(); die "$!\n" unless defined $p; if (!$p) { POSIX::setsid(); open(my $f, ">", $ARGV[0]) or die "$!\n"; print $f "bad"; exit 0 } waitpid($p, 0); exit($? >> 8)' "$src/canary"
deny network /usr/bin/perl -MSocket -e 'socket(S, PF_INET, SOCK_STREAM, 0) or die "$!\n"; connect(S, sockaddr_in(9, inet_aton("127.0.0.1"))) or die "$!\n"; exit 0'
printf 'PROBE_PASS\n'
