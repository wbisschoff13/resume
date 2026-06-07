#!/usr/bin/env bash
# test_yaml_adapter.sh — T002: YAML import adapter integration test
#
# Phase 1 (RED): Verifies broken YAML stub causes compilation failure.
#   Confirms that the YAML mapping is the critical integration seam.
#
# Phase 2 (GREEN): Will verify correct YAML adapter compiles cleanly.
#
# Usage: ./tests/test_yaml_adapter.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATA_FILE="$REPO_ROOT/content/data.typ"
STUB_FILE="$REPO_ROOT/tests/stubs/data_wrong_keys.typ"
BACKUP_FILE="${DATA_FILE}.bak"

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

pass() { echo -e "${GREEN}PASS${NC}: $1"; }
fail() { echo -e "${RED}FAIL${NC}: $1"; exit 1; }

ENTRY_POINTS=(
  cv.typ
  cv_systems.typ
  cv_infrastructure.typ
  cv_embedded.typ
  cv_enterprise.typ
  cover_letter.typ
)

# --- Phase 1: Broken YAML stub must fail compilation ---
echo "=== Phase 1: Verify broken YAML stub fails compilation ==="

cp "$DATA_FILE" "$BACKUP_FILE"
cp "$STUB_FILE" "$DATA_FILE"

for f in "${ENTRY_POINTS[@]}"; do
  if typst compile --font-path fonts "$REPO_ROOT/$f" "/tmp/test_red_${f%.typ}.pdf" 2>/dev/null; then
    cp "$BACKUP_FILE" "$DATA_FILE"
    fail "Compilation should have failed for $f with broken YAML stub"
  else
    pass "Compilation correctly failed for $f"
  fi
done

cp "$BACKUP_FILE" "$DATA_FILE"
rm "$BACKUP_FILE"

echo ""
echo "=== Phase 1: PASS ==="
echo ""

# --- Phase 2: Correct YAML adapter must compile all entry points ---
echo "=== Phase 2: Verify YAML adapter compiles all entry points ==="

for f in "${ENTRY_POINTS[@]}"; do
  if typst compile --font-path fonts "$REPO_ROOT/$f" "/tmp/test_green_${f%.typ}.pdf" 2>/dev/null; then
    pass "Compilation succeeded for $f with YAML adapter"
  else
    fail "Compilation should have succeeded for $f with YAML adapter"
  fi
done

echo ""
echo "=== Phase 2: PASS ==="

echo ""
echo "=== YAML adapter integration test: ALL PASS ==="

exit 0
