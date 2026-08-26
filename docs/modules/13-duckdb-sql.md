# Module 13: DuckDB: SQL-Based Data Analysis

## Introduction

Almost every organization keeps its operational data in systems that speak **SQL** — order databases, cloud warehouses, BI tools, even Excel's Power Query. SQL is the shared language of corporate data, and analysts who can read and write it can pull answers from nearly any system they encounter. This module adds SQL to your toolkit through **DuckDB**, an analytical database that runs entirely inside your Python process: no server to install, no administrator to call, and the ability to query CSV files directly without loading them first. The goal is not to replace Polars — it is to give you a second, complementary tool, plus the glue that joins the two: DuckDB can query a Polars DataFrame by name, and any DuckDB result converts back to Polars with a single method call. By the end of the module you will use SQL for what SQL does best (multi-table joins, ad-hoc questions) and Polars for what it does best (transformation pipelines and feeding charts), combined in one workflow that ends with a small business-intelligence report.

---

## Learning Objectives

By the end of this module, you should be able to:

1. **Explain** what DuckDB is and when to choose SQL over Polars expressions
2. **Run** SQL queries on CSV files directly, without a loading step
3. **Shape** results with SELECT, WHERE, ORDER BY, calculated columns, and CASE WHEN
4. **Summarize** data with aggregate functions (SUM, AVG, COUNT, MIN, MAX), GROUP BY, and HAVING
5. **Join** multiple tables and write scalar and IN subqueries
6. **Convert** between DuckDB results and Polars DataFrames for combined SQL-plus-Python workflows

---

## 13.1 What Is DuckDB?

DuckDB is an **embedded analytical database** — think of it as SQLite's data-analysis cousin. "Embedded" means it runs entirely inside your Python process: there is no separate server to install, start, or connect to. "Analytical" means it is optimized for the kind of queries analysts run all day — filtering, grouping, joining, and aggregating — rather than for the one-record-at-a-time updates a transactional system handles.

### Why Learn SQL When We Already Have Polars?

Modules 9 and 10 gave you a capable data-analysis toolkit in Polars. Four reasons justify adding SQL beside it:

- SQL is the universal language of data — every database, every cloud warehouse, every BI tool understands it
- Many business analysts already know SQL from Excel Power Query or database courses, so SQL queries are often the easiest artifact to share with colleagues
- DuckDB can query files (CSV, Parquet, JSON) directly — no loading step
- Some questions are more natural to express as a SQL query than as a method chain

The goal is not to replace Polars. It is to add SQL as a second tool in your analytical toolkit — and, as the integration section shows, DuckDB and Polars work together seamlessly.

### The Three-Table Retail Dataset

Every example in this module works on a small retail-orders dataset with three related tables — the kind of schema you would see in a real business database:

| Table | One row per... | Key columns |
|-------|----------------|-------------|
| `orders` | order | `order_id`, `customer_id`, `order_date`, `total`, `status` |
| `customers` | customer | `customer_id`, `name`, `city`, `state`, `join_date` |
| `order_items` | line item within an order | `item_id`, `order_id`, `product`, `category`, `quantity`, `unit_price` |

Notice the shared columns: `customer_id` links orders to customers, and `order_id` links line items to orders. Splitting data this way avoids repeating customer details on every order row — and the joins section shows how SQL reconnects the pieces. The dataset lives in three CSV files (`m13_orders.csv`, `m13_customers.csv`, `m13_order_items.csv`).

!!! example "Worked Example: The Three-Table Retail Dataset"

    ```python
    import polars as pl

    orders = pl.read_csv("m13_orders.csv")
    customers = pl.read_csv("m13_customers.csv")
    order_items = pl.read_csv("m13_order_items.csv")

    print(f"orders:      {orders.shape[0]} rows, {orders.shape[1]} columns")
    print(f"customers:   {customers.shape[0]} rows, {customers.shape[1]} columns")
    print(f"order_items: {order_items.shape[0]} rows, {order_items.shape[1]} columns")
    ```

    **Output:**

    ```
    orders:      20 rows, 5 columns
    customers:   9 rows, 5 columns
    order_items: 31 rows, 6 columns
    ```

    **Interpretation:** The dataset is deliberately small — 20 orders placed by 9 customers, broken down into 31 line items — so every query result in this module can be checked by hand. The structure, however, is realistic: a transaction table, a customer lookup table, and a line-item detail table connected by shared ID columns.

    *Source: `computations/module13_examples.py` — `demo_dataset_overview()`*

### Your First Query

DuckDB can query a CSV file directly — you write standard SQL and put the file's path where a table name would normally go. The `duckdb.sql()` function runs the query and returns a result object, and calling `.pl()` on that result converts it to a Polars DataFrame.

One habit this module adds to the notebook's version of these queries: an explicit `ORDER BY`. SQL makes **no guarantee about row order** unless you ask for one — the teaching notebook's first queries relied on the file's row order, which usually holds for a small single-file read but is not promised. The examples here sort explicitly whenever the displayed rows depend on order.

!!! example "Worked Example: Your First Query — SQL Straight from a CSV File"

    ```python
    import duckdb

    result = duckdb.sql("""
        SELECT *
        FROM 'm13_orders.csv'
        ORDER BY order_id
        LIMIT 5
    """)
    print("First 5 orders (queried directly from CSV):")
    print(result)

    df = duckdb.sql("SELECT * FROM 'm13_orders.csv'").pl()
    print(f"Result as Polars DataFrame: {df.shape}")
    print(f"Columns: {df.columns}")
    ```

    **Output:**

    ```
    First 5 orders (queried directly from CSV):
    ┌──────────┬─────────────┬────────────┬────────┬───────────┐
    │ order_id │ customer_id │ order_date │ total  │  status   │
    │ varchar  │   varchar   │    date    │ double │  varchar  │
    ├──────────┼─────────────┼────────────┼────────┼───────────┤
    │ ORD-001  │ C101        │ 2025-01-15 │  245.5 │ Completed │
    │ ORD-002  │ C102        │ 2025-01-18 │  189.0 │ Completed │
    │ ORD-003  │ C103        │ 2025-01-22 │ 512.75 │ Completed │
    │ ORD-004  │ C101        │ 2025-02-03 │  78.25 │ Completed │
    │ ORD-005  │ C104        │ 2025-02-10 │ 1250.0 │ Completed │
    └──────────┴─────────────┴────────────┴────────┴───────────┘

    Result as Polars DataFrame: (20, 5)
    Columns: ['order_id', 'customer_id', 'order_date', 'total', 'status']
    ```

    **Interpretation:** No loading step: DuckDB read the file, *inferred* each column's type (see the second header row — `order_date` became `date`, `total` became `double`), ran the query, and printed its own table format. The `.pl()` call then turned a full-table query into a Polars DataFrame of shape (20, 5), ready for any technique from the Polars modules. That type inference matters later: a date column is a real `date`, not text, which changes how you filter it.

    *Source: `computations/module13_examples.py` — `demo_first_query()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "Databases require a server, so DuckDB must need one too." | DuckDB is *embedded*: it runs inside your Python process. `import duckdb` is the entire installation-and-connection story. |
| "I have to load a CSV into a table before I can query it." | `SELECT * FROM 'file.csv'` queries the file directly. Creating a table (covered in the integration section) is an optimization for repeated querying, not a requirement. |
| "Learning SQL means abandoning Polars." | They are complementary. DuckDB queries Polars DataFrames by name, and `.pl()` converts results back — the course uses both, often in the same analysis. |
| "Query results come back in a reliable order." | Without `ORDER BY`, SQL promises nothing about row order. Small file reads usually preserve file order, but any query whose output order matters should sort explicitly. |

---

## 13.2 SQL Essentials: SELECT, WHERE, and Calculated Columns

SQL reads like structured English. A query names the columns it wants, the table (or file) they come from, and the conditions rows must meet:

```sql
SELECT column1, column2
FROM 'file.csv'
WHERE condition
ORDER BY column1
LIMIT n
```

The clauses map directly onto Polars operations you already know:

| SQL clause | Polars equivalent | Purpose |
|------------|-------------------|---------|
| `SELECT` | `.select()` | Which columns to return |
| `WHERE` | `.filter()` | Which rows to keep |
| `ORDER BY` | `.sort()` | Sort the result (`DESC` = largest first) |
| `LIMIT` | `.head()` | Cap the number of rows returned |

### SELECT and WHERE

`SELECT` lists columns; `*` means "all of them." `WHERE` keeps only rows that satisfy a condition, and conditions combine with `AND` / `OR` just as in Python.

!!! example "Worked Example: SELECT and WHERE"

    ```python
    result = duckdb.sql("""
        SELECT order_id, customer_id, total
        FROM 'm13_orders.csv'
        ORDER BY order_id
        LIMIT 5
    """)
    print("Selected columns:")
    print(result)

    result = duckdb.sql("""
        SELECT order_id, customer_id, total, status
        FROM 'm13_orders.csv'
        WHERE total > 500
          AND status = 'Completed'
        ORDER BY order_id
    """)
    print("Orders over $500 (completed only):")
    print(result)
    ```

    **Output:**

    ```
    Selected columns:
    ┌──────────┬─────────────┬────────┐
    │ order_id │ customer_id │ total  │
    │ varchar  │   varchar   │ double │
    ├──────────┼─────────────┼────────┤
    │ ORD-001  │ C101        │  245.5 │
    │ ORD-002  │ C102        │  189.0 │
    │ ORD-003  │ C103        │ 512.75 │
    │ ORD-004  │ C101        │  78.25 │
    │ ORD-005  │ C104        │ 1250.0 │
    └──────────┴─────────────┴────────┘

    Orders over $500 (completed only):
    ┌──────────┬─────────────┬────────┬───────────┐
    │ order_id │ customer_id │ total  │  status   │
    │ varchar  │   varchar   │ double │  varchar  │
    ├──────────┼─────────────┼────────┼───────────┤
    │ ORD-003  │ C103        │ 512.75 │ Completed │
    │ ORD-005  │ C104        │ 1250.0 │ Completed │
    │ ORD-008  │ C103        │  678.3 │ Completed │
    │ ORD-012  │ C104        │ 2100.0 │ Completed │
    │ ORD-016  │ C103        │  890.0 │ Completed │
    │ ORD-018  │ C101        │  560.0 │ Completed │
    │ ORD-019  │ C109        │ 1425.0 │ Completed │
    └──────────┴─────────────┴────────┴───────────┘
    ```

    **Interpretation:** The first query trims the table to three named columns. The second combines two conditions with `AND`: seven completed orders exceed the $500 bar, topped by ORD-012 at 2100.0. Note the SQL quirk that trips up Python programmers — SQL uses a single `=` for comparison (`status = 'Completed'`), not `==`, and string literals take single quotes.

    *Source: `computations/module13_examples.py` — `demo_select_where()`*

### Calculated Columns with `AS`

A SELECT list is not limited to existing columns — any expression works, and `AS` names the result. This is SQL's version of the `with_columns()` + `.alias()` pattern from Polars: the source file is never modified; the new columns exist only in the query result.

!!! example "Worked Example: Calculated Columns and a Top-Five List"

    ```python
    result = duckdb.sql("""
        SELECT
            order_id,
            total,
            total * 0.08 AS tax,
            total * 1.08 AS total_with_tax
        FROM 'm13_orders.csv'
        WHERE total > 300
        ORDER BY total DESC
    """)
    print("Orders over $300 with tax calculated:")
    print(result)

    result = duckdb.sql("""
        SELECT order_id, customer_id, total
        FROM 'm13_orders.csv'
        WHERE status = 'Completed'
        ORDER BY total DESC
        LIMIT 5
    """)
    print("Top 5 orders by value:")
    print(result)
    ```

    **Output:**

    ```
    Orders over $300 with tax calculated:
    ┌──────────┬────────┬────────────────────┬────────────────────┐
    │ order_id │ total  │        tax         │   total_with_tax   │
    │ varchar  │ double │       double       │       double       │
    ├──────────┼────────┼────────────────────┼────────────────────┤
    │ ORD-012  │ 2100.0 │              168.0 │             2268.0 │
    │ ORD-019  │ 1425.0 │              114.0 │             1539.0 │
    │ ORD-005  │ 1250.0 │              100.0 │             1350.0 │
    │ ORD-016  │  890.0 │               71.2 │              961.2 │
    │ ORD-008  │  678.3 │ 54.263999999999996 │            732.564 │
    │ ORD-018  │  560.0 │ 44.800000000000004 │  604.8000000000001 │
    │ ORD-003  │ 512.75 │              41.02 │             553.77 │
    │ ORD-013  │  445.5 │              35.64 │ 481.14000000000004 │
    │ ORD-010  │  420.0 │               33.6 │              453.6 │
    │ ORD-006  │  345.0 │               27.6 │              372.6 │
    │ ORD-015  │ 310.25 │              24.82 │ 335.07000000000005 │
    └──────────┴────────┴────────────────────┴────────────────────┘
      11 rows                                           4 columns

    Top 5 orders by value:
    ┌──────────┬─────────────┬────────┐
    │ order_id │ customer_id │ total  │
    │ varchar  │   varchar   │ double │
    ├──────────┼─────────────┼────────┤
    │ ORD-012  │ C104        │ 2100.0 │
    │ ORD-019  │ C109        │ 1425.0 │
    │ ORD-005  │ C104        │ 1250.0 │
    │ ORD-016  │ C103        │  890.0 │
    │ ORD-008  │ C103        │  678.3 │
    └──────────┴─────────────┴────────┘
    ```

    **Interpretation:** Each row now carries an eight-percent `tax` and a `total_with_tax` computed on the fly. Look closely at ORD-008's tax: `54.263999999999996` — the same floating-point representation noise you met in the early arithmetic modules, now appearing in SQL. The `ROUND()` function (used from the aggregation section onward) cleans this up for presentation. The second query is the classic top-N pattern — `ORDER BY total DESC` puts the largest first, `LIMIT` caps the list — led again by ORD-012 at 2100.0. Note the first query filters on the amount only, so the cancelled order ORD-006 still appears in the tax table; the top-five query adds the completed-status filter.

    *Source: `computations/module13_examples.py` — `demo_calculated_columns()`*

!!! question "Try It Yourself: March Orders"

    Write a query that selects `order_id`, `order_date`, and `total` from the
    orders CSV, but only for orders placed in March 2025 (`order_date` starts
    with `2025-03`).

    **Hint:** When DuckDB reads the CSV it inspects the data and infers that
    `order_date` is a `DATE` column, not text. The `LIKE` operator only works
    on text, so you have to convert the date to a string first:
    `WHERE CAST(order_date AS VARCHAR) LIKE '2025-03%'`. Without the cast,
    DuckDB stops with a *"no function matches"* binder error, because there is
    no `LIKE` that compares a `DATE` to a text pattern.

### A Toolbox of Useful SQL Functions

DuckDB supports hundreds of functions. These are the ones this module's queries lean on:

| Function | Purpose | Example |
|----------|---------|---------|
| `ROUND(x, n)` | Round to n decimal places | `ROUND(avg_price, 2)` |
| `COALESCE(a, b)` | Return first non-null value | `COALESCE(discount, 0)` |
| `CAST(x AS type)` | Convert data type | `CAST(order_date AS VARCHAR)` |
| `strftime(date, fmt)` | Format a date | `strftime(order_date, '%Y-%m')` |
| `CASE WHEN ... THEN ...` | Conditional logic | see the next example |
| `LIKE` | Pattern matching | `WHERE name LIKE 'A%'` |
| `IN (...)` | Match any value in a list | `WHERE state IN ('CA', 'OR')` |
| `BETWEEN a AND b` | Range check | `WHERE total BETWEEN 100 AND 500` |

### Conditional Columns with CASE WHEN

`CASE WHEN` is SQL's if/elif/else: conditions are checked top to bottom, and the first match wins. It is how analysts build **business categories** — order-size tiers, risk bands, customer segments — directly inside a query.

!!! example "Worked Example: Classifying Orders with CASE WHEN"

    ```python
    result = duckdb.sql("""
        SELECT
            order_id,
            total,
            CASE
                WHEN total < 100 THEN 'Small'
                WHEN total < 500 THEN 'Medium'
                WHEN total < 1000 THEN 'Large'
                ELSE 'Premium'
            END AS order_size
        FROM 'm13_orders.csv'
        WHERE status = 'Completed'
        ORDER BY total DESC
    """)
    print("Orders classified by size:")
    print(result)
    ```

    **Output:**

    ```
    Orders classified by size:
    ┌──────────┬────────┬────────────┐
    │ order_id │ total  │ order_size │
    │ varchar  │ double │  varchar   │
    ├──────────┼────────┼────────────┤
    │ ORD-012  │ 2100.0 │ Premium    │
    │ ORD-019  │ 1425.0 │ Premium    │
    │ ORD-005  │ 1250.0 │ Premium    │
    │ ORD-016  │  890.0 │ Large      │
    │ ORD-008  │  678.3 │ Large      │
    │ ORD-018  │  560.0 │ Large      │
    │ ORD-003  │ 512.75 │ Large      │
    │ ORD-013  │  445.5 │ Medium     │
    │ ORD-010  │  420.0 │ Medium     │
    │ ORD-015  │ 310.25 │ Medium     │
    │ ORD-001  │  245.5 │ Medium     │
    │ ORD-020  │  235.0 │ Medium     │
    │ ORD-002  │  189.0 │ Medium     │
    │ ORD-017  │  175.5 │ Medium     │
    │ ORD-009  │  156.0 │ Medium     │
    │ ORD-007  │   92.5 │ Small      │
    │ ORD-011  │  88.75 │ Small      │
    │ ORD-004  │  78.25 │ Small      │
    └──────────┴────────┴────────────┘
      18 rows              3 columns
    ```

    **Interpretation:** All 18 completed orders receive a size label from the same tier ladder — the `if`/`elif`/`else` reasoning of the control-flow module, expressed in SQL. Because conditions are evaluated top to bottom, ORD-016 at 890.0 stops at the under-one-thousand rung and is labeled `Large`; only the three orders above that rung fall through to the `ELSE` branch and earn `Premium`. Segment labels like these become grouping columns in the next section.

    *Source: `computations/module13_examples.py` — `demo_case_when()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "`AS tax` adds a tax column to the CSV file." | A query never modifies its source. Calculated columns exist only in the result — the same immutability principle as Polars `with_columns()`. |
| "`=` vs `==`: SQL works like Python." | SQL uses a single `=` for comparison and single quotes for strings. Writing `status == "Completed"` is a Python habit that SQL rejects. |
| "`LIKE` works on any column." | `LIKE` matches *text*. DuckDB inferred `order_date` as a `DATE`, so pattern-matching it requires `CAST(order_date AS VARCHAR)` first. |
| "`ORDER BY` sorts largest-first by default." | The default is ascending. Add `DESC` for largest-first — forgetting it is the most common cause of a "top 5" list that shows the *bottom* five. |
| "`CASE WHEN` branches are checked in the best order automatically." | Conditions run strictly top to bottom and the first match wins. Ordering the rungs wrong (for example, the broadest condition first) silently mislabels every row. |

---

## 13.3 Aggregation: Summary Functions, GROUP BY, and HAVING

Aggregation collapses many rows into summary numbers — the totals, averages, and counts that headline every management report. SQL's built-in aggregate functions:

| Function | Purpose | Example |
|----------|---------|---------|
| `COUNT(*)` | Number of rows | `COUNT(*)` |
| `COUNT(col)` | Number of non-NULL values | `COUNT(order_id)` |
| `SUM(col)` | Total | `SUM(total)` |
| `AVG(col)` | Average | `AVG(total)` |
| `MIN(col)` | Smallest value | `MIN(total)` |
| `MAX(col)` | Largest value | `MAX(total)` |
| `COUNT(DISTINCT col)` | Unique values | `COUNT(DISTINCT customer_id)` |

**`COUNT(*)` vs. `COUNT(col)`:** `COUNT(*)` counts every row; `COUNT(col)` counts only rows where `col` is not NULL. The difference is invisible on a clean table but becomes important with LEFT JOINs, where unmatched rows are padded with NULLs — the joins section returns to this exact trap.

### Whole-Table Summaries

Without GROUP BY, aggregate functions return a single summary row for the entire table.

!!! example "Worked Example: Whole-Table Summary Statistics"

    ```python
    result = duckdb.sql("""
        SELECT
            COUNT(*) AS total_orders,
            SUM(total) AS revenue,
            AVG(total) AS avg_order,
            MIN(total) AS smallest_order,
            MAX(total) AS largest_order,
            COUNT(DISTINCT customer_id) AS unique_customers
        FROM 'm13_orders.csv'
        WHERE status = 'Completed'
    """)
    print("Order summary (completed orders only):")
    print(result)
    ```

    **Output:**

    ```
    Order summary (completed orders only):
    ┌──────────────┬─────────┬───────────────────┬────────────────┬───────────────┬──────────────────┐
    │ total_orders │ revenue │     avg_order     │ smallest_order │ largest_order │ unique_customers │
    │    int64     │ double  │      double       │     double     │    double     │      int64       │
    ├──────────────┼─────────┼───────────────────┼────────────────┼───────────────┼──────────────────┤
    │           18 │  9852.3 │ 547.3499999999999 │          78.25 │        2100.0 │                8 │
    └──────────────┴─────────┴───────────────────┴────────────────┴───────────────┴──────────────────┘
    ```

    **Interpretation:** One query, six business facts: 18 completed orders from 8 distinct customers produced $9,852.30 of revenue, with order values ranging from 78.25 to 2100.0 and averaging $547.35 (shown raw as `547.3499999999999` — a `ROUND()` wrapper would tidy it). The `WHERE` clause runs *before* aggregation, so the two cancelled orders never enter any of these numbers.

    *Source: `computations/module13_examples.py` — `demo_aggregates()`*

### GROUP BY — Summarize by Category

GROUP BY splits the rows into groups and computes each aggregate once per group — SQL's version of split-apply-combine, equivalent to Polars `group_by().agg()`. One rule governs the SELECT list: **every column must be either inside an aggregate function or listed in GROUP BY.** A bare column would be ambiguous — which of the group's many values should be shown?

!!! example "Worked Example: Customer Spending with GROUP BY"

    ```python
    result = duckdb.sql("""
        SELECT
            customer_id,
            COUNT(*) AS order_count,
            SUM(total) AS total_spent,
            AVG(total) AS avg_order,
            MAX(total) AS largest_order
        FROM 'm13_orders.csv'
        WHERE status = 'Completed'
        GROUP BY customer_id
        ORDER BY total_spent DESC
    """)
    print("Customer spending summary:")
    print(result)
    ```

    **Output:**

    ```
    Customer spending summary:
    ┌─────────────┬─────────────┬─────────────┬───────────────────┬───────────────┐
    │ customer_id │ order_count │ total_spent │     avg_order     │ largest_order │
    │   varchar   │    int64    │   double    │      double       │    double     │
    ├─────────────┼─────────────┼─────────────┼───────────────────┼───────────────┤
    │ C104        │           2 │      3350.0 │            1675.0 │        2100.0 │
    │ C103        │           3 │     2081.05 │ 693.6833333333334 │         890.0 │
    │ C109        │           1 │      1425.0 │            1425.0 │        1425.0 │
    │ C101        │           4 │     1303.75 │          325.9375 │         560.0 │
    │ C102        │           2 │       634.5 │            317.25 │         445.5 │
    │ C105        │           2 │      402.75 │           201.375 │        310.25 │
    │ C106        │           2 │       331.5 │            165.75 │         175.5 │
    │ C107        │           2 │      323.75 │           161.875 │         235.0 │
    └─────────────┴─────────────┴─────────────┴───────────────────┴───────────────┘
    ```

    **Interpretation:** Eighteen order rows collapse into eight customer rows, and two different "best customer" stories emerge: C104 spends the most (3350.0 across just 2 orders, averaging 1675.0), while C101 orders most *frequently* — 4 orders — yet totals only 1303.75. Which customer matters more is a business judgment; the query's job is to surface both facts. The unrounded averages (`693.6833333333334`) again argue for wrapping presentation columns in `ROUND()`, which the remaining examples do.

    *Source: `computations/module13_examples.py` — `demo_group_by_customer()`*

### Grouping by a Derived Value

The grouping column does not have to exist in the data — it can be computed in the query. Grouping by `strftime(order_date, '%Y-%m')` rolls daily orders up to months; grouping the line-items file by `category` rolls products up to categories.

!!! example "Worked Example: Grouping by Month and by Category"

    ```python
    result = duckdb.sql("""
        SELECT
            strftime(order_date::DATE, '%Y-%m') AS month,
            COUNT(*) AS order_count,
            ROUND(SUM(total), 2) AS revenue
        FROM 'm13_orders.csv'
        WHERE status = 'Completed'
        GROUP BY month
        ORDER BY month
    """)
    print("Monthly revenue:")
    print(result)

    result = duckdb.sql("""
        SELECT
            category,
            COUNT(*) AS line_items,
            SUM(quantity) AS total_units,
            ROUND(SUM(quantity * unit_price), 2) AS total_revenue,
            ROUND(AVG(unit_price), 2) AS avg_price
        FROM 'm13_order_items.csv'
        GROUP BY category
        ORDER BY total_revenue DESC
    """)
    print("Revenue by product category:")
    print(result)
    ```

    **Output:**

    ```
    Monthly revenue:
    ┌─────────┬─────────────┬─────────┐
    │  month  │ order_count │ revenue │
    │ varchar │    int64    │ double  │
    ├─────────┼─────────────┼─────────┤
    │ 2025-01 │           3 │  947.25 │
    │ 2025-02 │           3 │ 1420.75 │
    │ 2025-03 │           5 │ 3443.05 │
    │ 2025-04 │           3 │ 1645.75 │
    │ 2025-05 │           4 │  2395.5 │
    └─────────┴─────────────┴─────────┘

    Revenue by product category:
    ┌─────────────┬────────────┬─────────────┬───────────────┬───────────┐
    │  category   │ line_items │ total_units │ total_revenue │ avg_price │
    │   varchar   │   int64    │   int128    │    double     │  double   │
    ├─────────────┼────────────┼─────────────┼───────────────┼───────────┤
    │ Electronics │         11 │          14 │       1357.22 │    113.38 │
    │ Furniture   │          3 │           3 │        1139.0 │    379.67 │
    │ Office      │         11 │          21 │         531.5 │     31.11 │
    │ Accessories │          6 │          10 │         195.0 │     22.92 │
    └─────────────┴────────────┴─────────────┴───────────────┴───────────┘
    ```

    **Interpretation:** The monthly view shows revenue peaking in `2025-03` at 3443.05 across 5 orders — a trend line waiting to be drawn, which the capstone does. The category view tells a high-ticket-versus-high-volume story: Furniture earns 1139.0 from only 3 units at the highest average price (379.67), while Office ships 21 units for just 531.5. One caution: this query reads the raw items file with *no* order-status filter, so the cancelled order's line items are still counted — the capstone's category report joins to the orders table to exclude them, and its numbers differ accordingly.

    *Source: `computations/module13_examples.py` — `demo_group_by_month_category()`*

!!! question "Try It Yourself: Revenue by Product"

    Write a GROUP BY query on the order-items CSV that finds the total quantity
    and total revenue for each **product** (not category). Sort by total
    revenue descending. Which product generates the most revenue?

### HAVING — Filter After Grouping

WHERE filters rows **before** grouping; HAVING filters groups **after** aggregation. Use HAVING when the condition involves an aggregate — you cannot ask WHERE about a group total that has not been computed yet. Think of it as: WHERE is the bouncer at the door, HAVING is the bouncer at the VIP section.

> **Portability note:** Referring to the output alias `total_spent` inside `HAVING` is a DuckDB convenience. Standard SQL evaluates `HAVING` before the SELECT aliases exist, so some databases (PostgreSQL, SQL Server, Oracle) reject it and want the aggregate repeated: `HAVING SUM(total) > 500`. That fully portable form also works in DuckDB, so reach for it when your query may run elsewhere.

!!! example "Worked Example: HAVING — Keeping Only the Big Groups"

    ```python
    result = duckdb.sql("""
        SELECT
            customer_id,
            COUNT(*) AS order_count,
            ROUND(SUM(total), 2) AS total_spent
        FROM 'm13_orders.csv'
        WHERE status = 'Completed'
        GROUP BY customer_id
        HAVING total_spent > 500
        ORDER BY total_spent DESC
    """)
    print("High-value customers (>$500 total):")
    print(result)

    result = duckdb.sql("""
        SELECT
            category,
            SUM(quantity) AS total_units,
            ROUND(SUM(quantity * unit_price), 2) AS total_revenue
        FROM 'm13_order_items.csv'
        GROUP BY category
        HAVING total_units > 10
        ORDER BY total_revenue DESC
    """)
    print("Categories with >10 units sold:")
    print(result)
    ```

    **Output:**

    ```
    High-value customers (>$500 total):
    ┌─────────────┬─────────────┬─────────────┐
    │ customer_id │ order_count │ total_spent │
    │   varchar   │    int64    │   double    │
    ├─────────────┼─────────────┼─────────────┤
    │ C104        │           2 │      3350.0 │
    │ C103        │           3 │     2081.05 │
    │ C109        │           1 │      1425.0 │
    │ C101        │           4 │     1303.75 │
    │ C102        │           2 │       634.5 │
    └─────────────┴─────────────┴─────────────┘

    Categories with >10 units sold:
    ┌─────────────┬─────────────┬───────────────┐
    │  category   │ total_units │ total_revenue │
    │   varchar   │   int128    │    double     │
    ├─────────────┼─────────────┼───────────────┤
    │ Electronics │          14 │       1357.22 │
    │ Office      │          21 │         531.5 │
    └─────────────┴─────────────┴───────────────┘
    ```

    **Interpretation:** Both queries filter twice, at different stages. The first keeps completed orders (WHERE, before grouping), totals them per customer, then keeps only customers whose *total* clears $500 (HAVING, after) — five of the eight customers survive, with C102 just inside the cut at 634.5. The second keeps categories that moved more than 10 units: Electronics (14 units, 1357.22) and Office (21 units, 531.5). Furniture and Accessories are dropped by HAVING — not because their rows were filtered, but because their group totals fell short.

    *Source: `computations/module13_examples.py` — `demo_having()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "WHERE and HAVING are interchangeable." | WHERE filters rows before grouping; HAVING filters groups after aggregation. A condition on `SUM(total)` can only live in HAVING — the sum does not exist yet when WHERE runs. |
| "`COUNT(*)` and `COUNT(col)` always agree." | They agree only when `col` has no NULLs. After a LEFT JOIN, unmatched rows carry NULLs, and only `COUNT(col)` reports them as zero — the joins section demonstrates this. |
| "Any column can appear in the SELECT of a grouped query." | Every selected column must be in GROUP BY or inside an aggregate. SQL refuses bare columns because a group holds many values for them. |
| "`HAVING total_spent > 500` works in every database." | Referencing a SELECT alias in HAVING is a DuckDB (and a few others') convenience. The portable form repeats the aggregate: `HAVING SUM(total) > 500`. |

---

## 13.4 Combining Tables: JOINs and Subqueries

Real databases split data across multiple tables — this module's orders, customers, and line items — and **JOINs** reconnect them by matching key values:

| Join type | Returns |
|-----------|---------|
| `INNER JOIN` | Only matching rows from both tables |
| `LEFT JOIN` | All rows from the left table, matches from the right |
| `FULL OUTER JOIN` | All rows from both tables |

```sql
SELECT o.order_id, c.name, o.total
FROM orders AS o
JOIN customers AS c ON o.customer_id = c.customer_id
```

The aliases `o` and `c` are shorthand for the table names, and the `ON` clause states which columns must match. (A bare `JOIN` means `INNER JOIN`.)

### INNER JOIN — Matching Rows Only

!!! example "Worked Example: INNER JOIN — Orders with Customer Details"

    ```python
    result = duckdb.sql("""
        SELECT
            o.order_id,
            c.name AS customer_name,
            c.city,
            o.order_date,
            o.total
        FROM 'm13_orders.csv' AS o
        INNER JOIN 'm13_customers.csv' AS c
            ON o.customer_id = c.customer_id
        WHERE o.status = 'Completed'
        ORDER BY o.total DESC
        LIMIT 10
    """)
    print("Top 10 orders with customer details:")
    print(result)
    ```

    **Output:**

    ```
    Top 10 orders with customer details:
    ┌──────────┬───────────────┬───────────────┬────────────┬────────┐
    │ order_id │ customer_name │     city      │ order_date │ total  │
    │ varchar  │    varchar    │    varchar    │    date    │ double │
    ├──────────┼───────────────┼───────────────┼────────────┼────────┤
    │ ORD-012  │ David Kim     │ San Francisco │ 2025-03-25 │ 2100.0 │
    │ ORD-019  │ Irene Davis   │ Los Angeles   │ 2025-05-18 │ 1425.0 │
    │ ORD-005  │ David Kim     │ San Francisco │ 2025-02-10 │ 1250.0 │
    │ ORD-016  │ Carol Johnson │ Portland      │ 2025-04-22 │  890.0 │
    │ ORD-008  │ Carol Johnson │ Portland      │ 2025-03-01 │  678.3 │
    │ ORD-018  │ Alice Chen    │ Portland      │ 2025-05-10 │  560.0 │
    │ ORD-003  │ Carol Johnson │ Portland      │ 2025-01-22 │ 512.75 │
    │ ORD-013  │ Bob Martinez  │ Seattle       │ 2025-04-02 │  445.5 │
    │ ORD-010  │ Alice Chen    │ Portland      │ 2025-03-12 │  420.0 │
    │ ORD-015  │ Eve Wilson    │ Seattle       │ 2025-04-15 │ 310.25 │
    └──────────┴───────────────┴───────────────┴────────────┴────────┘
      10 rows                                              5 columns
    ```

    **Interpretation:** The orders file knows only `customer_id`; the join replaces that code with a human answer — David Kim of San Francisco placed the largest order, ORD-012 at 2100.0. Customers with several big orders repeat once per order (Carol Johnson appears three times in the top ten), because a join matches row to row. INNER JOIN keeps only matches, which loses nothing here: every order has a valid customer.

    *Source: `computations/module13_examples.py` — `demo_inner_join()`*

### LEFT JOIN — Keep Everything on the Left

An INNER JOIN silently drops left-table rows with no match. When the report must show *every* customer — including the ones who have never completed an order — you need a LEFT JOIN.

!!! example "Worked Example: LEFT JOIN — Every Customer, Even Without Orders"

    ```python
    # COUNT(o.order_id) is deliberate: a customer with no completed orders
    # still appears (that is the point of LEFT JOIN), but their order columns
    # come back NULL. COUNT(o.order_id) skips those NULLs and reports 0 —
    # COUNT(*) would count the NULL-padded row and wrongly report 1.
    result = duckdb.sql("""
        SELECT
            c.customer_id,
            c.name,
            c.city,
            COUNT(o.order_id) AS order_count,
            COALESCE(SUM(o.total), 0) AS total_spent
        FROM 'm13_customers.csv' AS c
        LEFT JOIN 'm13_orders.csv' AS o
            ON c.customer_id = o.customer_id
            AND o.status = 'Completed'
        GROUP BY c.customer_id, c.name, c.city
        ORDER BY total_spent DESC
    """)
    print("All customers with order totals (LEFT JOIN):")
    print(result)
    ```

    **Output:**

    ```
    All customers with order totals (LEFT JOIN):
    ┌─────────────┬───────────────┬───────────────┬─────────────┬─────────────┐
    │ customer_id │     name      │     city      │ order_count │ total_spent │
    │   varchar   │    varchar    │    varchar    │    int64    │   double    │
    ├─────────────┼───────────────┼───────────────┼─────────────┼─────────────┤
    │ C104        │ David Kim     │ San Francisco │           2 │      3350.0 │
    │ C103        │ Carol Johnson │ Portland      │           3 │     2081.05 │
    │ C109        │ Irene Davis   │ Los Angeles   │           1 │      1425.0 │
    │ C101        │ Alice Chen    │ Portland      │           4 │     1303.75 │
    │ C102        │ Bob Martinez  │ Seattle       │           2 │       634.5 │
    │ C105        │ Eve Wilson    │ Seattle       │           2 │      402.75 │
    │ C106        │ Frank Brown   │ Los Angeles   │           2 │       331.5 │
    │ C107        │ Grace Lee     │ Portland      │           2 │      323.75 │
    │ C108        │ Henry Patel   │ San Francisco │           0 │         0.0 │
    └─────────────┴───────────────┴───────────────┴─────────────┴─────────────┘
    ```

    **Interpretation:** All nine customers appear — including Henry Patel with `order_count` 0 and `total_spent` 0.0, whose only order was cancelled. An INNER JOIN would have erased him from the report entirely, hiding exactly the dormant customer a marketing team most wants to see. Two NULL-handling details make his zeros correct: `COUNT(o.order_id)` skips the NULL padding (where `COUNT(*)` would report 1 for his NULL-padded row), and `COALESCE` turns his NULL sum into 0. Note also that the status filter sits inside the `ON` clause — putting it in WHERE would discard the NULL-padded row and quietly turn the LEFT JOIN back into an INNER JOIN.

    *Source: `computations/module13_examples.py` — `demo_left_join()`*

### Joining Three Tables

Joins chain: each additional `JOIN ... ON ...` bolts one more table onto the result. Connecting line items to orders to customers answers questions none of the tables can answer alone.

!!! example "Worked Example: Joining Three Tables"

    ```python
    result = duckdb.sql("""
        SELECT
            c.name AS customer_name,
            o.order_id,
            i.product,
            i.category,
            i.quantity,
            i.unit_price,
            i.quantity * i.unit_price AS line_total
        FROM 'm13_orders.csv' AS o
        INNER JOIN 'm13_customers.csv' AS c
            ON o.customer_id = c.customer_id
        INNER JOIN 'm13_order_items.csv' AS i
            ON o.order_id = i.order_id
        WHERE o.status = 'Completed'
        ORDER BY line_total DESC, o.order_id
        LIMIT 10
    """)
    print("Top 10 line items with customer names:")
    print(result)
    ```

    **Output:**

    ```
    Top 10 line items with customer names:
    ┌───────────────┬──────────┬───────────────┬─────────────┬──────────┬────────────┬────────────┐
    │ customer_name │ order_id │    product    │  category   │ quantity │ unit_price │ line_total │
    │    varchar    │ varchar  │    varchar    │   varchar   │  int64   │   double   │   double   │
    ├───────────────┼──────────┼───────────────┼─────────────┼──────────┼────────────┼────────────┤
    │ David Kim     │ ORD-005  │ Standing Desk │ Furniture   │        1 │      899.0 │      899.0 │
    │ Carol Johnson │ ORD-003  │ Keyboard      │ Electronics │        1 │      219.5 │      219.5 │
    │ Alice Chen    │ ORD-010  │ Keyboard      │ Electronics │        1 │      219.5 │      219.5 │
    │ Carol Johnson │ ORD-003  │ Monitor Stand │ Electronics │        1 │     189.75 │     189.75 │
    │ David Kim     │ ORD-005  │ Monitor Arm   │ Furniture   │        1 │      175.0 │      175.0 │
    │ Carol Johnson │ ORD-008  │ Webcam        │ Electronics │        1 │      149.0 │      149.0 │
    │ Carol Johnson │ ORD-008  │ USB Hub       │ Electronics │        2 │       45.5 │       91.0 │
    │ Bob Martinez  │ ORD-002  │ Desk Lamp     │ Office      │        1 │       89.0 │       89.0 │
    │ Carol Johnson │ ORD-008  │ Desk Lamp     │ Office      │        1 │       89.0 │       89.0 │
    │ Carol Johnson │ ORD-008  │ Ring Light    │ Electronics │        1 │       85.0 │       85.0 │
    └───────────────┴──────────┴───────────────┴─────────────┴──────────┴────────────┴────────────┘
      10 rows                                                                           7 columns
    ```

    **Interpretation:** Each output row now draws on all three tables at once: a customer name, that customer's order, and one product line within it — David Kim's Standing Desk at 899.0 is the single largest line item. Notice the *ties*: two Keyboard lines at 219.5 and two Desk Lamp lines at 89.0. The teaching notebook sorted by `line_total` alone, which leaves the order of tied rows to chance; the query here adds `o.order_id` as a tiebreaker so the result is stable — a good habit whenever a sort key can repeat.

    *Source: `computations/module13_examples.py` — `demo_three_table_join()`*

### Conditional Aggregation Across a Join

`SUM(CASE WHEN ... THEN 1 ELSE 0 END)` is a widely used reporting idiom: it *counts the rows that satisfy a condition* inside an ordinary GROUP BY, letting one query mix overall totals with conditional counts.

!!! example "Worked Example: Conditional Aggregation Across a Join"

    ```python
    result = duckdb.sql("""
        SELECT
            c.state,
            COUNT(*) AS orders,
            ROUND(SUM(o.total), 2) AS revenue,
            ROUND(AVG(o.total), 2) AS avg_order,
            SUM(CASE WHEN o.total >= 500 THEN 1 ELSE 0 END) AS large_orders
        FROM 'm13_orders.csv' AS o
        JOIN 'm13_customers.csv' AS c
            ON o.customer_id = c.customer_id
        WHERE o.status = 'Completed'
        GROUP BY c.state
        ORDER BY revenue DESC
    """)
    print("State summary with large-order count:")
    print(result)
    ```

    **Output:**

    ```
    State summary with large-order count:
    ┌─────────┬────────┬─────────┬───────────┬──────────────┐
    │  state  │ orders │ revenue │ avg_order │ large_orders │
    │ varchar │ int64  │ double  │  double   │    int128    │
    ├─────────┼────────┼─────────┼───────────┼──────────────┤
    │ CA      │      5 │  5106.5 │    1021.3 │            3 │
    │ OR      │      9 │ 3708.55 │    412.06 │            4 │
    │ WA      │      4 │ 1037.25 │    259.31 │            0 │
    └─────────┴────────┴─────────┴───────────┴──────────────┘
    ```

    **Interpretation:** The join supplies the grouping column (`state` lives in the customers table, not in orders), and the CASE expression counts big-ticket orders inline. The result reads like an executive brief: California produces the most revenue (5106.5) from only 5 orders because its orders are large — average 1021.3, with 3 crossing the five-hundred-dollar line — while Oregon's 9 orders average just 412.06, and Washington logged 0 large orders. One query, three analytical layers: join, group, conditional count.

    *Source: `computations/module13_examples.py` — `demo_state_summary()`*

!!! question "Try It Yourself: Revenue by City"

    Write a query that joins orders and customers, then groups by `city` to
    find the total revenue per city. Sort by revenue descending. Which city
    generates the most revenue?

### Subqueries — Queries Inside Queries

A subquery is a SELECT nested inside another SELECT. Two patterns cover most business uses:

**Scalar subquery** — returns a single value for comparison:

```sql
SELECT * FROM orders
WHERE total > (SELECT AVG(total) FROM orders)
```

**IN subquery** — returns a list for membership filtering:

```sql
SELECT * FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders WHERE total > 1000)
```

The inner query runs first; its result plugs into the outer query's condition. This is what makes the filter *dynamic* — "above average" recomputes itself as the data changes, with no hard-coded threshold to maintain.

!!! example "Worked Example: Scalar and IN Subqueries"

    ```python
    result = duckdb.sql("""
        SELECT
            order_id,
            customer_id,
            total,
            (SELECT ROUND(AVG(total), 2) FROM 'm13_orders.csv'
             WHERE status = 'Completed') AS avg_total
        FROM 'm13_orders.csv'
        WHERE status = 'Completed'
          AND total > (SELECT AVG(total) FROM 'm13_orders.csv'
                       WHERE status = 'Completed')
        ORDER BY total DESC
    """)
    print("Orders above the average order value:")
    print(result)

    result = duckdb.sql("""
        SELECT customer_id, name, city, state
        FROM 'm13_customers.csv'
        WHERE customer_id IN (
            SELECT DISTINCT customer_id
            FROM 'm13_orders.csv'
            WHERE total > 500
              AND status = 'Completed'
        )
        ORDER BY customer_id
    """)
    print("Customers with at least one order over $500:")
    print(result)
    ```

    **Output:**

    ```
    Orders above the average order value:
    ┌──────────┬─────────────┬────────┬───────────┐
    │ order_id │ customer_id │ total  │ avg_total │
    │ varchar  │   varchar   │ double │  double   │
    ├──────────┼─────────────┼────────┼───────────┤
    │ ORD-012  │ C104        │ 2100.0 │    547.35 │
    │ ORD-019  │ C109        │ 1425.0 │    547.35 │
    │ ORD-005  │ C104        │ 1250.0 │    547.35 │
    │ ORD-016  │ C103        │  890.0 │    547.35 │
    │ ORD-008  │ C103        │  678.3 │    547.35 │
    │ ORD-018  │ C101        │  560.0 │    547.35 │
    └──────────┴─────────────┴────────┴───────────┘

    Customers with at least one order over $500:
    ┌─────────────┬───────────────┬───────────────┬─────────┐
    │ customer_id │     name      │     city      │  state  │
    │   varchar   │    varchar    │    varchar    │ varchar │
    ├─────────────┼───────────────┼───────────────┼─────────┤
    │ C101        │ Alice Chen    │ Portland      │ OR      │
    │ C103        │ Carol Johnson │ Portland      │ OR      │
    │ C104        │ David Kim     │ San Francisco │ CA      │
    │ C109        │ Irene Davis   │ Los Angeles   │ CA      │
    └─────────────┴───────────────┴───────────────┴─────────┘
    ```

    **Interpretation:** The first query uses the scalar subquery twice — once as the filter bar and once as a display column, so every row shows the 547.35 average it cleared; six orders beat it, led by ORD-012 at 2100.0. The second query answers a question that spans two tables *without* a join: the inner query builds the list of qualifying customer IDs from orders, and the outer query keeps only customers on that list — four of them, notably including Alice Chen, whose many smaller orders hid the fact that one crossed the $500 line.

    *Source: `computations/module13_examples.py` — `demo_subqueries()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "A JOIN stacks one table's rows under the other's." | A join adds *columns* by matching key values row to row. Stacking rows is concatenation — a different operation. |
| "A LEFT JOIN drops customers with no orders." | It is the *inner* join that drops non-matching rows. LEFT JOIN keeps every left-table row and pads the missing right-side columns with NULL. |
| "After a LEFT JOIN, `COUNT(*)` counts each customer's orders." | `COUNT(*)` counts rows — including the NULL-padded row of a customer with no orders, reporting one instead of zero. Count the join key (`COUNT(o.order_id)`) so NULLs are skipped. |
| "Extra filters behave the same in `ON` and in `WHERE`." | For a LEFT JOIN they do not: a right-table condition in `WHERE` discards the NULL-padded rows, silently converting the query to an inner join. Put right-table conditions in the `ON` clause to keep unmatched left rows. |
| "Subqueries are just a slower way to write joins." | They answer a different shape of question — comparing rows against a computed value ("above average") or a membership list. Many subqueries have join rewrites, but the nested form often states the business question more directly. |

---

## 13.5 DuckDB + Polars: The Integrated Workflow

This section is where the module's two tools become one workflow. DuckDB can query Polars DataFrames as if they were tables, and every DuckDB result converts back to Polars — so you can do the heavy relational lifting (joins, grouping) in SQL and the presentation work (further transformation, charting) in Python.

### Querying Polars DataFrames by Name

Reference a Polars DataFrame's *variable name* inside a SQL query and DuckDB finds it automatically. This is **zero-copy integration**: DuckDB reads the DataFrame's memory directly (both tools build on Apache Arrow's format) without making a copy, so it is fast even for large data.

> **Marimo note:** The DataFrame name lives *inside a SQL string*, so marimo cannot see it when it builds its reactive dependency graph. Unlike normal Python cells, these SQL cells will **not** re-run automatically when the `orders` data changes — you have to re-run them yourself. (Querying a CSV file by path has the same limitation.)

!!! example "Worked Example: Querying Polars DataFrames by Name"

    ```python
    orders = pl.read_csv("m13_orders.csv")
    customers = pl.read_csv("m13_customers.csv")

    result = duckdb.sql("""
        SELECT
            customer_id,
            COUNT(*) AS order_count,
            ROUND(SUM(total), 2) AS total_spent
        FROM orders
        WHERE status = 'Completed'
        GROUP BY customer_id
        ORDER BY total_spent DESC
    """)
    print("Querying the Polars 'orders' DataFrame with SQL:")
    print(result)

    result = duckdb.sql("""
        SELECT
            c.name,
            c.city,
            COUNT(*) AS orders,
            ROUND(SUM(o.total), 2) AS revenue
        FROM orders AS o
        JOIN customers AS c ON o.customer_id = c.customer_id
        WHERE o.status = 'Completed'
        GROUP BY c.name, c.city
        ORDER BY revenue DESC
    """)
    print("Joining Polars DataFrames with SQL:")
    print(result)
    ```

    **Output:**

    ```
    Querying the Polars 'orders' DataFrame with SQL:
    ┌─────────────┬─────────────┬─────────────┐
    │ customer_id │ order_count │ total_spent │
    │   varchar   │    int64    │   double    │
    ├─────────────┼─────────────┼─────────────┤
    │ C104        │           2 │      3350.0 │
    │ C103        │           3 │     2081.05 │
    │ C109        │           1 │      1425.0 │
    │ C101        │           4 │     1303.75 │
    │ C102        │           2 │       634.5 │
    │ C105        │           2 │      402.75 │
    │ C106        │           2 │       331.5 │
    │ C107        │           2 │      323.75 │
    └─────────────┴─────────────┴─────────────┘

    Joining Polars DataFrames with SQL:
    ┌───────────────┬───────────────┬────────┬─────────┐
    │     name      │     city      │ orders │ revenue │
    │    varchar    │    varchar    │ int64  │ double  │
    ├───────────────┼───────────────┼────────┼─────────┤
    │ David Kim     │ San Francisco │      2 │  3350.0 │
    │ Carol Johnson │ Portland      │      3 │ 2081.05 │
    │ Irene Davis   │ Los Angeles   │      1 │  1425.0 │
    │ Alice Chen    │ Portland      │      4 │ 1303.75 │
    │ Bob Martinez  │ Seattle       │      2 │   634.5 │
    │ Eve Wilson    │ Seattle       │      2 │  402.75 │
    │ Frank Brown   │ Los Angeles   │      2 │   331.5 │
    │ Grace Lee     │ Portland      │      2 │  323.75 │
    └───────────────┴───────────────┴────────┴─────────┘
    ```

    **Interpretation:** No file paths anywhere in the SQL — `FROM orders` and `JOIN customers` refer to the Python variables directly, and the totals (C104 at 3350.0, with David Kim leading the joined view at the same 3350.0) match the file-based queries from the grouping section exactly. In practice this means data already loaded and cleaned with Polars never needs to be written out just so SQL can reach it.

    *Source: `computations/module13_examples.py` — `demo_query_polars_dfs()`*

### DuckDB Results Back to Polars

The reverse direction is one method call: `.pl()`. Use SQL for the relational heavy lifting, then hand the result to Polars for further transformation or to a plotting library.

!!! example "Worked Example: From DuckDB Result to Polars DataFrame"

    ```python
    customer_summary = duckdb.sql("""
        SELECT
            c.name,
            c.city,
            c.state,
            COUNT(*) AS order_count,
            ROUND(SUM(o.total), 2) AS total_spent,
            ROUND(AVG(o.total), 2) AS avg_order
        FROM orders AS o
        JOIN customers AS c ON o.customer_id = c.customer_id
        WHERE o.status = 'Completed'
        GROUP BY c.name, c.city, c.state
        ORDER BY total_spent DESC
    """).pl()

    print("DuckDB result as Polars DataFrame:")
    print(f"Shape: {customer_summary.shape}")
    print(customer_summary)
    ```

    **Output:**

    ```
    DuckDB result as Polars DataFrame:
    Shape: (8, 6)
    shape: (8, 6)
    ┌───────────────┬───────────────┬───────┬─────────────┬─────────────┬───────────┐
    │ name          ┆ city          ┆ state ┆ order_count ┆ total_spent ┆ avg_order │
    │ ---           ┆ ---           ┆ ---   ┆ ---         ┆ ---         ┆ ---       │
    │ str           ┆ str           ┆ str   ┆ i64         ┆ f64         ┆ f64       │
    ╞═══════════════╪═══════════════╪═══════╪═════════════╪═════════════╪═══════════╡
    │ David Kim     ┆ San Francisco ┆ CA    ┆ 2           ┆ 3350.0      ┆ 1675.0    │
    │ Carol Johnson ┆ Portland      ┆ OR    ┆ 3           ┆ 2081.05     ┆ 693.68    │
    │ Irene Davis   ┆ Los Angeles   ┆ CA    ┆ 1           ┆ 1425.0      ┆ 1425.0    │
    │ Alice Chen    ┆ Portland      ┆ OR    ┆ 4           ┆ 1303.75     ┆ 325.94    │
    │ Bob Martinez  ┆ Seattle       ┆ WA    ┆ 2           ┆ 634.5       ┆ 317.25    │
    │ Eve Wilson    ┆ Seattle       ┆ WA    ┆ 2           ┆ 402.75      ┆ 201.38    │
    │ Frank Brown   ┆ Los Angeles   ┆ CA    ┆ 2           ┆ 331.5       ┆ 165.75    │
    │ Grace Lee     ┆ Portland      ┆ OR    ┆ 2           ┆ 323.75      ┆ 161.88    │
    └───────────────┴───────────────┴───────┴─────────────┴─────────────┴───────────┘
    ```

    **Interpretation:** The Polars-style frame (`shape: (8, 6)`, dtype row of `str`/`i64`/`f64`, `┆` separators) confirms this is now an ordinary DataFrame — every Polars method from the earlier modules applies, and it can feed a chart directly. Because the SQL wrapped its averages in `ROUND()`, `avg_order` arrives presentation-ready (693.68 for Carol Johnson) instead of trailing a dozen decimal places.

    *Source: `computations/module13_examples.py` — `demo_sql_to_polars()`*

!!! question "Try It Yourself: Top Products via SQL"

    Use DuckDB to query the `order_items` Polars DataFrame (not the CSV file)
    with SQL. Find the top 5 products by total revenue (`quantity * unit_price`).
    Convert the result to a Polars DataFrame with `.pl()`.

### Creating In-Memory Tables

Querying files re-reads them on every query. When you will hit the same data repeatedly, create proper tables inside DuckDB once and query those. `duckdb.connect()` opens a private in-memory database whose tables persist for your Python session; the teaching notebook used the shared default database (plain `duckdb.sql()`), which works the same way — a dedicated connection simply keeps this example self-contained.

!!! example "Worked Example: In-Memory Tables"

    ```python
    con = duckdb.connect()  # a private in-memory database

    con.sql("CREATE TABLE orders_tbl AS SELECT * FROM 'm13_orders.csv'")
    con.sql("CREATE TABLE customers_tbl AS SELECT * FROM 'm13_customers.csv'")
    con.sql("CREATE TABLE items_tbl AS SELECT * FROM 'm13_order_items.csv'")

    print("Tables created. Let's verify:")
    print(con.sql("SHOW TABLES"))

    result = con.sql("""
        SELECT
            c.state,
            COUNT(DISTINCT o.order_id) AS order_count,
            ROUND(SUM(o.total), 2) AS revenue
        FROM orders_tbl o
        JOIN customers_tbl c ON o.customer_id = c.customer_id
        WHERE o.status = 'Completed'
        GROUP BY c.state
        ORDER BY revenue DESC
    """)
    print("Revenue by state (from in-memory tables):")
    print(result)
    ```

    **Output:**

    ```
    Tables created. Let's verify:
    ┌───────────────┐
    │     name      │
    │    varchar    │
    ├───────────────┤
    │ customers_tbl │
    │ items_tbl     │
    │ orders_tbl    │
    └───────────────┘

    Revenue by state (from in-memory tables):
    ┌─────────┬─────────────┬─────────┐
    │  state  │ order_count │ revenue │
    │ varchar │    int64    │ double  │
    ├─────────┼─────────────┼─────────┤
    │ CA      │           5 │  5106.5 │
    │ OR      │           9 │ 3708.55 │
    │ WA      │           4 │ 1037.25 │
    └─────────┴─────────────┴─────────┘
    ```

    **Interpretation:** `CREATE TABLE ... AS SELECT` copies each CSV into the database once; `SHOW TABLES` confirms the three tables exist; and the state query then runs against tables, not files — same answers as the conditional-aggregation example (California leads at 5106.5), but repeated queries no longer pay the file-parsing cost. In-memory tables vanish when the Python session ends; passing a filename to `duckdb.connect()` instead would persist them to disk.

    *Source: `computations/module13_examples.py` — `demo_in_memory_tables()`*

### When to Use Which Tool

| Criterion | DuckDB (SQL) | Polars (Python) |
|-----------|-------------|----------------|
| **Syntax** | SQL — familiar to database users | Method chaining — Pythonic |
| **Multi-table joins** | Natural — SQL was designed for joins | Works but more verbose |
| **File querying** | Query CSV/Parquet directly | Must load first with `read_csv()` |
| **Window functions** | Full SQL window function support | Available via `over()` |
| **Visualization** | Export to Polars/pandas first | Direct `.to_pandas()` handoff |
| **Best for** | Ad-hoc exploration, complex joins | Transformation pipelines, visualization |

**Rule of thumb:** use DuckDB when the task is naturally a SQL query (especially multi-table joins and ad-hoc exploration); use Polars when you need a transformation pipeline or the result feeds a chart. The capstone below deliberately uses both.

### Capstone: A Business Intelligence Report

The module closes the way a real analysis would: a business question, several SQL queries, Polars DataFrames, and (in the notebook) Plotly Express charts. **Business question:** *Who are our best customers, what do they buy, and where is our revenue concentrated?*

!!! example "Worked Example: The Business Intelligence Report"

    ```python
    customer_ltv = duckdb.sql("""
        SELECT
            c.name,
            c.state,
            COUNT(DISTINCT o.order_id) AS total_orders,
            ROUND(SUM(o.total), 2) AS lifetime_value,
            ROUND(AVG(o.total), 2) AS avg_order,
            MIN(o.order_date) AS first_order,
            MAX(o.order_date) AS last_order
        FROM 'm13_orders.csv' AS o
        INNER JOIN 'm13_customers.csv' AS c
            ON o.customer_id = c.customer_id
        WHERE o.status = 'Completed'
        GROUP BY c.name, c.state
        ORDER BY lifetime_value DESC
    """).pl()
    print("Customer Lifetime Value Report:")
    print(customer_ltv)

    category_perf = duckdb.sql("""
        SELECT
            i.category,
            COUNT(DISTINCT i.order_id) AS orders_containing,
            SUM(i.quantity) AS units_sold,
            ROUND(SUM(i.quantity * i.unit_price), 2) AS revenue,
            ROUND(AVG(i.unit_price), 2) AS avg_unit_price,
            COUNT(DISTINCT i.product) AS unique_products
        FROM 'm13_order_items.csv' AS i
        INNER JOIN 'm13_orders.csv' AS o
            ON i.order_id = o.order_id
        WHERE o.status = 'Completed'
        GROUP BY i.category
        ORDER BY revenue DESC
    """).pl()
    print("\nCategory Performance:")
    print(category_perf)

    monthly_trend = duckdb.sql("""
        SELECT
            strftime(order_date::DATE, '%Y-%m') AS month,
            COUNT(*) AS orders,
            ROUND(SUM(total), 2) AS revenue,
            COUNT(DISTINCT customer_id) AS active_customers
        FROM 'm13_orders.csv'
        WHERE status = 'Completed'
        GROUP BY month
        ORDER BY month
    """).pl()
    print("\nMonthly Trend:")
    print(monthly_trend)

    print(
        f"\nSummary: {customer_ltv.shape[0]} customers, "
        f"${customer_ltv['lifetime_value'].sum():,.2f} total revenue, "
        f"{category_perf['unique_products'].sum()} unique products"
    )
    ```

    **Output:**

    ```
    Customer Lifetime Value Report:
    shape: (8, 7)
    ┌───────────────┬───────┬──────────────┬────────────────┬───────────┬─────────────┬────────────┐
    │ name          ┆ state ┆ total_orders ┆ lifetime_value ┆ avg_order ┆ first_order ┆ last_order │
    │ ---           ┆ ---   ┆ ---          ┆ ---            ┆ ---       ┆ ---         ┆ ---        │
    │ str           ┆ str   ┆ i64          ┆ f64            ┆ f64       ┆ date        ┆ date       │
    ╞═══════════════╪═══════╪══════════════╪════════════════╪═══════════╪═════════════╪════════════╡
    │ David Kim     ┆ CA    ┆ 2            ┆ 3350.0         ┆ 1675.0    ┆ 2025-02-10  ┆ 2025-03-25 │
    │ Carol Johnson ┆ OR    ┆ 3            ┆ 2081.05        ┆ 693.68    ┆ 2025-01-22  ┆ 2025-04-22 │
    │ Irene Davis   ┆ CA    ┆ 1            ┆ 1425.0         ┆ 1425.0    ┆ 2025-05-18  ┆ 2025-05-18 │
    │ Alice Chen    ┆ OR    ┆ 4            ┆ 1303.75        ┆ 325.94    ┆ 2025-01-15  ┆ 2025-05-10 │
    │ Bob Martinez  ┆ WA    ┆ 2            ┆ 634.5          ┆ 317.25    ┆ 2025-01-18  ┆ 2025-04-02 │
    │ Eve Wilson    ┆ WA    ┆ 2            ┆ 402.75         ┆ 201.38    ┆ 2025-02-20  ┆ 2025-04-15 │
    │ Frank Brown   ┆ CA    ┆ 2            ┆ 331.5          ┆ 165.75    ┆ 2025-03-05  ┆ 2025-05-01 │
    │ Grace Lee     ┆ OR    ┆ 2            ┆ 323.75         ┆ 161.88    ┆ 2025-03-18  ┆ 2025-05-25 │
    └───────────────┴───────┴──────────────┴────────────────┴───────────┴─────────────┴────────────┘

    Category Performance:
    shape: (4, 6)
    ┌─────────────┬───────────────────┬───────────────┬─────────┬────────────────┬─────────────────┐
    │ category    ┆ orders_containing ┆ units_sold    ┆ revenue ┆ avg_unit_price ┆ unique_products │
    │ ---         ┆ ---               ┆ ---           ┆ ---     ┆ ---            ┆ ---             │
    │ str         ┆ i64               ┆ decimal[38,0] ┆ f64     ┆ f64            ┆ i64             │
    ╞═════════════╪═══════════════════╪═══════════════╪═════════╪════════════════╪═════════════════╡
    │ Electronics ┆ 4                 ┆ 13            ┆ 1158.22 ┆ 104.82         ┆ 7               │
    │ Furniture   ┆ 1                 ┆ 3             ┆ 1139.0  ┆ 379.67         ┆ 3               │
    │ Office      ┆ 5                 ┆ 21            ┆ 531.5   ┆ 31.11          ┆ 4               │
    │ Accessories ┆ 4                 ┆ 7             ┆ 135.0   ┆ 22.5           ┆ 2               │
    └─────────────┴───────────────────┴───────────────┴─────────┴────────────────┴─────────────────┘

    Monthly Trend:
    shape: (5, 4)
    ┌─────────┬────────┬─────────┬──────────────────┐
    │ month   ┆ orders ┆ revenue ┆ active_customers │
    │ ---     ┆ ---    ┆ ---     ┆ ---              │
    │ str     ┆ i64    ┆ f64     ┆ i64              │
    ╞═════════╪════════╪═════════╪══════════════════╡
    │ 2025-01 ┆ 3      ┆ 947.25  ┆ 3                │
    │ 2025-02 ┆ 3      ┆ 1420.75 ┆ 3                │
    │ 2025-03 ┆ 5      ┆ 3443.05 ┆ 5                │
    │ 2025-04 ┆ 3      ┆ 1645.75 ┆ 3                │
    │ 2025-05 ┆ 4      ┆ 2395.5  ┆ 4                │
    └─────────┴────────┴─────────┴──────────────────┘

    Summary: 8 customers, $9,852.30 total revenue, 16 unique products
    ```

    **Interpretation:** Three queries answer the business question from three angles. *Who are our best customers?* David Kim — lifetime value 3350.0 — with Carol Johnson (2081.05) the steadier repeat buyer; the MIN/MAX date columns show each relationship's span. *What do they buy?* Electronics leads (1158.22 across 7 unique products) but Furniture nearly matches it (1139.0) from a single order of 3 big-ticket units — these figures sit below the raw category totals in the aggregation section because the join's status filter now excludes the cancelled order's items. *Where is revenue concentrated?* The monthly trend peaks in `2025-03` (3443.05, 5 active customers). The closing summary line — 8 customers, $9,852.30, 16 unique products — matches the whole-table aggregate demo, a quick cross-check that the report is internally consistent. (The teaching notebook's version of the first query also carries the customer's city; it is trimmed here so the printed table fits the page.)

    *Source: `computations/module13_examples.py` — `demo_capstone_report()`*

Because each query ended in `.pl()`, the results are Polars DataFrames — exactly what Plotly Express (Module 11) wants. The notebook completes the dashboard like this:

```python
import plotly.express as px

ltv_fig = px.bar(
    customer_ltv.to_pandas(),
    x="name",
    y="lifetime_value",
    color="state",
    title="Customer Lifetime Value",
    labels={"lifetime_value": "Lifetime Value ($)", "name": "Customer"},
)

trend_fig = px.line(
    monthly_trend.to_pandas(),
    x="month",
    y="revenue",
    markers=True,
    title="Monthly Revenue Trend",
    labels={"revenue": "Revenue ($)", "month": "Month"},
)
```

That is the full modern-analyst pipeline in miniature: **SQL for querying → Polars for data → Plotly for charts.**

!!! question "Try It Yourself: Capstone Challenge"

    Write a SQL query that answers this question: **Which customers ordered
    Electronics products, and how much did they spend on Electronics
    specifically?**

    You will need to join all three tables (orders, customers, order_items)
    and filter by `category = 'Electronics'`. Group by customer name and sort
    by total Electronics spending descending.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "`FROM orders` in the SQL copies the DataFrame into DuckDB." | It is zero-copy: DuckDB reads the Polars DataFrame's Arrow memory in place. No duplicate of the data is made. |
| "Marimo will re-run my SQL cell when the DataFrame changes." | Marimo builds its dependency graph from Python variable names — and a name inside a SQL *string* is invisible to it. Re-run SQL-string cells yourself after changing the data. |
| "In-memory tables are saved when my session ends." | An in-memory database disappears at session end. Persist by connecting to a file (`duckdb.connect("mydata.db")`) or by exporting results. |
| "I should always create tables first." | For one-off questions, querying the file (or DataFrame) directly is simpler and just as correct. Tables pay off when the same data is queried repeatedly. |

---

## Reflection Questions

1. Take any GROUP BY report from this module and sketch how you would produce the same result with Polars `group_by().agg()`. Which version reads more naturally to you, and what does that suggest about when you will reach for each tool at work?
2. Explain the difference between `WHERE` and `HAVING` to a colleague who knows Excel but not SQL. Why *must* a condition like "customers whose total spending exceeds $500" go in HAVING?
3. A dashboard titled "Revenue by Customer" is built with an INNER JOIN between customers and orders. Which customers silently vanish from that dashboard, why might those be exactly the customers management needs to see, and what two changes (the join type and the counting function) fix the report?
4. DuckDB's `.pl()` gives "zero-copy" conversion to Polars. Why is that better than writing query results to a CSV file and reading them back — beyond just speed? Consider data types and the risk of stale intermediate files.
5. When would you query a CSV file directly, and when would you `CREATE TABLE` first? Describe a work scenario for each choice.
6. The IN-subquery example found customers with at least one large order — including one whose overall total was unremarkable. Give a business situation where "has at least one qualifying transaction" and "has a large total" would lead to genuinely different decisions.

---

## Your Assignment

The Module 13 assignment is worth **100 points plus a 10-point bonus**. You complete it in a **marimo notebook (`.py` file)** and submit the file to **Blackboard**. The final reflection section is not graded separately — it counts toward participation. Setup cells create every CSV file the tasks use (under `/tmp/`) and register the multi-table datasets as DuckDB tables; do not modify those cells. Each task asks you to run SQL with `duckdb.sql()` and, where stated, convert the result to Polars with `.pl()`.

**Task 1: Basic SELECT and WHERE (10 points).** A gym's membership roster lives in a CSV file. You query the file *directly* — no loading step — selecting the name, membership-type, and monthly-fee columns, filtering to members above the fee threshold given in the task, sorting by fee descending, and converting the result with `.pl()`. Direct file querying is §13.1; SELECT, WHERE, and ORDER BY are §13.2.

**Task 2: Aggregation Functions (15 points).** A movie-theater chain's ticket sales must be summarized by genre: total tickets, a rounded average revenue, a show count, and a maximum revenue, sorted by total tickets. This is §13.3's aggregate-function toolkit applied through GROUP BY, with `ROUND()` from §13.2's function table.

**Task 3: HAVING and Calculated Columns (15 points).** Warehouse inventory is grouped by category with three computed measures — total units, an inventory value calculated as quantity times unit cost (a calculated column named with `AS`), and a product count — after which `HAVING` keeps only categories above a units threshold. Calculated columns come from §13.2; GROUP BY and HAVING from §13.3.

**Task 4: JOINs (15 points).** A school database provides `courses` and `enrollments` tables. Part A (8 points) is an INNER JOIN filtered to the top letter grades and sorted by course and student. Part B (7 points) is a LEFT JOIN that counts enrollments per course — including any course with none, which is why LEFT (not INNER) is specified. Both patterns, and the counting subtlety they involve, are §13.4.

**Task 5: Subqueries (20 points).** An airline database provides `flights` and `airports` tables. Part A (10 points) uses a *scalar* subquery to find flights priced above the average fare. Part B (10 points) uses an *IN* subquery to find flights departing from airports in a named region. Both subquery forms are demonstrated in §13.4.

**Task 6: Full Pipeline — DuckDB to Polars to Plotly (25 points).** A music-streaming platform's three tables (artists, albums, plays) must be joined, grouped by artist and genre, and summarized (total plays, distinct album count, and average plays per album), converted with `.pl()`, and then visualized as a Plotly Express bar chart colored by genre (via `.to_pandas()`). The multi-table join is §13.4; the SQL → Polars → chart pipeline is §13.5, with the charting itself resting on Module 11.

**Task 7: Creative SQL Analysis — Bonus (10 points).** Design your own analysis using the notebook's existing tables or CSVs you create. It must include at least one JOIN, at least one aggregation, at least one subquery, at least one Plotly Express chart, and a markdown cell explaining what question you are answering and what the results show — the whole module in one self-chosen scenario.

---

## Chapter Summary

DuckDB is an embedded analytical database: it lives inside your Python process, needs no server, and queries CSV files directly — `SELECT * FROM 'file.csv'` with no loading step. The core clauses map cleanly onto Polars operations you already know: SELECT chooses columns, WHERE filters rows, ORDER BY sorts (an explicit sort being the *only* guarantee of row order), and LIMIT caps output. Calculated columns with `AS` and conditional columns with `CASE WHEN` build derived measures and business categories inside the query, and a small function toolbox — `ROUND`, `COALESCE`, `CAST`, `strftime`, `LIKE`, `IN`, `BETWEEN` — handles the formatting and matching chores, including the date-versus-text casting that `LIKE` demands.

Aggregation is where SQL earns its keep in reporting. Aggregate functions (COUNT, SUM, AVG, MIN, MAX, COUNT DISTINCT) summarize whole tables in one row; GROUP BY computes them per group; HAVING filters *groups* after aggregation the way WHERE filters *rows* before it. JOINs then recombine what a relational design splits apart: INNER JOIN keeps only matches, LEFT JOIN keeps every left-table row and pads misses with NULL — which is precisely why per-group counting after a LEFT JOIN must use `COUNT(column)` rather than `COUNT(*)`, and why right-table filters belong in the ON clause. Subqueries nest one query inside another for dynamic comparisons ("above average") and membership tests (IN), and `SUM(CASE WHEN ...)` adds conditional counts to any grouped report.

Finally, DuckDB and Polars interlock: SQL can query a Polars DataFrame by its variable name (zero-copy, via their shared Arrow memory layout), and any result converts back with `.pl()`. In-memory tables (`CREATE TABLE ... AS SELECT`) speed up repeated querying. The capstone assembled all of it — joins, grouping, date rollups, `.pl()`, and Plotly Express — into a three-view business-intelligence report: the same SQL-for-querying, Polars-for-data, Plotly-for-charts pipeline you will use whenever an analysis outgrows a single table.

---

## What's Next

So far, every dataset in this course arrived as a tidy file. Module 14 removes that assumption: **Web Scraping** teaches you to acquire data from the open web, using the `requests` library to fetch pages and BeautifulSoup to parse their HTML into structured rows. The payoff loops straight back to this module — once scraped data lands in a DataFrame, everything you now know applies, and DuckDB can join your scraped tables to the rest of your data with the same SQL you wrote here.
