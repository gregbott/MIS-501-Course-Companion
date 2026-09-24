# Linking the MIS501 Course Companion into Blackboard

**Audience:** course creators and instructional designers building the Blackboard
shell for MIS501: Application Development for the Data-Driven Organization.

**What you need from this document:** the companion is already published on the open
web. You are not hosting it, copying it, or converting it. Your job is to point
Blackboard at the right URLs, and this document gives you every URL you will need
plus the conventions to use them consistently.

---

## 1. What the companion is

The MIS501 Course Companion is a 17-chapter student-facing reference for the 16-module
course (the Module 16 capstone has two chapters, 16.1 and 16.2). It parallels
the course's video lectures and marimo notebooks. Each chapter covers the same
concepts as its module, with worked examples, common misconceptions, reflection
questions, and a plain-language walkthrough of the module's graded assignment.

It is **not** a replacement for the lectures or the notebooks, and it contains **no
assignment solutions**. It is the reading companion students turn to before, during,
and after a module.

The site also includes a Q&A Reference — 134 of the questions students most often ask,
organized by module — and a changelog.

| | |
|---|---|
| **Live site** | <https://gregbott.github.io/MIS-501-Course-Companion/> |
| **Hosted on** | GitHub Pages (public, HTTPS, no login) |
| **Source repository** | <https://github.com/gregbott/MIS-501-Course-Companion> |
| **Content owner** | Gregory Bott |

---

## 2. Before you start: three things that are already true

**It is already published.** Nothing needs to be deployed, exported, or uploaded. The
site is live right now and every URL in this document resolves today.

**It updates itself.** When the instructor pushes a content change, GitHub Actions
rebuilds and redeploys the site automatically, usually within a minute. Any link you
place in Blackboard keeps working and always shows the current version. You never need
to re-upload anything at the start of a term.

**It is fully public.** There is no login, no enrollment check, and no LTI
integration. Anyone with the URL can read it. That is intentional — it makes linking
trivial — but it means the companion must never carry solutions, keys, or anything
FERPA-sensitive. Keep graded material in Blackboard.

> **Do not copy the content into Blackboard.** Pasting chapters into Blackboard
> Documents creates a fork that silently goes stale the first time the instructor
> revises a chapter. Always link.

---

## 3. The URL pattern

Every page has its own permanent URL. The pattern is:

```
https://gregbott.github.io/MIS-501-Course-Companion/modules/<module-slug>/
```

For example, Module 3:

```
https://gregbott.github.io/MIS-501-Course-Companion/modules/03-control-flow/
```

Note the **trailing slash** — include it. The site will redirect without it, but the
redirect adds a round trip and some link-checkers flag it.

The two non-module pages you will most likely link:

```
https://gregbott.github.io/MIS-501-Course-Companion/reference/qa/     (Q&A Reference)
https://gregbott.github.io/MIS-501-Course-Companion/                  (Home)
```

**Appendix A** lists all 17 chapter URLs in a copy-paste table.

---

## 4. Linking to a specific section

This is the part worth using well. Every heading on every page has an anchor, so you
can send a student to one exact subsection instead of a whole chapter. Append the
anchor to the module URL:

```
https://gregbott.github.io/MIS-501-Course-Companion/modules/03-control-flow/#33-for-loops-and-range
```

That lands the reader directly on *3.3 for Loops and range()*.

Each module chapter has the same section skeleton, which makes the conventions easy to
apply across all 17 chapters:

| Section | Anchor | Typical Blackboard use |
|---|---|---|
| Introduction | `#introduction` | Module overview page |
| Learning Objectives | `#learning-objectives` | Paste alongside the module's stated outcomes |
| Numbered topics (e.g. 3.1–3.5) | `#31-…` through `#35-…` | Attach to the specific lecture video or activity that covers it |
| Reflection Questions | `#reflection-questions` | Discussion board prompt seed |
| Your Assignment | `#your-assignment` | Link from the assignment's instructions |
| Chapter Summary | `#chapter-summary` | Pre-exam review |
| What's Next | `#whats-next` | End-of-module wrap |

**Appendix B** lists every section anchor for all 17 chapters. **Appendix C** does the
same for the Q&A Reference, so you can link to just the Module 7 questions rather than
the whole 134-question page.

### How to find an anchor yourself

Open the page, hover over any heading, and a **¶** symbol appears to its right.
Right-click it and choose *Copy link address* — you get the full URL with the anchor
already attached.

---

## 5. Putting the links into Blackboard Ultra

### 5a. A link in a Learning Module (the recommended default)

Use this for the main "read this chapter" pointer inside each module's folder.

1. **Course Content** → open the Learning Module for the course module.
2. Click the **+** where you want the item → **Create** → **Link**.
3. **Link URL:** paste the module URL from Appendix A.
4. **Link Display Name:** follow the naming convention in §6.
5. **Description:** one sentence on when to read it (see §6 for suggested text).
6. Set **Visible to students**.
7. Save.

### 5b. An inline link inside a Document or an Assignment

Use this when the pointer belongs *inside* prose — assignment instructions, a module
overview, an announcement.

1. In the content editor, type and select the words that should become the link.
   Select meaningful words, not a bare URL and not "click here."
2. Click the **link** icon in the toolbar (or press **Ctrl+K** / **Cmd+K**).
3. Paste the URL, including any `#anchor`.
4. Insert.

This is the right place to use deep links. In a Module 3 assignment, for instance,
link the phrase *"loop over a range of values"* to the `#33-for-loops-and-range`
anchor rather than making students hunt through the chapter.

### 5c. Embedding the page inside Blackboard

The site can be displayed in an iframe if you want the chapter to appear without
leaving the course — it sets no `X-Frame-Options` or frame-ancestors restriction, so
embedding works.

That said, **prefer a plain link.** The companion uses a full documentation theme with
its own left navigation, search, and table of contents; squeezed into a Blackboard
content frame it becomes cramped and hard to navigate, and the double scrollbar is a
common accessibility complaint. Embedding also hides the URL, so students cannot
bookmark or share the page.

If you do embed, use the HTML view of the content editor and give the iframe a
descriptive `title` attribute:

```html
<iframe
  src="https://gregbott.github.io/MIS-501-Course-Companion/modules/03-control-flow/"
  title="MIS501 Course Companion — Module 3: Control Flow"
  width="100%" height="800" style="border:1px solid #ccc;">
</iframe>
```

### 5d. Blackboard Original (if your shell is not Ultra)

**Build Content** → **Web Link**. Enter the name and URL, set *Open in New Window* to
**Yes**, and leave *This link is to a Tool Provider* set to **No** — the companion is a
plain web page, not an LTI tool. Do not attempt an LTI configuration; there is nothing
to configure.

### 5e. Open in a new window?

Set links to open in a new tab. Students typically read the companion **while** working
in the assignment or the notebook, and losing their place in Blackboard to navigate to
a reading is a small but constant friction. In Ultra this is the default behavior for
Link items.

---

## 6. Naming and description conventions

Consistency matters more than cleverness here — students should be able to recognize
the companion at a glance in a content list that also holds videos, notebooks, and
assignments.

**Use this display name format:**

```
Course Companion — Module N: <Module Title>
```

For example: `Course Companion — Module 3: Control Flow`

**For a deep link, name the destination, not the chapter:**

```
Course Companion — 3.3 for Loops and range()
```

**Suggested description text** (adjust per module):

> Read alongside the Module N lecture videos. Covers the same concepts with worked
> examples you can run, common mistakes to avoid, and a walkthrough of what the
> assignment is asking for. No solutions.

**Avoid:** "Click here," "Course website," bare URLs as link text, and display names
that differ from module to module. Screen-reader users navigate by pulling a list of
link texts out of the page; "click here" tells them nothing.

---

## 7. A recommended per-module build pattern

Applied to each of the 17 chapters, this gives students the companion at the three
moments they need it. Steal what fits your shell.

| Where in Blackboard | What to link | Anchor |
|---|---|---|
| Top of the module's Learning Module | The chapter itself | none (whole page) |
| Next to the module's learning outcomes | Learning Objectives | `#learning-objectives` |
| Inside the assignment instructions | Your Assignment | `#your-assignment` |
| Discussion board prompt | Reflection Questions | `#reflection-questions` |
| Module wrap-up or review item | Chapter Summary | `#chapter-summary` |
| Course-wide "Get Help" area | Q&A Reference | none (whole page) |

Add one course-level link outside the module structure — in **Course Information**, a
**Start Here** module, or the syllabus — pointing at the site home page, so students
who lose a module link can always find their way back.

---

## 8. Accessibility notes

The site is built with the MkDocs Material theme, which handles most of the basics for
you: semantic headings, keyboard-navigable menus, a light/dark toggle, responsive
layout down to phone width, and copy buttons on every code block. What you control on
the Blackboard side:

- **Descriptive link text.** Cover this by following §6.
- **Don't rely on the embed.** §5c's iframe is harder to navigate by keyboard than a
  plain link; if you embed, also provide the direct link nearby.
- **Say where the link goes.** Because the companion lives outside Blackboard, note in
  the description that it opens a public website in a new tab, so nobody is surprised
  by leaving the course.
- **Code is real text.** Every code block is selectable text with a copy button, not a
  screenshot, so it works with screen readers and with students who enlarge text.

---

## 9. What can break a link, and what cannot

**Safe — these do not affect your links:**

- The instructor revising the wording of a chapter.
- Adding, correcting, or re-verifying a worked example.
- Anything in the changelog.

**Breaks a deep link (`#anchor`):** renaming a heading. The anchor is generated from
the heading text, so changing *"3.3 for Loops and range()"* to *"3.3 Looping with
range()"* silently changes the anchor. The page still loads; the student just lands at
the top instead of the section. No error is shown, which is exactly what makes this
worth watching.

**Breaks a page link:** renaming or renumbering a module file, or renaming the GitHub
repository. The link returns a 404.

**Practical guidance:** once a term's Blackboard shell is built, treat module headings
and filenames as frozen for that term. If a heading genuinely must change mid-term,
ask the instructor to flag it so the affected Blackboard links can be updated in the
same pass. A link check at the start of each term — clicking through Appendix A — takes
about five minutes and catches everything.

---

## 10. How the companion refers to the LMS

The companion names **Blackboard** as the submission platform throughout — once in
each of the 17 chapters (in the *Your Assignment* section, where it tells
students to submit the marimo `.py` file), twice more in Module 1, and once in the
Q&A Reference. Twenty references in all, and they are consistent with the Blackboard
shell you are building.

This was corrected on 2026-08-26; the chapters previously said *Brightspace*, carried
over from an earlier delivery. If you find a stray *Brightspace* anywhere in the live
site, it is a bug — report it rather than papering over it in Blackboard.

The companion deliberately does not name specific Blackboard locations ("the Module 3
assignment folder"), only the platform. Where an assignment lives inside the shell is
yours to define, and keeping it out of the companion means reorganizing the shell
never makes the reading stale.

---

## 11. Who to contact

| Need | Contact |
|---|---|
| Content correction, a broken example, a heading rename | Gregory Bott (content owner) |
| A new page or section you want to link to | Gregory Bott |
| Blackboard shell, LTI, enrollment, gradebook | Your institutional Blackboard support |

The site's own **Changelog** page lists what changed and when, which is the fastest way
to check whether a content update affects links you have already placed.

---

## Appendix A — Every module URL

Copy the URL column straight into Blackboard's **Link URL** field.

| # | Module | URL |
|---|--------|-----|
| 1 | Why Python & Environment Setup | `https://gregbott.github.io/MIS-501-Course-Companion/modules/01-why-python-and-setup/` |
| 2 | Variables, Data Types & Expressions | `https://gregbott.github.io/MIS-501-Course-Companion/modules/02-variables-and-types/` |
| 3 | Control Flow | `https://gregbott.github.io/MIS-501-Course-Companion/modules/03-control-flow/` |
| 4 | Functions & Modular Thinking | `https://gregbott.github.io/MIS-501-Course-Companion/modules/04-functions/` |
| 5 | Strings & Regular Expressions | `https://gregbott.github.io/MIS-501-Course-Companion/modules/05-strings-and-regex/` |
| 6 | Data Structures: Lists & Tuples | `https://gregbott.github.io/MIS-501-Course-Companion/modules/06-lists-and-tuples/` |
| 7 | Data Structures: Dictionaries & Sets | `https://gregbott.github.io/MIS-501-Course-Companion/modules/07-dictionaries-and-sets/` |
| 8 | File I/O & Working with JSON | `https://gregbott.github.io/MIS-501-Course-Companion/modules/08-file-io-and-json/` |
| 9 | Introduction to Polars | `https://gregbott.github.io/MIS-501-Course-Companion/modules/09-polars-intro/` |
| 10 | Polars: Transformations & Aggregations | `https://gregbott.github.io/MIS-501-Course-Companion/modules/10-polars-transformations/` |
| 11 | Visualization: Matplotlib & Plotly Express | `https://gregbott.github.io/MIS-501-Course-Companion/modules/11-visualization/` |
| 12 | Marimo Interactive Features | `https://gregbott.github.io/MIS-501-Course-Companion/modules/12-marimo-interactivity/` |
| 13 | DuckDB: SQL-Based Data Analysis | `https://gregbott.github.io/MIS-501-Course-Companion/modules/13-duckdb-sql/` |
| 14 | Web Scraping | `https://gregbott.github.io/MIS-501-Course-Companion/modules/14-web-scraping/` |
| 15 | REST APIs & Data Acquisition | `https://gregbott.github.io/MIS-501-Course-Companion/modules/15-rest-apis/` |
| 16.1 | Capstone: Proposal & Data Acquisition | `https://gregbott.github.io/MIS-501-Course-Companion/modules/16-capstone-proposal/` |
| 16.2 | Capstone: Analysis & Presentation | `https://gregbott.github.io/MIS-501-Course-Companion/modules/17-capstone-analysis/` |

Two more pages worth linking:

| Page | URL |
|------|-----|
| Home / How to use this companion | `https://gregbott.github.io/MIS-501-Course-Companion/` |
| Q&A Reference (134 questions) | `https://gregbott.github.io/MIS-501-Course-Companion/reference/qa/` |
| Changelog | `https://gregbott.github.io/MIS-501-Course-Companion/changelog/` |

---

## Appendix B — Every linkable section

Append one of these anchors to the module URL to land the student on that exact
section. Example:

```
https://gregbott.github.io/MIS-501-Course-Companion/modules/03-control-flow/#33-for-loops-and-range
```

### Module 1: Why Python & Environment Setup

`https://gregbott.github.io/MIS-501-Course-Companion/modules/01-why-python-and-setup/`

| Section | Anchor to append |
|---------|------------------|
| Introduction | `#introduction` |
| Learning Objectives | `#learning-objectives` |
| 1.1 Why Python? | `#11-why-python` |
| 1.2 Setting Up Your Environment with Pixi | `#12-setting-up-your-environment-with-pixi` |
| 1.3 Marimo: A Reactive Notebook | `#13-marimo-a-reactive-notebook` |
| 1.4 Your First Python Code | `#14-your-first-python-code` |
| 1.5 print(), Variables, and Comments | `#15-print-variables-and-comments` |
| Reflection Questions | `#reflection-questions` |
| Your Assignment | `#your-assignment` |
| Chapter Summary | `#chapter-summary` |
| What's Next | `#whats-next` |

### Module 2: Variables, Data Types & Expressions

`https://gregbott.github.io/MIS-501-Course-Companion/modules/02-variables-and-types/`

| Section | Anchor to append |
|---------|------------------|
| Introduction | `#introduction` |
| Learning Objectives | `#learning-objectives` |
| 2.1 Variables and Assignment | `#21-variables-and-assignment` |
| 2.2 Core Data Types | `#22-core-data-types` |
| 2.3 Arithmetic and Comparison Operators | `#23-arithmetic-and-comparison-operators` |
| 2.4 Dynamic Typing and Type Conversion | `#24-dynamic-typing-and-type-conversion` |
| 2.5 F-Strings: Clean Output Formatting | `#25-f-strings-clean-output-formatting` |
| Reflection Questions | `#reflection-questions` |
| Your Assignment | `#your-assignment` |
| Chapter Summary | `#chapter-summary` |
| What's Next | `#whats-next` |

### Module 3: Control Flow

`https://gregbott.github.io/MIS-501-Course-Companion/modules/03-control-flow/`

| Section | Anchor to append |
|---------|------------------|
| Introduction | `#introduction` |
| Learning Objectives | `#learning-objectives` |
| 3.1 Conditional Statements: if, elif, else | `#31-conditional-statements-if-elif-else` |
| 3.2 Logical Operators: and, or, not | `#32-logical-operators-and-or-not` |
| 3.3 for Loops and range() | `#33-for-loops-and-range` |
| 3.4 while Loops and Loop Control | `#34-while-loops-and-loop-control` |
| 3.5 Nested Logic and Common Loop Patterns | `#35-nested-logic-and-common-loop-patterns` |
| Reflection Questions | `#reflection-questions` |
| Your Assignment | `#your-assignment` |
| Chapter Summary | `#chapter-summary` |
| What's Next | `#whats-next` |

### Module 4: Functions & Modular Thinking

`https://gregbott.github.io/MIS-501-Course-Companion/modules/04-functions/`

| Section | Anchor to append |
|---------|------------------|
| Introduction | `#introduction` |
| Learning Objectives | `#learning-objectives` |
| 4.1 From Repetition to Reuse: The DRY Principle | `#41-from-repetition-to-reuse-the-dry-principle` |
| 4.2 Function Fundamentals: Defining, Calling, and Returning | `#42-function-fundamentals-defining-calling-and-returning` |
| 4.3 Keyword Arguments and Default Values | `#43-keyword-arguments-and-default-values` |
| 4.4 Variable Scope and Docstrings | `#44-variable-scope-and-docstrings` |
| 4.5 Modular Thinking: Refactoring, Lambdas, and the Payroll Report | `#45-modular-thinking-refactoring-lambdas-and-the-payroll-report` |
| Reflection Questions | `#reflection-questions` |
| Your Assignment | `#your-assignment` |
| Chapter Summary | `#chapter-summary` |
| What's Next | `#whats-next` |

### Module 5: Strings & Regular Expressions

`https://gregbott.github.io/MIS-501-Course-Companion/modules/05-strings-and-regex/`

| Section | Anchor to append |
|---------|------------------|
| Introduction | `#introduction` |
| Learning Objectives | `#learning-objectives` |
| 5.1 String Indexing and Slicing | `#51-string-indexing-and-slicing` |
| 5.2 Essential String Methods | `#52-essential-string-methods` |
| 5.3 Regular Expressions and the re Module | `#53-regular-expressions-and-the-re-module` |
| 5.4 Building Patterns: Character Classes, Quantifiers, and Groups | `#54-building-patterns-character-classes-quantifiers-and-groups` |
| 5.5 Cleaning and Parsing Business Text | `#55-cleaning-and-parsing-business-text` |
| Reflection Questions | `#reflection-questions` |
| Your Assignment | `#your-assignment` |
| Chapter Summary | `#chapter-summary` |
| What's Next | `#whats-next` |

### Module 6: Data Structures: Lists & Tuples

`https://gregbott.github.io/MIS-501-Course-Companion/modules/06-lists-and-tuples/`

| Section | Anchor to append |
|---------|------------------|
| Introduction | `#introduction` |
| Learning Objectives | `#learning-objectives` |
| 6.1 Lists: Creating, Indexing, and Slicing | `#61-lists-creating-indexing-and-slicing` |
| 6.2 List Methods: Adding, Removing, and Organizing | `#62-list-methods-adding-removing-and-organizing` |
| 6.3 Iterating Over Lists | `#63-iterating-over-lists` |
| 6.4 List Comprehensions | `#64-list-comprehensions` |
| 6.5 Tuples, Unpacking, and Mutability | `#65-tuples-unpacking-and-mutability` |
| Reflection Questions | `#reflection-questions` |
| Your Assignment | `#your-assignment` |
| Chapter Summary | `#chapter-summary` |
| What's Next | `#whats-next` |

### Module 7: Data Structures: Dictionaries & Sets

`https://gregbott.github.io/MIS-501-Course-Companion/modules/07-dictionaries-and-sets/`

| Section | Anchor to append |
|---------|------------------|
| Introduction | `#introduction` |
| Learning Objectives | `#learning-objectives` |
| 7.1 Dictionaries: Looking Up Data by Name | `#71-dictionaries-looking-up-data-by-name` |
| 7.2 Modifying and Iterating Over Dictionaries | `#72-modifying-and-iterating-over-dictionaries` |
| 7.3 Nested Dictionaries, Comprehensions, and Counting | `#73-nested-dictionaries-comprehensions-and-counting` |
| 7.4 Sets and Set Operations | `#74-sets-and-set-operations` |
| 7.5 Choosing the Right Data Structure | `#75-choosing-the-right-data-structure` |
| Reflection Questions | `#reflection-questions` |
| Your Assignment | `#your-assignment` |
| Chapter Summary | `#chapter-summary` |
| What's Next | `#whats-next` |

### Module 8: File I/O & Working with JSON

`https://gregbott.github.io/MIS-501-Course-Companion/modules/08-file-io-and-json/`

| Section | Anchor to append |
|---------|------------------|
| Introduction | `#introduction` |
| Learning Objectives | `#learning-objectives` |
| 8.1 Reading Text Files | `#81-reading-text-files` |
| 8.2 Writing Text Files | `#82-writing-text-files` |
| 8.3 The pathlib Module | `#83-the-pathlib-module` |
| 8.4 Working with JSON | `#84-working-with-json` |
| 8.5 CSV and the Data Pipeline | `#85-csv-and-the-data-pipeline` |
| Reflection Questions | `#reflection-questions` |
| Your Assignment | `#your-assignment` |
| Chapter Summary | `#chapter-summary` |
| What's Next | `#whats-next` |

### Module 9: Introduction to Polars

`https://gregbott.github.io/MIS-501-Course-Companion/modules/09-polars-intro/`

| Section | Anchor to append |
|---------|------------------|
| Introduction | `#introduction` |
| Learning Objectives | `#learning-objectives` |
| 9.1 Why Polars? DataFrames and Series | `#91-why-polars-dataframes-and-series` |
| 9.2 Reading Data from Files | `#92-reading-data-from-files` |
| 9.3 Selecting Columns with select() | `#93-selecting-columns-with-select` |
| 9.4 Filtering Rows with filter() | `#94-filtering-rows-with-filter` |
| 9.5 Sorting, Writing, and Chaining Pipelines | `#95-sorting-writing-and-chaining-pipelines` |
| Reflection Questions | `#reflection-questions` |
| Your Assignment | `#your-assignment` |
| Chapter Summary | `#chapter-summary` |
| What's Next | `#whats-next` |

### Module 10: Polars: Transformations & Aggregations

`https://gregbott.github.io/MIS-501-Course-Companion/modules/10-polars-transformations/`

| Section | Anchor to append |
|---------|------------------|
| Introduction | `#introduction` |
| Learning Objectives | `#learning-objectives` |
| 10.1 Transforming Columns: Adding, Renaming, and Casting | `#101-transforming-columns-adding-renaming-and-casting` |
| 10.2 Group-By Aggregations | `#102-group-by-aggregations` |
| 10.3 Joining DataFrames | `#103-joining-dataframes` |
| 10.4 Handling Null Values | `#104-handling-null-values` |
| 10.5 Method Chaining: The End-to-End Pipeline | `#105-method-chaining-the-end-to-end-pipeline` |
| Reflection Questions | `#reflection-questions` |
| Your Assignment | `#your-assignment` |
| Chapter Summary | `#chapter-summary` |
| What's Next | `#whats-next` |

### Module 11: Visualization: Matplotlib & Plotly Express

`https://gregbott.github.io/MIS-501-Course-Companion/modules/11-visualization/`

| Section | Anchor to append |
|---------|------------------|
| Introduction | `#introduction` |
| Learning Objectives | `#learning-objectives` |
| 11.1 Getting Started: The Sales Dataset, Figures, and Axes | `#111-getting-started-the-sales-dataset-figures-and-axes` |
| 11.2 The Four Core Chart Types | `#112-the-four-core-chart-types` |
| 11.3 Customization and Multi-Panel Figures | `#113-customization-and-multi-panel-figures` |
| 11.4 Plotly Express and the Polars-to-Visualization Workflow | `#114-plotly-express-and-the-polars-to-visualization-workflow` |
| 11.5 Capstone: A Multi-Chart Business Dashboard | `#115-capstone-a-multi-chart-business-dashboard` |
| Reflection Questions | `#reflection-questions` |
| Your Assignment | `#your-assignment` |
| Chapter Summary | `#chapter-summary` |
| What's Next | `#whats-next` |

### Module 12: Marimo Interactive Features

`https://gregbott.github.io/MIS-501-Course-Companion/modules/12-marimo-interactivity/`

| Section | Anchor to append |
|---------|------------------|
| Introduction | `#introduction` |
| Learning Objectives | `#learning-objectives` |
| 12.1 From Static Notebooks to Interactive Tools | `#121-from-static-notebooks-to-interactive-tools` |
| 12.2 The Core Widgets: Dropdown, Slider, Text, and Checkbox | `#122-the-core-widgets-dropdown-slider-text-and-checkbox` |
| 12.3 Combining Widgets and Interactive Tables | `#123-combining-widgets-and-interactive-tables` |
| 12.4 Layout Composition and Live Charts | `#124-layout-composition-and-live-charts` |
| 12.5 Design Patterns and the Capstone Dashboard | `#125-design-patterns-and-the-capstone-dashboard` |
| Reflection Questions | `#reflection-questions` |
| Your Assignment | `#your-assignment` |
| Chapter Summary | `#chapter-summary` |
| What's Next | `#whats-next` |

### Module 13: DuckDB: SQL-Based Data Analysis

`https://gregbott.github.io/MIS-501-Course-Companion/modules/13-duckdb-sql/`

| Section | Anchor to append |
|---------|------------------|
| Introduction | `#introduction` |
| Learning Objectives | `#learning-objectives` |
| 13.1 What Is DuckDB? | `#131-what-is-duckdb` |
| 13.2 SQL Essentials: SELECT, WHERE, and Calculated Columns | `#132-sql-essentials-select-where-and-calculated-columns` |
| 13.3 Aggregation: Summary Functions, GROUP BY, and HAVING | `#133-aggregation-summary-functions-group-by-and-having` |
| 13.4 Combining Tables: JOINs and Subqueries | `#134-combining-tables-joins-and-subqueries` |
| 13.5 DuckDB + Polars: The Integrated Workflow | `#135-duckdb-polars-the-integrated-workflow` |
| Reflection Questions | `#reflection-questions` |
| Your Assignment | `#your-assignment` |
| Chapter Summary | `#chapter-summary` |
| What's Next | `#whats-next` |

### Module 14: Web Scraping

`https://gregbott.github.io/MIS-501-Course-Companion/modules/14-web-scraping/`

| Section | Anchor to append |
|---------|------------------|
| Introduction | `#introduction` |
| Learning Objectives | `#learning-objectives` |
| 14.1 Web Scraping and How the Web Works | `#141-web-scraping-and-how-the-web-works` |
| 14.2 Parsing HTML with BeautifulSoup | `#142-parsing-html-with-beautifulsoup` |
| 14.3 Tables, CSS Selectors, and Tree Navigation | `#143-tables-css-selectors-and-tree-navigation` |
| 14.4 From Scraped HTML to Polars DataFrames | `#144-from-scraped-html-to-polars-dataframes` |
| 14.5 Robust, Reusable Scraping Workflows | `#145-robust-reusable-scraping-workflows` |
| Reflection Questions | `#reflection-questions` |
| Your Assignment | `#your-assignment` |
| Chapter Summary | `#chapter-summary` |
| What's Next | `#whats-next` |

### Module 15: REST APIs & Data Acquisition

`https://gregbott.github.io/MIS-501-Course-Companion/modules/15-rest-apis/`

| Section | Anchor to append |
|---------|------------------|
| Introduction | `#introduction` |
| Learning Objectives | `#learning-objectives` |
| 15.1 What Is a REST API? | `#151-what-is-a-rest-api` |
| 15.2 JSON Responses, Query Parameters, and Headers | `#152-json-responses-query-parameters-and-headers` |
| 15.3 Robust Data Acquisition: Errors, Rate Limits, and Pagination | `#153-robust-data-acquisition-errors-rate-limits-and-pagination` |
| 15.4 Building a Data Pipeline: API to Polars DataFrame | `#154-building-a-data-pipeline-api-to-polars-dataframe` |
| Reflection Questions | `#reflection-questions` |
| Your Assignment | `#your-assignment` |
| Chapter Summary | `#chapter-summary` |
| What's Next | `#whats-next` |

### Module 16.1: Capstone: Proposal & Data Acquisition

`https://gregbott.github.io/MIS-501-Course-Companion/modules/16-capstone-proposal/`

| Section | Anchor to append |
|---------|------------------|
| Introduction | `#introduction` |
| Learning Objectives | `#learning-objectives` |
| 16.1.1 What Makes a Good Capstone Project? | `#1611-what-makes-a-good-capstone-project` |
| 16.1.2 Choosing a Research Question | `#1612-choosing-a-research-question` |
| 16.1.3 Evaluating Data Sources | `#1613-evaluating-data-sources` |
| 16.1.4 Writing the Proposal | `#1614-writing-the-proposal` |
| 16.1.5 Example Walkthrough: Bike-Sharing Usage Patterns | `#1615-example-walkthrough-bike-sharing-usage-patterns` |
| Reflection Questions | `#reflection-questions` |
| Your Assignment | `#your-assignment` |
| Chapter Summary | `#chapter-summary` |
| What's Next | `#whats-next` |

### Module 16.2: Capstone: Analysis & Presentation

`https://gregbott.github.io/MIS-501-Course-Companion/modules/17-capstone-analysis/`

| Section | Anchor to append |
|---------|------------------|
| Introduction | `#introduction` |
| Learning Objectives | `#learning-objectives` |
| 16.2.1 The Capstone Workflow: From Raw Data to Deliverable | `#1621-the-capstone-workflow-from-raw-data-to-deliverable` |
| 16.2.2 Analysis with Polars | `#1622-analysis-with-polars` |
| 16.2.3 Analysis with DuckDB | `#1623-analysis-with-duckdb` |
| 16.2.4 Visualizations and Interactive Elements | `#1624-visualizations-and-interactive-elements` |
| 16.2.5 Communicating Results | `#1625-communicating-results` |
| Reflection Questions | `#reflection-questions` |
| Your Assignment | `#your-assignment` |
| Chapter Summary | `#chapter-summary` |
| What's Next | `#whats-next` |

---

## Appendix C — Q&A Reference, by module

Base URL: `https://gregbott.github.io/MIS-501-Course-Companion/reference/qa/`

| Module section | Anchor to append |
|----------------|------------------|
| Module 1: Why Python & Environment Setup | `#module-1-why-python-environment-setup` |
| Module 2: Variables, Data Types & Expressions | `#module-2-variables-data-types-expressions` |
| Module 3: Control Flow | `#module-3-control-flow` |
| Module 4: Functions & Modular Thinking | `#module-4-functions-modular-thinking` |
| Module 5: Strings & Regular Expressions | `#module-5-strings-regular-expressions` |
| Module 6: Data Structures: Lists & Tuples | `#module-6-data-structures-lists-tuples` |
| Module 7: Data Structures: Dictionaries & Sets | `#module-7-data-structures-dictionaries-sets` |
| Module 8: File I/O & Working with JSON | `#module-8-file-io-working-with-json` |
| Module 9: Introduction to Polars | `#module-9-introduction-to-polars` |
| Module 10: Polars: Transformations & Aggregations | `#module-10-polars-transformations-aggregations` |
| Module 11: Visualization: Matplotlib & Plotly Express | `#module-11-visualization-matplotlib-plotly-express` |
| Module 12: Marimo Interactive Features | `#module-12-marimo-interactive-features` |
| Module 13: DuckDB: SQL-Based Data Analysis | `#module-13-duckdb-sql-based-data-analysis` |
| Module 14: Web Scraping | `#module-14-web-scraping` |
| Module 15: REST APIs & Data Acquisition | `#module-15-rest-apis-data-acquisition` |
| Module 16.1: Capstone: Proposal & Data Acquisition | `#module-161-capstone-proposal-data-acquisition` |
| Module 16.2: Capstone: Analysis & Presentation | `#module-162-capstone-analysis-presentation` |

