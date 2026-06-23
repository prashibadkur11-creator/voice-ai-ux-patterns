#!/usr/bin/env python3
"""
Generate CATALOG.md from the pattern YAML files in patterns/.

Reads every .yaml file, validates required fields, and writes a readable
catalog grouped by category. Never edit CATALOG.md by hand — edit the source
YAML and re-run this.

Usage:
    python scripts/generate_catalog.py

Requires: pyyaml
"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency: pyyaml. Install with `pip install pyyaml`.")

ROOT = Path(__file__).resolve().parent.parent
PATTERN_DIR = ROOT / "patterns"
OUTPUT = ROOT / "CATALOG.md"

REQUIRED = ["id", "name", "category", "problem", "approach",
            "anti_pattern", "example", "applies_when"]

CATEGORY_ORDER = ["turn-taking", "latency", "error-recovery", "trust", "persona", "memory"]
CATEGORY_TITLES = {
    "turn-taking": "Turn-Taking",
    "latency": "Latency",
    "error-recovery": "Error Recovery",
    "trust": "Trust",
    "persona": "Persona",
    "memory": "Memory",
}

TAXONOMY_URL = "https://github.com/prashibadkur11-creator/ai-failure-mode-taxonomy"


def load_patterns():
    patterns = []
    for path in sorted(PATTERN_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        missing = [f for f in REQUIRED if f not in data]
        if missing:
            sys.exit(f"{path.name} missing required fields: {', '.join(missing)}")
        patterns.append(data)
    return patterns


def render(p):
    lines = [
        f"### {p['name']}",
        "",
        f"`{p['id']}` · **Category:** {CATEGORY_TITLES.get(p['category'], p['category'])}",
        "",
        "**Problem**",
        "",
        p["problem"].strip(),
        "",
        "**Approach**",
        "",
        p["approach"].strip(),
        "",
        "**Anti-pattern**",
        "",
        p["anti_pattern"].strip(),
        "",
        "**Example**",
        "",
        f"> {p['example'].strip()}",
        "",
        "**Applies when**",
        "",
        "\n".join(f"- {a.strip()}" for a in p["applies_when"]),
    ]
    if p.get("related_failure_modes"):
        fms = ", ".join(f"[`{fm}`]({TAXONOMY_URL})" for fm in p["related_failure_modes"])
        lines += ["", f"**Prevents failure modes:** {fms}"]
    if p.get("related"):
        rel = ", ".join(f"`{r}`" for r in p["related"])
        lines += ["", f"**Related patterns:** {rel}"]
    return "\n".join(lines)


def build(patterns):
    by_cat = {}
    for p in patterns:
        by_cat.setdefault(p["category"], []).append(p)

    out = [
        "# Voice AI UX Pattern Catalog",
        "",
        "> Auto-generated from `patterns/`. Do not edit by hand — edit the source "
        "YAML and run `python scripts/generate_catalog.py`.",
        "",
        f"**{len(patterns)} patterns** across "
        f"{len([c for c in CATEGORY_ORDER if c in by_cat])} categories.",
        "",
        "## Contents",
        "",
    ]
    for cat in CATEGORY_ORDER:
        if cat not in by_cat:
            continue
        out.append(f"- **{CATEGORY_TITLES[cat]}**")
        for p in by_cat[cat]:
            anchor = p["name"].lower().replace(" ", "-")
            out.append(f"  - [{p['name']}](#{anchor})")
    out.append("")

    for cat in CATEGORY_ORDER:
        if cat not in by_cat:
            continue
        out += [f"## {CATEGORY_TITLES[cat]}", ""]
        for p in by_cat[cat]:
            out += [render(p), "", "---", ""]
    return "\n".join(out).rstrip() + "\n"


def main():
    patterns = load_patterns()
    OUTPUT.write_text(build(patterns), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(patterns)} patterns).")


if __name__ == "__main__":
    main()
