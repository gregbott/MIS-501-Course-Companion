# Module 10: Polars: Transformations & Aggregations

## Introduction

In Module 9 you learned to read data, select columns, filter rows, and sort — the operations that let you *explore* a dataset. This module teaches you to *transform* it: adding computed columns, summarizing groups, combining tables, and handling missing values. These are the operations that turn raw data into business insights. Nearly every managerial report you have ever read — revenue by region, average order value by customer segment, headcount by department — is the product of exactly the operations covered here: compute a column, group the rows, aggregate each group, and join in context from another table. By the end of the module you will chain these steps into a single pipeline that goes from raw order records to a finished report written to disk.

---

## Learning Objectives

By the end of this module, you should be able to:

1. **Add** and rename columns using `with_columns()` and `rename()`
2. **Cast** data types to fix incorrect column types
3. **Perform** group-by aggregations to summarize data
4. **Join** two DataFrames on shared keys
5. **Handle** null (missing) values in a DataFrame
6. **Build** multi-step transformation pipelines using method chaining

---

## 10.1 Transforming Columns: Adding, Renaming, and Casting

Every example in this module works on the same small business dataset: 12 sales orders, each with a customer, product, category, quantity, unit price, region, and order date. Small enough to check by hand, rich enough to answer real questions.

### Adding Columns with `with_columns()`

The `with_columns()` method adds new columns (or replaces existing ones) in a DataFrame. Each new column is defined as an expression built from `pl.col()`, and `.alias()` gives the result its name:

```python
df.with_columns(
    (pl.col("quantity") * pl.col("unit_price")).alias("total"),
)
```

This is Polars' equivalent of adding a formula column in a spreadsheet. One point matters more than any other: **the original DataFrame is not modified**. Polars DataFrames are immutable — `with_columns()` returns a *new* DataFrame, and if you do not assign the result to a variable, the computed column is gone.

!!! example "Worked Example: The Orders Data and a First Computed Column"

    ```python
    import polars as pl

    orders = pl.DataFrame({
        "order_id": ["ORD-001", "ORD-002", "ORD-003", "ORD-004", "ORD-005", "ORD-006",
                     "ORD-007", "ORD-008", "ORD-009", "ORD-010", "ORD-011", "ORD-012"],
        "customer": ["Acme Corp", "Bright Solutions", "CyberTech", "Acme Corp",
                     "DataFlow Inc", "Bright Solutions", "EcoGoods", "DataFlow Inc",
                     "CyberTech", "Acme Corp", "EcoGoods", "Bright Solutions"],
        "product": ["Laptop", "Monitor", "Keyboard", "Mouse", "Laptop", "Webcam",
                    "Keyboard", "Monitor", "Mouse", "Webcam", "Laptop", "Keyboard"],
        "category": ["Electronics", "Electronics", "Accessories", "Accessories",
                     "Electronics", "Electronics", "Accessories", "Electronics",
                     "Accessories", "Electronics", "Electronics", "Accessories"],
        "quantity": [3, 5, 20, 50, 2, 10, 15, 8, 30, 5, 1, 25],
        "unit_price": [999.99, 349.50, 79.95, 24.99, 999.99, 64.50,
                       79.95, 349.50, 24.99, 64.50, 999.99, 79.95],
        "region": ["West", "East", "West", "West", "Central", "East",
                   "East", "Central", "West", "West", "East", "East"],
        "order_date": ["2025-01-05", "2025-01-08", "2025-01-10", "2025-01-12",
                       "2025-01-15", "2025-01-18", "2025-01-20", "2025-01-22",
                       "2025-01-25", "2025-01-28", "2025-02-01", "2025-02-03"],
    })

    print(f"The orders dataset: {orders.shape[0]} rows x {orders.shape[1]} columns")

    orders_with_total = orders.with_columns(
        (pl.col("quantity") * pl.col("unit_price")).round(2).alias("total"),
    )

    print("\nWith the computed 'total' column:")
    print(
        orders_with_total.select(
            "order_id", "customer", "product", "quantity", "unit_price", "total"
        )
    )
    ```

    **Output:**

    ```
    The orders dataset: 12 rows x 8 columns

    With the computed 'total' column:
    shape: (12, 6)
    ┌──────────┬──────────────────┬──────────┬──────────┬────────────┬─────────┐
    │ order_id ┆ customer         ┆ product  ┆ quantity ┆ unit_price ┆ total   │
    │ ---      ┆ ---              ┆ ---      ┆ ---      ┆ ---        ┆ ---     │
    │ str      ┆ str              ┆ str      ┆ i64      ┆ f64        ┆ f64     │
    ╞══════════╪══════════════════╪══════════╪══════════╪════════════╪═════════╡
    │ ORD-001  ┆ Acme Corp        ┆ Laptop   ┆ 3        ┆ 999.99     ┆ 2999.97 │
    │ ORD-002  ┆ Bright Solutions ┆ Monitor  ┆ 5        ┆ 349.5      ┆ 1747.5  │
    │ ORD-003  ┆ CyberTech        ┆ Keyboard ┆ 20       ┆ 79.95      ┆ 1599.0  │
    │ ORD-004  ┆ Acme Corp        ┆ Mouse    ┆ 50       ┆ 24.99      ┆ 1249.5  │
    │ ORD-005  ┆ DataFlow Inc     ┆ Laptop   ┆ 2        ┆ 999.99     ┆ 1999.98 │
    │ …        ┆ …                ┆ …        ┆ …        ┆ …          ┆ …       │
    │ ORD-008  ┆ DataFlow Inc     ┆ Monitor  ┆ 8        ┆ 349.5      ┆ 2796.0  │
    │ ORD-009  ┆ CyberTech        ┆ Mouse    ┆ 30       ┆ 24.99      ┆ 749.7   │
    │ ORD-010  ┆ Acme Corp        ┆ Webcam   ┆ 5        ┆ 64.5       ┆ 322.5   │
    │ ORD-011  ┆ EcoGoods         ┆ Laptop   ┆ 1        ┆ 999.99     ┆ 999.99  │
    │ ORD-012  ┆ Bright Solutions ┆ Keyboard ┆ 25       ┆ 79.95      ┆ 1998.75 │
    └──────────┴──────────────────┴──────────┴──────────┴────────────┴─────────┘
    ```

    **Interpretation:** Each order now carries its revenue: ORD-001 is 3 laptops at $999.99, so `total` = $2,999.97. Note the `…` row — when a table is taller than ten rows, Polars prints the first five and last five rows and elides the middle; all 12 rows are still in the DataFrame. Also note the dtype row (`str`, `i64`, `f64`) under each column name — checking it becomes a habit in the casting section below.

    *Source: `computations/module10_examples.py` — `demo_add_total_column()`*

### Adding Several Columns in One Call

`with_columns()` accepts any number of expressions, so a single call can compute an order total, an 8% tax amount, and an uppercase product label all at once. String transformations live under the `.str` namespace you met in Module 5's regex work — here `str.to_uppercase()`.

!!! example "Worked Example: Several Columns in One Call"

    ```python
    # orders: the 12-order DataFrame built above
    enriched = orders.with_columns(
        (pl.col("quantity") * pl.col("unit_price")).round(2).alias("total"),
        (pl.col("quantity") * pl.col("unit_price") * 0.08).round(2).alias("tax"),
        pl.col("product").str.to_uppercase().alias("product_upper"),
    )

    print(enriched.select("order_id", "product", "product_upper", "total", "tax").head(5))
    ```

    **Output:**

    ```
    shape: (5, 5)
    ┌──────────┬──────────┬───────────────┬─────────┬────────┐
    │ order_id ┆ product  ┆ product_upper ┆ total   ┆ tax    │
    │ ---      ┆ ---      ┆ ---           ┆ ---     ┆ ---    │
    │ str      ┆ str      ┆ str           ┆ f64     ┆ f64    │
    ╞══════════╪══════════╪═══════════════╪═════════╪════════╡
    │ ORD-001  ┆ Laptop   ┆ LAPTOP        ┆ 2999.97 ┆ 240.0  │
    │ ORD-002  ┆ Monitor  ┆ MONITOR       ┆ 1747.5  ┆ 139.8  │
    │ ORD-003  ┆ Keyboard ┆ KEYBOARD      ┆ 1599.0  ┆ 127.92 │
    │ ORD-004  ┆ Mouse    ┆ MOUSE         ┆ 1249.5  ┆ 99.96  │
    │ ORD-005  ┆ Laptop   ┆ LAPTOP        ┆ 1999.98 ┆ 160.0  │
    └──────────┴──────────┴───────────────┴─────────┴────────┘
    ```

    **Interpretation:** Three new columns arrive in one pass over the data: a numeric total, a tax figure (eight percent of the total — ORD-001's $2,999.97 yields $240.00), and a text transformation. Batching expressions into one `with_columns()` call keeps related calculations together and lets Polars compute them in parallel.

    *Source: `computations/module10_examples.py` — `demo_multiple_columns()`*

### Replacing an Existing Column

If `.alias()` uses a name that already exists, the expression **replaces** that column rather than raising an error. This is how you overwrite a column in place — round its values, recase its text, or (as in the next subsection) change its type — while keeping the same column name:

```python
df.with_columns(
    pl.col("unit_price").round(0).alias("unit_price"),  # replaces the original
)
```

### Renaming Columns

Use `rename()` with a dictionary of `{"old_name": "new_name"}` pairs to change column names without touching the values. This is a routine first step when data arrives from another system with awkward or inconsistent names.

!!! example "Worked Example: Renaming Columns"

    ```python
    renamed = orders.rename({
        "unit_price": "price",
        "order_date": "date",
    })

    print(f"Before: {orders.columns}")
    print(f"After:  {renamed.columns}")
    ```

    **Output:**

    ```
    Before: ['order_id', 'customer', 'product', 'category', 'quantity', 'unit_price', 'region', 'order_date']
    After:  ['order_id', 'customer', 'product', 'category', 'quantity', 'price', 'region', 'date']
    ```

    **Interpretation:** Only the two names in the dictionary changed; every value and every other column is untouched. Because `rename()` also returns a new DataFrame, `orders` itself still has the original names — which is exactly what the `Before:` line demonstrates even though it is printed *after* the rename.

    *Source: `computations/module10_examples.py` — `demo_rename_columns()`*

### Casting Data Types

Sometimes a column is stored as the wrong type — most commonly, a date read from CSV that arrives as a plain string. Until it is cast, you cannot sort it chronologically or do date arithmetic with it. Use `.cast()` for numeric conversions and `.str.to_date()` for string-to-date conversions:

| From | To | Method |
|------|----|--------|
| String → Integer | `pl.Int64` | `pl.col("x").cast(pl.Int64)` |
| String → Float | `pl.Float64` | `pl.col("x").cast(pl.Float64)` |
| String → Date | `pl.Date` | `pl.col("x").str.to_date()` |
| Integer → Float | `pl.Float64` | `pl.col("x").cast(pl.Float64)` |

The `.schema` attribute reports each column's current type — check it before and after a cast to confirm the conversion worked.

!!! example "Worked Example: Casting a String Column to a Date"

    ```python
    print(f"order_date type before: {orders.schema['order_date']}")

    orders_typed = orders.with_columns(
        pl.col("order_date").str.to_date("%Y-%m-%d").alias("order_date"),
    )

    print(f"order_date type after:  {orders_typed.schema['order_date']}")
    print(orders_typed.select("order_id", "order_date").head(5))
    ```

    **Output:**

    ```
    order_date type before: String
    order_date type after:  Date
    shape: (5, 2)
    ┌──────────┬────────────┐
    │ order_id ┆ order_date │
    │ ---      ┆ ---        │
    │ str      ┆ date       │
    ╞══════════╪════════════╡
    │ ORD-001  ┆ 2025-01-05 │
    │ ORD-002  ┆ 2025-01-08 │
    │ ORD-003  ┆ 2025-01-10 │
    │ ORD-004  ┆ 2025-01-12 │
    │ ORD-005  ┆ 2025-01-15 │
    └──────────┴────────────┘
    ```

    **Interpretation:** The printed values look identical before and after — the change is in the dtype row, which now reads `date` instead of `str`. The format string `"%Y-%m-%d"` tells Polars how to parse the text (four-digit year, month, day). Reusing the name `order_date` in `.alias()` replaces the string column with the typed one.

    *Source: `computations/module10_examples.py` — `demo_cast_types()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "`with_columns()` modifies my DataFrame in place." | Polars DataFrames are immutable. `with_columns()` returns a *new* DataFrame; if you do not assign the result (`df = df.with_columns(...)`), the new column is discarded. |
| "Using `.alias()` with an existing column name causes an error." | It silently *replaces* that column. This is the standard way to overwrite a column — and a source of surprise if the name collision was accidental. |
| "If a column looks like a date, Polars treats it as a date." | A CSV date usually loads as `String`. Until you convert it with `str.to_date()`, sorting is alphabetical and date arithmetic is unavailable. Check `.schema` rather than trusting appearances. |

---

## 10.2 Group-By Aggregations

**Group-by** is one of the most powerful operations in data analysis. It answers questions of the form "what is the total/average/count *per* region, *per* product, *per* customer?" — the shape of almost every management report. It follows the **split-apply-combine** pattern:

1. **Split** the data into groups (by region, by product, by customer)
2. **Apply** an aggregation to each group (sum, mean, count, min, max)
3. **Combine** the results into a new DataFrame with one row per group

In Polars this reads as `group_by(...)` followed by `.agg(...)`:

```python
df.group_by("category").agg(
    pl.col("total").sum().alias("revenue"),
    pl.col("total").mean().alias("avg_order"),
    pl.len().alias("num_orders"),
)
```

### Grouping by One Column

The examples below use the orders data with the `total` column already added from §10.1. Note the closing `.sort()` on each result: Polars does not guarantee the order of groups in the output, so a sort makes the report stable and readable.

!!! example "Worked Example: Grouping by One Column"

    ```python
    orders = orders.with_columns(
        (pl.col("quantity") * pl.col("unit_price")).round(2).alias("total"),
    )

    by_region = orders.group_by("region").agg(
        pl.col("total").sum().alias("revenue"),
        pl.col("total").mean().round(2).alias("avg_order"),
        pl.len().alias("num_orders"),
    ).sort("revenue", descending=True)

    print("Revenue by Region:")
    print(by_region)

    by_category = orders.group_by("category").agg(
        pl.col("total").sum().alias("revenue"),
        pl.col("quantity").sum().alias("units_sold"),
        pl.len().alias("num_orders"),
    ).sort("revenue", descending=True)

    print("\nRevenue by Category:")
    print(by_category)
    ```

    **Output:**

    ```
    Revenue by Region:
    shape: (3, 4)
    ┌─────────┬─────────┬───────────┬────────────┐
    │ region  ┆ revenue ┆ avg_order ┆ num_orders │
    │ ---     ┆ ---     ┆ ---       ┆ ---        │
    │ str     ┆ f64     ┆ f64       ┆ u32        │
    ╞═════════╪═════════╪═══════════╪════════════╡
    │ West    ┆ 6920.67 ┆ 1384.13   ┆ 5          │
    │ East    ┆ 6590.49 ┆ 1318.1    ┆ 5          │
    │ Central ┆ 4795.98 ┆ 2397.99   ┆ 2          │
    └─────────┴─────────┴───────────┴────────────┘

    Revenue by Category:
    shape: (2, 4)
    ┌─────────────┬──────────┬────────────┬────────────┐
    │ category    ┆ revenue  ┆ units_sold ┆ num_orders │
    │ ---         ┆ ---      ┆ ---        ┆ ---        │
    │ str         ┆ f64      ┆ i64        ┆ u32        │
    ╞═════════════╪══════════╪════════════╪════════════╡
    │ Electronics ┆ 11510.94 ┆ 34         ┆ 7          │
    │ Accessories ┆ 6796.2   ┆ 140        ┆ 5          │
    └─────────────┴──────────┴────────────┴────────────┘
    ```

    **Interpretation:** Twelve order rows collapse into three region rows and two category rows. The West leads on revenue ($6,920.67), but Central has the highest average order ($2,397.99 across only 2 orders) — a split-apply-combine insight you could not see in the raw rows. Electronics earns nearly two-thirds of the revenue from only 34 units, while Accessories moves 140 units for far less revenue: high-ticket versus high-volume.

    *Source: `computations/module10_examples.py` — `demo_group_by_single()`*

### Grouping by Multiple Columns

Pass several columns to `group_by()` to get one row per *combination* — here, region and category together. The order of the grouping columns sets the hierarchy of the report.

!!! example "Worked Example: Grouping by Two Columns"

    ```python
    by_region_cat = orders.group_by("region", "category").agg(
        pl.col("total").sum().alias("revenue"),
        pl.len().alias("num_orders"),
    ).sort("region", "revenue", descending=[False, True])

    print("Revenue by Region and Category:")
    print(by_region_cat)
    ```

    **Output:**

    ```
    Revenue by Region and Category:
    shape: (5, 4)
    ┌─────────┬─────────────┬─────────┬────────────┐
    │ region  ┆ category    ┆ revenue ┆ num_orders │
    │ ---     ┆ ---         ┆ ---     ┆ ---        │
    │ str     ┆ str         ┆ f64     ┆ u32        │
    ╞═════════╪═════════════╪═════════╪════════════╡
    │ Central ┆ Electronics ┆ 4795.98 ┆ 2          │
    │ East    ┆ Electronics ┆ 3392.49 ┆ 3          │
    │ East    ┆ Accessories ┆ 3198.0  ┆ 2          │
    │ West    ┆ Accessories ┆ 3598.2  ┆ 3          │
    │ West    ┆ Electronics ┆ 3322.47 ┆ 2          │
    └─────────┴─────────────┴─────────┴────────────┘
    ```

    **Interpretation:** Five region-and-category combinations appear (Central sold no Accessories, so that combination simply has no row). The two-level sort — region ascending, then revenue descending within each region — shows that Accessories lead in the West while Electronics lead in the East. `descending=[False, True]` supplies one direction per sort column.

    *Source: `computations/module10_examples.py` — `demo_group_by_multiple()`*

### Common Aggregation Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `.sum()` | Total | `pl.col("revenue").sum()` |
| `.mean()` | Average | `pl.col("price").mean()` |
| `.median()` | Median | `pl.col("salary").median()` |
| `.min()` / `.max()` | Extremes | `pl.col("date").min()` |
| `pl.len()` | Count rows | `pl.len()` |
| `.count()` | Count non-empty values | `pl.col("id").count()` |
| `.n_unique()` | Count unique | `pl.col("customer").n_unique()` |
| `.first()` / `.last()` | First/last value | `pl.col("name").first()` |

**`pl.len()` vs `.count()` — a distinction that matters.** Think of a spreadsheet column where a few cells were left blank. `pl.len()` counts the **rows**, blanks included. `.count()` looks at one column and counts only the cells that actually have a value, skipping the blanks. When the business question is *"how many orders came from this region?"* you want a row count, so reach for `pl.len()`. Blank cells (**nulls**) are common in real data — §10.4 is devoted to them — and that is exactly when these two give different answers.

### A Multi-Metric Customer Summary

A single `agg()` can mix aggregation functions freely — totals, averages, counts, unique counts, and extremes side by side. This is how one line of grouping code produces a complete per-customer scorecard.

!!! example "Worked Example: A Multi-Metric Customer Summary"

    ```python
    customer_summary = orders.group_by("customer").agg(
        pl.col("total").sum().alias("total_spent"),
        pl.col("total").mean().round(2).alias("avg_order"),
        pl.len().alias("num_orders"),
        pl.col("product").n_unique().alias("unique_products"),
        pl.col("total").max().alias("largest_order"),
    ).sort("total_spent", descending=True)

    print("Customer Summary:")
    print(customer_summary)
    ```

    **Output:**

    ```
    Customer Summary:
    shape: (5, 6)
    ┌──────────────────┬─────────────┬───────────┬────────────┬─────────────────┬───────────────┐
    │ customer         ┆ total_spent ┆ avg_order ┆ num_orders ┆ unique_products ┆ largest_order │
    │ ---              ┆ ---         ┆ ---       ┆ ---        ┆ ---             ┆ ---           │
    │ str              ┆ f64         ┆ f64       ┆ u32        ┆ u32             ┆ f64           │
    ╞══════════════════╪═════════════╪═══════════╪════════════╪═════════════════╪═══════════════╡
    │ DataFlow Inc     ┆ 4795.98     ┆ 2397.99   ┆ 2          ┆ 2               ┆ 2796.0        │
    │ Acme Corp        ┆ 4571.97     ┆ 1523.99   ┆ 3          ┆ 3               ┆ 2999.97       │
    │ Bright Solutions ┆ 4391.25     ┆ 1463.75   ┆ 3          ┆ 3               ┆ 1998.75       │
    │ CyberTech        ┆ 2348.7      ┆ 1174.35   ┆ 2          ┆ 2               ┆ 1599.0        │
    │ EcoGoods         ┆ 2199.24     ┆ 1099.62   ┆ 2          ┆ 2               ┆ 1199.25       │
    └──────────────────┴─────────────┴───────────┴────────────┴─────────────────┴───────────────┘
    ```

    **Interpretation:** One grouping call yields a per-customer scorecard: DataFlow Inc spends the most in total ($4,795.98) despite placing only 2 orders, while Acme Corp places more orders across more distinct products. `n_unique("product")` measures breadth of purchasing, and `max("total")` flags each customer's single largest order.

    *Source: `computations/module10_examples.py` — `demo_customer_summary()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "`pl.len()` and `.count()` are interchangeable." | They agree only when the counted column has no nulls. `pl.len()` counts rows in the group; `.count()` counts non-null values in one column. For "how many orders?" use `pl.len()`. |
| "The grouped result comes back in a predictable order." | Group order is not guaranteed. Always finish a report with `.sort()` if the row order matters. |
| "The order of columns in `group_by()` doesn't matter." | Group membership is the same, but the column order sets the grouping hierarchy of the report — `group_by("region", "category")` reads as categories *within* regions. |
| "`agg()` computes one statistic at a time." | `agg()` accepts any number of expressions, each with its own function and `.alias()` — a full scorecard in one call. |

---

## 10.3 Joining DataFrames

**Joins** combine two DataFrames based on a shared column (the "key"). This is identical to SQL JOINs if you have used databases — and it is how analysts attach *context* to transactions: customer attributes onto orders, product details onto sales, employee info onto timesheets. The workhorse in business reporting is the **left join**: keep every transaction (the left table), and bring in descriptive columns from the lookup table where a match exists.

```python
orders.join(
    customers,
    on="customer_id",     # shared column name
    how="left",           # join type
)
```

| Join type | Keeps... |
|-----------|----------|
| `"inner"` | Only rows that match in both tables |
| `"left"` | All rows from left table, matched from right |
| `"full"` | All rows from both tables |

### A Left Join in Action

!!! example "Worked Example: Left Join — Adding Customer Attributes to Orders"

    ```python
    customers = pl.DataFrame({
        "customer": ["Acme Corp", "Bright Solutions", "CyberTech", "DataFlow Inc", "EcoGoods"],
        "industry": ["Manufacturing", "Consulting", "Technology", "Analytics", "Retail"],
        "tier": ["Gold", "Silver", "Gold", "Bronze", "Silver"],
    })

    print("Customer Info:")
    print(customers)

    enriched = orders.join(
        customers,
        on="customer",
        how="left",
    )

    print("\nOrders with customer info (first 6 rows):")
    print(enriched.select("order_id", "customer", "industry", "tier", "product", "total").head(6))
    ```

    **Output:**

    ```
    Customer Info:
    shape: (5, 3)
    ┌──────────────────┬───────────────┬────────┐
    │ customer         ┆ industry      ┆ tier   │
    │ ---              ┆ ---           ┆ ---    │
    │ str              ┆ str           ┆ str    │
    ╞══════════════════╪═══════════════╪════════╡
    │ Acme Corp        ┆ Manufacturing ┆ Gold   │
    │ Bright Solutions ┆ Consulting    ┆ Silver │
    │ CyberTech        ┆ Technology    ┆ Gold   │
    │ DataFlow Inc     ┆ Analytics     ┆ Bronze │
    │ EcoGoods         ┆ Retail        ┆ Silver │
    └──────────────────┴───────────────┴────────┘

    Orders with customer info (first 6 rows):
    shape: (6, 6)
    ┌──────────┬──────────────────┬───────────────┬────────┬──────────┬─────────┐
    │ order_id ┆ customer         ┆ industry      ┆ tier   ┆ product  ┆ total   │
    │ ---      ┆ ---              ┆ ---           ┆ ---    ┆ ---      ┆ ---     │
    │ str      ┆ str              ┆ str           ┆ str    ┆ str      ┆ f64     │
    ╞══════════╪══════════════════╪═══════════════╪════════╪══════════╪═════════╡
    │ ORD-001  ┆ Acme Corp        ┆ Manufacturing ┆ Gold   ┆ Laptop   ┆ 2999.97 │
    │ ORD-002  ┆ Bright Solutions ┆ Consulting    ┆ Silver ┆ Monitor  ┆ 1747.5  │
    │ ORD-003  ┆ CyberTech        ┆ Technology    ┆ Gold   ┆ Keyboard ┆ 1599.0  │
    │ ORD-004  ┆ Acme Corp        ┆ Manufacturing ┆ Gold   ┆ Mouse    ┆ 1249.5  │
    │ ORD-005  ┆ DataFlow Inc     ┆ Analytics     ┆ Bronze ┆ Laptop   ┆ 1999.98 │
    │ ORD-006  ┆ Bright Solutions ┆ Consulting    ┆ Silver ┆ Webcam   ┆ 645.0   │
    └──────────┴──────────────────┴───────────────┴────────┴──────────┴─────────┘
    ```

    **Interpretation:** The 5-row lookup table contributes `industry` and `tier` to every order row — customers with several orders (Acme Corp) have their attributes repeated on each of their rows. The number of order rows is unchanged, because a left join keeps every left-table row exactly once when each key matches one lookup row.

    *Source: `computations/module10_examples.py` — `demo_left_join()`*

### Join, Then Aggregate

Joins earn their keep when combined with group-by: attach an attribute from the lookup table, then summarize by it. The question "how much revenue comes from each customer *tier*?" cannot be answered from the orders table alone — `tier` lives in the customers table.

!!! example "Worked Example: Join, Then Aggregate — Revenue by Tier"

    ```python
    tier_revenue = (
        orders
        .join(customers, on="customer", how="left")
        .group_by("tier")
        .agg(
            pl.col("total").sum().alias("revenue"),
            pl.col("customer").n_unique().alias("num_customers"),
            pl.len().alias("num_orders"),
        )
        .sort("revenue", descending=True)
    )

    print("Revenue by Customer Tier:")
    print(tier_revenue)
    ```

    **Output:**

    ```
    Revenue by Customer Tier:
    shape: (3, 4)
    ┌────────┬─────────┬───────────────┬────────────┐
    │ tier   ┆ revenue ┆ num_customers ┆ num_orders │
    │ ---    ┆ ---     ┆ ---           ┆ ---        │
    │ str    ┆ f64     ┆ u32           ┆ u32        │
    ╞════════╪═════════╪═══════════════╪════════════╡
    │ Gold   ┆ 6920.67 ┆ 2             ┆ 5          │
    │ Silver ┆ 6590.49 ┆ 2             ┆ 5          │
    │ Bronze ┆ 4795.98 ┆ 1             ┆ 2          │
    └────────┴─────────┴───────────────┴────────────┘
    ```

    **Interpretation:** Two Gold customers generate $6,920.67 across 5 orders — but the single Bronze customer (DataFlow Inc) produces $4,795.98 from just 2 orders, the highest revenue per order of any tier. The join supplied the grouping column; the aggregation did the summarizing.

    *Source: `computations/module10_examples.py` — `demo_join_then_group()`*

### Joining on Different Column Names

If the key column has a different name in each table, use `left_on` and `right_on` instead of `on`:

```python
orders.join(
    customers,
    left_on="customer_name",
    right_on="company",
    how="left",
)
```

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "A join stacks one table's rows under the other's." | A join adds *columns* by matching key values row to row. Stacking rows is concatenation — a different operation. |
| "A left join drops rows that have no match." | A left join keeps *every* left-table row; unmatched rows get `null` in the columns from the right table. It is the *inner* join that drops non-matching rows. |
| "Left and inner joins always give different row counts." | When every left-table key exists in the right table, the two produce identical results. The difference only appears when some keys fail to match. |
| "The key column must have the same name in both tables." | Use `left_on=` and `right_on=` when the names differ — no renaming required. |

---

## 10.4 Handling Null Values

Real-world data often has **missing values** — a survey question skipped, a price not yet entered, a sensor that failed to report. In Polars these are represented as `null`, and the library gives you tools to find them, fill them, or remove them:

| Method | Purpose | Example |
|--------|---------|---------|
| `.is_null()` | Check for nulls | `pl.col("x").is_null()` |
| `.is_not_null()` | Check for non-nulls | `pl.col("x").is_not_null()` |
| `.fill_null(value)` | Replace nulls | `pl.col("x").fill_null(0)` |
| `.drop_nulls()` | Remove rows with nulls | `df.drop_nulls()` |
| `.null_count()` | Count nulls per column | `df.null_count()` |

### Detecting Nulls

The first step is always diagnosis: which columns have gaps, and how many? `df.null_count()` answers in one call.

!!! example "Worked Example: Finding the Gaps"

    ```python
    products = pl.DataFrame({
        "product": ["Laptop", "Monitor", "Keyboard", "Mouse", "Webcam"],
        "price": [999.99, 349.50, None, 24.99, None],
        "rating": [4.5, None, 4.2, 3.8, 4.0],
        "stock": [45, 120, 200, None, 85],
    })

    print("Dataset with nulls:")
    print(products)
    print("\nNull counts per column:")
    print(products.null_count())
    ```

    **Output:**

    ```
    Dataset with nulls:
    shape: (5, 4)
    ┌──────────┬────────┬────────┬───────┐
    │ product  ┆ price  ┆ rating ┆ stock │
    │ ---      ┆ ---    ┆ ---    ┆ ---   │
    │ str      ┆ f64    ┆ f64    ┆ i64   │
    ╞══════════╪════════╪════════╪═══════╡
    │ Laptop   ┆ 999.99 ┆ 4.5    ┆ 45    │
    │ Monitor  ┆ 349.5  ┆ null   ┆ 120   │
    │ Keyboard ┆ null   ┆ 4.2    ┆ 200   │
    │ Mouse    ┆ 24.99  ┆ 3.8    ┆ null  │
    │ Webcam   ┆ null   ┆ 4.0    ┆ 85    │
    └──────────┴────────┴────────┴───────┘

    Null counts per column:
    shape: (1, 4)
    ┌─────────┬───────┬────────┬───────┐
    │ product ┆ price ┆ rating ┆ stock │
    │ ---     ┆ ---   ┆ ---    ┆ ---   │
    │ u32     ┆ u32   ┆ u32    ┆ u32   │
    ╞═════════╪═══════╪════════╪═══════╡
    │ 0       ┆ 2     ┆ 1      ┆ 1     │
    └─────────┴───────┴────────┴───────┘
    ```

    **Interpretation:** Polars prints missing cells as the literal word `null`, and `null_count()` totals them per column: two products lack a price, one lacks a rating, one lacks a stock figure. In Python code, you supply a missing value as `None` — Polars stores and displays it as `null`.

    *Source: `computations/module10_examples.py` — `demo_null_detection()`*

### Filling Nulls

`fill_null()` replaces missing values. The replacement can be a constant (`0`, `"Unknown"`) or a computed expression — filling a missing rating with the *mean* of the observed ratings is a common default.

!!! example "Worked Example: Filling Nulls with Defaults"

    ```python
    filled = products.with_columns(
        pl.col("price").fill_null(0).alias("price"),
        pl.col("rating").fill_null(pl.col("rating").mean()).alias("rating"),
        pl.col("stock").fill_null(0).alias("stock"),
    )

    print("After filling nulls:")
    print(filled)
    ```

    **Output:**

    ```
    After filling nulls:
    shape: (5, 4)
    ┌──────────┬────────┬────────┬───────┐
    │ product  ┆ price  ┆ rating ┆ stock │
    │ ---      ┆ ---    ┆ ---    ┆ ---   │
    │ str      ┆ f64    ┆ f64    ┆ i64   │
    ╞══════════╪════════╪════════╪═══════╡
    │ Laptop   ┆ 999.99 ┆ 4.5    ┆ 45    │
    │ Monitor  ┆ 349.5  ┆ 4.125  ┆ 120   │
    │ Keyboard ┆ 0.0    ┆ 4.2    ┆ 200   │
    │ Mouse    ┆ 24.99  ┆ 3.8    ┆ 0     │
    │ Webcam   ┆ 0.0    ┆ 4.0    ┆ 85    │
    └──────────┴────────┴────────┴───────┘
    ```

    **Interpretation:** Missing prices and stock became `0`, while the Monitor's missing rating became `4.125` — the mean of the four observed ratings (4.5, 4.2, 3.8, 4.0). The fill value is a business decision: a `0` price says "free" to any later calculation, which may be exactly wrong. Choose fills that match what the missing value *means*.

    *Source: `computations/module10_examples.py` — `demo_fill_null()`*

### Removing Incomplete Rows

The alternative to filling is removing. `filter(pl.col(...).is_not_null())` keeps rows that are complete *in one specific column*; `drop_nulls()` keeps only rows with no nulls *anywhere*.

!!! example "Worked Example: Filtering and Dropping Incomplete Rows"

    ```python
    valid_prices = products.filter(pl.col("price").is_not_null())
    print("Rows with valid prices:")
    print(valid_prices)

    clean = products.drop_nulls()
    print(f"\nOriginal rows: {products.shape[0]}, After drop_nulls: {clean.shape[0]}")
    print(clean)
    ```

    **Output:**

    ```
    Rows with valid prices:
    shape: (3, 4)
    ┌─────────┬────────┬────────┬───────┐
    │ product ┆ price  ┆ rating ┆ stock │
    │ ---     ┆ ---    ┆ ---    ┆ ---   │
    │ str     ┆ f64    ┆ f64    ┆ i64   │
    ╞═════════╪════════╪════════╪═══════╡
    │ Laptop  ┆ 999.99 ┆ 4.5    ┆ 45    │
    │ Monitor ┆ 349.5  ┆ null   ┆ 120   │
    │ Mouse   ┆ 24.99  ┆ 3.8    ┆ null  │
    └─────────┴────────┴────────┴───────┘

    Original rows: 5, After drop_nulls: 1
    shape: (1, 4)
    ┌─────────┬────────┬────────┬───────┐
    │ product ┆ price  ┆ rating ┆ stock │
    │ ---     ┆ ---    ┆ ---    ┆ ---   │
    │ str     ┆ f64    ┆ f64    ┆ i64   │
    ╞═════════╪════════╪════════╪═══════╡
    │ Laptop  ┆ 999.99 ┆ 4.5    ┆ 45    │
    └─────────┴────────┴────────┴───────┘
    ```

    **Interpretation:** Filtering on one column keeps 3 rows — note the Monitor row survives with its rating still `null`, because only `price` was checked. `drop_nulls()` is far stricter: any null in any column disqualifies the row, leaving just the Laptop. On a wide table, blanket `drop_nulls()` can quietly delete most of your data — count before and after, as done here.

    *Source: `computations/module10_examples.py` — `demo_remove_nulls()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "`null` is the same as `0` (or an empty string)." | `null` means *absent*, not zero. Filling a missing price with `0` changes averages and totals; the right fill depends on what the gap means in the business. |
| "Aggregating a column with nulls raises an error." | Aggregations like `.mean()` and `.sum()` silently *skip* nulls. The code runs — but the answer may not describe the rows you think it does, which is why you diagnose and handle nulls *before* aggregating. |
| "`drop_nulls()` only removes rows that are entirely empty." | By default it removes any row containing a null in *any* column. Pass a subset (or filter on `is_not_null()`) to be selective. |
| "You can find nulls with `pl.col('x') == None`." | Null comparisons do not behave like value comparisons. Use `.is_null()` / `.is_not_null()`. |

---

## 10.5 Method Chaining: The End-to-End Pipeline

Polars' real power emerges when you chain multiple operations into a single pipeline. Because every operation returns a new DataFrame, each result immediately supports the next method call:

```python
result = (
    df
    .with_columns(...)    # Step 1: compute new columns
    .filter(...)          # Step 2: keep relevant rows
    .group_by(...)        # Step 3: summarize by group
    .agg(...)
    .sort(...)            # Step 4: order the results
)
```

The surrounding parentheses are ordinary Python line-continuation — they let each step sit on its own line so the pipeline reads top-to-bottom like a recipe. This section closes the module the way the teaching notebook does: a complete order-analysis pipeline from raw data to a report on disk.

### Step 1: Enrich the Orders

The first stage applies everything from §10.1 and §10.3 in one chain: compute `total` and an 8.25% `tax`, cast the date column, join the customer attributes, then compute the tax-inclusive total from the columns created earlier in the same pipeline.

!!! example "Worked Example: Enriching the Orders"

    ```python
    analysis = (
        orders
        # Compute order total and tax
        .with_columns(
            (pl.col("quantity") * pl.col("unit_price")).round(2).alias("total"),
            (pl.col("quantity") * pl.col("unit_price") * 0.0825).round(2).alias("tax"),
            pl.col("order_date").str.to_date("%Y-%m-%d").alias("order_date"),
        )
        # Join customer info
        .join(customers, on="customer", how="left")
        # Compute total with tax
        .with_columns(
            (pl.col("total") + pl.col("tax")).round(2).alias("total_with_tax"),
        )
    )

    print("Enriched Orders (first 6 rows):")
    print(
        analysis.select(
            "order_id", "customer", "tier", "product", "total", "tax", "total_with_tax"
        ).head(6)
    )
    ```

    **Output:**

    ```
    Enriched Orders (first 6 rows):
    shape: (6, 7)
    ┌──────────┬──────────────────┬────────┬──────────┬─────────┬────────┬────────────────┐
    │ order_id ┆ customer         ┆ tier   ┆ product  ┆ total   ┆ tax    ┆ total_with_tax │
    │ ---      ┆ ---              ┆ ---    ┆ ---      ┆ ---     ┆ ---    ┆ ---            │
    │ str      ┆ str              ┆ str    ┆ str      ┆ f64     ┆ f64    ┆ f64            │
    ╞══════════╪══════════════════╪════════╪══════════╪═════════╪════════╪════════════════╡
    │ ORD-001  ┆ Acme Corp        ┆ Gold   ┆ Laptop   ┆ 2999.97 ┆ 247.5  ┆ 3247.47        │
    │ ORD-002  ┆ Bright Solutions ┆ Silver ┆ Monitor  ┆ 1747.5  ┆ 144.17 ┆ 1891.67        │
    │ ORD-003  ┆ CyberTech        ┆ Gold   ┆ Keyboard ┆ 1599.0  ┆ 131.92 ┆ 1730.92        │
    │ ORD-004  ┆ Acme Corp        ┆ Gold   ┆ Mouse    ┆ 1249.5  ┆ 103.08 ┆ 1352.58        │
    │ ORD-005  ┆ DataFlow Inc     ┆ Bronze ┆ Laptop   ┆ 1999.98 ┆ 165.0  ┆ 2164.98        │
    │ ORD-006  ┆ Bright Solutions ┆ Silver ┆ Webcam   ┆ 645.0   ┆ 53.21  ┆ 698.21         │
    └──────────┴──────────────────┴────────┴──────────┴─────────┴────────┴────────────────┘
    ```

    **Interpretation:** One chained expression performs four transformations: ORD-001's $2,999.97 total gains $247.50 of tax for a $3,247.47 invoice amount, and each order now carries its customer's tier. The second `with_columns()` can reference `total` and `tax` because they already exist by that point in the chain.

    *Source: `computations/module10_examples.py` — `demo_pipeline_enrich()`*

### Step 2: Summary Reports

With the enriched table built, the reporting stage is join-then-aggregate from §10.3 applied twice: once by tier, once by customer.

!!! example "Worked Example: Tier and Top-Customer Reports"

    ```python
    # analysis: orders with 'total' computed and customer info joined (Step 1)
    tier_summary = (
        analysis
        .group_by("tier")
        .agg(
            pl.col("total").sum().alias("revenue"),
            pl.col("total").mean().round(2).alias("avg_order"),
            pl.len().alias("num_orders"),
            pl.col("customer").n_unique().alias("num_customers"),
        )
        .sort("revenue", descending=True)
    )

    print("Summary by Customer Tier:")
    print(tier_summary)

    top_customers = (
        analysis
        .group_by("customer", "tier", "industry")
        .agg(
            pl.col("total").sum().alias("total_spent"),
            pl.len().alias("num_orders"),
            pl.col("product").n_unique().alias("unique_products"),
        )
        .sort("total_spent", descending=True)
    )

    print("\nTop Customers by Total Spending:")
    print(top_customers)
    ```

    **Output:**

    ```
    Summary by Customer Tier:
    shape: (3, 5)
    ┌────────┬─────────┬───────────┬────────────┬───────────────┐
    │ tier   ┆ revenue ┆ avg_order ┆ num_orders ┆ num_customers │
    │ ---    ┆ ---     ┆ ---       ┆ ---        ┆ ---           │
    │ str    ┆ f64     ┆ f64       ┆ u32        ┆ u32           │
    ╞════════╪═════════╪═══════════╪════════════╪═══════════════╡
    │ Gold   ┆ 6920.67 ┆ 1384.13   ┆ 5          ┆ 2             │
    │ Silver ┆ 6590.49 ┆ 1318.1    ┆ 5          ┆ 2             │
    │ Bronze ┆ 4795.98 ┆ 2397.99   ┆ 2          ┆ 1             │
    └────────┴─────────┴───────────┴────────────┴───────────────┘

    Top Customers by Total Spending:
    shape: (5, 6)
    ┌──────────────────┬────────┬───────────────┬─────────────┬────────────┬─────────────────┐
    │ customer         ┆ tier   ┆ industry      ┆ total_spent ┆ num_orders ┆ unique_products │
    │ ---              ┆ ---    ┆ ---           ┆ ---         ┆ ---        ┆ ---             │
    │ str              ┆ str    ┆ str           ┆ f64         ┆ u32        ┆ u32             │
    ╞══════════════════╪════════╪═══════════════╪═════════════╪════════════╪═════════════════╡
    │ DataFlow Inc     ┆ Bronze ┆ Analytics     ┆ 4795.98     ┆ 2          ┆ 2               │
    │ Acme Corp        ┆ Gold   ┆ Manufacturing ┆ 4571.97     ┆ 3          ┆ 3               │
    │ Bright Solutions ┆ Silver ┆ Consulting    ┆ 4391.25     ┆ 3          ┆ 3               │
    │ CyberTech        ┆ Gold   ┆ Technology    ┆ 2348.7      ┆ 2          ┆ 2               │
    │ EcoGoods         ┆ Silver ┆ Retail        ┆ 2199.24     ┆ 2          ┆ 2               │
    └──────────────────┴────────┴───────────────┴─────────────┴────────────┴─────────────────┘
    ```

    **Interpretation:** The same enriched table answers two different management questions. Grouping the customer report by `customer`, `tier`, *and* `industry` is a practical trick: since each customer has exactly one tier and industry, the extra grouping columns carry those labels into the report without a second join. DataFlow Inc — the lone Bronze customer — tops the spending table, a finding a tier-only view would have hidden.

    *Source: `computations/module10_examples.py` — `demo_pipeline_summaries()`*

### Step 3: The Product Report, Written to CSV

The final stage produces the deliverable: a product performance report aggregated from the raw orders, written to CSV with `write_csv()`, then read back to confirm the file is intact — the same read/write round-trip discipline you practiced in Module 8.

!!! example "Worked Example: Product Report Written to CSV"

    ```python
    product_perf = (
        orders
        .with_columns(
            (pl.col("quantity") * pl.col("unit_price")).round(2).alias("total"),
        )
        .group_by("product", "category")
        .agg(
            pl.col("total").sum().alias("revenue"),
            pl.col("quantity").sum().alias("units_sold"),
            pl.len().alias("num_orders"),
            pl.col("region").n_unique().alias("regions_sold_in"),
        )
        .sort("revenue", descending=True)
    )

    print("Product Performance:")
    print(product_perf)

    product_perf.write_csv("product_performance.csv")
    print(f"\nWrote product performance report ({product_perf.shape[0]} products) to product_performance.csv")

    verified = pl.read_csv("product_performance.csv")
    print("\nRead back from CSV to verify:")
    print(verified)
    ```

    **Output:**

    ```
    Product Performance:
    shape: (5, 6)
    ┌──────────┬─────────────┬─────────┬────────────┬────────────┬─────────────────┐
    │ product  ┆ category    ┆ revenue ┆ units_sold ┆ num_orders ┆ regions_sold_in │
    │ ---      ┆ ---         ┆ ---     ┆ ---        ┆ ---        ┆ ---             │
    │ str      ┆ str         ┆ f64     ┆ i64        ┆ u32        ┆ u32             │
    ╞══════════╪═════════════╪═════════╪════════════╪════════════╪═════════════════╡
    │ Laptop   ┆ Electronics ┆ 5999.94 ┆ 6          ┆ 3          ┆ 3               │
    │ Keyboard ┆ Accessories ┆ 4797.0  ┆ 60         ┆ 3          ┆ 2               │
    │ Monitor  ┆ Electronics ┆ 4543.5  ┆ 13         ┆ 2          ┆ 2               │
    │ Mouse    ┆ Accessories ┆ 1999.2  ┆ 80         ┆ 2          ┆ 1               │
    │ Webcam   ┆ Electronics ┆ 967.5   ┆ 15         ┆ 2          ┆ 2               │
    └──────────┴─────────────┴─────────┴────────────┴────────────┴─────────────────┘

    Wrote product performance report (5 products) to product_performance.csv

    Read back from CSV to verify:
    shape: (5, 6)
    ┌──────────┬─────────────┬─────────┬────────────┬────────────┬─────────────────┐
    │ product  ┆ category    ┆ revenue ┆ units_sold ┆ num_orders ┆ regions_sold_in │
    │ ---      ┆ ---         ┆ ---     ┆ ---        ┆ ---        ┆ ---             │
    │ str      ┆ str         ┆ f64     ┆ i64        ┆ i64        ┆ i64             │
    ╞══════════╪═════════════╪═════════╪════════════╪════════════╪═════════════════╡
    │ Laptop   ┆ Electronics ┆ 5999.94 ┆ 6          ┆ 3          ┆ 3               │
    │ Keyboard ┆ Accessories ┆ 4797.0  ┆ 60         ┆ 3          ┆ 2               │
    │ Monitor  ┆ Electronics ┆ 4543.5  ┆ 13         ┆ 2          ┆ 2               │
    │ Mouse    ┆ Accessories ┆ 1999.2  ┆ 80         ┆ 2          ┆ 1               │
    │ Webcam   ┆ Electronics ┆ 967.5   ┆ 15         ┆ 2          ┆ 2               │
    └──────────┴─────────────┴─────────┴────────────┴────────────┴─────────────────┘
    ```

    **Interpretation:** Laptops earn the most revenue ($5,999.94) from only 6 units, while Mice ship 80 units for a third of that — and the read-back confirms the CSV round-trip preserved every figure. One subtle change: the counting columns come back as `i64` instead of `u32`, because a CSV file stores no dtype information and `read_csv()` re-infers types from the text.

    *Source: `computations/module10_examples.py` — `demo_pipeline_write_report()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "Each step in a chain modifies the original DataFrame." | Every step returns a *new* DataFrame that feeds the next step; the original is untouched. Chaining works precisely because of the immutability from §10.1. |
| "The parentheses around a chain are special Polars syntax." | They are ordinary Python line-continuation. They exist only so each `.method()` can sit on its own line for readability. |
| "Chaining and separate intermediate variables give different results." | The results are identical. Chaining reduces variable clutter and stale-copy bugs; intermediate variables ease inspection while debugging. Pick per situation — many analysts debug with variables, then consolidate into a chain. |
| "`write_csv()` saves my analysis." | It saves a *snapshot of the data* only. The analysis is the pipeline code — which is why reproducible scripts and notebooks matter more than any single output file. |

---

## Reflection Questions

1. Polars DataFrames are immutable, so `with_columns()` returns a new DataFrame instead of modifying the old one. What kinds of bugs does this design prevent, and what habit does it force on you when writing transformation code?
2. A sales VP asks, "What is our average order size?" Give three different grouping choices that answer three different versions of that question, and explain how you would find out which one the VP actually wants.
3. Your orders table has 500 rows, but after joining a customer lookup table with an inner join, the result has 480 rows. What happened to the other 20, what would a left join have done instead, and which behavior is right for a revenue report?
4. A colleague fills every null in a price column with `0` before computing the average price. Explain what this does to the average, and propose two alternative treatments with the trade-offs of each.
5. Compare a five-step method chain to five separate assignments producing the same result. In what circumstances would you prefer each style, and how would you debug a chain that produces a wrong number somewhere in the middle?

---

## Your Assignment

The Module 10 assignment is worth **100 points plus a 10-point bonus**. You complete it in a **marimo notebook (`.py` file)** and submit the file to **Brightspace**. The final reflection section is not graded separately — it counts toward participation. Setup cells in the notebook create every CSV file the tasks read (under `/tmp/`), so you only write the analysis code. Work through the tasks in order; they follow the module's sections and build toward a full pipeline.

**Task 1: Adding Computed Columns (10 points).** An HR dataset holds six employees' annual salaries and years employed. You read the CSV and use `with_columns()` to add three derived columns — a monthly salary, a daily rate, and a seniority bonus — each computed from the existing columns with the rounding specified in the task. Everything you need is in §10.1.

**Task 2: Renaming and Casting (15 points).** A product catalog exported from a legacy system arrives with CamelCase column names, prices stored as strings with dollar signs, and dates stored as text. You rename the columns to snake_case, strip the `$` with a regex replacement before casting price to a float, cast the launch date to a real `Date`, and show the schema before and after to prove the cleanup worked. Concepts come from §10.1 (rename and casting) plus the `str.replace()` pattern from Module 5's string work.

**Task 3: Group-By Aggregations (15 points).** Retail transactions from three stores must be summarized two ways: by store (total revenue, average order value, transaction count, and distinct categories) and by category (units and revenue), each sorted by revenue. This is §10.2 end to end — note that the revenue being aggregated is itself a computed `quantity * price` expression.

**Task 4: Joining DataFrames (15 points).** A registrar has a grades table and a students table sharing a `student_id` key. You perform a left join, summarize grade points by major, then repeat with an inner join and compare the row counts, explaining why they relate the way they do for this data. The join mechanics are §10.3; the post-join summary uses §10.2.

**Task 5: Handling Null Values (20 points).** A customer survey has missing responses scattered across three columns. You diagnose the gaps with `null_count()`, fill each column with a sensible default (a number, a category label, and a placeholder sentence), and separately filter the original data down to fully complete responses, reporting the row counts at each stage. This is §10.4's detect-fill-remove workflow.

**Task 6: Full Pipeline Challenge (25 points).** Airline flight records — some with missing delay values — must become a finished report: fill the nulls, compute a revenue column, aggregate four metrics by airline, join an airline-info lookup table, sort, write the result to CSV, and read it back to confirm. The task asks you to build the middle steps as a single chained expression, which is §10.5 applied to everything from §10.1 through §10.4.

**Task 7: Creative Exercise — Bonus (10 points).** Design your own business scenario (the prompt suggests gym memberships, recipes, e-commerce returns, or a sports league) with at least 8 rows and 5 columns. Your solution must demonstrate a `with_columns()` computed column, a `group_by().agg()` with at least two aggregation expressions, a `join()` between two DataFrames, and formatted print output explaining what you found — every section of this module in one scenario of your choosing.

---

## Chapter Summary

This module moved you from exploring data to transforming it. `with_columns()` adds computed columns the way a spreadsheet adds formula columns — except each expression is explicit, repeatable code, and the result is always a new DataFrame because Polars DataFrames are immutable. `rename()` fixes column names, and `.cast()` / `.str.to_date()` fix column *types*, which matters because a date stored as a string can be neither sorted chronologically nor used in date arithmetic.

`group_by().agg()` implements split-apply-combine, the single most-used pattern in business analytics: split rows into groups, apply aggregations like `.sum()`, `.mean()`, `.n_unique()`, and `pl.len()` to each group, and combine the answers into a one-row-per-group report. Two details separate careful work from sloppy work here: group order is not guaranteed (so sort your reports), and `pl.len()` counts rows while `.count()` counts non-null values — a distinction that only matters exactly when your data has gaps. Joins then attach context from a second table by matching key values — `"left"` keeps every row of your main table, `"inner"` keeps only matches — and join-then-aggregate is how you summarize transactions by attributes that live in a lookup table.

Null handling closes the loop on messy data: `null_count()` to diagnose, `fill_null()` to repair, `is_not_null()` / `drop_nulls()` to remove, with the choice among them being a business judgment about what a missing value means. Method chaining then ties every operation in this module into pipelines that read top-to-bottom — read, compute, join, aggregate, sort, write — which is precisely the shape of the capstone analysis you will build later in the course.

---

## What's Next

You can now turn raw records into summary tables — revenue by region, spending by customer tier, product performance ranked by revenue. In Module 11 you will learn **data visualization** with matplotlib and Plotly Express, turning those DataFrames into charts, graphs, and dashboards. The group-by summaries you built in this module are exactly the inputs a chart wants: a bar per category, a line per month, a point per customer. The pipeline gains one final step: read → transform → aggregate → *visualize*.
