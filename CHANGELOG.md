# Changelog

All notable changes to the MIS501 Course Companion are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Module 16.1 bike-sharing walkthrough: `day_of_week` was drawn at random,
  independently of `date`, so the two disagreed in 171 of 204 rows (the first
  row showed 2025-01-15 as a Saturday). Each date now moves forward to the first
  day matching its weekday (back a week if that would pass the 28th), staying
  within its month. The random calls are unchanged, so
  every other value and every number in the chapter is the same; only the dates
  in the displayed first ten rows changed. The chapter's code listing also drew
  its random values in a different order from `computations/module16_examples.py`
  and the notebook, so running it gave different data from the output shown; it
  now matches and reproduces the displayed output exactly.
- The companion now matches the course's 16-module structure. The two capstone
  chapters are Module 16.1 (Proposal & Data Acquisition) and Module 16.2
  (Analysis & Presentation), matching Blackboard, instead of Modules 16 and 17.
  Their sections are renumbered 16.1.1–16.1.5 and 16.2.1–16.2.5, and every
  cross-reference, the navigation, the home-page roadmap, the Q&A Reference
  headings and the "seventeen modules" wording were updated. Page URLs are
  unchanged, but the section anchors on both capstone pages and the two capstone
  Q&A anchors changed (see BLACKBOARD_GUIDE.md appendices B and C).
- Submission platform corrected from Brightspace to Blackboard throughout the
  companion (20 references: the *Your Assignment* section of all 17 module
  chapters, two further mentions in Module 1, and one in the Q&A Reference).
  The course is delivered in Blackboard; the Brightspace wording was carried
  over from an earlier delivery.
- Repository renamed from `591-mis-501-course-companion` to
  `MIS-501-Course-Companion`. The site now lives at
  <https://gregbott.github.io/MIS-501-Course-Companion/>; the previous Pages URL
  no longer resolves (GitHub Pages does not redirect renamed project paths).

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
