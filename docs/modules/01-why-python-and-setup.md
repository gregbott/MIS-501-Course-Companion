# Module 1: Why Python & Environment Setup

## Introduction

If you have never written a line of code, this module is your starting line — and it is designed for exactly that situation. Business decisions increasingly run on data, and the analysts, product managers, and consultants who can work with data directly command better roles and better pay than those who wait in line for someone else's report. Python is the language those professionals use, and this module explains why: where Python fits next to Excel, SQL, and R, what it means that Python gives instant feedback, and how the two tools you will use all semester — **Pixi** (which manages your Python environment) and **marimo** (the reactive notebook where you write code) — take care of the setup work so you can focus on analysis. By the end you will have run your first Python code: arithmetic, a profit-margin calculation, `print()`, variables, and comments.

---

## Learning Objectives

By the end of this module, you should be able to:

1. **Explain** why Python is the leading language for business data analysis
2. **Install** and configure a Python environment using Pixi
3. **Navigate** the marimo notebook interface and describe reactive execution
4. **Write** and execute basic Python expressions and use the `print()` function

---

## 1.1 Why Python?

This course starts from zero. By the end of the semester you will be using Python to analyze real business data — and the reason the course teaches Python, specifically, comes down to three points.

**1. Industry adoption.** Python is the most widely used programming language in data analytics, data science, and machine learning. Companies like Google, Netflix, JPMorgan, and thousands of others rely on it daily.

**2. Career value.** According to multiple salary surveys, professionals who can work with data using Python earn significantly more than those who rely solely on spreadsheets. Python skills show up in job postings for business analysts, data analysts, product managers, and consultants — not just software engineers.

**3. Versatility.** Python can do everything from simple calculations to building dashboards, automating reports, scraping websites, and training machine learning models. Learning one language gives you access to all of these capabilities.

### Python vs. Other Tools You May Know

You might be wondering how Python compares to tools you have used before. The comparison below is not about declaring a winner — it shows where Python fits.

| Tool | Strengths | Limitations |
|------|-----------|-------------|
| **Excel** | Familiar, visual, great for small datasets | Slows down with large data, hard to reproduce steps, manual and error-prone |
| **SQL** | Powerful for querying databases | Cannot build visualizations or statistical models on its own |
| **R** | Excellent for statistics | Smaller job market outside of academia |
| **Python** | General-purpose, huge ecosystem, strong job market | Requires learning to write code (that is what this course is for) |

Think of Python as the Swiss Army knife of data tools. Excel is the pocket knife you already own — great for quick tasks, but limited for bigger jobs. Nothing in this course asks you to give up Excel; it gives you a second, more capable tool for the jobs Excel handles poorly.

### What Is an Interpreted Language?

Python is an *interpreted* language. What does that mean?

**Analogy: simultaneous translation vs. publishing a book.**

- A *compiled* language (like C or Java) is like writing a book, sending it to a publisher, waiting for it to be printed, and then reading it. You have to finish the whole thing before you can run it.
- An *interpreted* language (like Python) is like having a simultaneous translator. You say one sentence, it gets translated and understood immediately, and you can say the next sentence right away.

This is good news for learning. You can write one line of Python, run it, see what happens, and then write the next line. There is no waiting. You get instant feedback, which makes experimenting easy — and experimenting is how you will learn.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Learning Python means abandoning Excel. | The tools coexist. Excel stays useful for quick, small tasks; Python takes over when data grows, steps must be reproducible, or the analysis has to run again next quarter without manual rework. |
| Python is only for software engineers. | Python skills appear in job postings for business analysts, data analysts, product managers, and consultants. This course assumes no prior programming experience. |
| You must write a whole program before anything runs. | Python is interpreted: write one line, run it, and see the result immediately — like a simultaneous translator, not a book waiting at the publisher. |
| SQL or R would cover the same ground. | SQL queries databases but cannot build visualizations or statistical models on its own, and R's job market is smaller outside academia. Python is the general-purpose option with the broadest reach. |

---

## 1.2 Setting Up Your Environment with Pixi

Before you can write Python code, you need Python installed on your computer — along with a few extra tools. This is where **Pixi** comes in.

**Analogy: Pixi is like an app store for Python.**

When you get a new phone, you go to the App Store or Google Play to install apps. You do not have to hunt for the right files, worry about compatibility, or figure out where to put things — the store handles it all.

Pixi does the same thing for Python and its libraries:

- It installs Python itself
- It installs additional packages (libraries) your code needs
- It makes sure everything is compatible and organized
- It keeps your project's tools separate from other projects (no conflicts)

In short, **Pixi is the tool that gives you a clean, ready-to-go Python workspace.**

### Installing Pixi

You will install Pixi and set up your environment as part of the Module 1 assignment, which walks through each step for your operating system. The short version is a single terminal command:

```bash
# macOS / Linux
curl -fsSL https://pixi.sh/install.sh | sh
```

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"
```

After installing, close and reopen your terminal, then confirm Pixi is available:

```bash
pixi --version
```

If a version number prints, you are ready to create a project:

```bash
pixi init my-mis501-project
cd my-mis501-project
pixi add python marimo polars
```

`pixi init` creates the project folder, and `pixi add` records each package in the project's recipe file and installs it.

### How a Pixi Project Works

When you create a Pixi project, it creates a file called `pixi.toml` that lists everything your project needs. Think of it as a recipe card:

```toml
[workspace]
name = "my-mis501-project"
channels = ["conda-forge"]
platforms = ["linux-64"]

[dependencies]
python = ">=3.12"
polars = ">=1.0"
marimo = ">=0.10"
```

The `[workspace]` section describes the project itself: `channels` is where Pixi downloads packages from, and `platforms` lists the operating systems the project runs on (`win-64` for Windows, `osx-arm64` for Apple Silicon Macs, `linux-64` for Linux). The `[dependencies]` section lists the packages you want and the versions you need.

On disk, the project looks like this:

```text
my-mis501-project/
├── pixi.toml    <- the recipe card: what your project needs
├── pixi.lock    <- the exact versions Pixi resolved (managed for you)
└── .pixi/       <- the installed environment itself (do not edit)
```

You edit only `pixi.toml` (usually through `pixi add`); Pixi maintains the rest.

Anyone with this recipe can recreate your exact setup. This matters in business because it means your analysis is **reproducible** — a colleague can run your code and get the same results, even on a different computer.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Installing Python once covers every project. | Different projects need different packages and versions. Pixi keeps each project's tools separate from other projects, so nothing conflicts. |
| `pixi.toml` is a program you have to run. | It is a recipe card, not code. It lists what the project needs; Pixi reads it and handles the installing. |
| A colleague needs your computer to rerun your analysis. | Anyone with the `pixi.toml` recipe can recreate the exact setup on their own machine — that is what makes the analysis reproducible. |
| The `platforms` line limits what Python can do. | It simply declares which operating systems the project supports (`win-64`, `osx-arm64`, `linux-64`) so Pixi can prepare packages for each one. |

---

## 1.3 Marimo: A Reactive Notebook

Marimo is the notebook environment we will use throughout this course. If you have heard of Jupyter notebooks, marimo is the next generation.

**Analogy: marimo is like a spreadsheet that runs code.**

In Excel, when you change a cell, every formula that depends on it updates automatically. Marimo works the same way — when you change a code cell, every cell that uses its results updates automatically. This is called **reactive execution**.

Why this matters:

- **No stale results.** In traditional notebooks, you can accidentally look at old output that does not match your current code. Marimo prevents this.
- **Run in any order.** Marimo figures out the right order to run cells based on their dependencies. You do not have to remember to "run all cells from the top."
- **Clean and reproducible.** Your notebook always shows the correct, current state.

A marimo notebook is made of **cells**. Each cell contains either narrative text (headings, explanations) or Python code. The teaching notebook for this module is itself a marimo notebook — every section you read there is a cell.

### Opening a Notebook

From inside your Pixi project folder, marimo opens in your web browser with one command:

```bash
pixi run marimo edit m01_teaching.py
```

The `pixi run` prefix runs marimo using the project's own environment — the one Pixi built from your recipe. Your browser opens the notebook; you edit and run cells there, and saving writes your changes back to the file.

One practical detail worth noticing: a marimo notebook is stored as a plain Python `.py` file. That is the file you edit, the file you save, and — for assignments — the file you submit to Blackboard.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| You must run cells top to bottom, in order, yourself. | Marimo determines the right order from cell dependencies and runs them automatically — no "run all cells from the top" ritual. |
| Output on screen might be stale, left over from an earlier run. | Reactive execution keeps every result in sync with the current code. The stale-output trap of traditional notebooks does not apply. |
| A notebook is a special file you cannot open elsewhere. | A marimo notebook is a plain Python `.py` file — readable in any text editor and submitted directly to Blackboard. |
| Your spreadsheet experience does not transfer. | The reactive model is exactly how Excel behaves: change a cell, and everything that depends on it recalculates. If you understand that, you understand marimo's core idea. |

---

## 1.4 Your First Python Code

Time to write some code. Python can work as a calculator right out of the box — type an expression, run it, and the result appears.

One difference between the notebook and this companion is worth flagging. In marimo, the **last expression in a cell displays automatically**, so the notebook can write a bare `2 + 2` and the result simply appears below the cell. This companion's examples run as plain Python scripts, where nothing displays unless you ask — so each example wraps its expressions in `print()`. The `print()` function gets its full introduction in the next section; for now, read `print("2 + 2 =", 2 + 2)` as "show me this label and this result."

Python supports all the standard math operations you would expect:

| Operation | Symbol | Example |
|-----------|--------|---------|
| Addition | `+` | `10 + 5` |
| Subtraction | `-` | `10 - 5` |
| Multiplication | `*` | `10 * 5` |
| Division | `/` | `10 / 5` |
| Exponent (power) | `**` | `10 ** 2` |
| Integer division | `//` | `10 // 3` |
| Remainder (modulo) | `%` | `10 % 3` |

!!! example "Worked Example: Python as a Calculator"

    ```python
    # Your first Python expression — just like using a calculator
    print("2 + 2 =", 2 + 2)

    # The standard arithmetic operators
    print("10 + 5 =", 10 + 5)    # addition
    print("10 - 5 =", 10 - 5)    # subtraction
    print("10 * 5 =", 10 * 5)    # multiplication
    print("10 / 5 =", 10 / 5)    # division
    print("10 ** 2 =", 10 ** 2)  # exponent (power)
    print("10 // 3 =", 10 // 3)  # integer division
    print("10 % 3 =", 10 % 3)    # remainder (modulo)
    ```

    **Output:**

    ```
    2 + 2 = 4
    10 + 5 = 15
    10 - 5 = 5
    10 * 5 = 50
    10 / 5 = 2.0
    10 ** 2 = 100
    10 // 3 = 3
    10 % 3 = 1
    ```

    **Interpretation:** Every expression evaluates instantly — no setup, no formula bar. Note the division family: `/` keeps the decimal part (`10 / 5` gives `2.0`), while `//` keeps only the whole number of times the divisor fits and `%` reports what is left over. That last pair answers business questions like "how many full cases, and how many leftover units?"

    *Source: `computations/module01_examples.py` — `demo_python_as_calculator()`*

You just ran your first Python program. That is genuinely all it takes.

### Business Example: Calculating Profit Margin

Now for a real business calculation. Suppose your company had revenue of $450,000 and costs of $320,000 last quarter. What is the profit margin?

!!! example "Worked Example: Calculating Profit Margin"

    ```python
    # Calculate profit margin
    revenue = 450000
    costs = 320000
    profit = revenue - costs
    margin = (profit / revenue) * 100

    print("Revenue:", revenue)
    print("Costs:", costs)
    print("Profit:", profit)
    print("Profit margin:", margin)
    ```

    **Output:**

    ```
    Revenue: 450000
    Costs: 320000
    Profit: 130000
    Profit margin: 28.888888888888886
    ```

    **Interpretation:** The company kept a profit margin of about 28.9% — just under twenty-nine cents of every revenue dollar remained after costs. Not bad for your first day writing Python. The long tail of digits is Python showing the division at full precision; the next module introduces formatting that rounds the display for reports.

    *Source: `computations/module01_examples.py` — `demo_profit_margin()`*

!!! question "Try It Yourself: Sales Tax Calculator"

    Modify the code below to calculate the total price of an $85.00 item with
    7.5% sales tax.

    ```python
    # Change these values and see what happens
    price = 85.00
    tax_rate = 0.075

    # Calculate total price with tax — replace the 0 with your formula
    total = 0

    total
    ```

    *Hint: Multiply the price by (1 + tax rate). Remember that 7.5% as a decimal
    is 0.075.*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| `/` and `//` do the same thing. | `/` is division and keeps the decimal part; `//` is integer division and keeps only the whole part, with `%` supplying the remainder. |
| Every value a cell computes appears on screen. | Marimo displays only the last expression in a cell. To show intermediate values — or several values at once — use `print()`, introduced next. |
| Math in Python needs special commands or an equation editor. | Arithmetic is typed directly with `+`, `-`, `*`, `/`, and `**`. Python works as a calculator out of the box. |

---

## 1.5 print(), Variables, and Comments

The last three ideas in this module are small individually but appear in every program you will write this semester: displaying output, naming values, and leaving notes for human readers.

### The `print()` Function

So far, marimo has been displaying results automatically — it shows the value of the last expression in each cell. But what if you want to display multiple values, or add a label to your output?

That is what `print()` is for. It writes text to the screen. Think of it as Python's way of talking to you.

!!! example "Worked Example: Displaying Output with print()"

    ```python
    # print() lets you display text and values
    print("Hello, MIS 501!")

    # You can print as many values as you want, each on its own line
    revenue = 450000
    costs = 320000
    profit = revenue - costs

    print("Revenue:", revenue)
    print("Costs:", costs)
    print("Profit:", profit)
    ```

    **Output:**

    ```
    Hello, MIS 501!
    Revenue: 450000
    Costs: 320000
    Profit: 130000
    ```

    **Interpretation:** The first line prints a text greeting; the next three each print a label and a value together. Without `print()`, only a cell's last value would appear — with it, every line you ask for shows up. The comma between a label and a value adds a space automatically, which keeps output readable with no extra effort.

    *Source: `computations/module01_examples.py` — `demo_print_basics()`*

You can mix text and numbers inside `print()` by separating them with commas. Python puts a space between each item automatically.

### A Quick Look at Variables

You may have noticed lines like `revenue = 450000`. The word `revenue` is a **variable** — a named container that holds a value.

**Analogy: variables are like labeled boxes.**

Imagine you have a box labeled "Revenue" and you put the number 450,000 inside it. Later, whenever you need that number, you just look in the box labeled "Revenue" instead of remembering the number itself.

Module 2 covers variables in depth. For now, three things to know:

- The `=` sign means "store this value" (not "equals" in the math sense)
- Variable names should be descriptive: `revenue` is better than `x`
- Python remembers the value so you can use it later

!!! example "Worked Example: Storing Values in Variables"

    ```python
    # Variables store values for later use
    items_sold = 1200
    price_per_item = 29.99

    total_revenue = items_sold * price_per_item
    print("Items sold:", items_sold)
    print("Price per item:", price_per_item)
    print("Total revenue:", total_revenue)
    ```

    **Output:**

    ```
    Items sold: 1200
    Price per item: 29.99
    Total revenue: 35988.0
    ```

    **Interpretation:** Each value is stored once under a descriptive name and reused by name: `1200` items at `29.99` each produce total revenue of `35988.0`. Change either input and rerun, and the total updates — the calculation is written once and works for any values you store.

    *Source: `computations/module01_examples.py` — `demo_variables_first_look()`*

#### Why the Notebook Writes `_revenue` Instead of `revenue`

In the marimo teaching notebooks you will see variables written with a leading underscore, like `_revenue = 450000`. Because marimo runs cells reactively, an ordinary variable name may only be defined in one cell of a notebook. Putting `_` in front of a name marks that variable as belonging to *that cell only*, which is how the notebooks reuse convenient names like `_revenue` or `_total` in cell after cell without collisions.

The underscore is a marimo convention, not part of the variable's name. In a plain Python script — like the examples in this companion — you simply write `revenue = 450000`.

### Comments: Notes for Humans

You have seen lines in the code that start with `#`. These are **comments** — notes that Python completely ignores. They exist only for humans reading the code.

```python
# This is a comment — Python skips this line
2 + 2  # You can also put comments at the end of a line
```

Why bother? Because code you write today may need to be understood by someone else tomorrow — or by *you* six months from now. Good comments explain *why* you are doing something, not just *what* the code does.

In this course, comments are how you explain your thinking and document your analysis.

!!! example "Worked Example: Documenting an ROI Calculation with Comments"

    ```python
    # Calculate return on investment (ROI)
    # ROI = (gain from investment - cost of investment) / cost of investment

    investment_cost = 50000    # Marketing campaign budget
    revenue_gained = 73000     # Revenue attributed to the campaign

    roi = (revenue_gained - investment_cost) / investment_cost
    print("Investment cost:", investment_cost)
    print("Revenue gained:", revenue_gained)
    print("ROI:", roi)
    print("ROI as percentage:", roi * 100, "%")
    ```

    **Output:**

    ```
    Investment cost: 50000
    Revenue gained: 73000
    ROI: 0.46
    ROI as percentage: 46.0 %
    ```

    **Interpretation:** The campaign returned `0.46` on every invested dollar — an ROI of 46%. The comments change nothing about the result; they record the formula and what each input means, so a colleague reviewing the analysis can follow the reasoning without guessing.

    *Source: `computations/module01_examples.py` — `demo_roi_with_comments()`*

!!! question "Try It Yourself: Business Calculations"

    Use a fresh notebook cell to calculate the following:

    1. A company sold 3,500 units at $15.50 each. What is the total revenue?
    2. Operating expenses were $38,200. What is the operating profit?
    3. What is the operating profit margin (as a percentage)?

    Write your code with a comment labeling each calculation.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| `=` checks whether two things are equal. | In Python, `=` means "store this value" — it is assignment, not mathematical equality. |
| Short names like `x` are better because they save typing. | Descriptive names like `revenue` make the code explain itself — to colleagues, and to you six months from now. |
| Comments slow the program down. | Python skips `#` lines entirely. Comments exist only for human readers and have no effect on execution. |
| The leading underscore in `_revenue` is required by Python. | It is a marimo convention marking a variable as local to one cell. In a plain Python script you would write `revenue = 450000`. |

---

## Reflection Questions

1. Think of a spreadsheet you maintain or have inherited. Which entries in the module's Excel-vs-Python comparison table describe it best, and at what point — data size, repetition, error risk — would moving that work to Python pay off?
2. The `pixi.toml` recipe lets anyone recreate your exact environment and get the same results. Describe a business situation in which an analysis that a colleague *cannot* reproduce would be a genuine problem.
3. Marimo's reactive execution guarantees that displayed results always match the current code. In a traditional notebook where stale output can linger, what could go wrong in a report built from that notebook — and who would bear the consequences?
4. Python is interpreted: each line runs and responds immediately. How does that instant feedback change the way you would experiment with a calculation, compared with a tool that only shows results after everything is finished?
5. The module argues that good comments explain *why*, not just *what*. Pick a calculation you perform regularly at work or home, and write the one-line "why" comment you would attach so someone else could take it over.
6. `revenue = 450000` stores a value in a labeled box. Why does the choice of label (`revenue` versus `x`) matter more and more as an analysis grows and gets handed from person to person?

---

## Your Assignment

The Module 1 assignment, **First Steps with Python**, is worth **100 points plus a 10-point bonus**. You complete it in the provided marimo notebook and submit the `.py` file to Blackboard. The closing reflection accounts for 10 of the 100 points and is graded as participation-style credit — honest answers, not right-or-wrong ones. Read each task carefully, use comments to explain your thinking, and if you get stuck, return to the module sections referenced below.

### Task 1: Verify Your Environment (5 points)

Confirm that your Python setup works by writing a single multiplication expression — the notebook specifies the two numbers. Write it as a bare expression with no `print()`, so marimo displays the result automatically. Marimo's automatic display of a cell's last expression is described in §1.3 and §1.4.

### Task 2: Business Arithmetic — Total Cost with Tax (15 points)

A consulting firm is buying laptops in bulk; the notebook gives the quantity, the unit price, and the local sales-tax rate. Store each input in a variable, compute the total cost including tax, and print it with a descriptive label. The arithmetic comes from §1.4 — the Try It Yourself sales-tax exercise there is a direct rehearsal — and variables and `print()` come from §1.5.

### Task 3: Displaying Results with `print()` (15 points)

A retail store's unit sales are given for last month and this month. Use `print()` to display three labeled lines: last month's units, this month's units, and the increase between them. The label-comma-value pattern is exactly the one shown in §1.5.

### Task 4: Writing Clear Comments (10 points)

The notebook provides working code that calculates a product's break-even point — the number of units to sell before turning a profit. Your job is to add a comment above each line explaining in plain English what it does; you do not change the code itself. What makes a comment useful is covered in §1.5.

### Task 5: Multi-Step Business Calculation (20 points)

You are evaluating a marketing campaign. Compute the total investment over the campaign's run, the revenue generated by the customers it brought in, the net profit, and the ROI as a percentage — storing each in a variable and printing all four with descriptive labels. This mirrors the ROI worked example in §1.5, using the arithmetic operators from §1.4.

### Task 6: Working with Text (15 points)

Create three string variables — a company name, a quarter, and a year — and join them with the `+` operator (called *concatenation*) into a single formatted report title displayed with `print()`. The task description in the notebook introduces the string concepts you need; strings get their full treatment in Module 2. The `print()` usage comes from §1.5.

### Task 7: Creative Challenge — Bonus (10 points)

Write a small program that calculates something useful to you personally — splitting a restaurant bill with tip, estimating monthly savings, converting a temperature, or anything else you find interesting. It must use at least two variables, at least one arithmetic operator, a `print()` with a descriptive label, and at least one comment explaining what the code does. Everything you need is in §1.4 and §1.5.

### Reflection (10 points)

Answer the notebook's three questions in your own words: one thing you learned, what you found most challenging and how you worked through it, and how calculations like these might be used in a business setting. There is no wrong answer — honest reflection helps you learn and shows your instructor where to provide support.

---

## Chapter Summary

Python earns its place in a business skill set on three grounds: it is the most widely adopted language for data work, it carries measurable career value beyond spreadsheet-only skills, and one language covers everything from quick calculations to dashboards, automation, and machine learning. Against familiar tools, the comparison is complementary rather than competitive — Excel remains the pocket knife for small jobs, SQL queries databases, R serves statistics — while Python is the general-purpose Swiss Army knife. Because Python is interpreted, each line runs the moment you write it, and that instant feedback loop is what makes learning by experiment practical.

Two tools carry the course. Pixi manages your environment like an app store for Python: it installs Python and packages, keeps projects isolated from one another, and records everything in a `pixi.toml` recipe card that lets anyone — a teammate, a grader, future you — recreate the exact same setup. That recipe is what makes an analysis reproducible. Marimo is the notebook where you write code: a reactive environment that, like a spreadsheet, reruns every dependent cell when an input changes, so results are never stale and cell order is never your problem. A marimo notebook is stored as a plain Python `.py` file, which is what you submit for assignments.

The module closed with your first working code. Python evaluates arithmetic directly — `+`, `-`, `*`, `/`, `**`, plus `//` and `%` for whole-number division and remainders — and a few lines of it turn revenue and costs into a profit margin. `print()` displays labeled values, as many per cell as you need. Variables store values in named boxes, where descriptive names like `revenue` beat cryptic ones like `x`, and the `=` sign means "store," not "equals." Comments marked with `#` are ignored by Python entirely; they exist to tell human readers *why* the code does what it does. These four small ideas — expressions, `print()`, variables, comments — appear in every program you will write from here on.

---

## What's Next

Module 2 takes the "quick look" at variables from this module and makes it a full treatment: **variables, data types, and expressions**. You will learn how Python classifies values — text (strings), numbers (integers and floats), and True/False values (booleans) — and why the type of a value determines what you can do with it. You will also fix the one rough edge you saw here: results like the profit margin's long trail of decimals will become clean, report-ready output once f-strings and format specifiers enter the picture. These are the building blocks for everything that follows.
