#!/usr/bin/env bash
# Re-download avrae-ls upstream markdown from the default branch into upstream/.
# (.cursor/avrae-ls-reference/, alongside Cursor rules).
# See README.md in this directory for canonical repo links and when to run this.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE="https://raw.githubusercontent.com/1drturtle/avrae-ls/main"
UP="${HERE}/upstream"
DOCS="${UP}/docs"

mkdir -p "${DOCS}"

curl -fsSL "${BASE}/README.md" -o "${UP}/README.md"
curl -fsSL "${BASE}/docs/alias-tests.md" -o "${DOCS}/alias-tests.md"
curl -fsSL "${BASE}/docs/configuration.md" -o "${DOCS}/configuration.md"

echo "Updated:"
echo "  ${UP}/README.md"
echo "  ${DOCS}/alias-tests.md"
echo "  ${DOCS}/configuration.md"
echo "Bump Last upstream fetch and Tracked avrae-ls version in ${HERE}/README.md before committing."
