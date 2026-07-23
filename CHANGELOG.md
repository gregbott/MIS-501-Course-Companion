# Changelog

All notable changes to the MIS 501 Course Companion are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-24

### Added

- Companion chapters for all 17 course modules, each derived from the module's
  marimo teaching notebook: introduction, learning objectives, numbered topic
  sections with worked examples, common-misconception tables, reflection
  questions, an assignment overview (task descriptions and point values, no
  solutions), chapter summary, and a bridge to the next module.
- Computation-verification suite: `computations/moduleNN_examples.py` scripts
  whose `demo_*()` functions produce every worked-example output, plus
  `computations/verify_all.py`, which checks that every number shown in a
  worked example appears in the cited function's actual stdout at the displayed
  precision (233 functions, all verified).
- `CODE_EXAMPLE_MAPPING.md` index mapping every demo function to its worked
  example (regenerable via `computations/generate_mapping.py`).
- Q&A Reference page: 134 common student questions with prose answers,
  organized by module.
- MkDocs Material site with search, light/dark themes, and MathJax; pixi
  environments for the docs build (`default`) and the verification suite
  (`compute`); GitHub Actions deployment to GitHub Pages.
