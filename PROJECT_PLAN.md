# MIS 501 Course Companion — Project Plan

This file is the living source of truth for building, verifying, and publishing the
MIS 501 online course companion. Update the status markers and the Findings &
Decisions Log at the end of every phase.

Status markers: `[ ]` pending · `[~]` in progress · `[x]` done · `[!]` blocked/needs user

---

## Context

- **Course:** MIS 501: Application Development for the Data-Driven Organization —
  a 17-module fully online Python course for MBA/graduate students with no prior
  programming experience. Progression: core Python (modules 1–8), data tooling with
  Polars/visualization/Marimo/DuckDB (9–13), data acquisition (14–15), capstone (16–17).
- **Source material:** `/home/gjbott/github/gregbott/1_Projects/590-mis-501-python-online`.
  Canonical sources per module: `module_NN/notebooks/mNN_teaching.py` (marimo teaching
  notebook) and `module_NN/notebooks/mNN_assignment.py` (marimo assignment notebook).
  IGNORE: `*_recording*.py`, `*_orig*`, `*.html`, `__pycache__`.
- **Structural template:** `/home/gjbott/github/nkfreeman/BAN-501-online-course-companion`.
  We replicate its **structure and process only** — MkDocs Material site, per-module docs,
  Q&A reference, computation-verification suite (`computations/` + `verify_all.py`),
  `CODE_EXAMPLE_MAPPING.md`, changelog, GitHub Pages deploy. BAN-501's ML content is NOT
  ported; all content here derives from the MIS 501 teaching notebooks.
- **This repo:** `gregbott/MIS-501-Course-Companion` (public; renamed from 591-mis-501-course-companion on 2026-07-24), site at
  `https://gregbott.github.io/MIS-501-Course-Companion/`.

### User decisions (2026-07-23)

1. **Scope:** 17 module docs + Q&A reference. No deep-dive appendices (no source material).
2. **Verification:** full BAN-501-style replication — `computations/moduleN_examples.py`
   with `demo_*()` functions, `*Source:*` citations on every worked example,
   `verify_all.py`, `CODE_EXAMPLE_MAPPING.md`.
3. **Module tail:** Reflection Questions → **Your Assignment** (explain the graded
   assignment task-by-task WITHOUT giving answers) → Chapter Summary → What's Next.
   No invented Practice Problems section.
4. **Deploy:** GitHub Pages via Actions on push to main; Pages enabled via gh api.

---

## Phases

- [x] **Phase 1 — Repo scaffold & tooling.** `pixi.toml` (docs + compute envs),
  `mkdocs.yml`, docs skeleton + stubs, CI workflow, `.gitignore`, `README.md`,
  `CHANGELOG.md`. Done when `mkdocs build --strict` passes on the skeleton.
- [x] **Phase 2 — Module content + computations (subagent fan-out).** For each of the
  17 modules: author `docs/modules/NN-slug.md` from `mNN_teaching.py` +
  `mNN_assignment.py`, and `computations/moduleN_examples.py` whose `demo_*()`
  functions produce every worked-example output verbatim. Agents run their own
  scripts (`pixi run -e compute python ...`) and paste real stdout into the docs.
- [x] **Phase 3 — Verification harness.** Adapt BAN-501's `verify_all.py` (numeric-aware
  comparison of doc Output blocks vs. actual demo stdout, ADJUDICATED allowlist).
  Run, reconcile every mismatch, generate `CODE_EXAMPLE_MAPPING.md`.
- [x] **Phase 4 — Q&A reference.** `docs/reference/qa.md`: ~6–8 common student
  questions per module, derived from the teaching notebooks, organized by module.
- [x] **Phase 5 — Review pass.** Cross-module consistency (skeleton, admonition shape,
  terminology), answer-leak audit of every Your Assignment section, link check,
  `mkdocs build --strict` clean.
- [x] **Phase 6 — Changelog & polish.** Finalize `CHANGELOG.md` v1.0.0, README polish.
- [x] **Phase 7 — Publish.** Commit, push to main, enable GitHub Pages
  (Source: GitHub Actions), confirm live deploy, tag `v1.0.0`.

Commit at phase boundaries. Trailer: `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.

---

## Module map

| # | Doc file | Title (nav) | Source teaching / assignment |
|---|----------|-------------|------------------------------|
| 1 | `modules/01-why-python-and-setup.md` | Why Python & Environment Setup | `module_01/notebooks/m01_{teaching,assignment}.py` |
| 2 | `modules/02-variables-and-types.md` | Variables, Data Types & Expressions | `module_02/...` |
| 3 | `modules/03-control-flow.md` | Control Flow | `module_03/...` |
| 4 | `modules/04-functions.md` | Functions & Modular Thinking | `module_04/...` |
| 5 | `modules/05-strings-and-regex.md` | Strings & Regular Expressions | `module_05/...` |
| 6 | `modules/06-lists-and-tuples.md` | Data Structures: Lists & Tuples | `module_06/...` |
| 7 | `modules/07-dictionaries-and-sets.md` | Data Structures: Dictionaries & Sets | `module_07/...` |
| 8 | `modules/08-file-io-and-json.md` | File I/O & Working with JSON | `module_08/...` |
| 9 | `modules/09-polars-intro.md` | Introduction to Polars | `module_09/...` |
| 10 | `modules/10-polars-transformations.md` | Polars: Transformations & Aggregations | `module_10/...` |
| 11 | `modules/11-visualization.md` | Visualization: Matplotlib & Plotly Express | `module_11/...` |
| 12 | `modules/12-marimo-interactivity.md` | Marimo Interactive Features | `module_12/...` |
| 13 | `modules/13-duckdb-sql.md` | DuckDB: SQL-Based Data Analysis | `module_13/...` |
| 14 | `modules/14-web-scraping.md` | Web Scraping | `module_14/...` |
| 15 | `modules/15-rest-apis.md` | REST APIs & Data Acquisition | `module_15/...` |
| 16 | `modules/16-capstone-proposal.md` | Capstone: Proposal & Data Acquisition | `module_16/...` |
| 17 | `modules/17-capstone-analysis.md` | Capstone: Analysis & Presentation | `module_17/...` |

---

## Authoring spec (Phase 2 — read this before writing a module doc)

### Module doc skeleton (exact heading order; `---` rule between H2 blocks)

```
# Module N: <Title>

## Introduction            — 1 paragraph: why this module matters to business students
## Learning Objectives     — numbered list, bold action verbs; adapt from the teaching notebook
## N.1 <Major Topic>       — 2–5 numbered H2 topic sections per module, following the
   ### <Sub-topic>           teaching notebook's own progression; H3/H4 for subdivisions
   ...                       each N.x section ends with a "### Common Misconceptions" table
## N.2 <Major Topic> ...     when the source material surfaces real beginner confusions
## Reflection Questions    — 4–6 numbered open-ended questions
## Your Assignment         — see rules below
## Chapter Summary         — 2–4 paragraphs
## What's Next             — short bridge to the next module (module 17: course wrap-up)
```

Target length ≈ 600–1,000 lines (up to ~1,250 where the source's demo volume demands
it). Pipe tables for comparisons/misconceptions. Math only where the source uses
formulas (arithmetic, interest) — `$...$` / `$$...$$`.

### Worked Example admonition (the verification unit)

Every substantive code demonstration from the teaching notebook becomes:

```
!!! example "Worked Example: <Short Title>"

    ```python
    <the demo code, readable for beginners>
    ```

    **Output:**

    ```
    <VERBATIM stdout of the cited demo function — copy-paste, do not retype>
    ```

    **Interpretation:** <1–3 sentences of business-relevant meaning>

    *Source: `computations/moduleN_examples.py` — `demo_<name>()`*
```

4-space indent inside the admonition. Curation of Output (trimming long repetition) is
allowed but every NUMBER shown must appear verbatim in the function's stdout —
`verify_all.py` enforces exact match at displayed precision.

VERIFIER SCOPE — the harness checks every number in the ENTIRE admonition body
outside python/sql fences: the title, the Output block, AND the Interpretation
prose (including inline backtick code). Only cite numbers that literally appear in
the demo's stdout. If prose needs an input value ("the $10,000 principal…"), either
have the demo print an input-recap line so the value is in stdout, or write the
prose without digits ("the principal grows…"). Genuinely prose-derived arithmetic
goes in `verify_all.py`'s ADJUDICATED allowlist — but only the orchestrator edits
that file; agents report proposed entries instead of editing it.

"Try It Yourself" prompts from the teaching notebook are preserved inline as
`!!! question "Try It Yourself: <Topic>"` admonitions (prompt only, no solution).

### computations/moduleNN_examples.py conventions

- Filename is zero-padded: `module01_examples.py` … `module17_examples.py`; the
  `*Source:*` citation in docs uses the same zero-padded name.
- Plain Python script (NOT marimo). Header docstring lists
  `References in Course Companion: demo_x() -> Module N, Section N.y (<Title>)` and
  `Last updated: <date>`.
- One `demo_<snake_case>()` per worked example, `print()`-ing its output.
  `if __name__ == "__main__":` calls all demos in doc order with separator headers.
- Deterministic: `random.seed(42)` / `np.random.seed(42)` where randomness exists;
  polars-first for tabular work; NO network access — modules 14/15 embed sample
  HTML/JSON literals in the script; module 8 file demos write/read under
  `computations/_scratch/moduleNN/` (deterministic relative paths only — never print
  absolute paths); module 12 simulates widget values as plain variables; module 11
  demos print the numbers behind each chart (totals, extremes, counts) rather than
  rendering figures — chart-building code still appears in the doc's python fence.
- `pl.Config` note: leave default DataFrame printing; docs paste it verbatim.

### Your Assignment section rules (strict)

- State: total points (100 + 10 bonus), format (marimo `.py` notebook), submission
  (Blackboard), and that the reflection section is participation credit.
- Per task: task name, point value, a 2–3 sentence paraphrase of WHAT it asks, and
  which module sections (§N.x) supply the needed concepts.
- NEVER: solution code, final answers, partial solution snippets, or reproduction of
  the assignment's expected-output values. Describing WHICH functions/methods a task
  exercises is fine; showing the call that produces a task's answer is not.

### Tone & style

- Audience: MBA students, first programming course. Business-flavored examples
  (invoices, payroll, inventory) mirroring the teaching notebooks' own scenarios.
- State facts without emphatic qualifiers (no "extremely", "absolutely", "incredibly").
- Course terms: Pixi (environments), marimo (reactive notebooks), Polars (not pandas),
  DuckDB, Plotly Express. `random_state`/seed 42 convention where sampling appears.

---

## Findings & Decisions Log

- **2026-07-24 (post-1.0.0):** Repo renamed to `MIS-501-Course-Companion` at Greg's
  request. GitHub redirects the old repo URL; the old Pages URL does NOT redirect —
  new site URL is https://gregbott.github.io/MIS-501-Course-Companion/. Updated
  mkdocs.yml (site_url/repo_url/repo_name), README, this file's Context, and the
  local git remote. Local folder name left as `591-mis-501-course-companion`.
- **2026-07-24 (Phase 7):** Published. GitHub Pages enabled (Source: GitHub Actions)
  BEFORE the first push, so the first deploy succeeded. Live at
  https://gregbott.github.io/591-mis-501-course-companion/ (home + spot-checked module
  pages return 200). Tagged v1.0.0.
- **2026-07-24 (Phases 4–6):** Q&A reference authored (134 questions, 17 modules).
  Review pass: structural consistency — zero blockers, 3 minor fixes applied (module 11
  question-title form, lowercase marimo in modules 16/17); module 1's reflection-points
  wording intentionally differs (its source assignment grades the reflection 10/100,
  unlike modules 2–17 — source-faithful, kept). Answer-leak audit: all 17 chapters
  CLEAN, all task/part point values match the assignment files exactly. CHANGELOG
  v1.0.0 finalized. Source quirk worth fixing upstream: m01_assignment.py task points
  sum to 90 (+10 bonus) though its header says Total 100.
- **2026-07-23 (Phases 2–3):** All 17 modules authored by subagent fan-out (3 pilots,
  then batches of 7). 233 demo functions; verify suite fully clean (222 PASS, 11
  NO-NUMS qualitative, 0 FLAG/ERROR, empty ADJUDICATED — all prose-number flags were
  resolved by digit-free rewrites or input-recap prints). CODE_EXAMPLE_MAPPING.md:
  17 files → 233 functions → 17 pages, 0 problems. Notable conventions: modules
  16/17 use the notebooks' own seed 501; modules 14/15 run fully offline via
  embedded HTML/JSON samples; module 17 demos use the teaching notebook's
  coffee-shop dataset, never the graded library dataset (answer firewall audited).
- **2026-07-23 (Phase 1):** Repo scaffolded. Slugs/titles fixed in Module map above.
  Compute env excludes CUDA (course stack is CPU-only: polars, duckdb, matplotlib,
  plotly, numpy, requests, beautifulsoup4). Modules 14/15 demos must be offline
  (embedded HTML/JSON) so `verify_all.py` stays deterministic.

---

## Resume prompt

If resuming mid-project: read this file top to bottom, check phase markers, then
continue with the first non-`[x]` phase. Phase 2 fan-out: one subagent per module,
each reads this spec + its two source notebooks, writes the module doc + computations
file, runs the script via `pixi run -e compute python computations/moduleN_examples.py`,
and pastes real stdout into Output blocks.
