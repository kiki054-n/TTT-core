#!/bin/sh
set -e
cd "$(dirname "$0")"
for s in thirtyfour one37_twelve inside_outside f_emergence; do
  echo "### $s"
  if [ -f "scripts/$s.py" ]; then python3 "scripts/$s.py"; else python3 "$s.py"; fi | tail -1
done
