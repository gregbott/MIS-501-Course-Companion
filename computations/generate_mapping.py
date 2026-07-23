"""
generate_mapping.py — regenerate CODE_EXAMPLE_MAPPING.md.

Maps every ``demo_*`` function in ``computations/moduleNN_examples.py`` to the
Worked Example admonition in ``docs/`` whose ``*Source:*`` line cites it.
Run after any phase that touches docs examples or computation code:

    pixi run -e compute python computations/generate_mapping.py
"""

from __future__ import annotations

import datetime
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COMP_DIR = REPO / "computations"
DOCS_DIR = REPO / "docs"

SOURCE_RE = re.compile(
    r"\*Source:\s*`computations/([A-Za-z0-9_]+\.py)`\s*[–—-]\s*`(demo_[A-Za-z0-9_]+)\(\)`\*"
)
TITLE_RE = re.compile(r'!!!\s+example\s+"([^"]+)"')
DEF_RE = re.compile(r"^def (demo_[A-Za-z0-9_]+)\(", re.M)


def docs_citations():
    """(file, func) -> (page, admonition title, line number of the admonition)."""
    cites = {}
    for md in sorted(DOCS_DIR.rglob("*.md")):
        lines = md.read_text(encoding="utf-8").splitlines()
        current_title = None
        current_line = None
        for lineno, line in enumerate(lines, start=1):
            mt = TITLE_RE.search(line)
            if mt:
                current_title = mt.group(1)
                current_line = lineno
            ms = SOURCE_RE.search(line)
            if ms:
                key = (ms.group(1), ms.group(2))
                cites.setdefault(key, []).append(
                    (str(md.relative_to(REPO)), current_title or "?", current_line or lineno)
                )
    return cites


def main():
    cites = docs_citations()
    files = sorted(COMP_DIR.glob("module*_examples.py"))
    today = datetime.date.today().isoformat()

    lines = [
        "# Code Example Mapping",
        "",
        f"Maps every `demo_*` function in `computations/` to its Worked Example",
        f"admonition in the online course companion (`docs/`). Every function is",
        f"referenced by exactly one `!!! example` admonition whose `*Source:*` line",
        f"cites it. Regenerated {today} via `computations/generate_mapping.py`.",
        "",
    ]

    total_funcs = 0
    problems = []
    for path in files:
        funcs = DEF_RE.findall(path.read_text(encoding="utf-8"))
        total_funcs += len(funcs)
        lines.append(f"## `computations/{path.name}` ({len(funcs)} functions)")
        lines.append("")
        lines.append("| Function | Docs page | Example title | Line |")
        lines.append("|----------|-----------|---------------|------|")
        for fn in funcs:
            entries = cites.get((path.name, fn), [])
            if not entries:
                lines.append(f"| `{fn}()` | — | **UNCITED** | — |")
                problems.append(f"UNCITED: {path.name} :: {fn}")
            else:
                for page, title, lineno in entries:
                    lines.append(f"| `{fn}()` | `{page}` | {title} | {lineno} |")
                if len(entries) > 1:
                    problems.append(f"MULTI-CITED ({len(entries)}x): {path.name} :: {fn}")
        lines.append("")

    # Citations pointing at functions that do not exist.
    known = {
        (p.name, fn) for p in files for fn in DEF_RE.findall(p.read_text(encoding="utf-8"))
    }
    for key in sorted(set(cites) - known):
        problems.append(f"DANGLING CITATION: {key[0]} :: {key[1]} (no such function)")

    pages = {e[0] for v in cites.values() for e in v}
    lines.insert(6, f"Totals: {len(files)} files → {total_funcs} functions → {len(pages)} pages.")
    lines.insert(7, "")

    if problems:
        lines.append("## Problems")
        lines.append("")
        lines.extend(f"- {p}" for p in problems)
        lines.append("")

    (REPO / "CODE_EXAMPLE_MAPPING.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote CODE_EXAMPLE_MAPPING.md: {len(files)} files, {total_funcs} functions, "
          f"{len(pages)} pages, {len(problems)} problems.")
    for p in problems:
        print(" ", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
