# Module 2: Variables, Data Types & Expressions

## Introduction

Every dashboard, invoice total, and quarterly report starts the same way: as individual values stored in a program's memory. This module covers the vocabulary Python uses for those values — variables to name them, data types to classify them, and expressions to combine them into answers. For a business analyst, these are not abstract programming concepts. Knowing that a price is a `float`, a unit count is an `int`, an employee ID is a `str`, and "did we hit the target?" is a `bool` is what lets you calculate a margin, filter a customer list, or catch the bug where a spreadsheet export turned all your numbers into text. By the end of the module you will also be able to present results the way a finance team expects them — with dollar signs, comma separators, and controlled decimal places — using f-strings.

---

## Learning Objectives

By the end of this module, you should be able to:

1. **Create** and use variables with descriptive `snake_case` names
2. **Identify** and work with Python's core data types (`int`, `float`, `str`, `bool`)
3. **Use** arithmetic and comparison operators correctly, including operator precedence
4. **Convert** between data types with `int()`, `float()`, `str()`, and `bool()`, and inspect any value's type with `type()`
5. **Format** output using f-strings and number format specifiers

---

## 2.1 Variables and Assignment

Module 1 briefly introduced variables as "labeled boxes." Now we dig deeper.

A **variable** is a name that refers to a value stored in your computer's memory. You create a variable using the **assignment operator** (`=`):

```python
company_name = "Acme Corp"
```

This reads as: "store the text `Acme Corp` and give it the name `company_name`." The value goes on the right, the name goes on the left, and the `=` connects them.

### Rules for Variable Names

Python enforces a few rules, and the course adds one convention:

- Must start with a letter or underscore (not a number)
- Can contain letters, numbers, and underscores
- Case-sensitive: `Revenue` and `revenue` are different variables
- Cannot be a Python keyword (`if`, `for`, `class`, etc.)

**Convention in this course:** use `snake_case` — lowercase words separated by underscores. This is the standard Python style and makes names easy to read.

!!! example "Worked Example: Descriptive Variable Names"

    ```python
    # Good variable names — descriptive and snake_case
    quarterly_revenue = 128500
    customer_count = 342
    average_order_value = quarterly_revenue / customer_count

    print("Quarterly revenue:", quarterly_revenue)
    print("Customer count:", customer_count)
    print("Average order value:", average_order_value)
    ```

    **Output:**

    ```
    Quarterly revenue: 128500
    Customer count: 342
    Average order value: 375.7309941520468
    ```

    **Interpretation:** The variable names tell you exactly what each value represents — this code reads like a sentence about the business. The average order value prints with many decimal places because division produces a full-precision float; the f-string section at the end of this module shows how to display it as a clean dollar amount.

    *Source: `computations/module02_examples.py` — `demo_descriptive_variables()`*

Compare that to the same calculation written with meaningless names:

```python
x = 128500
y = 342
z = x / y
```

The code does the same thing, but you have no idea what `x`, `y`, or `z` mean. Descriptive names are not just nice to have — they are essential for writing code that other people (and future you) can understand.

### Reassignment

Variables can be updated. When you assign a new value to an existing name, the old value is replaced:

!!! example "Worked Example: Reassigning a Variable"

    ```python
    price = 19.99
    print("Original price:", price)

    price = 24.99
    print("Updated price:", price)
    ```

    **Output:**

    ```
    Original price: 19.99
    Updated price: 24.99
    ```

    **Interpretation:** After the second assignment, `price` refers to `24.99` and the old value is gone. This is how programs track changing business data — a price update, a running total, a revised forecast — under a single stable name.

    *Source: `computations/module02_examples.py` — `demo_reassignment()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| `=` checks whether two values are equal. | `=` **stores** a value under a name. Equality testing uses `==`, covered in Section 2.3. |
| `Revenue` and `revenue` are the same variable. | Variable names are case-sensitive — those are two different variables. Sticking to `snake_case` avoids the confusion entirely. |
| Short names like `x` and `y` are fine because the code still runs. | The code runs, but nobody — including future you — can tell what it means. Descriptive names are part of writing maintainable code. |
| Reassigning a variable keeps the old value around somewhere. | Assignment replaces the value. After `price = 24.99`, the earlier `19.99` is no longer accessible through `price`. |

---

## 2.2 Core Data Types

Every value in Python has a **type** that determines what you can do with it. Think of it this way: a price tag and a customer name are both pieces of data, but you would not try to multiply two names together. Types tell Python what kind of data it is working with.

Python has four fundamental types you will use constantly:

| Type | Name | Examples | Use Case |
|------|------|----------|----------|
| `int` | Integer | `42`, `-7`, `0` | Counts, quantities, IDs |
| `float` | Floating-point | `3.14`, `-0.5`, `100.0` | Prices, percentages, measurements |
| `str` | String | `"hello"`, `'MIS 501'` | Names, labels, text data |
| `bool` | Boolean | `True`, `False` | Yes/no decisions, filters |

### Integers and Floats

**Integers** (`int`) are whole numbers — no decimal point. Use them for things you count: number of employees, units sold, year.

**Floats** (`float`) are numbers with decimal points. Use them for things you measure: prices, percentages, weights.

Python handles the distinction automatically. If you write `42`, it is an integer. If you write `42.0`, it is a float. Division (`/`) always produces a float, even if the result is a whole number.

!!! example "Worked Example: Integers, Floats, and Mixed Arithmetic"

    ```python
    units_sold = 500          # int — a count
    unit_price = 12.50        # float — a price
    total = units_sold * unit_price  # int * float = float

    print("Units sold:", units_sold, "  type:", type(units_sold))
    print("Unit price:", unit_price, "  type:", type(unit_price))
    print("Total:", total, "  type:", type(total))
    ```

    **Output:**

    ```
    Units sold: 500   type: <class 'int'>
    Unit price: 12.5   type: <class 'float'>
    Total: 6250.0   type: <class 'float'>
    ```

    **Interpretation:** Multiplying an `int` by a `float` produces a `float` — Python promotes to the more general type so no precision is lost. Notice also that `12.50` displays as `12.5`: Python drops the trailing zero when printing a raw float, which is one reason the formatted output covered at the end of this module matters for financial figures.

    *Source: `computations/module02_examples.py` — `demo_ints_and_floats()`*

### Strings

A **string** (`str`) is a sequence of characters — text. You create strings by wrapping text in quotes. Python accepts single quotes (`'...'`) or double quotes (`"..."`) — pick one style and be consistent. In this course we use double quotes.

Strings can also be combined with the `+` operator, which is called **concatenation** — it joins strings end to end.

!!! example "Worked Example: Strings and Concatenation"

    ```python
    company = "Northwind Traders"
    department = "Marketing"
    employee_id = "EMP-2847"

    print("Company:", company)
    print("Department:", department)
    print("Employee ID:", employee_id)

    first_name = "Sarah"
    last_name = "Chen"

    # Concatenation joins strings together
    full_name = first_name + " " + last_name
    print("Full name:", full_name)
    ```

    **Output:**

    ```
    Company: Northwind Traders
    Department: Marketing
    Employee ID: EMP-2847
    Full name: Sarah Chen
    ```

    **Interpretation:** `employee_id` is a string even though it contains numbers — the quotes make it text. You would not do math with an employee ID; it is a label, not a quantity. Concatenation with `+` builds the full name, and the explicit `" "` supplies the space between the parts.

    *Source: `computations/module02_examples.py` — `demo_strings_and_concatenation()`*

### Booleans

A **boolean** (`bool`) has only two possible values: `True` or `False`. These are used for decisions and comparisons — think of them as answering yes/no questions.

Booleans are the foundation of all the filtering and conditional logic later in the course — for example, "show me only customers who spent more than $100."

!!! example "Worked Example: Boolean Flags"

    ```python
    is_active_customer = True
    has_overdue_invoice = False

    print("Active customer?", is_active_customer)
    print("Overdue invoice?", has_overdue_invoice)
    ```

    **Output:**

    ```
    Active customer? True
    Overdue invoice? False
    ```

    **Interpretation:** Boolean variables named as yes/no questions (`is_...`, `has_...`) make code self-documenting. When we reach filtering in later modules, columns of `True`/`False` values like these are exactly what select which rows of data to keep.

    *Source: `computations/module02_examples.py` — `demo_booleans()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| `"EMP-2847"` contains digits, so Python treats it as a number. | The quotes make it a string. It is a label, not a quantity — arithmetic on it either fails or does something unexpected. |
| `42` and `42.0` are interchangeable. | `42` is an `int` and `42.0` is a `float` — two different types. Use `int` for counts, `float` for measurements like prices. |
| Dividing two integers gives an integer when the result is whole. | `/` always produces a `float`, even when the result is a whole number (`10 / 5` is `2.0`). |
| `True` and `False` are just words, so `"True"` works the same way. | `True` and `False` (capitalized, no quotes) are the two values of `bool`. `"True"` with quotes is a string — a different type entirely. |

---

## 2.3 Arithmetic and Comparison Operators

Expressions combine variables and operators to compute new values. Python's arithmetic operators cover standard math, and its comparison operators turn questions about values into booleans.

### Arithmetic Operators and Precedence

You saw basic math in Module 1. Here is the full set of arithmetic operators, along with **operator precedence** — the order Python evaluates them:

| Priority | Operator | Meaning | Example |
|----------|----------|---------|---------|
| 1 (first) | `**` | Exponent | `2 ** 3` → `8` |
| 2 | `*`, `/`, `//`, `%` | Multiply, divide, floor divide, modulo | `10 / 4` → `2.5` |
| 3 (last) | `+`, `-` | Add, subtract | `5 + 3` → `8` |

When in doubt, use **parentheses** to make the order explicit. It also makes your code easier to read.

Precedence matters in real financial formulas. Compound interest is a good example:

$$
A = P \times (1 + r)^n
$$

where $P$ is the principal, $r$ is the annual rate, and $n$ is the number of years.

!!! example "Worked Example: Compound Interest and Precedence"

    ```python
    # Compound interest: A = P * (1 + r) ** n
    # How much is $10,000 worth after 5 years at 7% annual return?
    principal = 10000
    rate = 0.07
    years = 5

    future_value = principal * (1 + rate) ** years
    print("Future value:", future_value)
    ```

    **Output:**

    ```
    Future value: 14025.517307000004
    ```

    **Interpretation:** The invested principal grows to about $14,025.52 over the five-year horizon at the stated annual return. The parentheses force the addition inside them to happen first; `**` has the highest precedence, so the exponent applies before the final multiplication. The long tail of digits (`...000004`) is normal floating-point behavior — the f-string section at the end of this module shows how to round the display for a report.

    *Source: `computations/module02_examples.py` — `demo_compound_interest()`*

### Comparison Operators

Comparison operators compare two values and return a **boolean** (`True` or `False`). These are the building blocks for filtering data and making decisions.

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `5 != 3` | `True` |
| `>` | Greater than | `5 > 3` | `True` |
| `<` | Less than | `5 < 3` | `False` |
| `>=` | Greater than or equal | `5 >= 5` | `True` |
| `<=` | Less than or equal | `3 <= 5` | `True` |

**Important:** `=` is assignment (store a value). `==` is comparison (check if equal). This trips up almost everyone at first — just remember: one equals stores, two equals compares.

!!! example "Worked Example: Revenue vs. Target"

    ```python
    monthly_revenue = 45000
    monthly_target = 50000

    on_target = monthly_revenue >= monthly_target
    gap = monthly_target - monthly_revenue

    print("Revenue:", monthly_revenue)
    print("Target:", monthly_target)
    print("Met target?", on_target)
    print("Gap to target:", gap)
    ```

    **Output:**

    ```
    Revenue: 45000
    Target: 50000
    Met target? False
    Gap to target: 5000
    ```

    **Interpretation:** The comparison `monthly_revenue >= monthly_target` produces a boolean that can be stored in a variable just like a number. Here it answers the management question directly — the target was missed by $5,000. This store-the-answer pattern becomes the basis for the `if` statements introduced in the next module.

    *Source: `computations/module02_examples.py` — `demo_comparison_operators()`*

!!! question "Try It Yourself: Comparison Practice"

    A product costs $34.99 to make and sells for $59.99. The company considers a
    product "high margin" if the profit margin is greater than 40%.

    Starting from the variables below, calculate the profit margin as a percentage
    and use a comparison operator to check whether the product qualifies as high
    margin.

    ```python
    cost = 34.99
    sell_price = 59.99

    # Calculate profit margin as a percentage
    # margin = ???

    # Is it high margin (greater than 40%)?
    # is_high_margin = ???
    ```

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| `=` and `==` do the same thing. | One equals **stores**, two equals **compares**. `x = 5` assigns; `x == 5` asks a question and returns a boolean. |
| Python evaluates arithmetic strictly left to right. | Python follows precedence: `**` first, then `*` `/` `//` `%`, then `+` `-`. Use parentheses to make the intended order explicit. |
| A comparison changes the variables involved. | Comparisons only read their operands and produce a new `True`/`False` value; `monthly_revenue` is unchanged afterward. |
| A comparison prints "yes" or "no". | It produces a `bool` value (`True`/`False`) that you can store, print, or use in later logic — it is data like any other value. |

---

## 2.4 Dynamic Typing and Type Conversion

Python is a **dynamically typed** language. You do not declare the type of a variable in advance — Python figures it out from the value you assign.

**Analogy:** imagine a labeled box that can hold anything. You can put a number in it today and replace it with text tomorrow. The box does not care — it just holds whatever you put in it.

### Inspecting Types with `type()`

You can check a value's type at any time using the `type()` function:

!!! example "Worked Example: One Name, Four Types"

    ```python
    value = 42
    print(value, "is", type(value))

    value = 42.0
    print(value, "is", type(value))

    value = "forty-two"
    print(value, "is", type(value))

    value = True
    print(value, "is", type(value))
    ```

    **Output:**

    ```
    42 is <class 'int'>
    42.0 is <class 'float'>
    forty-two is <class 'str'>
    True is <class 'bool'>
    ```

    **Interpretation:** The same variable name holds an `int`, a `float`, a `str`, and a `bool` in sequence — the type belongs to the *value*, not the name. `type()` is your first debugging tool: when a calculation misbehaves, checking types usually reveals why.

    *Source: `computations/module02_examples.py` — `demo_dynamic_typing()`*

### Converting Between Types

Sometimes you need to convert a value from one type to another. This is called **type conversion** or **casting**. The most common conversions:

| Function | Converts to | Example |
|----------|-------------|---------|
| `int()` | Integer | `int("25")` → `25` |
| `float()` | Float | `float("3.14")` → `3.14` |
| `str()` | String | `str(100)` → `"100"` |
| `bool()` | Boolean | `bool(1)` → `True` |

This comes up constantly in real data work. Data loaded from a CSV file often arrives as text (strings), even when it represents numbers. You need to convert it before you can do math with it.

!!! example "Worked Example: Cleaning Text Data from a CSV"

    ```python
    # Simulating data that arrived as text from a CSV
    revenue_text = "52300"
    expenses_text = "41800"

    # This would fail: revenue_text - expenses_text (can't subtract strings)

    # Convert to numbers first
    revenue = float(revenue_text)
    expenses = float(expenses_text)
    profit = revenue - expenses

    print("Revenue (as number):", revenue)
    print("Expenses (as number):", expenses)
    print("Profit:", profit)
    ```

    **Output:**

    ```
    Revenue (as number): 52300.0
    Expenses (as number): 41800.0
    Profit: 10500.0
    ```

    **Interpretation:** Subtracting the raw strings would raise an error, because `-` has no meaning for text. Converting with `float()` turns `"52300"` into `52300.0`, and the profit calculation works. This convert-before-calculating step is one of the most common data-cleaning moves you will make all semester.

    *Source: `computations/module02_examples.py` — `demo_type_conversion()`*

### Truthy and Falsy Values

When Python converts other types to booleans, it follows simple rules:

- **Falsy** (becomes `False`): `0`, `0.0`, `""` (empty string), `None`
- **Truthy** (becomes `True`): everything else — any non-zero number, any non-empty string

This will matter more when we get to `if` statements in Module 3, but it is good to know the concept now.

!!! example "Worked Example: Truthy and Falsy Conversions"

    ```python
    print("bool(0):", bool(0))
    print("bool(42):", bool(42))
    print('bool(""):', bool(""))
    print('bool("hello"):', bool("hello"))
    ```

    **Output:**

    ```
    bool(0): False
    bool(42): True
    bool(""): False
    bool("hello"): True
    ```

    **Interpretation:** Zero and the empty string convert to `False`; any non-zero number or non-empty string converts to `True`. In practice this lets you ask questions like "did the customer leave the comment field blank?" by converting the value to a boolean.

    *Source: `computations/module02_examples.py` — `demo_truthy_falsy()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Numbers loaded from a CSV file are ready for math. | Exported data often arrives as strings. Convert with `int()` or `float()` before calculating, or the math will fail or misbehave. |
| `"52300" + "41800"` adds the two numbers. | With strings, `+` concatenates: the result is `"5230041800"`. Subtraction (`-`) fails outright. Convert to numbers first. |
| `bool("0")` is `False` because zero is falsy. | Only the *empty* string is falsy. `"0"` is a non-empty string, so it converts to `True`. |
| `type()` converts a value to a different type. | `type()` only *inspects*. The conversion functions — `int()`, `float()`, `str()`, `bool()` — produce a new converted value. |

---

## 2.5 F-Strings: Clean Output Formatting

So far we have used `print()` with commas to display values. That works, but the output can look messy — extra spaces, no control over decimal places.

**F-strings** (formatted string literals) give you precise control over how values appear in text. You create one by putting `f` before the opening quote, then placing variables inside curly braces `{}`:

```python
name = "Alice"
f"Hello, {name}!"   # → "Hello, Alice!"
```

Think of the curly braces as windows — Python looks through them and inserts the value of whatever is inside.

### F-String Basics

!!! example "Worked Example: F-String Basics"

    ```python
    product = "Premium Widget"
    quantity = 250
    unit_price = 34.99
    total = quantity * unit_price

    print(f"Product: {product}")
    print(f"Quantity: {quantity} units")
    print(f"Unit price: ${unit_price}")
    print(f"Total: ${total}")
    ```

    **Output:**

    ```
    Product: Premium Widget
    Quantity: 250 units
    Unit price: $34.99
    Total: $8747.5
    ```

    **Interpretation:** Each `{...}` is replaced by the variable's value, and surrounding text like `$` and `units` sits exactly where you put it. Note the flaw that remains: the total displays as `$8747.5` — a dollar amount should show two decimal places and a thousands separator. Format specifiers fix that next.

    *Source: `computations/module02_examples.py` — `demo_fstring_basics()`*

### Formatting Numbers in F-Strings

F-strings can format numbers with special syntax inside the curly braces. The most useful formats:

| Format | Meaning | Example | Output |
|--------|---------|---------|--------|
| `:.2f` | 2 decimal places | `f"{3.14159:.2f}"` | `3.14` |
| `:,.0f` | Comma separator, no decimals | `f"{1234567:,.0f}"` | `1,234,567` |
| `:,.2f` | Comma separator, 2 decimals | `f"{1234.5:,.2f}"` | `1,234.50` |
| `:.1%` | As percentage, 1 decimal | `f"{0.856:.1%}"` | `85.6%` |

!!! example "Worked Example: Report-Ready Number Formatting"

    ```python
    annual_revenue = 2847563.50
    annual_expenses = 1923841.75
    profit = annual_revenue - annual_expenses
    margin = profit / annual_revenue

    print(f"Annual Revenue:  ${annual_revenue:,.2f}")
    print(f"Annual Expenses: ${annual_expenses:,.2f}")
    print(f"Profit:          ${profit:,.2f}")
    print(f"Profit Margin:   {margin:.1%}")
    ```

    **Output:**

    ```
    Annual Revenue:  $2,847,563.50
    Annual Expenses: $1,923,841.75
    Profit:          $923,721.75
    Profit Margin:   32.4%
    ```

    **Interpretation:** This output looks like something you could put in a business report. `:,.2f` adds thousands separators and fixes two decimal places, and `:.1%` converts the raw ratio to a percentage and appends the sign itself — you pass the decimal fraction, not a pre-scaled value. F-strings turn raw numbers into polished output with very little effort.

    *Source: `computations/module02_examples.py` — `demo_fstring_number_formats()`*

!!! question "Try It Yourself: F-String Practice"

    A store had 1,247 transactions last month with total sales of $89,312.45. Use
    f-strings to print a summary that includes:

    - Total transactions (with comma formatting)
    - Total sales (with dollar sign, commas, 2 decimal places)
    - Average transaction value (with dollar sign, 2 decimal places)

### Putting It All Together: A Quarterly Sales Report

The closing example combines everything from this module — descriptive variables, integer and float arithmetic, a comparison, and formatted f-string output — in a realistic business scenario: analyzing a simple sales report.

!!! example "Worked Example: CloudSync Pro Sales Report"

    ```python
    # Sales report for Q3
    product_name = "CloudSync Pro"
    units_q1 = 1340
    units_q2 = 1580
    units_q3 = 1875
    price_per_unit = 49.99

    # Calculate totals
    total_units = units_q1 + units_q2 + units_q3
    total_revenue = total_units * price_per_unit
    avg_units_per_quarter = total_units / 3

    # Growth from Q1 to Q3
    growth_rate = (units_q3 - units_q1) / units_q1

    # Check if we hit the annual target of 5,000 units
    annual_target = 5000
    on_track = total_units >= annual_target

    print(f"=== Sales Report: {product_name} ===")
    print(f"Units Sold — Q1: {units_q1:,}  Q2: {units_q2:,}  Q3: {units_q3:,}")
    print(f"Total units (3 quarters): {total_units:,}")
    print(f"Total revenue: ${total_revenue:,.2f}")
    print(f"Avg units/quarter: {avg_units_per_quarter:,.0f}")
    print(f"Growth (Q1 to Q3): {growth_rate:.1%}")
    print(f"Annual target: {annual_target:,} units")
    print(f"Target reached? {on_track}")
    ```

    **Output:**

    ```
    === Sales Report: CloudSync Pro ===
    Units Sold — Q1: 1,340  Q2: 1,580  Q3: 1,875
    Total units (3 quarters): 4,795
    Total revenue: $239,702.05
    Avg units/quarter: 1,598
    Growth (Q1 to Q3): 39.9%
    Annual target: 5,000 units
    Target reached? False
    ```

    **Interpretation:** Ten lines of variables and arithmetic produce a report a manager could read as-is: 4,795 units sold through three quarters, revenue near $240K, and 39.9% unit growth since Q1 — but still short of the 5,000-unit annual target, which the boolean comparison reports directly. Every concept in this module appears here, and this is the pattern your assignment asks you to reproduce.

    *Source: `computations/module02_examples.py` — `demo_sales_report()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| The braces work without the `f` prefix. | Without the leading `f`, `"{name}"` is ordinary text and prints literally as `{name}`. The `f` is what activates the substitution. |
| Percentages must be multiplied by 100 before using `:.1%`. | The `%` specifier does the multiplication and adds the sign itself. Pass the raw decimal (`0.856` → `85.6%`); pre-multiplying gives `8560.0%`. |
| Format specifiers change the stored value. | `{profit:,.2f}` only controls the *display*. The variable still holds its full-precision value for later calculations. |
| `print(a, b)` with commas and an f-string are equivalent. | Comma-separated `print` inserts spaces you cannot control and gives no say over decimals (`12.50` shows as `12.5`). F-string specifiers control both. |

---

## Reflection Questions

1. A colleague writes an analysis using variables named `x1`, `x2`, and `temp`. The code produces correct numbers. What risks does this naming create when the analysis is handed to another analyst — or revisited by the author six months later?
2. Employee IDs, ZIP codes, and phone numbers are made of digits, yet this module stores an ID like `"EMP-2847"` as a string. Why is string the right type for these values? What operations do you give up by not storing them as numbers, and why is that acceptable?
3. Python's `/` operator always returns a float, even for `10 / 5`. How might this design choice prevent subtle bugs in financial calculations compared to a language where integer division silently drops the remainder?
4. Data exported from spreadsheets often arrives with every value as a string. Describe a business calculation that would fail — or worse, silently produce a wrong answer — if the strings were never converted, and explain how `type()` could help you diagnose it.
5. The same value `0.324` can be shown to an executive as `0.32439935...`, `0.32`, or `32.4%`. How does the choice of f-string format affect how the number is understood, and who should decide which format a report uses?
6. The comparison `total_units >= annual_target` stores its answer in a variable instead of printing "yes" or "no". Why is having the answer as a `bool` value more useful for the automation topics coming in Module 3?

---

## Your Assignment

The Module 2 assignment, **Data Type Exploration**, is worth **100 points plus a 10-point bonus**. You complete it in the provided marimo notebook and submit the `.py` file to Brightspace. The closing reflection section is not graded separately — it counts toward participation. Use descriptive `snake_case` names throughout, and verify your data types with `type()` when a task asks for it.

### Task 1: Building a Customer Record (10 points)

Create four variables describing one retail customer — the customer's name, account balance, number of orders this year, and preferred-status flag — choosing the correct type for each (`str`, `float`, `int`, `bool`). Then print each variable along with its type. This exercises variable creation from §2.1, the four core types from §2.2, and `type()` inspection from §2.4.

### Task 2: Type Conversion — Cleaning Import Data (15 points)

Product data exported from a spreadsheet arrives as text: a quantity string and a unit-cost string. Convert the quantity to an integer and the unit cost to a float, calculate the total cost, and print the converted values with their types followed by the total. The conversion functions come from §2.4; the multiplication and type behavior come from §2.2 and §2.3.

### Task 3: Comparison Operators — Evaluating Performance (15 points)

Given actual revenue and expenses alongside a revenue target and an expense budget, use `>=` and `<=` to determine whether revenue met the target and whether expenses stayed within budget, then compute the dollar amount by which revenue exceeded or fell short of the target. Everything you need is in §2.3, with the boolean results explained in §2.2.

### Task 4: String Operations — Product Catalog (15 points)

Given a brand, product line, model, and price, first use string concatenation (`+`) to combine the three name parts — with spaces between them — into a single full-name variable and print it with a label. Then use an f-string to print a catalog line showing the full name and the price with a dollar sign and two decimal places. Concatenation is covered in §2.2; the f-string formatting in §2.5.

### Task 5: Formatted Financial Summary (20 points)

From quarterly revenue, cost of goods sold, and operating expenses, calculate gross profit, net income, and net margin, then print a formatted income statement. Dollar amounts use comma separators with two decimal places (`:,.2f`) and the margin displays as a percentage with one decimal place (`:.1%`). The arithmetic draws on §2.3 and the formatting on §2.5.

### Task 6: Mixed Challenge — Compensation Analysis (25 points)

An employee's record arrives from an HR system with the salary and bonus percentage stored as strings. Convert both to floats, calculate the bonus amount and total compensation, determine with a comparison whether total compensation exceeds a stated threshold, and print a formatted compensation report. This task combines every section of the module: types (§2.2), arithmetic and comparison (§2.3), conversion (§2.4), and f-string formatting (§2.5).

### Task 7: Creative Exercise — Bonus (10 points)

Design your own business calculation — a loan payment summary, a pricing calculator with a margin check, or a budget tracker are suggested directions. It must use at least three Module 2 concepts and, specifically: at least four variables, at least one type conversion, at least one comparison producing a boolean, f-strings with format specifiers, and at least two comments explaining your logic.

### Reflection (participation credit)

Answer the notebook's three reflection prompts in your own words: why a value's type matters (with a specific example of a type-related problem), how f-string formatting helps when presenting data to a business audience, and what you found most challenging. There is no wrong answer — honest reflection helps your instructor see where support is needed.

---

## Chapter Summary

Variables are named containers for values, created with the assignment operator `=` and updated by reassignment. Descriptive `snake_case` names turn code into something a colleague can read: `quarterly_revenue / customer_count` explains itself in a way `x / y` never will. Every value carries one of Python's four core types — `int` for counts, `float` for measurements, `str` for text (including digit-bearing labels like employee IDs), and `bool` for yes/no answers — and the type determines which operations make sense.

Expressions combine those values. Arithmetic operators follow standard precedence (`**` before `*` and `/` before `+` and `-`), with parentheses available to make intent explicit, as in the compound interest formula. Comparison operators (`==`, `!=`, `>`, `<`, `>=`, `<=`) ask questions and return booleans — remember that one equals stores while two equals compares. Because Python is dynamically typed, a variable can hold any type over its lifetime; `type()` inspects what a value is, and `int()`, `float()`, `str()`, and `bool()` convert between types — a step you will perform constantly, since real-world data exports routinely deliver numbers as text.

Finally, f-strings connect calculation to communication. Placing variables in `{...}` inside an `f"..."` literal inserts their values into text, and format specifiers like `:,.2f` and `:.1%` produce the comma-separated dollar amounts and percentages a business report requires — without altering the underlying full-precision values. The closing sales-report example showed all of these pieces working together, which is exactly what the assignment asks you to do on your own.

---

## What's Next

Module 3 covers **control flow** — `if`/`else` statements and loops. This is where your code starts making decisions and repeating tasks automatically, which is what makes programming powerful. The booleans you produced with comparison operators in this module become the conditions that `if` statements test, and the truthy/falsy rules from §2.4 explain how non-boolean values behave inside those tests. Instead of just reporting `Target reached? False`, your programs will decide what to do about it.
