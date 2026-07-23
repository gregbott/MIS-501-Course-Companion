"""
verify_all.py — computation verification for the MIS 501 course companion.

Runs every ``demo_*`` function in the ``moduleNN_examples.py`` files, captures
each function's stdout, and checks that the numbers presented in the companion
(``docs/**/*.md``) are actually produced by the code.

Design notes (process ported from the BAN-501 companion)
--------------------------------------------------------
* Each demo is a zero-argument, pure-stdout function. Randomness-using demos
  re-seed themselves (seed 42), and every file's ``__main__`` calls the demos
  in definition order. Running each file's demos in definition order inside one
  process reproduces the exact conditions under which the book numbers were
  generated. We deliberately do NOT reset RNG state between calls.
* The book "Output" may be a *curated* transcription of stdout (trimmed
  repetition), so a byte diff is meaningless. Instead we do a numeric-aware
  comparison: every number the book shows for a demo must appear in that
  demo's stdout at the book's displayed precision.
* Every check is keyed on the (file, function) pair parsed from each
  admonition's ``*Source:*`` line.

Run with:  pixi run -e compute verify        (i.e. python computations/verify_all.py)
"""

from __future__ import annotations

import importlib.util
import io
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COMP_DIR = REPO / "computations"
DOCS_DIR = REPO / "docs"
OUT_DIR = COMP_DIR / "_verify"
RAW_DIR = OUT_DIR / "raw"

# Discovered dynamically: zero-padded names (module01_examples.py ...) sort in
# module order, which is also the order the docs present them.
EXAMPLE_FILES = sorted(p.name for p in COMP_DIR.glob("module*_examples.py"))

# ---------------------------------------------------------------------------
# Number extraction / comparison
# ---------------------------------------------------------------------------

# A numeric token not glued to a letter/underscore identifier (so "x1", "q1",
# "10x" do not yield spurious digits). Handles sign, decimals, scientific form.
NUM_RE = re.compile(
    r"(?<![A-Za-z0-9_.])[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?(?![A-Za-z0-9_])"
)
INF_RE = re.compile(r"(?<![A-Za-z0-9_])(?:inf|-inf|∞|nan)(?![A-Za-z0-9_])", re.I)


def _normalize(text: str) -> str:
    """Fold typographic number forms so tokenization sees plain ASCII numbers.

    * U+2212 minus sign (−) written in markdown tables -> ASCII '-'.
    * Thousands separators (1,024 / 196,672) -> joined digits.
    """
    text = text.replace("−", "-")
    text = re.sub(r"(?<=\d),(?=\d{3}(?:\D|$))", "", text)
    return text


def _decimals(token: str) -> int:
    """Number of decimal places displayed in a plain-decimal token."""
    if "." in token:
        return len(token.split(".", 1)[1])
    return 0


def extract_numbers(text: str):
    """Return [(raw, value, decimals, is_pct, is_sci)] for every number in text.

    is_pct marks a value immediately followed by '%' (the book sometimes prints
    a fraction the code emits as a percentage, or vice versa).
    is_sci marks scientific notation (compared on value, not decimal places).
    """
    text = _normalize(text)
    out = []
    for m in NUM_RE.finditer(text):
        tok = m.group(0)
        try:
            val = float(tok)
        except ValueError:
            continue
        is_sci = "e" in tok or "E" in tok
        nxt = text[m.end():m.end() + 1]
        is_pct = nxt == "%"
        out.append((tok, val, _decimals(tok), is_pct, is_sci))
    return out


def has_inf(text: str) -> bool:
    return bool(INF_RE.search(_normalize(text)))


def stdout_number_set(stdout: str):
    """All numeric values in stdout."""
    return [v for (_, v, _, _, _) in extract_numbers(stdout)]


def _match_one(value: float, decimals: int, is_sci: bool, stdout_vals) -> bool:
    if is_sci:  # scientific notation: relative tolerance
        tol = max(abs(value) * 1e-3, 1e-12)
        return any(abs(v - value) <= tol for v in stdout_vals)
    target = round(value, decimals)
    step = 10 ** (-decimals)
    # EXACT match at the book's displayed precision: round each stdout value to
    # the book's decimals and require equality. No last-digit slack -- a book
    # number that differs by a full displayed unit is a real mismatch, not a
    # match. Prose-derived numbers that legitimately do not appear in stdout
    # are documented explicitly in ADJUDICATED instead.
    return any(abs(round(v, decimals) - target) < 0.5 * step for v in stdout_vals)


def book_number_found(value, decimals, stdout_vals, is_pct=False, is_sci=False) -> bool:
    """Is a book number reproduced somewhere in stdout, at book precision?

    Tries the value as printed and, for percentages, the fraction form
    (value/100) -- so a book '66%' matches a code-printed 0.661.
    """
    if _match_one(value, decimals, is_sci, stdout_vals):
        return True
    if is_pct:
        frac = value / 100.0
        # a fraction carries two more significant decimals than the percentage
        if _match_one(frac, decimals + 2, is_sci, stdout_vals):
            return True
    return False


# ---------------------------------------------------------------------------
# Docs admonition parsing:  (source_file, func) -> book text for that example
# ---------------------------------------------------------------------------

SOURCE_RE = re.compile(
    r"\*Source:\s*`computations/([A-Za-z0-9_]+\.py)`\s*[–—-]\s*`(demo_[A-Za-z0-9_]+)\(\)`\*"
)
PYFENCE_RE = re.compile(r"```python.*?```", re.S)
SQLFENCE_RE = re.compile(r"```sql.*?```", re.S)


def parse_docs():
    """Map (file, func) -> dict(full_body, page) from every example admonition."""
    examples: dict[tuple[str, str], dict] = {}
    for md in sorted(DOCS_DIR.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        lines = text.splitlines()
        i = 0
        n = len(lines)
        while i < n:
            if lines[i].lstrip().startswith("!!! example"):
                # Collect the admonition block: subsequent blank or 4-space lines.
                block = [lines[i]]
                j = i + 1
                while j < n and (lines[j].strip() == "" or lines[j].startswith("    ")):
                    block.append(lines[j])
                    j += 1
                body = "\n".join(block)
                msrc = SOURCE_RE.search(body)
                if msrc:
                    key = (msrc.group(1), msrc.group(2))
                    examples[key] = {
                        "body": body,
                        "page": str(md.relative_to(REPO)),
                    }
                i = j
            else:
                i += 1
    return examples


def book_numbers_for(body: str):
    """Extract book numbers to check: admonition body minus input code + source.

    Python and SQL fences are the example's INPUT (shown code), not its output,
    so numbers inside them (literals, seeds, slice bounds) are not claims the
    demo must reproduce.
    """
    no_src = SOURCE_RE.sub("", body)
    no_py = PYFENCE_RE.sub("", no_src)
    no_sql = SQLFENCE_RE.sub("", no_py)
    nums = extract_numbers(no_sql)
    inf = has_inf(no_sql)
    return nums, inf


# ---------------------------------------------------------------------------
# Running the demos
# ---------------------------------------------------------------------------

def import_module_from(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = mod
    spec.loader.exec_module(mod)
    return mod


def demo_functions_in_order(mod):
    demos = [
        (name, obj)
        for name, obj in vars(mod).items()
        if name.startswith("demo_") and callable(obj)
        and getattr(obj, "__module__", None) == mod.__name__
    ]
    demos.sort(key=lambda kv: kv[1].__code__.co_firstlineno)
    return demos


def run_all():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    results = {}  # (file, func) -> stdout
    for fname in EXAMPLE_FILES:
        path = COMP_DIR / fname
        mod = import_module_from(path)
        for name, fn in demo_functions_in_order(mod):
            buf = io.StringIO()
            try:
                with redirect_stdout(buf):
                    fn()
                out = buf.getvalue()
            except Exception as exc:  # noqa: BLE001
                out = buf.getvalue() + f"\n<<EXCEPTION>> {type(exc).__name__}: {exc}\n"
            results[(fname, name)] = out
            (RAW_DIR / f"{fname[:-3]}__{name}.txt").write_text(out, encoding="utf-8")
    return results


# ---------------------------------------------------------------------------
# Adjudicated residuals: book numbers that legitimately do NOT appear verbatim
# in stdout -- prose-derived arithmetic, "~" approximations, or rounded
# presentation, traced by hand during Phase 3 reconciliation. Keyed by
# (file, func) -> {tokens, reason}. If a function's actual unmatched set grows
# beyond `tokens`, the extra token is reported as UNEXPLAINED, so this
# allowlist cannot hide a newly-introduced mismatch.
# ---------------------------------------------------------------------------
ADJUDICATED: dict[tuple[str, str], dict] = {}


def main():
    print(f"Discovering demos in {len(EXAMPLE_FILES)} example files under", sys.executable)
    results = run_all()
    print(f"Captured stdout for {len(results)} functions.\n")

    examples = parse_docs()
    print(f"Parsed {len(examples)} example admonitions from docs/.\n")

    # Cross-check coverage.
    run_keys = set(results)
    doc_keys = set(examples)
    missing_in_docs = sorted(run_keys - doc_keys)
    missing_in_code = sorted(doc_keys - run_keys)

    report_lines = []
    n_pass = n_flag = n_err = n_adj = n_nonum = 0
    flagged = []

    for key in sorted(run_keys | doc_keys):
        fname, func = key
        stdout = results.get(key)
        ex = examples.get(key)
        if stdout is None:
            report_lines.append(f"[NO-CODE ] {fname} :: {func}  (in docs, no function run)")
            continue
        if "<<EXCEPTION>>" in stdout:
            n_err += 1
            flagged.append(key)
            report_lines.append(f"[ERROR   ] {fname} :: {func}  (raised exception)")
            continue
        if ex is None:
            report_lines.append(f"[NO-DOCS ] {fname} :: {func}  (ran, no admonition found)")
            continue

        nums, book_inf = book_numbers_for(ex["body"])

        # Qualitative examples carry no numbers to check. Report them as
        # NO-NUMS rather than silently awarding an (unverifiable) PASS.
        if not nums and not book_inf:
            n_nonum += 1
            report_lines.append(
                f"[NO-NUMS ] {fname} :: {func}  (qualitative example, no numbers to verify)"
            )
            continue

        stdout_vals = stdout_number_set(stdout)
        not_found = []
        for tok, val, dec, is_pct, is_sci in nums:
            if not book_number_found(val, dec, stdout_vals, is_pct, is_sci):
                not_found.append(tok)
        inf_ok = (not book_inf) or has_inf(stdout)

        adj = ADJUDICATED.get(key)
        residual = not_found
        if adj is not None:
            residual = [t for t in not_found if t not in adj["tokens"]]

        if not not_found and inf_ok:
            n_pass += 1
            report_lines.append(
                f"[PASS    ] {fname} :: {func}  ({len(nums)} numbers matched)"
            )
        elif not residual and inf_ok:
            # Every unmatched token is a documented prose/formatting number.
            n_adj += 1
            report_lines.append(
                f"[ADJUDGD ] {fname} :: {func}  ({len(nums)} numbers; "
                f"{len(not_found)} prose/formatting, verified: {adj['reason']})"
            )
        else:
            n_flag += 1
            flagged.append(key)
            detail = []
            if residual:
                detail.append(f"{len(residual)} UNEXPLAINED not in stdout: {residual[:15]}")
            if not inf_ok:
                detail.append("book shows inf/∞ but stdout does not")
            report_lines.append(
                f"[FLAG    ] {fname} :: {func}  ({len(nums)} numbers; " + "; ".join(detail) + ")"
            )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    header = [
        "# Computation verification report",
        "",
        f"- functions run: {len(results)}",
        f"- admonitions in docs: {len(examples)}",
        f"- PASS: {n_pass}   ADJUDICATED (prose/formatting, verified): {n_adj}"
        f"   NO-NUMS (qualitative): {n_nonum}"
        f"   UNEXPLAINED FLAG: {n_flag}   ERROR: {n_err}",
        f"- verified = PASS + ADJUDICATED = {n_pass + n_adj}; "
        f"qualitative (no numbers) = {n_nonum}; "
        f"clean (no FLAG/ERROR) over {len(results)} = {n_flag == 0 and n_err == 0}",
        f"- keys run but no admonition: {missing_in_docs}",
        f"- admonitions but no code: {missing_in_code}",
        "",
        "## Per-function",
        "",
    ]
    (OUT_DIR / "report.md").write_text(
        "\n".join(header + report_lines) + "\n", encoding="utf-8"
    )

    print("\n".join(report_lines))
    print()
    print("=" * 70)
    print(f"PASS={n_pass}  ADJUDICATED={n_adj}  NO-NUMS={n_nonum}  "
          f"UNEXPLAINED FLAG={n_flag}  ERROR={n_err}  (of {len(results)} functions)")
    print(f"verified (PASS+ADJUDICATED) = {n_pass + n_adj}/{len(results)}  "
          f"| qualitative (no numbers) = {n_nonum}  "
          f"| clean (no FLAG/ERROR) = {n_flag == 0 and n_err == 0}")
    if missing_in_docs:
        print(f"Ran but no admonition matched: {missing_in_docs}")
    if missing_in_code:
        print(f"Admonition but no code matched: {missing_in_code}")
    print(f"Raw outputs: {RAW_DIR}")
    print(f"Report: {OUT_DIR / 'report.md'}")
    print("=" * 70)
    return 0 if (n_flag == 0 and n_err == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
