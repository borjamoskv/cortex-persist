#!/bin/bash
set -euo pipefail
test -f src/lib.rs
test -f local-untracked.txt
if printf bad > src/lib.rs 2> "$NEMESIS_OUTPUT/verify-write.stderr"; then
  exit 9
fi
printf 'VERIFIED_FIXTURE\n' > "$NEMESIS_OUTPUT/verification.txt"
printf 'VERIFIED_FIXTURE\n'
