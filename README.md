# MIS501 Course Companion

Online course companion for **MIS501: Application Development for the Data-Driven
Organization** — a 16-module Python course for business graduate students.

Live site: <https://gregbott.github.io/MIS-501-Course-Companion/>

## What this is

A student-facing reference that parallels the course's video lectures and marimo
notebooks: one companion chapter per module, plus a Q&A reference. Every worked
example in the companion is produced by a script in `computations/`, so the outputs
you read are reproducible.

## Repository layout

```
docs/                  MkDocs content (modules, Q&A reference, changelog)
computations/          moduleN_examples.py demo scripts + verify_all.py harness
mkdocs.yml             Site configuration (Material theme)
pixi.toml              Environments: default (docs build) and compute (verification)
PROJECT_PLAN.md        Living build plan, authoring spec, and decisions log
CODE_EXAMPLE_MAPPING.md  Index: every demo_*() function -> its Worked Example
```

## Working locally

```bash
pixi install                 # docs environment
pixi run serve               # live-reload preview at http://127.0.0.1:8000
pixi run build               # strict static build (fails on broken links/nav)

pixi run -e compute verify   # re-run all computation verifications
```

## Updating content

1. Edit the module doc in `docs/modules/`, and if a Worked Example changes, update the
   matching `demo_*()` function in `computations/moduleN_examples.py`.
2. Run `pixi run -e compute verify` — every number in an Output block must match the
   demo function's actual stdout.
3. Add a `CHANGELOG.md` entry (the in-site changelog page renders it automatically).
4. Push to `main`. GitHub Actions builds with `mkdocs build --strict` and deploys to
   GitHub Pages. One-time repo setting: GitHub → Settings → Pages → Source: GitHub Actions.
