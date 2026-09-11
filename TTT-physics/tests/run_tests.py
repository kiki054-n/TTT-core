"""Minimal runner so the checks work without pytest:  python tests/run_tests.py"""
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(__file__))
import test_core  # noqa: E402

failed = 0
names = [n for n in dir(test_core) if n.startswith("test_")]
for n in names:
    try:
        getattr(test_core, n)()
        print(f"PASS  {n}")
    except Exception:  # noqa: BLE001
        failed += 1
        print(f"FAIL  {n}")
        traceback.print_exc()
print(f"\n{len(names) - failed}/{len(names)} passed")
sys.exit(1 if failed else 0)
