# Module 9: Introduction to Polars

## Introduction

In Modules 1 through 8 you worked with individual values, lists, dictionaries, and files — and in Module 8 you parsed CSV files by hand: open the file, split each line on commas, convert each field to the right type. That approach works for a dozen rows. Real business datasets have thousands or millions of rows across many columns, and processing them with loops and dictionaries is slow to run and slower to write. This module introduces **Polars**, the data analysis library used for the rest of the course. You will learn its two core structures — the DataFrame and the Series — and the operations that let you *explore* any dataset: read it from a file, inspect its shape and types, select the columns you need, filter to the rows that matter, sort, and write results back to disk. By the end you will chain those steps into a single pipeline that turns a raw employee roster into a ranked list of raise candidates ready for HR.

---

## Learning Objectives

By the end of this module, you should be able to:

1. **Explain** why Polars is preferred over pandas for modern data analysis
2. **Create** DataFrames and Series from Python data, and inspect shape, columns, schema, and summary statistics
3. **Read** data from CSV and JSON files with `pl.read_csv()` and `pl.read_json()`
4. **Select** and transform columns with `select()`, `pl.col()` expressions, and `.alias()`
5. **Filter** rows with `filter()`, combining conditions with `&`, `|`, and `is_in()`
6. **Sort** data, preview it with `head()`, write results to files, and chain operations into readable pipelines

---

## 9.1 Why Polars? DataFrames and Series

Polars is a modern data analysis library designed for speed and clarity. Its engine is written in Rust, it handles datasets far larger than anything you would attempt with plain Python loops, and its API is built around a single consistent idea: **expressions** that describe what to do with whole columns at once.

If you have heard of **pandas** — the older, widely used Python data library — here is how the two compare:

| Feature | Polars | pandas |
|---------|--------|--------|
| Speed | Very fast (Rust engine) | Slower (C/Python engine) |
| Memory | Efficient — uses less RAM | Higher memory usage |
| API style | Expression-based | Method chaining + indexing |
| Missing values | Clear `null` handling | Confusing `NaN` vs `None` |
| Learning curve | Clean, consistent API | Many ways to do the same thing |

Polars thinks in **columns** and **expressions** rather than row-by-row loops. That is a small mental shift after eight modules of `for` loops, but the payoff is code that is shorter, faster, and easier to read — the same shift a manager makes when moving from checking invoices one at a time to reading a summary column in a spreadsheet.

### Your First DataFrame

The two core data structures in Polars are:

- **DataFrame** — a table with named columns, like a spreadsheet
- **Series** — a single column of data

A DataFrame is made up of multiple Series, one per column. The conventional import is `import polars as pl`, and the simplest way to build a DataFrame is from a dictionary: each key becomes a column name, and each list of values becomes that column's data.

!!! example "Worked Example: Importing Polars and Building a DataFrame"

    ```python
    import polars as pl

    print(f"Polars version: {pl.__version__}")
    print()

    products = pl.DataFrame({
        "product": ["Laptop", "Monitor", "Keyboard", "Mouse", "Webcam"],
        "category": ["Electronics", "Electronics", "Accessories", "Accessories", "Electronics"],
        "price": [999.99, 349.50, 79.95, 24.99, 64.50],
        "units_sold": [45, 120, 200, 350, 85],
    })

    print("Product DataFrame:")
    print(products)
    ```

    **Output:**

    ```
    Polars version: 1.43.0

    Product DataFrame:
    shape: (5, 4)
    ┌──────────┬─────────────┬────────┬────────────┐
    │ product  ┆ category    ┆ price  ┆ units_sold │
    │ ---      ┆ ---         ┆ ---    ┆ ---        │
    │ str      ┆ str         ┆ f64    ┆ i64        │
    ╞══════════╪═════════════╪════════╪════════════╡
    │ Laptop   ┆ Electronics ┆ 999.99 ┆ 45         │
    │ Monitor  ┆ Electronics ┆ 349.5  ┆ 120        │
    │ Keyboard ┆ Accessories ┆ 79.95  ┆ 200        │
    │ Mouse    ┆ Accessories ┆ 24.99  ┆ 350        │
    │ Webcam   ┆ Electronics ┆ 64.5   ┆ 85         │
    └──────────┴─────────────┴────────┴────────────┘
    ```

    **Interpretation:** Each dictionary key became a named column. The header `shape: (5, 4)` reads rows first, then columns, and the row of type codes under the column names — `str`, `f64`, `i64` — shows what Polars inferred for each column: text, decimal numbers, whole numbers. Note the display detail that the Monitor price shows as `349.5`: Polars drops trailing zeros when printing floats, but the stored value is unchanged.

    *Source: `computations/module09_examples.py` — `demo_create_dataframe()`*

### Series: A Single Column

A Series is one column on its own — it carries a name, a data type, and its values. Because a Series knows its type, statistics like the sum and mean are a single method call away.

!!! example "Worked Example: A Revenue Series and Its Statistics"

    ```python
    revenue = pl.Series("monthly_revenue", [42000, 51000, 38000, 47000, 55000])

    print(revenue)
    print(f"Dtype: {revenue.dtype}")
    print(f"Length: {len(revenue)}")
    print(f"Sum: ${revenue.sum():,}")
    print(f"Mean: ${revenue.mean():,.2f}")
    ```

    **Output:**

    ```
    shape: (5,)
    Series: 'monthly_revenue' [i64]
    [
    	42000
    	51000
    	38000
    	47000
    	55000
    ]
    Dtype: Int64
    Length: 5
    Sum: $233,000
    Mean: $46,600.00
    ```

    **Interpretation:** The Series prints its shape, name, and dtype before its values. Five months of revenue total $233,000, an average of $46,600.00 per month — computed by `.sum()` and `.mean()` with no loop in sight. This is the column-oriented thinking Polars is built on: you ask a whole column a question, and it answers.

    *Source: `computations/module09_examples.py` — `demo_series()`*

### Inspecting DataFrames

Before analyzing any dataset, understand its structure. Polars provides several inspection methods:

| Method | Purpose |
|--------|---------|
| `df.shape` | Number of (rows, columns) |
| `df.columns` | List of column names |
| `df.dtypes` | Data types of each column |
| `df.schema` | Column names and their types together |
| `df.head(n)` | First n rows (default 5) |
| `df.tail(n)` | Last n rows |
| `df.describe()` | Summary statistics per column |
| `df.glimpse()` | Compact transposed overview |

The first three answer "what am I looking at?"; `head()` and `tail()` answer "what does the data actually look like?"; and `describe()` answers "what are the typical values?"

!!! example "Worked Example: Shape, Schema, and describe()"

    ```python
    # products: the product DataFrame built in the first example
    print(f"Shape: {products.shape}")
    print(f"Columns: {products.columns}")
    print(f"Schema: {products.schema}")
    print()
    print("Summary statistics (describe):")
    print(products.describe())
    ```

    **Output:**

    ```
    Shape: (5, 4)
    Columns: ['product', 'category', 'price', 'units_sold']
    Schema: Schema({'product': String, 'category': String, 'price': Float64, 'units_sold': Int64})

    Summary statistics (describe):
    shape: (9, 5)
    ┌────────────┬──────────┬─────────────┬───────────┬────────────┐
    │ statistic  ┆ product  ┆ category    ┆ price     ┆ units_sold │
    │ ---        ┆ ---      ┆ ---         ┆ ---       ┆ ---        │
    │ str        ┆ str      ┆ str         ┆ f64       ┆ f64        │
    ╞════════════╪══════════╪═════════════╪═══════════╪════════════╡
    │ count      ┆ 5        ┆ 5           ┆ 5.0       ┆ 5.0        │
    │ null_count ┆ 0        ┆ 0           ┆ 0.0       ┆ 0.0        │
    │ mean       ┆ null     ┆ null        ┆ 303.786   ┆ 160.0      │
    │ std        ┆ null     ┆ null        ┆ 409.84062 ┆ 120.571556 │
    │ min        ┆ Keyboard ┆ Accessories ┆ 24.99     ┆ 45.0       │
    │ 25%        ┆ null     ┆ null        ┆ 64.5      ┆ 85.0       │
    │ 50%        ┆ null     ┆ null        ┆ 79.95     ┆ 120.0      │
    │ 75%        ┆ null     ┆ null        ┆ 349.5     ┆ 200.0      │
    │ max        ┆ Webcam   ┆ Electronics ┆ 999.99    ┆ 350.0      │
    └────────────┴──────────┴─────────────┴───────────┴────────────┘
    ```

    **Interpretation:** `describe()` computes one statistic per row for every column. The mean price is 303.786 while the median price (the `50%` row) is 79.95 — a gap that tells you one expensive laptop is pulling the average far above the typical product. String columns show `null` for numeric statistics but still report a count and alphabetical min. Numbers like these are the first sanity check on any new dataset: do the ranges and averages look plausible for the business?

    *Source: `computations/module09_examples.py` — `demo_inspect_dataframe()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "`shape: (5, 4)` means five columns and four rows." | Shape always reads **(rows, columns)** — rows first. |
| "`str`, `f64`, and `i64` in the printout are variable names." | They are type codes: string, 64-bit float (decimals), 64-bit integer (whole numbers). Checking them is a habit that catches import problems early. |
| "A DataFrame stores data row by row, like a list of dictionaries." | Polars stores data column by column — each column is a Series. That is why whole-column operations are fast and natural. |
| "`describe()` changes the DataFrame." | It returns a *new* summary DataFrame; the original is untouched. Nearly every Polars method works this way. |

---

## 9.2 Reading Data from Files

In real projects you rarely type data by hand — it arrives as files exported from other systems. Polars reads the common formats with one function call each:

| Function | Format | Typical source |
|----------|--------|----------------|
| `pl.read_csv("file.csv")` | CSV | Spreadsheet and database exports |
| `pl.read_json("file.json")` | JSON | API responses, web applications |
| `pl.read_parquet("file.parquet")` | Parquet | Fast columnar storage in data pipelines |

CSV and JSON are the formats you met in Module 8; Parquet is a compressed, column-oriented format you will see in professional data pipelines. This module demonstrates CSV and JSON.

### Reading CSV Files

Recall what reading a CSV took in Module 8: `open()` the file, read the lines, `.split(",")` each one, and convert every field to the right type yourself. Polars does all of it in one call — including the type conversion.

The example below first *creates* a small CSV file using your Module 8 skills, then reads it back with Polars. This employee roster is the dataset for the rest of the module.

!!! example "Worked Example: An Employee Roster from CSV"

    ```python
    # Create a small CSV file (Module 8 skills)
    csv_content = """employee_id,name,department,hire_date,salary,performance_score
    E101,Alice Park,Engineering,2020-03-15,95000,4.2
    E102,Bob Martinez,Marketing,2019-07-01,72000,3.8
    E103,Carol Wu,Finance,2021-01-10,88000,4.5
    E104,David Chen,Engineering,2022-06-20,85000,3.9
    E105,Eva Lopez,Marketing,2020-11-05,76000,4.1
    E106,Frank Kim,Finance,2018-04-18,92000,4.3
    E107,Grace Patel,Engineering,2023-02-14,82000,3.7
    E108,Henry Okafor,Operations,2019-09-30,68000,4.0
    E109,Iris Tanaka,Operations,2021-08-22,71000,3.6
    E110,Jack Rivera,Marketing,2020-05-12,74000,4.4"""

    with open("employees.csv", "w") as f:
        f.write(csv_content)
    print("Created employees.csv with 10 employee records")
    print()

    # Reading it with Polars — one line
    employees = pl.read_csv("employees.csv")
    print(f"Shape: {employees.shape}")
    print(f"Columns: {employees.columns}")
    print()
    print(employees)
    ```

    **Output:**

    ```
    Created employees.csv with 10 employee records

    Shape: (10, 6)
    Columns: ['employee_id', 'name', 'department', 'hire_date', 'salary', 'performance_score']

    shape: (10, 6)
    ┌─────────────┬──────────────┬─────────────┬────────────┬────────┬───────────────────┐
    │ employee_id ┆ name         ┆ department  ┆ hire_date  ┆ salary ┆ performance_score │
    │ ---         ┆ ---          ┆ ---         ┆ ---        ┆ ---    ┆ ---               │
    │ str         ┆ str          ┆ str         ┆ str        ┆ i64    ┆ f64               │
    ╞═════════════╪══════════════╪═════════════╪════════════╪════════╪═══════════════════╡
    │ E101        ┆ Alice Park   ┆ Engineering ┆ 2020-03-15 ┆ 95000  ┆ 4.2               │
    │ E102        ┆ Bob Martinez ┆ Marketing   ┆ 2019-07-01 ┆ 72000  ┆ 3.8               │
    │ E103        ┆ Carol Wu     ┆ Finance     ┆ 2021-01-10 ┆ 88000  ┆ 4.5               │
    │ E104        ┆ David Chen   ┆ Engineering ┆ 2022-06-20 ┆ 85000  ┆ 3.9               │
    │ E105        ┆ Eva Lopez    ┆ Marketing   ┆ 2020-11-05 ┆ 76000  ┆ 4.1               │
    │ E106        ┆ Frank Kim    ┆ Finance     ┆ 2018-04-18 ┆ 92000  ┆ 4.3               │
    │ E107        ┆ Grace Patel  ┆ Engineering ┆ 2023-02-14 ┆ 82000  ┆ 3.7               │
    │ E108        ┆ Henry Okafor ┆ Operations  ┆ 2019-09-30 ┆ 68000  ┆ 4.0               │
    │ E109        ┆ Iris Tanaka  ┆ Operations  ┆ 2021-08-22 ┆ 71000  ┆ 3.6               │
    │ E110        ┆ Jack Rivera  ┆ Marketing   ┆ 2020-05-12 ┆ 74000  ┆ 4.4               │
    └─────────────┴──────────────┴─────────────┴────────────┴────────┴───────────────────┘
    ```

    **Interpretation:** One `pl.read_csv()` call replaced the entire open-split-convert routine: 10 employee records arrived as a fully typed table. Look at the dtype row — `salary` came back as `i64` and `performance_score` as `f64` without any conversion code, because Polars inspects the values and infers each column's type. The identifier and date columns stayed `str`, which is exactly right until you need date arithmetic (a topic for the next module's casting section).

    *Source: `computations/module09_examples.py` — `demo_read_csv()`*

No `open()` bookkeeping, no `.split(",")`, no `float()` calls — the single function call did the parsing *and* the type detection. That is the recurring trade in this half of the course: hand the mechanical work to the library and spend your attention on the analysis.

### Reading JSON Files

JSON is the format APIs speak (Module 8, and again in Module 15). When a JSON file contains a list of flat objects — one object per record — `pl.read_json()` turns it straight into a table.

!!! example "Worked Example: Sales Records from JSON"

    ```python
    import json

    sales_data = [
        {"date": "2025-01-15", "region": "West", "product": "Laptop", "units": 12, "revenue": 11999.88},
        {"date": "2025-01-15", "region": "East", "product": "Monitor", "units": 25, "revenue": 8737.50},
        {"date": "2025-01-16", "region": "West", "product": "Keyboard", "units": 50, "revenue": 3997.50},
        {"date": "2025-01-16", "region": "East", "product": "Laptop", "units": 8, "revenue": 7999.92},
        {"date": "2025-01-17", "region": "Central", "product": "Mouse", "units": 100, "revenue": 2499.00},
        {"date": "2025-01-17", "region": "West", "product": "Webcam", "units": 30, "revenue": 1935.00},
    ]

    with open("sales.json", "w") as f:
        json.dump(sales_data, f, indent=2)
    print("Created sales.json with 6 records")
    print()

    sales = pl.read_json("sales.json")
    print(f"Shape: {sales.shape}")
    print(sales)
    ```

    **Output:**

    ```
    Created sales.json with 6 records

    Shape: (6, 5)
    shape: (6, 5)
    ┌────────────┬─────────┬──────────┬───────┬──────────┐
    │ date       ┆ region  ┆ product  ┆ units ┆ revenue  │
    │ ---        ┆ ---     ┆ ---      ┆ ---   ┆ ---      │
    │ str        ┆ str     ┆ str      ┆ i64   ┆ f64      │
    ╞════════════╪═════════╪══════════╪═══════╪══════════╡
    │ 2025-01-15 ┆ West    ┆ Laptop   ┆ 12    ┆ 11999.88 │
    │ 2025-01-15 ┆ East    ┆ Monitor  ┆ 25    ┆ 8737.5   │
    │ 2025-01-16 ┆ West    ┆ Keyboard ┆ 50    ┆ 3997.5   │
    │ 2025-01-16 ┆ East    ┆ Laptop   ┆ 8     ┆ 7999.92  │
    │ 2025-01-17 ┆ Central ┆ Mouse    ┆ 100   ┆ 2499.0   │
    │ 2025-01-17 ┆ West    ┆ Webcam   ┆ 30    ┆ 1935.0   │
    └────────────┴─────────┴──────────┴───────┴──────────┘
    ```

    **Interpretation:** Each JSON object became a row and each key became a column — 6 records, five fields each, with `units` inferred as integers and `revenue` as decimals. This list-of-objects shape is precisely what most business APIs return, so this one function is your bridge from web data to tabular analysis.

    *Source: `computations/module09_examples.py` — `demo_read_json()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "After `read_csv()` everything is text and must be converted." | Polars infers types automatically — check the dtype row to confirm what it decided. |
| "The DataFrame stays connected to the file." | Reading takes a snapshot into memory. Later changes to the DataFrame do not touch the file (and vice versa) until you write it back. |
| "JSON is too nested for tables." | A list of flat objects maps directly to rows and columns. Deeply nested JSON needs reshaping first, but flat API-style records do not. |

---

## 9.3 Selecting Columns with `select()`

The `select()` method picks specific columns from a DataFrame — like choosing which columns of a spreadsheet to keep:

```python
df.select("name", "salary")                    # by column name strings
df.select(pl.col("name"), pl.col("salary"))    # using expressions
```

The `pl.col()` function creates a **column expression** — a description of which column to work with and, optionally, what to do with it. Expressions are the heart of Polars: everything from arithmetic to string manipulation is phrased as an expression applied to whole columns.

### Selecting by Name

For simply keeping columns, plain name strings are all you need.

!!! example "Worked Example: Three Columns from the Roster"

    ```python
    employees = pl.read_csv("employees.csv")

    selected = employees.select("name", "department", "salary")
    print(selected)
    ```

    **Output:**

    ```
    shape: (10, 3)
    ┌──────────────┬─────────────┬────────┐
    │ name         ┆ department  ┆ salary │
    │ ---          ┆ ---         ┆ ---    │
    │ str          ┆ str         ┆ i64    │
    ╞══════════════╪═════════════╪════════╡
    │ Alice Park   ┆ Engineering ┆ 95000  │
    │ Bob Martinez ┆ Marketing   ┆ 72000  │
    │ Carol Wu     ┆ Finance     ┆ 88000  │
    │ David Chen   ┆ Engineering ┆ 85000  │
    │ Eva Lopez    ┆ Marketing   ┆ 76000  │
    │ Frank Kim    ┆ Finance     ┆ 92000  │
    │ Grace Patel  ┆ Engineering ┆ 82000  │
    │ Henry Okafor ┆ Operations  ┆ 68000  │
    │ Iris Tanaka  ┆ Operations  ┆ 71000  │
    │ Jack Rivera  ┆ Marketing   ┆ 74000  │
    └──────────────┴─────────────┴────────┘
    ```

    **Interpretation:** All ten rows survive; only the columns change — the result is `shape: (10, 3)`. The output columns appear in the order you list them, which is how you control the layout of a report. The original `employees` DataFrame still has all six columns; `select()` returned a new, narrower one.

    *Source: `computations/module09_examples.py` — `demo_select_columns()`*

### Why `pl.col()`? Expressions Transform Columns

Column-name strings can only *keep* columns. Wrapping a name in `pl.col()` gives you an expression you can compute with — multiply it, divide it, round it — and `.alias()` names the result:

```python
df.select(
    pl.col("name"),
    pl.col("price") * 1.1,                          # 10% markup
    (pl.col("revenue") / 1000).alias("revenue_k"),  # compute, then rename
)
```

Without `.alias()`, a computed column keeps the source column's name, which becomes confusing the moment you have two different calculations built from the same column.

!!! example "Worked Example: Salary Breakdowns with Expressions and .alias()"

    ```python
    employees = pl.read_csv("employees.csv")

    result = employees.select(
        pl.col("name"),
        pl.col("department"),
        pl.col("salary").alias("annual_salary"),
        (pl.col("salary") / 12).round(2).alias("monthly_salary"),
        (pl.col("salary") / 52).round(2).alias("weekly_salary"),
    )
    print(result)
    ```

    **Output:**

    ```
    shape: (10, 5)
    ┌──────────────┬─────────────┬───────────────┬────────────────┬───────────────┐
    │ name         ┆ department  ┆ annual_salary ┆ monthly_salary ┆ weekly_salary │
    │ ---          ┆ ---         ┆ ---           ┆ ---            ┆ ---           │
    │ str          ┆ str         ┆ i64           ┆ f64            ┆ f64           │
    ╞══════════════╪═════════════╪═══════════════╪════════════════╪═══════════════╡
    │ Alice Park   ┆ Engineering ┆ 95000         ┆ 7916.67        ┆ 1826.92       │
    │ Bob Martinez ┆ Marketing   ┆ 72000         ┆ 6000.0         ┆ 1384.62       │
    │ Carol Wu     ┆ Finance     ┆ 88000         ┆ 7333.33        ┆ 1692.31       │
    │ David Chen   ┆ Engineering ┆ 85000         ┆ 7083.33        ┆ 1634.62       │
    │ Eva Lopez    ┆ Marketing   ┆ 76000         ┆ 6333.33        ┆ 1461.54       │
    │ Frank Kim    ┆ Finance     ┆ 92000         ┆ 7666.67        ┆ 1769.23       │
    │ Grace Patel  ┆ Engineering ┆ 82000         ┆ 6833.33        ┆ 1576.92       │
    │ Henry Okafor ┆ Operations  ┆ 68000         ┆ 5666.67        ┆ 1307.69       │
    │ Iris Tanaka  ┆ Operations  ┆ 71000         ┆ 5916.67        ┆ 1365.38       │
    │ Jack Rivera  ┆ Marketing   ┆ 74000         ┆ 6166.67        ┆ 1423.08       │
    └──────────────┴─────────────┴───────────────┴────────────────┴───────────────┘
    ```

    **Interpretation:** One `select()` call produced a small payroll report: Alice Park's $95,000 annual salary becomes $7,916.67 per month and $1,826.92 per week. Each expression ran against the entire column at once — no loop — and rounding kept the money columns at two decimal places. The `.alias()` names (`annual_salary`, `monthly_salary`, `weekly_salary`) are what make the output readable as a report.

    *Source: `computations/module09_examples.py` — `demo_select_expressions()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "`select()` deletes the other columns from my DataFrame." | It returns a **new** DataFrame with the chosen columns; the original keeps everything. |
| "`.alias()` renames the column in the source data." | It names only the expression's output column in the result. |
| "`pl.col('salary')` fetches the salary values immediately." | It builds an *expression* — a recipe. The recipe runs when you hand it to `select()` (or `filter()`). |
| "To compute a new column you loop over rows." | Expressions operate on whole columns at once; that is why Polars is fast and the code is short. |

---

## 9.4 Filtering Rows with `filter()`

Where `select()` chooses columns, `filter()` chooses **rows** — it keeps only those matching a condition built from `pl.col()` and comparison operators:

```python
df.filter(pl.col("salary") > 80000)
df.filter(pl.col("department") == "Engineering")
```

Conditions combine with `&` (and), `|` (or), and `~` (not) — not with Python's `and`/`or` keywords, which do not work on column expressions:

```python
df.filter(
    (pl.col("salary") > 80000) & (pl.col("department") == "Engineering")
)
```

**Each condition must be wrapped in parentheses** when combining with `&` or `|`. Without them, Python's operator precedence groups the expression incorrectly and you get an error (or worse, a wrong answer).

### Comparisons and Combined Conditions

!!! example "Worked Example: High Earners, Then an AND Condition"

    ```python
    employees = pl.read_csv("employees.csv")

    # One condition: a numeric comparison
    high_earners = employees.filter(pl.col("salary") > 80000)
    print("High earners (salary > $80,000):")
    print(high_earners.select("name", "department", "salary", "performance_score"))
    print()

    # Two conditions combined with & — each wrapped in parentheses
    top_engineers = employees.filter(
        (pl.col("department") == "Engineering")
        & (pl.col("performance_score") >= 4.0)
    )
    print("Engineering employees with performance >= 4.0:")
    print(top_engineers.select("name", "department", "salary", "performance_score"))
    ```

    **Output:**

    ```
    High earners (salary > $80,000):
    shape: (5, 4)
    ┌─────────────┬─────────────┬────────┬───────────────────┐
    │ name        ┆ department  ┆ salary ┆ performance_score │
    │ ---         ┆ ---         ┆ ---    ┆ ---               │
    │ str         ┆ str         ┆ i64    ┆ f64               │
    ╞═════════════╪═════════════╪════════╪═══════════════════╡
    │ Alice Park  ┆ Engineering ┆ 95000  ┆ 4.2               │
    │ Carol Wu    ┆ Finance     ┆ 88000  ┆ 4.5               │
    │ David Chen  ┆ Engineering ┆ 85000  ┆ 3.9               │
    │ Frank Kim   ┆ Finance     ┆ 92000  ┆ 4.3               │
    │ Grace Patel ┆ Engineering ┆ 82000  ┆ 3.7               │
    └─────────────┴─────────────┴────────┴───────────────────┘

    Engineering employees with performance >= 4.0:
    shape: (1, 4)
    ┌────────────┬─────────────┬────────┬───────────────────┐
    │ name       ┆ department  ┆ salary ┆ performance_score │
    │ ---        ┆ ---         ┆ ---    ┆ ---               │
    │ str        ┆ str         ┆ i64    ┆ f64               │
    ╞════════════╪═════════════╪════════╪═══════════════════╡
    │ Alice Park ┆ Engineering ┆ 95000  ┆ 4.2               │
    └────────────┴─────────────┴────────┴───────────────────┘
    ```

    **Interpretation:** Five employees clear the $80,000 bar. Adding the second condition with `&` narrows the answer to a single row: Alice Park is the only engineer scoring at least 4.0 — David Chen earns 85000 but his 3.9 score misses the cutoff. Both conditions must be true for a row to survive an `&` filter, which is why the combined result is smaller than either condition alone.

    *Source: `computations/module09_examples.py` — `demo_filter_rows()`*

### String Conditions

Conditions are not limited to numbers. The `.str` namespace from Module 5 works inside filters — `str.contains()`, `str.starts_with()`, and friends.

!!! example "Worked Example: Filtering on Text with str.contains()"

    ```python
    employees = pl.read_csv("employees.csv")

    result = employees.filter(
        pl.col("name").str.contains("P")   # capital P — case-sensitive
    )
    print("Employees with a capital 'P' in their name:")
    print(result.select("name", "department"))
    ```

    **Output:**

    ```
    Employees with a capital 'P' in their name:
    shape: (2, 2)
    ┌─────────────┬─────────────┐
    │ name        ┆ department  │
    │ ---         ┆ ---         │
    │ str         ┆ str         │
    ╞═════════════╪═════════════╡
    │ Alice Park  ┆ Engineering │
    │ Grace Patel ┆ Engineering │
    └─────────────┴─────────────┘
    ```

    **Interpretation:** `str.contains()` is case-sensitive by default: Park and Patel match the capital letter, while Eva Lopez — whose only p is lowercase — is excluded. Case-sensitivity is a classic source of silently missing rows when filtering names, product codes, or region labels, so check your data's capitalization before you trust a text filter.

    *Source: `computations/module09_examples.py` — `demo_filter_strings()`*

### Matching a List of Values with `is_in()`

When one column should match any of several values, you *could* chain `|` conditions — but `is_in()` says it directly:

```python
# Instead of this:
df.filter((pl.col("dept") == "Marketing") | (pl.col("dept") == "Finance"))

# Write this:
df.filter(pl.col("dept").is_in(["Marketing", "Finance"]))
```

!!! example "Worked Example: OR Conditions Versus is_in()"

    ```python
    employees = pl.read_csv("employees.csv")

    # Two conditions joined with |
    with_or = employees.filter(
        (pl.col("department") == "Marketing")
        | (pl.col("department") == "Finance")
    )
    print("Marketing or Finance employees (two conditions with |):")
    print(with_or.select("name", "department", "salary"))
    print()

    # The same filter with is_in()
    with_is_in = employees.filter(pl.col("department").is_in(["Marketing", "Finance"]))
    print("Same rows with is_in():")
    print(with_is_in.select("name", "department", "salary"))
    ```

    **Output:**

    ```
    Marketing or Finance employees (two conditions with |):
    shape: (5, 3)
    ┌──────────────┬────────────┬────────┐
    │ name         ┆ department ┆ salary │
    │ ---          ┆ ---        ┆ ---    │
    │ str          ┆ str        ┆ i64    │
    ╞══════════════╪════════════╪════════╡
    │ Bob Martinez ┆ Marketing  ┆ 72000  │
    │ Carol Wu     ┆ Finance    ┆ 88000  │
    │ Eva Lopez    ┆ Marketing  ┆ 76000  │
    │ Frank Kim    ┆ Finance    ┆ 92000  │
    │ Jack Rivera  ┆ Marketing  ┆ 74000  │
    └──────────────┴────────────┴────────┘

    Same rows with is_in():
    shape: (5, 3)
    ┌──────────────┬────────────┬────────┐
    │ name         ┆ department ┆ salary │
    │ ---          ┆ ---        ┆ ---    │
    │ str          ┆ str        ┆ i64    │
    ╞══════════════╪════════════╪════════╡
    │ Bob Martinez ┆ Marketing  ┆ 72000  │
    │ Carol Wu     ┆ Finance    ┆ 88000  │
    │ Eva Lopez    ┆ Marketing  ┆ 76000  │
    │ Frank Kim    ┆ Finance    ┆ 92000  │
    │ Jack Rivera  ┆ Marketing  ┆ 74000  │
    └──────────────┴────────────┴────────┘
    ```

    **Interpretation:** Both filters return the same five rows. The difference is readability and scale: with two departments the `|` version is tolerable, but a filter for a dozen product codes would be unreadable as chained conditions and trivial as `is_in([...])`. When the condition is "this column matches any value in a list," reach for `is_in()`.

    *Source: `computations/module09_examples.py` — `demo_filter_is_in()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "I can write `and` / `or` between conditions." | Python's keywords do not work on column expressions — use `&` and `|`. |
| "The parentheses around each condition are optional." | Without them, operator precedence misgroups the expression and Polars raises an error. Parenthesize every condition. |
| "`=` compares values in a condition." | `=` assigns; `==` compares. A filter condition always uses `==`. |
| "`str.contains()` ignores capitalization." | It is case-sensitive by default — a lowercase letter will not match its uppercase counterpart. |
| "`filter()` removes rows from my DataFrame." | It returns a new DataFrame containing the matching rows; the original is unchanged. |

---

## 9.5 Sorting, Writing, and Chaining Pipelines

The final trio of skills turns filtered data into finished deliverables: put rows in a meaningful order, save the result to a file, and express the whole workflow as one readable pipeline.

### Sorting with `sort()` and Previewing with `head()`

```python
df.sort("salary")                                           # ascending (default)
df.sort("salary", descending=True)                          # descending
df.sort("department", "salary", descending=[False, True])   # multi-column
```

`head(n)` returns the first n rows and `tail(n)` the last n — most useful right after a sort, when "first" means "best" or "biggest."

!!! example "Worked Example: Ranking by Salary and Taking the Top Rows"

    ```python
    employees = pl.read_csv("employees.csv")

    by_salary = employees.sort("salary", descending=True)
    print("Employees by salary (highest first):")
    print(by_salary.select("name", "department", "salary"))
    print()

    print("Top 3 earners:")
    print(by_salary.head(3).select("name", "salary"))
    ```

    **Output:**

    ```
    Employees by salary (highest first):
    shape: (10, 3)
    ┌──────────────┬─────────────┬────────┐
    │ name         ┆ department  ┆ salary │
    │ ---          ┆ ---         ┆ ---    │
    │ str          ┆ str         ┆ i64    │
    ╞══════════════╪═════════════╪════════╡
    │ Alice Park   ┆ Engineering ┆ 95000  │
    │ Frank Kim    ┆ Finance     ┆ 92000  │
    │ Carol Wu     ┆ Finance     ┆ 88000  │
    │ David Chen   ┆ Engineering ┆ 85000  │
    │ Grace Patel  ┆ Engineering ┆ 82000  │
    │ Eva Lopez    ┆ Marketing   ┆ 76000  │
    │ Jack Rivera  ┆ Marketing   ┆ 74000  │
    │ Bob Martinez ┆ Marketing   ┆ 72000  │
    │ Iris Tanaka  ┆ Operations  ┆ 71000  │
    │ Henry Okafor ┆ Operations  ┆ 68000  │
    └──────────────┴─────────────┴────────┘

    Top 3 earners:
    shape: (3, 2)
    ┌────────────┬────────┐
    │ name       ┆ salary │
    │ ---        ┆ ---    │
    │ str        ┆ i64    │
    ╞════════════╪════════╡
    │ Alice Park ┆ 95000  │
    │ Frank Kim  ┆ 92000  │
    │ Carol Wu   ┆ 88000  │
    └────────────┴────────┘
    ```

    **Interpretation:** With `descending=True`, Alice Park's $95,000 tops the list; `head(3)` then trims the ranked table to its top 3 rows. Sort-then-head is the standard recipe for every "top N" business question — top customers by revenue, top products by margin, top employees by pay.

    *Source: `computations/module09_examples.py` — `demo_sort_salary()`*

### Multi-Column Sorts

Sorting by two columns means: order by the first column, and use the second to arrange rows *within* each group of equal first-column values. The `descending` parameter takes a list, one flag per column.

!!! example "Worked Example: Department, Then Salary Within Each"

    ```python
    employees = pl.read_csv("employees.csv")

    result = employees.sort(
        "department",
        "salary",
        descending=[False, True],
    )
    print("By department (A-Z), then salary (high to low) within each:")
    print(result.select("name", "department", "salary"))
    ```

    **Output:**

    ```
    By department (A-Z), then salary (high to low) within each:
    shape: (10, 3)
    ┌──────────────┬─────────────┬────────┐
    │ name         ┆ department  ┆ salary │
    │ ---          ┆ ---         ┆ ---    │
    │ str          ┆ str         ┆ i64    │
    ╞══════════════╪═════════════╪════════╡
    │ Alice Park   ┆ Engineering ┆ 95000  │
    │ David Chen   ┆ Engineering ┆ 85000  │
    │ Grace Patel  ┆ Engineering ┆ 82000  │
    │ Frank Kim    ┆ Finance     ┆ 92000  │
    │ Carol Wu     ┆ Finance     ┆ 88000  │
    │ Eva Lopez    ┆ Marketing   ┆ 76000  │
    │ Jack Rivera  ┆ Marketing   ┆ 74000  │
    │ Bob Martinez ┆ Marketing   ┆ 72000  │
    │ Iris Tanaka  ┆ Operations  ┆ 71000  │
    │ Henry Okafor ┆ Operations  ┆ 68000  │
    └──────────────┴─────────────┴────────┘
    ```

    **Interpretation:** The `descending` list pairs with the columns position by position: departments run alphabetically (ascending) while salaries run high-to-low inside each department. The result reads like a compensation report grouped by team — the layout managers actually ask for — produced by one method call.

    *Source: `computations/module09_examples.py` — `demo_sort_multi_column()`*

### Writing Results to Files

Analysis results usually leave Python — to Excel, to a web app, to the next stage of a pipeline. Polars writes the same formats it reads:

| Method | Format | Use case |
|--------|--------|----------|
| `df.write_csv("out.csv")` | CSV | Share with Excel and other tools |
| `df.write_json("out.json")` | JSON | Web applications, APIs |
| `df.write_parquet("out.parquet")` | Parquet | Fast storage, data pipelines |

!!! example "Worked Example: Writing the Engineering Roster to CSV"

    ```python
    employees = pl.read_csv("employees.csv")

    engineers = employees.filter(pl.col("department") == "Engineering")
    engineers.write_csv("engineers.csv")

    # Read it back to verify the write worked
    verified = pl.read_csv("engineers.csv")
    print(f"Wrote {verified.shape[0]} engineering records to engineers.csv")
    print()
    print("Read back from engineers.csv to verify:")
    print(verified.select("employee_id", "name", "salary", "performance_score"))
    ```

    **Output:**

    ```
    Wrote 3 engineering records to engineers.csv

    Read back from engineers.csv to verify:
    shape: (3, 4)
    ┌─────────────┬─────────────┬────────┬───────────────────┐
    │ employee_id ┆ name        ┆ salary ┆ performance_score │
    │ ---         ┆ ---         ┆ ---    ┆ ---               │
    │ str         ┆ str         ┆ i64    ┆ f64               │
    ╞═════════════╪═════════════╪════════╪═══════════════════╡
    │ E101        ┆ Alice Park  ┆ 95000  ┆ 4.2               │
    │ E104        ┆ David Chen  ┆ 85000  ┆ 3.9               │
    │ E107        ┆ Grace Patel ┆ 82000  ┆ 3.7               │
    └─────────────┴─────────────┴────────┴───────────────────┘
    ```

    **Interpretation:** `write_csv()` saved the filtered subset — 3 engineering records — with no confirmation message of its own, so the demo prints one. Reading the file back immediately is a habit worth keeping: it proves the file landed where you intended, with the rows and types you expected, before you email it to anyone.

    *Source: `computations/module09_examples.py` — `demo_write_csv()`*

### Chaining Operations

Because every Polars method returns a new DataFrame, calls can be **chained** into a single pipeline that reads top to bottom:

```python
result = (
    df
    .filter(pl.col("salary") > 75000)
    .select("name", "department", "salary")
    .sort("salary", descending=True)
)
```

The outer parentheses let the expression span multiple lines, one operation per line. Read it like a sentence: *take the data, keep these rows, keep these columns, put them in this order.*

!!! example "Worked Example: A Filter-Select-Sort Pipeline"

    ```python
    employees = pl.read_csv("employees.csv")

    top_performers = (
        employees
        .filter(pl.col("performance_score") >= 4.0)
        .select(
            pl.col("name"),
            pl.col("department"),
            pl.col("salary"),
            pl.col("performance_score"),
        )
        .sort("performance_score", descending=True)
    )

    print("Top performers (score >= 4.0), sorted by score:")
    print(top_performers)
    ```

    **Output:**

    ```
    Top performers (score >= 4.0), sorted by score:
    shape: (6, 4)
    ┌──────────────┬─────────────┬────────┬───────────────────┐
    │ name         ┆ department  ┆ salary ┆ performance_score │
    │ ---          ┆ ---         ┆ ---    ┆ ---               │
    │ str          ┆ str         ┆ i64    ┆ f64               │
    ╞══════════════╪═════════════╪════════╪═══════════════════╡
    │ Carol Wu     ┆ Finance     ┆ 88000  ┆ 4.5               │
    │ Jack Rivera  ┆ Marketing   ┆ 74000  ┆ 4.4               │
    │ Frank Kim    ┆ Finance     ┆ 92000  ┆ 4.3               │
    │ Alice Park   ┆ Engineering ┆ 95000  ┆ 4.2               │
    │ Eva Lopez    ┆ Marketing   ┆ 76000  ┆ 4.1               │
    │ Henry Okafor ┆ Operations  ┆ 68000  ┆ 4.0               │
    └──────────────┴─────────────┴────────┴───────────────────┘
    ```

    **Interpretation:** Six employees score at or above the 4.0 cutoff, led by Carol Wu at 4.5. The pipeline states the whole analysis in one expression: filter to strong performers, keep the reporting columns, rank by score. Notice that the ranking mixes departments and pay levels freely — Jack Rivera outranks colleagues who earn far more — because the sort key is performance, not salary.

    *Source: `computations/module09_examples.py` — `demo_chained_pipeline()`*

### Capstone: The Employee Analysis Pipeline

The module's closing example combines everything: read the roster, summarize it, run a chained filter-select-sort pipeline that answers a real HR question — *which strong performers earn below a salary threshold?* — and write the answer to a CSV. One new helper appears: `.to_series().value_counts()` converts a one-column selection into a Series and counts how often each value occurs (a preview of the grouping operations in the next module).

!!! example "Worked Example: From Raw Roster to Raise Recommendations"

    ```python
    employees = pl.read_csv("employees.csv")

    print("=== Employee Dataset Overview ===")
    print(f"Total employees: {employees.shape[0]}")
    print(f"Columns: {employees.columns}")
    print()

    # Head count per department
    dept_counts = (
        employees
        .select("department")
        .to_series()
        .value_counts()
        .sort("count", "department", descending=[True, False])
    )
    print("Employees per department:")
    for dept, count in dept_counts.iter_rows():
        print(f"  {dept:<14} {count} employees")
    print()

    # Raise candidates: high performers earning under the threshold
    raise_candidates = (
        employees
        .filter(
            (pl.col("performance_score") >= 4.0)
            & (pl.col("salary") < 85000)
        )
        .select(
            pl.col("name"),
            pl.col("department"),
            pl.col("salary"),
            pl.col("performance_score"),
            (pl.col("salary") * 1.05).round(2).alias("proposed_salary"),
        )
        .sort("performance_score", descending=True)
    )
    print("Raise candidates (performance >= 4.0 and salary < $85,000):")
    print(raise_candidates)
    print()

    raise_candidates.write_csv("raise_candidates.csv")
    print(f"Wrote {raise_candidates.shape[0]} raise candidates to raise_candidates.csv")
    ```

    **Output:**

    ```
    === Employee Dataset Overview ===
    Total employees: 10
    Columns: ['employee_id', 'name', 'department', 'hire_date', 'salary', 'performance_score']

    Employees per department:
      Engineering    3 employees
      Marketing      3 employees
      Finance        2 employees
      Operations     2 employees

    Raise candidates (performance >= 4.0 and salary < $85,000):
    shape: (3, 5)
    ┌──────────────┬────────────┬────────┬───────────────────┬─────────────────┐
    │ name         ┆ department ┆ salary ┆ performance_score ┆ proposed_salary │
    │ ---          ┆ ---        ┆ ---    ┆ ---               ┆ ---             │
    │ str          ┆ str        ┆ i64    ┆ f64               ┆ f64             │
    ╞══════════════╪════════════╪════════╪═══════════════════╪═════════════════╡
    │ Jack Rivera  ┆ Marketing  ┆ 74000  ┆ 4.4               ┆ 77700.0         │
    │ Eva Lopez    ┆ Marketing  ┆ 76000  ┆ 4.1               ┆ 79800.0         │
    │ Henry Okafor ┆ Operations ┆ 68000  ┆ 4.0               ┆ 71400.0         │
    └──────────────┴────────────┴────────┴───────────────────┴─────────────────┘

    Wrote 3 raise candidates to raise_candidates.csv
    ```

    **Interpretation:** The overview confirms the dataset (10 employees), and the head-count loop shows Engineering and Marketing tied at 3 employees each. The main pipeline then answers the HR question and prices a five percent increase for each candidate as a `proposed_salary` column: Jack Rivera leads at 4.4, with a proposed salary of $77,700. The finished table — filtered, enriched, ranked — is written to `raise_candidates.csv`, ready to open in Excel. Every skill in this module appears once: read, inspect, filter, compute with expressions, sort, write.

    *Source: `computations/module09_examples.py` — `demo_capstone_pipeline()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "`sort()` puts the biggest values first by default." | The default is ascending; pass `descending=True` for biggest-first. |
| "`head()` picks a representative sample." | It returns the *first* n rows in the current order — which is why it usually follows a `sort()`. |
| "`write_csv()` shows me the file contents." | It writes silently and returns nothing to display. Read the file back if you want confirmation. |
| "A chain modifies the DataFrame at each step." | Each step returns a new DataFrame and the original is untouched — assign the end of the chain to a variable or the result is lost. |

---

## Reflection Questions

1. Compare `pl.read_csv()` to the manual parsing you wrote in Module 8 — open the file, split each line on commas, convert each field. What work moved from your code into the library, and what should you still verify (types, headers, odd values) after any import?
2. `df.select("salary")` and `df.select(pl.col("salary"))` produce the same result. When is the plain string enough, and what does wrapping the name in `pl.col()` make possible that a string cannot do?
3. Why does `filter()` require `&` and `|` instead of Python's `and` / `or`, and why must each condition sit inside its own parentheses? What might happen if you forget?
4. `select()` chooses columns and `filter()` chooses rows. Think of a report your organization produces (or one from a job you have held): which columns would you select, which rows would you filter, and would the order of those two steps matter?
5. The capstone expressed its analysis as one chained pipeline. What are the advantages over five separate assignments, and how would you track down the problem if the final table looked wrong somewhere in the middle of the chain?
6. Every Polars method returns a new DataFrame instead of modifying the original. What kinds of analysis mistakes does this design prevent, and what new habit does it require of you?

---

## Your Assignment

The Module 9 assignment is worth **100 points plus a 10-point bonus**. You complete it in a **marimo notebook (`.py` file)** and submit the file to **Blackboard**. The final reflection section is not graded separately — it counts toward participation. Setup cells in the notebook create the CSV files the tasks read (under `/tmp/`), so you only write the analysis code. The tasks follow this module's sections in order and build toward a complete pipeline.

**Task 1: Creating and Inspecting DataFrames (10 points).** A retail chain tracks monthly performance across six stores. You build a DataFrame from a provided dictionary of store data, print its shape, columns, and schema, preview the first rows with `head()`, and produce summary statistics with `describe()`. Everything you need is in §9.1.

**Task 2: Reading CSV and Basic Inspection (15 points).** A used-car dealership keeps its inventory in a CSV file that the setup cell creates for you. You read it with `pl.read_csv()`, report the shape and dtypes, and display the full DataFrame. The reading is §9.2; the inspection habits come from §9.1.

**Task 3: Selecting and Transforming Columns (15 points).** The dealership manager wants a pricing analysis. You first select a few identifying columns, then build a second selection with computed columns — a discounted sale price and a cost-per-MPG figure — each rounded and given a readable name with `.alias()`. This is §9.3's expression toolkit applied to new data.

**Task 4: Filtering Rows (15 points).** Customers ask questions about the inventory, and each becomes a filter: one equality condition on vehicle type, one numeric comparison on price, one combined `&` condition (a type *and* a fuel-economy requirement), and one `is_in()` filter matching a list of makes. Label each result with a print statement. All four patterns appear in §9.4.

**Task 5: Sorting and Top/Bottom (20 points).** The dealership wants ranked lists for its website: the most expensive vehicles (sort descending, then `head()`), the most fuel-efficient (same recipe on a different column), and a multi-column sort that groups vehicles by type with the priciest first within each group. These are the §9.5 sorting patterns.

**Task 6: Full Pipeline Challenge (25 points).** An office-supply company's order records arrive as a CSV. You build one chained expression that filters to orders at or above a quantity threshold, selects identifying columns plus a computed order total, sorts by that total, and writes the result to a new CSV — then you read the file back and display it to verify. This is the §9.5 chaining and writing workflow, drawing on §9.2 through §9.4.

**Task 7: Creative Exercise — Bonus (10 points).** Design your own business scenario (the prompt suggests a restaurant menu, a fitness tracker, a movie database, or a student gradebook) with at least 6 rows and 4 columns. Your solution must create or read a DataFrame, use `select()` with a computed `pl.col()` column and `.alias()`, apply at least one `filter()`, sort the result, and explain your findings with formatted print output.

---

## Chapter Summary

This module replaced hand-rolled data handling with Polars, the course's data analysis library. A **DataFrame** is a table of named, typed columns; a **Series** is a single column; and the first habit of any analysis is inspection — `shape`, `columns`, `schema`, `head()`, and `describe()` — to confirm what you are actually looking at. `pl.read_csv()` and `pl.read_json()` collapse Module 8's open-split-convert routine into one call that also infers each column's type, and `write_csv()` (plus its JSON and Parquet siblings) sends finished results back out to the tools your colleagues use.

The analytical core of the module is a pair of complementary operations. `select()` chooses **columns**, and with `pl.col()` expressions it also transforms them — arithmetic, rounding, renaming with `.alias()` — across the whole column at once, no loops. `filter()` chooses **rows** matching conditions built from the same expressions, combined with `&` and `|` (each condition parenthesized), with `str.contains()` for text and `is_in()` for matching a list of values. `sort()` orders the result, `head()` trims it to the top, and because every method returns a new DataFrame, the operations chain into pipelines that read like instructions: filter these rows, keep these columns, rank them, write the file.

The capstone put the full sequence to work on a business question — which strong performers earn below a threshold, and what would a raise cost? — and that pipeline shape (read, filter, compute, sort, write) is the skeleton of nearly everything you will build in the remainder of the course.

---

## What's Next

You can now *explore* a dataset: load it, inspect it, and cut it down to the rows and columns that matter. In **Module 10: Polars — Transformations & Aggregations** you learn to *transform* it: adding computed columns with `with_columns()`, renaming and casting types (turning those `str` dates into real dates), summarizing groups with `group_by().agg()` — the proper version of this module's department head-count — joining DataFrames on shared keys, and handling missing values. Those are the operations that turn raw records into the summary tables behind every managerial report.
