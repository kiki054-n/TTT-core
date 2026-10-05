#!/bin/sh
set -e
for s in thirtyfour one37_twelve inside_outside; do
  echo "### $s"; python3 scripts/$s.py | tail -1
done
