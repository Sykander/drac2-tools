#!/usr/bin/env bash
# Re-download official Avrae Read the Docs RST sources into this directory
# (.cursor/avrae-reference/, alongside Cursor rules).
# See README.md in this directory for canonical HTML URLs and when to run this.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ALIASE_RST="https://avrae.readthedocs.io/en/latest/_sources/aliasing/api.rst.txt"
AUTO_RST="https://avrae.readthedocs.io/en/latest/_sources/automation_ref.rst.txt"

curl -fsSL "${ALIASE_RST}" -o "${HERE}/aliasing-api.rst.txt"
curl -fsSL "${AUTO_RST}" -o "${HERE}/automation-reference.rst.txt"

echo "Updated:"
echo "  ${HERE}/aliasing-api.rst.txt"
echo "  ${HERE}/automation-reference.rst.txt"
echo "Bump the Last RST fetch date in ${HERE}/README.md before committing."
