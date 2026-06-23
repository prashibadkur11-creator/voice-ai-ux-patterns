#!/usr/bin/env python3
"""
Validate pattern YAML files against the schema. Exits non-zero on any problem
so it can gate a PR.

Usage:
    python scripts/validate_patterns.py

Requires: pyyaml
"""

import glob
import os
import sys

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency: pyyaml. Install with `pip install pyyaml`.")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED = ["id", "name", "category", "problem", "approach",
            "anti_pattern", "example", "applies_when"]
VALID_CATEGORIES = {"turn-taking", "latency", "error-recovery", "trust", "persona", "memory"}


def _nonempty(v):
    if v is None:
        return False
    if isinstance(v, str):
        return v.strip() != ""
    if isinstance(v, (list, dict)):
        return len(v) > 0
    return True


def validate(path):
    errors = []
    data = yaml.safe_load(open(path, encoding="utf-8"))
    if not isinstance(data, dict):
        return [f"{os.path.basename(path)}: not a valid pattern mapping"]

    for field in REQUIRED:
        if field not in data or not _nonempty(data[field]):
            errors.append(f"missing or empty required field: {field}")

    cat = data.get("category")
    if cat and cat not in VALID_CATEGORIES:
        errors.append(f"invalid category '{cat}' (allowed: {', '.join(sorted(VALID_CATEGORIES))})")

    fname = os.path.splitext(os.path.basename(path))[0]
    if data.get("id") and data["id"] != fname:
        errors.append(f"id '{data['id']}' does not match filename '{fname}'")

    return [f"{os.path.basename(path)}: {e}" for e in errors]


def main():
    paths = glob.glob(os.path.join(ROOT, "patterns", "*.yaml"))
    if not paths:
        print("No patterns found.")
        return

    all_errors = []
    for path in sorted(paths):
        errs = validate(path)
        if errs:
            all_errors.extend(errs)
            print(f"INVALID  {os.path.basename(path)}")
            for e in errs:
                print(f"    - {e.split(': ', 1)[1]}")
        else:
            print(f"OK       {os.path.basename(path)}")

    if all_errors:
        print(f"\n{len(all_errors)} validation error(s).")
        sys.exit(1)
    print(f"\nAll {len(paths)} patterns valid.")


if __name__ == "__main__":
    main()
