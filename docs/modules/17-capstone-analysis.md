# Module 16.2: Capstone: Analysis & Presentation

## Introduction

This is the second half of the final module of MIS501, and it completes the capstone project you began in Module 16.1. There you framed a research question, proposed a data source, and ran a first exploratory analysis. Here you carry a project through every remaining step: cleaning and feature engineering, systematic Polars aggregation, SQL analysis with DuckDB, presentation-quality visualizations, and — the part decision-makers actually read — a written narrative with an executive summary, honest limitations, and a reflection. The whole module is a complete worked example of a finished capstone, demonstrated on a fictional coffee-shop chain. Your graded assignment applies the identical workflow to a different business — a metropolitan public library system — so this chapter teaches you the *method* while your assignment produces the *answers*. That separation is deliberate: the analytical workflow is the same regardless of the subject matter, and being able to move it from one domain to another is precisely the skill a capstone certifies.

---

## Learning Objectives

By the end of this module, you should be able to:

1. **Apply** the Python data-analysis toolkit (Polars and visualization, optionally DuckDB) to a real problem
2. **Perform** meaningful analysis that answers a research question
3. **Create** clear, informative visualizations that support findings
4. **Write** a narrative that connects data, analysis, and conclusions
5. **Present** findings in a polished, reproducible marimo notebook
6. **Reflect** on the analytical process and identify limitations

---

## 16.2.1 The Capstone Workflow: From Raw Data to Deliverable

A finished capstone is not a pile of code cells — it is a structured document that walks a reader from a question to a defensible answer. Every step includes narrative *before* the code (what we are about to do and why) and *after* the code (what the results mean). That narrative thread is what separates a polished analysis from a collection of scripts.

### The Structure of a Finished Capstone

| Step | Purpose |
|------|---------|
| **1. Data Acquisition** | Obtain or generate the dataset |
| **2. Data Inspection** | Understand shape, types, and quality |
| **3. Data Cleaning** | Fix types, add computed columns, handle nulls |
| **4. Analysis with Polars** | Group, aggregate, and transform |
| **5. Analysis with DuckDB** *(optional)* | SQL-based cross-tabulations and window functions |
| **6. Visualizations** | Charts that answer the research question |
| **7. Executive Summary** | Written findings for a non-technical audience |
| **8. Limitations & Future Work** | What the analysis does not cover |
| **9. Reflection** | What you learned from the process |

### The Research Question

Every step below serves one question:

> **"How do location type, product category, and day of week affect revenue and customer traffic at a multi-location coffee shop chain?"**

The question has three independent variables (location, product, day) and two dependent variables (revenue, traffic) — specific enough to guide the analysis, broad enough to yield several distinct findings.

**The business context.** "Brewed Awakening" is a fictional coffee shop chain with five locations in different settings — downtown, near a university, inside an airport terminal, in a suburban strip mall, and in a shopping mall. Management wants to know which locations and products drive revenue, how traffic shifts across the week, and whether promotional campaigns work. The answers would inform staffing, inventory, and marketing decisions.

Note that this demonstration deliberately uses a *different* dataset from your Module 16.2 assignment (which analyzes a public library system). You practice every technique here on the coffee data; the assignment then asks you to transfer those techniques, not to copy results.

### Step 1: Data Acquisition

In a real capstone you would download a CSV from a public repository, call an API (Module 15), or scrape a page (Module 14). Here the notebook generates a synthetic dataset that mimics realistic coffee-shop sales patterns — the synthetic approach lets the instructor embed known patterns to demonstrate specific techniques, and the analysis workflow is identical either way.

Two ingredients matter. First, `random.seed(501)` makes the generation reproducible: anyone who runs the notebook gets identical numbers, which is a core principle of good analysis. Second, Python's built-in `date` and `timedelta` (from the `datetime` module) build the calendar: `date(2025, 1, 1)` is a specific day, adding `timedelta(days=n)` moves forward `n` days, and `.weekday()` returns 0 for Monday through 6 for Sunday — which is how each row gets its day-of-week label and weekend flag.

!!! example "Worked Example: Generating the Coffee-Shop Dataset"

    ```python
    import random
    from datetime import date, timedelta
    import polars as pl

    random.seed(501)

    stores = {
        "Downtown":   {"base_traffic": 220},
        "University": {"base_traffic": 180},
        "Airport":    {"base_traffic": 250},
        "Suburban":   {"base_traffic": 130},
        "Mall":       {"base_traffic": 170},
    }
    products = {
        "Coffee":   {"base_price": 4.50, "base_units": 45},
        "Tea":      {"base_price": 3.75, "base_units": 20},
        "Pastry":   {"base_price": 3.25, "base_units": 30},
        "Sandwich": {"base_price": 7.50, "base_units": 15},
        "Smoothie": {"base_price": 5.50, "base_units": 12},
    }

    start = date(2025, 1, 1)
    all_dates = [start + timedelta(days=d) for d in range(90)]

    rows = []
    for date_val in all_dates:
        is_weekend = date_val.weekday() >= 5
        weather = random.choices(
            ["Sunny", "Cloudy", "Rainy"],
            weights=[0.50, 0.30, 0.20],
            k=1,
        )[0]
        promo = random.random() < 0.20        # promo on ~20% of days
        promo_mult = 1.15 if promo else 1.0

        for store_name, store_info in stores.items():
            # store-level daily traffic: base * weekend adjustment
            # (Downtown -25%, University -15%, Airport +10%, Mall +30%,
            #  Suburban +15%) * weather effect * promo * random noise
            day_traffic = ...  # see the teaching notebook for the full formula

            for prod_name, prod_info in products.items():
                # units: base * store-product premium (Airport Coffee 1.4x,
                # University Smoothie 1.5x, Mall Pastry 1.3x) * promo * noise
                units = ...
                revenue = round(units * prod_info["base_price"]
                                * random.uniform(0.95, 1.05), 2)
                rows.append({
                    "store_id": store_name, "date": date_val,
                    "day_of_week": date_val.strftime("%A"),
                    "product_category": prod_name,
                    "units_sold": units, "revenue": revenue,
                    "customer_count": day_traffic, "weather": weather,
                    "is_weekend": is_weekend, "promo_active": promo,
                })

    sales_data = pl.DataFrame(rows)
    print(f"Dataset shape: {sales_data.shape[0]} rows x {sales_data.shape[1]} columns")
    print(sales_data.head(10))
    ```

    **Output:**

    ```
    Random seed: 501
    Coverage: 90 days x 5 stores x 5 product categories
    Dataset shape: 2250 rows x 10 columns
    Date range: 2025-01-01 to 2025-03-31

    First 10 rows (selected columns):
    shape: (10, 6)
    ┌────────────┬────────────┬──────────────────┬────────────┬─────────┬────────────────┐
    │ store_id   ┆ date       ┆ product_category ┆ units_sold ┆ revenue ┆ customer_count │
    │ ---        ┆ ---        ┆ ---              ┆ ---        ┆ ---     ┆ ---            │
    │ str        ┆ date       ┆ str              ┆ i64        ┆ f64     ┆ i64            │
    ╞════════════╪════════════╪══════════════════╪════════════╪═════════╪════════════════╡
    │ Downtown   ┆ 2025-01-01 ┆ Coffee           ┆ 51         ┆ 225.75  ┆ 202            │
    │ Downtown   ┆ 2025-01-01 ┆ Tea              ┆ 18         ┆ 68.97   ┆ 202            │
    │ Downtown   ┆ 2025-01-01 ┆ Pastry           ┆ 27         ┆ 91.67   ┆ 202            │
    │ Downtown   ┆ 2025-01-01 ┆ Sandwich         ┆ 14         ┆ 103.67  ┆ 202            │
    │ Downtown   ┆ 2025-01-01 ┆ Smoothie         ┆ 9          ┆ 50.77   ┆ 202            │
    │ University ┆ 2025-01-01 ┆ Coffee           ┆ 44         ┆ 201.47  ┆ 164            │
    │ University ┆ 2025-01-01 ┆ Tea              ┆ 19         ┆ 74.47   ┆ 164            │
    │ University ┆ 2025-01-01 ┆ Pastry           ┆ 28         ┆ 89.71   ┆ 164            │
    │ University ┆ 2025-01-01 ┆ Sandwich         ┆ 12         ┆ 85.76   ┆ 164            │
    │ University ┆ 2025-01-01 ┆ Smoothie         ┆ 14         ┆ 77.55   ┆ 164            │
    └────────────┴────────────┴──────────────────┴────────────┴─────────┴────────────────┘
    ```

    **Interpretation:** Each of the 2250 rows (90 days x 5 stores x 5 product categories) records one product's sales at one store on one day — the first row says Downtown sold 51 units of Coffee for $225.75 on 2025-01-01. Notice that `customer_count` (202 for Downtown that day) repeats across all five product rows for the same store-day: it is *store-level* daily foot traffic, not per-product traffic. Keeping that grain distinction in mind is essential later — summing it across product rows would count every visitor five times. The seed of 501 makes every number reproducible.

    *Source: `computations/module17_examples.py` — `demo_generate_dataset()`*

The generator embeds realistic business patterns on purpose: Airport and Downtown have the highest base foot traffic, weekend effects differ by store type (Downtown drops, Mall rises), promotions boost sales by roughly fifteen percent, and Coffee has the highest unit volume. A good analysis should *recover* these patterns from the data — which is exactly what the rest of the module does.

### Step 2: Data Inspection

Before any analysis, answer four fundamental questions — each maps to one method you already know:

1. **What columns do I have and what are their types?** — `schema`
2. **How much data is there?** — `shape`
3. **Are there missing values?** — `null_count()`
4. **What do the distributions look like?** — `describe()`

These checks take seconds and can reveal problems (wrong types, missing data, impossible ranges) before you invest hours in analysis built on sand.

!!! example "Worked Example: Schema, Nulls, and Summary Statistics"

    ```python
    print("Schema (column -> dtype):")
    for name, dtype in sales_data.schema.items():
        print(f"  {name}: {dtype}")

    print("\nNull values per column:")
    for name, count in zip(sales_data.columns, sales_data.null_count().row(0)):
        print(f"  {name}: {count}")

    print("\nSummary statistics for the numeric columns:")
    print(sales_data.select("units_sold", "revenue", "customer_count").describe())
    ```

    **Output:**

    ```
    Schema (column -> dtype):
      store_id: String
      date: Date
      day_of_week: String
      product_category: String
      units_sold: Int64
      revenue: Float64
      customer_count: Int64
      weather: String
      is_weekend: Boolean
      promo_active: Boolean

    Null values per column:
      store_id: 0
      date: 0
      day_of_week: 0
      product_category: 0
      units_sold: 0
      revenue: 0
      customer_count: 0
      weather: 0
      is_weekend: 0
      promo_active: 0

    Summary statistics for the numeric columns:
    shape: (9, 4)
    ┌────────────┬────────────┬────────────┬────────────────┐
    │ statistic  ┆ units_sold ┆ revenue    ┆ customer_count │
    │ ---        ┆ ---        ┆ ---        ┆ ---            │
    │ str        ┆ f64        ┆ f64        ┆ f64            │
    ╞════════════╪════════════╪════════════╪════════════════╡
    │ count      ┆ 2250.0     ┆ 2250.0     ┆ 2250.0         │
    │ null_count ┆ 0.0        ┆ 0.0        ┆ 0.0            │
    │ mean       ┆ 26.154222  ┆ 118.187147 ┆ 196.995556     │
    │ std        ┆ 14.979896  ┆ 61.778487  ┆ 51.20869       │
    │ min        ┆ 9.0        ┆ 47.11      ┆ 100.0          │
    │ 25%        ┆ 15.0       ┆ 75.82      ┆ 160.0          │
    │ 50%        ┆ 20.0       ┆ 97.55      ┆ 190.0          │
    │ 75%        ┆ 35.0       ┆ 135.86     ┆ 230.0          │
    │ max        ┆ 90.0       ┆ 400.22     ┆ 369.0          │
    └────────────┴────────────┴────────────┴────────────────┘
    ```

    **Interpretation:** The dataset is clean: every column shows 0 nulls, and the types are what they should be (a real `Date`, integers for counts, floats for money, booleans for flags). Ranges pass the sanity test for a coffee shop — daily per-product revenue runs from $47.11 to $400.22 with a mean of $118.19, units sold run 9 to 90, and daily store traffic runs 100 to 369 customers. In a real project this is where you would catch nulls, text-typed numbers, or impossible values; finding none, we can move straight to feature engineering.

    *Source: `computations/module17_examples.py` — `demo_inspect_dataset()`*

### Step 3: Data Cleaning & Feature Engineering

Even clean data usually needs **computed columns** that make the analysis easier. Two are added here, both patterns you met in Module 10:

- **`revenue_per_customer`** — revenue divided by store traffic. This normalizes revenue by how busy the location is, so a quiet store and a busy store can be compared on *efficiency* rather than raw volume.
- **`is_high_traffic`** — a boolean flag that is `True` when the day's customer count exceeds the median. It is the standard pattern for engineering a segment: compare a column against a threshold to label each row "busy" or "quiet."

The threshold comes from `.select(...).item()`: `select` returns a one-row, one-column DataFrame, and `.item()` pulls that single value out as a plain Python number.

!!! example "Worked Example: Two Engineered Columns"

    ```python
    median_traffic = sales_data.select(
        pl.col("customer_count").median()
    ).item()
    print(f"Median daily customer count: {median_traffic}")

    sales_clean = sales_data.with_columns(
        (pl.col("revenue") / pl.col("customer_count"))
        .round(2)
        .alias("revenue_per_customer"),
        (pl.col("customer_count") > median_traffic).alias("is_high_traffic"),
    )

    print(f"Cleaned dataset: {sales_clean.shape[0]} rows x {sales_clean.shape[1]} columns")
    print(sales_clean.head(5))
    ```

    **Output:**

    ```
    Median daily customer count: 189.5
    Cleaned dataset: 2250 rows x 12 columns

    First 5 rows (key columns):
    shape: (5, 6)
    ┌──────────┬──────────────────┬─────────┬────────────────┬──────────────────────┬─────────────────┐
    │ store_id ┆ product_category ┆ revenue ┆ customer_count ┆ revenue_per_customer ┆ is_high_traffic │
    │ ---      ┆ ---              ┆ ---     ┆ ---            ┆ ---                  ┆ ---             │
    │ str      ┆ str              ┆ f64     ┆ i64            ┆ f64                  ┆ bool            │
    ╞══════════╪══════════════════╪═════════╪════════════════╪══════════════════════╪═════════════════╡
    │ Downtown ┆ Coffee           ┆ 225.75  ┆ 202            ┆ 1.12                 ┆ true            │
    │ Downtown ┆ Tea              ┆ 68.97   ┆ 202            ┆ 0.34                 ┆ true            │
    │ Downtown ┆ Pastry           ┆ 91.67   ┆ 202            ┆ 0.45                 ┆ true            │
    │ Downtown ┆ Sandwich         ┆ 103.67  ┆ 202            ┆ 0.51                 ┆ true            │
    │ Downtown ┆ Smoothie         ┆ 50.77   ┆ 202            ┆ 0.25                 ┆ true            │
    └──────────┴──────────────────┴─────────┴────────────────┴──────────────────────┴─────────────────┘
    ```

    **Interpretation:** The dataset grows from ten columns to 12. On Downtown's first day, Coffee brought in $225.75 across 202 visitors — $1.12 of coffee revenue per person through the door — while Smoothies earned $0.25 per visitor. The day's traffic of 202 sits above the median of 189.5, so all five of its rows are flagged `true` for `is_high_traffic`. Because the flag uses a strict greater-than against the median, roughly half the rows land on each side.

    *Source: `computations/module17_examples.py` — `demo_clean_and_engineer()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "The data was generated clean, so inspection is a waste of time." | Inspection takes seconds and is how you *prove* the data is clean rather than assume it. In real projects, `describe()` and `null_count()` routinely surface text-typed numbers, sentinel values like `-999`, and gaps that would silently corrupt every later step. |
| "To get total store traffic, sum `customer_count`." | `customer_count` is store-*day* traffic repeated on each of the five product rows for that store-day. Summing it across raw rows counts every visitor five times. Use `.mean()`, `.first()` within a store-day group, or deduplicate first — the same trap appears (with checkouts) in your assignment. |
| "Adding a computed column changes `sales_data`." | Polars DataFrames are immutable. `with_columns()` returns a *new* DataFrame; the notebook assigns it to `sales_clean` and keeps the raw `sales_data` untouched — which is good practice, since you can always re-derive the clean version. |
| "Feature engineering means complicated math." | Both engineered columns here are one-liners: a ratio and a threshold comparison. The value is in choosing *which* simple derivation answers a business question — efficiency per visitor, busy-vs-quiet segmentation. |

---

## 16.2.2 Analysis with Polars

This is the core of the capstone: answering the research question through systematic aggregation. The pattern is always the one from Module 10 — `group_by().agg()`, then sort, then round for presentation — but the *choice of grouping* is what turns mechanics into insight. Five analyses each address a different facet of the question.

### Analysis 1: Revenue by Store — Volume vs. Efficiency

Which locations generate the most revenue, and which are most efficient per visitor? Grouping by `store_id` with both `revenue` sums and the engineered `revenue_per_customer` mean answers both at once.

!!! example "Worked Example: Store Summary with Two Rankings Hiding Inside"

    ```python
    store_summary = (
        sales_clean
        .group_by("store_id")
        .agg(
            pl.col("revenue").sum().alias("total_revenue"),
            pl.col("revenue").mean().alias("avg_product_rev"),
            pl.col("units_sold").sum().alias("total_units"),
            pl.col("customer_count").mean().round(1).alias("avg_traffic"),
            pl.col("revenue_per_customer").mean().alias("rev_per_customer"),
        )
        .sort("total_revenue", descending=True)
        .with_columns(
            pl.col("total_revenue").round(2),
            pl.col("avg_product_rev").round(2),
            pl.col("rev_per_customer").round(2),
        )
    )
    print(store_summary)
    ```

    **Output:**

    ```
    Store summary (sorted by total revenue):
    shape: (5, 6)
    ┌────────────┬───────────────┬─────────────────┬─────────────┬─────────────┬──────────────────┐
    │ store_id   ┆ total_revenue ┆ avg_product_rev ┆ total_units ┆ avg_traffic ┆ rev_per_customer │
    │ ---        ┆ ---           ┆ ---             ┆ ---         ┆ ---         ┆ ---              │
    │ str        ┆ f64           ┆ f64             ┆ i64         ┆ f64         ┆ f64              │
    ╞════════════╪═══════════════╪═════════════════╪═════════════╪═════════════╪══════════════════╡
    │ Airport    ┆ 58279.89      ┆ 129.51          ┆ 12883       ┆ 266.8       ┆ 0.49             │
    │ Mall       ┆ 53549.61      ┆ 119.0           ┆ 12051       ┆ 192.3       ┆ 0.63             │
    │ University ┆ 53207.12      ┆ 118.24          ┆ 11610       ┆ 178.2       ┆ 0.67             │
    │ Downtown   ┆ 50461.89      ┆ 112.14          ┆ 11150       ┆ 207.3       ┆ 0.55             │
    │ Suburban   ┆ 50422.57      ┆ 112.05          ┆ 11153       ┆ 140.4       ┆ 0.81             │
    └────────────┴───────────────┴─────────────────┴─────────────┴─────────────┴──────────────────┘
    ```

    **Interpretation:** Airport leads total revenue ($58,279.89), followed by Mall ($53,549.61) and University ($53,207.12), with Downtown ($50,461.89) and Suburban ($50,422.57) nearly tied at the bottom. But `rev_per_customer` tells almost the opposite story: Suburban earns the most per visitor ($0.81) and Airport the least ($0.49). Airport wins on sheer foot traffic (266.8 average daily customers), not on how much each customer spends. A busy store is not automatically an efficient one — the two metrics rank the locations in nearly reverse order, and a recommendation built on only one of them would mislead.

    *Source: `computations/module17_examples.py` — `demo_revenue_by_store()`*

### Analysis 2: Revenue by Product Category — Volume vs. Price

Which products carry the business? Adding a percent-of-total column turns raw sums into shares — note the expression `pl.col("total_revenue") / pl.col("total_revenue").sum()`, which divides each group's total by the grand total across groups.

!!! example "Worked Example: Product Shares of Total Revenue"

    ```python
    product_summary = (
        sales_clean
        .group_by("product_category")
        .agg(
            pl.col("revenue").sum().alias("total_revenue"),
            pl.col("units_sold").sum().alias("total_units"),
            pl.col("revenue").mean().alias("avg_revenue"),
        )
        .sort("total_revenue", descending=True)
        .with_columns(
            (pl.col("total_revenue") / pl.col("total_revenue").sum() * 100)
            .round(1)
            .alias("pct_of_total"),
            pl.col("total_revenue").round(2),
            pl.col("avg_revenue").round(2),
        )
    )
    print(product_summary)
    ```

    **Output:**

    ```
    Product summary (sorted by total revenue):
    shape: (5, 5)
    ┌──────────────────┬───────────────┬─────────────┬─────────────┬──────────────┐
    │ product_category ┆ total_revenue ┆ total_units ┆ avg_revenue ┆ pct_of_total │
    │ ---              ┆ ---           ┆ ---         ┆ ---         ┆ ---          │
    │ str              ┆ f64           ┆ i64         ┆ f64         ┆ f64          │
    ╞══════════════════╪═══════════════╪═════════════╪═════════════╪══════════════╡
    │ Coffee           ┆ 100787.08     ┆ 22421       ┆ 223.97      ┆ 37.9         │
    │ Sandwich         ┆ 50809.44      ┆ 6766        ┆ 112.91      ┆ 19.1         │
    │ Pastry           ┆ 47888.2       ┆ 14718       ┆ 106.42      ┆ 18.0         │
    │ Tea              ┆ 33858.94      ┆ 9031        ┆ 75.24       ┆ 12.7         │
    │ Smoothie         ┆ 32577.42      ┆ 5911        ┆ 72.39       ┆ 12.3         │
    └──────────────────┴───────────────┴─────────────┴─────────────┴──────────────┘
    ```

    **Interpretation:** Coffee dominates with 37.9% of all revenue ($100,787.08) — nearly double the runner-up. The second and third places illustrate a classic volume-versus-price trade-off: Sandwiches (19.1%) edge out Pastries (18.0%) on total revenue despite selling far fewer units — 6766 sandwiches against 14718 pastries — because each sandwich carries a much higher price. Tea (12.7%) and Smoothies (12.3%) round out the mix. When two products land within about one point of revenue share by completely different routes, staffing and inventory decisions for them should differ too.

    *Source: `computations/module17_examples.py` — `demo_revenue_by_product()`*

### Analysis 3: Weekday vs. Weekend — Traffic Moves, Spending Doesn't

Do weekend patterns differ by location type? Business intuition says Downtown should empty out on weekends (no office workers) while Mall fills up (shoppers). Grouping by *two* columns — `store_id` and `is_weekend` — produces one row per store-period combination, and a `pl.when().then().otherwise()` expression converts the boolean into a readable label.

!!! example "Worked Example: Weekend Effects Differ by Store Type"

    ```python
    weekend_analysis = (
        sales_clean
        .group_by("store_id", "is_weekend")
        .agg(
            pl.col("revenue").mean().alias("avg_revenue"),
            pl.col("customer_count").mean().alias("avg_traffic"),
            pl.col("units_sold").mean().alias("avg_units"),
        )
        .sort("store_id", "is_weekend")
        .with_columns(
            pl.when(pl.col("is_weekend"))
            .then(pl.lit("Weekend"))
            .otherwise(pl.lit("Weekday"))
            .alias("period"),
            pl.col("avg_revenue").round(2),
            pl.col("avg_traffic").round(1),
            pl.col("avg_units").round(1),
        )
    )
    print(weekend_analysis)
    ```

    **Output:**

    ```
    Weekday vs. weekend averages by store:
    shape: (10, 6)
    ┌────────────┬────────────┬─────────────┬─────────────┬───────────┬─────────┐
    │ store_id   ┆ is_weekend ┆ avg_revenue ┆ avg_traffic ┆ avg_units ┆ period  │
    │ ---        ┆ ---        ┆ ---         ┆ ---         ┆ ---       ┆ ---     │
    │ str        ┆ bool       ┆ f64         ┆ f64         ┆ f64       ┆ str     │
    ╞════════════╪════════════╪═════════════╪═════════════╪═══════════╪═════════╡
    │ Airport    ┆ false      ┆ 130.36      ┆ 258.1       ┆ 28.8      ┆ Weekday │
    │ Airport    ┆ true       ┆ 127.43      ┆ 288.3       ┆ 28.2      ┆ Weekend │
    │ Downtown   ┆ false      ┆ 111.56      ┆ 221.1       ┆ 24.7      ┆ Weekday │
    │ Downtown   ┆ true       ┆ 113.56      ┆ 173.4       ┆ 25.1      ┆ Weekend │
    │ Mall       ┆ false      ┆ 116.95      ┆ 177.0       ┆ 26.3      ┆ Weekday │
    │ Mall       ┆ true       ┆ 124.05      ┆ 229.9       ┆ 28.0      ┆ Weekend │
    │ Suburban   ┆ false      ┆ 111.6       ┆ 133.4       ┆ 24.7      ┆ Weekday │
    │ Suburban   ┆ true       ┆ 113.16      ┆ 157.4       ┆ 25.0      ┆ Weekend │
    │ University ┆ false      ┆ 117.97      ┆ 186.4       ┆ 25.7      ┆ Weekday │
    │ University ┆ true       ┆ 118.89      ┆ 158.1       ┆ 26.1      ┆ Weekend │
    └────────────┴────────────┴─────────────┴─────────────┴───────────┴─────────┘

    Weekend traffic change vs. weekday:
      Airport    +11.7%
      Downtown   -21.6%
      Mall       +29.9%
      Suburban   +18.0%
      University -15.2%
    ```

    **Interpretation:** The traffic patterns match the business intuition exactly: Downtown loses over a fifth of its traffic on weekends (-21.6%) as the office crowd disappears, Mall surges +29.9% with weekend shoppers, Airport rises a modest +11.7% (air travel ignores the work week), University dips -15.2%, and Suburban picks up +18.0% with families running errands. Now look at `avg_revenue`: it barely moves anywhere — Downtown weekdays average $111.56 per product-day against $113.56 on weekends even while its traffic collapses. Weekend visitors spend about the same per head as weekday visitors, so this finding is a *staffing* signal (Downtown can trim weekend shifts; Mall should staff up), not a revenue story.

    *Source: `computations/module17_examples.py` — `demo_weekend_patterns()`*

### Analysis 4: The Promotional Effect

Do promotional days generate meaningfully higher revenue? Grouping by the `promo_active` flag splits the whole dataset into two pools; a second grouping by store checks whether the effect is uniform. (The per-store table also feeds Chart 6 in §16.2.4.)

!!! example "Worked Example: Promo Days vs. Regular Days"

    ```python
    promo_effect = (
        sales_clean
        .group_by("promo_active")
        .agg(
            pl.col("revenue").mean().alias("avg_revenue"),
            pl.col("units_sold").mean().alias("avg_units"),
            pl.col("customer_count").mean().alias("avg_traffic"),
            pl.len().alias("num_records"),
        )
        .sort("promo_active")
        .with_columns(
            pl.when(pl.col("promo_active"))
            .then(pl.lit("Promo Day")).otherwise(pl.lit("Regular Day"))
            .alias("day_type"),
            pl.col("avg_revenue").round(2),
            pl.col("avg_units").round(1),
            pl.col("avg_traffic").round(1),
        )
    )
    print(promo_effect)

    # Is the lift uniform? Repeat the grouping per store.
    promo_by_store = (
        sales_clean
        .group_by("store_id", "promo_active")
        .agg(pl.col("revenue").mean().alias("avg_revenue"))
        .with_columns(
            pl.when(pl.col("promo_active"))
            .then(pl.lit("Promo")).otherwise(pl.lit("No Promo"))
            .alias("promo_label"),
            pl.col("avg_revenue").round(2),
        )
        .sort("store_id", "promo_active")
        .select("store_id", "promo_label", "avg_revenue")
    )
    print(promo_by_store)
    ```

    **Output:**

    ```
    Promotional effect (all stores pooled):
    shape: (2, 6)
    ┌──────────────┬─────────────┬───────────┬─────────────┬─────────────┬─────────────┐
    │ promo_active ┆ avg_revenue ┆ avg_units ┆ avg_traffic ┆ num_records ┆ day_type    │
    │ ---          ┆ ---         ┆ ---       ┆ ---         ┆ ---         ┆ ---         │
    │ bool         ┆ f64         ┆ f64       ┆ f64         ┆ u32         ┆ str         │
    ╞══════════════╪═════════════╪═══════════╪═════════════╪═════════════╪═════════════╡
    │ false        ┆ 113.75      ┆ 25.2      ┆ 190.4       ┆ 1675        ┆ Regular Day │
    │ true         ┆ 131.12      ┆ 28.9      ┆ 216.3       ┆ 575         ┆ Promo Day   │
    └──────────────┴─────────────┴───────────┴─────────────┴─────────────┴─────────────┘

    Promo-day lift in average revenue: +15.3%

    Average revenue per product-day, by store and promo status:
    shape: (10, 3)
    ┌────────────┬─────────────┬─────────────┐
    │ store_id   ┆ promo_label ┆ avg_revenue │
    │ ---        ┆ ---         ┆ ---         │
    │ str        ┆ str         ┆ f64         │
    ╞════════════╪═════════════╪═════════════╡
    │ Airport    ┆ No Promo    ┆ 125.85      │
    │ Airport    ┆ Promo       ┆ 140.17      │
    │ Downtown   ┆ No Promo    ┆ 107.3       │
    │ Downtown   ┆ Promo       ┆ 126.22      │
    │ Mall       ┆ No Promo    ┆ 114.23      │
    │ Mall       ┆ Promo       ┆ 132.9       │
    │ Suburban   ┆ No Promo    ┆ 107.43      │
    │ Suburban   ┆ Promo       ┆ 125.5       │
    │ University ┆ No Promo    ┆ 113.93      │
    │ University ┆ Promo       ┆ 130.8       │
    └────────────┴─────────────┴─────────────┘
    ```

    **Interpretation:** Promo days average $131.12 of revenue per product-day against $113.75 on regular days — a +15.3% lift — with traffic up as well (216.3 vs. 190.4). The per-store view shows the lift at every location (Airport 125.85 to 140.17, Downtown 107.3 to 126.22, and so on), so the promotion mechanism works broadly rather than favoring certain stores. Two cautions belong in the write-up: the comparison rests on 575 promo records against 1675 regular ones, and a revenue lift is not proof of *profit* — that verdict needs promotion-cost and margin data the dataset does not contain.

    *Source: `computations/module17_examples.py` — `demo_promo_effect()`*

### Analysis 5: Weather — A Traffic Lever, Not a Revenue Lever

Does weather affect the business, and if so, where does it show up — foot traffic, revenue, or both? This distinction matters for operations: you can plan staffing around a traffic predictor even if revenue per product barely moves.

!!! example "Worked Example: Weather Moves Traffic but Not Spending"

    ```python
    weather_summary = (
        sales_clean
        .group_by("weather")
        .agg(
            pl.col("revenue").mean().alias("avg_revenue"),
            pl.col("revenue").sum().alias("total_revenue"),
            pl.col("customer_count").mean().alias("avg_traffic"),
            pl.col("units_sold").mean().alias("avg_units"),
            pl.len().alias("num_records"),
        )
        .sort("avg_traffic", descending=True)
        .with_columns(
            pl.col("avg_revenue").round(2),
            pl.col("total_revenue").round(2),
            pl.col("avg_traffic").round(1),
            pl.col("avg_units").round(1),
        )
    )
    print(weather_summary)
    ```

    **Output:**

    ```
    Weather summary (sorted by average traffic):
    shape: (3, 6)
    ┌─────────┬─────────────┬───────────────┬─────────────┬───────────┬─────────────┐
    │ weather ┆ avg_revenue ┆ total_revenue ┆ avg_traffic ┆ avg_units ┆ num_records │
    │ ---     ┆ ---         ┆ ---           ┆ ---         ┆ ---       ┆ ---         │
    │ str     ┆ f64         ┆ f64           ┆ f64         ┆ f64       ┆ u32         │
    ╞═════════╪═════════════╪═══════════════╪═════════════╪═══════════╪═════════════╡
    │ Sunny   ┆ 118.07      ┆ 135779.86     ┆ 207.4       ┆ 26.2      ┆ 1150        │
    │ Cloudy  ┆ 116.63      ┆ 58314.06      ┆ 192.2       ┆ 25.8      ┆ 500         │
    │ Rainy   ┆ 119.71      ┆ 71827.16      ┆ 181.0       ┆ 26.4      ┆ 600         │
    └─────────┴─────────────┴───────────────┴─────────────┴───────────┴─────────────┘

    Sunny-vs-rainy traffic swing: +14.6%
    ```

    **Interpretation:** Sunny days draw the most customers (207.4 on average) and rainy days the fewest (181.0) — a +14.6% swing in foot traffic. Yet average revenue per product-day is nearly flat across all three conditions (from 116.63 to 119.71, with rainy days actually highest): the customers who do come in spend about the same regardless of the sky. Operationally, a weather forecast is therefore a rough *staffing* predictor, not a revenue predictor — trim the crew on a forecasted rainy day, but do not expect the day's revenue-per-visitor economics to change.

    *Source: `computations/module17_examples.py` — `demo_weather_impact()`*

### What the Five Analyses Add Up To

A consistent picture emerges across the five group-bys — and notice how often *traffic* and *revenue* move independently:

| Factor | Impact |
|--------|--------|
| **Location** | Strong on revenue — Airport leads; per-visitor efficiency nearly reverses the ranking |
| **Product** | Strong on revenue — Coffee dominates; Sandwich and Pastry tie by different routes |
| **Weekday/Weekend** | Strong on traffic, weak on revenue — direction depends on store type |
| **Promotions** | Moderate on revenue — a consistent lift at every store; profitability unknown |
| **Weather** | Clear on traffic, negligible on revenue — sunny draws crowds, rainy thins them |

The most actionable conclusion is that **location-specific strategies** (staffing, inventory, promotions) would outperform a uniform approach — and that traffic and revenue are separate levers that do not always move together.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "The store with the most revenue is the best-performing store." | Best *at what*? Airport leads total revenue but earns the least per visitor; Suburban is the reverse. Always decide which metric answers the actual business question before ranking. |
| "If average revenue barely changes, the factor doesn't matter." | Weekend and weather effects move *traffic* substantially while leaving per-product revenue flat. A factor can matter enormously for staffing and capacity even when it is invisible in revenue-per-row. |
| "A 15% revenue lift proves promotions pay off." | The lift is real, but promotions have costs (discounts, advertising) that this dataset does not record. Revenue analysis bounds the answer; only margin data settles it. Saying so explicitly belongs in the limitations section. |
| "`group_by` returns groups in a predictable order." | Group order is not guaranteed. Every analysis above ends with an explicit `.sort()` — a presentation habit that also makes reruns reproducible line-for-line. |

---

## 16.2.3 Analysis with DuckDB

DuckDB (Module 13) lets you write SQL directly against a Polars DataFrame — `duckdb.register()` makes the DataFrame visible to SQL under a table name, and `.pl()` converts each result back to Polars so the workflow stays consistent. Nothing here *requires* SQL; the point is tool choice. Cross-tabulations and window functions often read more naturally in SQL, while method-chaining transformations are often cleaner in Polars.

### A Cross-Tabulation in SQL

What is total revenue for every combination of store and product? This "pivot-table" question is a two-column `GROUP BY` — bread and butter in SQL.

!!! example "Worked Example: Store x Product Cross-Tabulation"

    ```python
    import duckdb

    duckdb.register("sales_clean", sales_clean)

    cross_tab = duckdb.sql("""
        SELECT
            store_id,
            product_category,
            ROUND(SUM(revenue), 2)  AS total_revenue,
            SUM(units_sold)         AS total_units,
            ROUND(AVG(revenue), 2)  AS avg_revenue
        FROM sales_clean
        GROUP BY store_id, product_category
        ORDER BY store_id, total_revenue DESC
    """).pl()

    print(cross_tab.head(10))
    ```

    **Output:**

    ```
    Cross-tabulation: 25 rows (5 stores x 5 products)

    First 10 rows (Airport and Downtown):
    shape: (10, 5)
    ┌──────────┬──────────────────┬───────────────┬───────────────┬─────────────┐
    │ store_id ┆ product_category ┆ total_revenue ┆ total_units   ┆ avg_revenue │
    │ ---      ┆ ---              ┆ ---           ┆ ---           ┆ ---         │
    │ str      ┆ str              ┆ f64           ┆ decimal[38,0] ┆ f64         │
    ╞══════════╪══════════════════╪═══════════════╪═══════════════╪═════════════╡
    │ Airport  ┆ Coffee           ┆ 26225.13      ┆ 5819          ┆ 291.39      │
    │ Airport  ┆ Sandwich         ┆ 10111.83      ┆ 1342          ┆ 112.35      │
    │ Airport  ┆ Pastry           ┆ 9148.86       ┆ 2812          ┆ 101.65      │
    │ Airport  ┆ Tea              ┆ 6848.4        ┆ 1829          ┆ 76.09       │
    │ Airport  ┆ Smoothie         ┆ 5945.67       ┆ 1081          ┆ 66.06       │
    │ Downtown ┆ Coffee           ┆ 18764.39      ┆ 4175          ┆ 208.49      │
    │ Downtown ┆ Sandwich         ┆ 10183.89      ┆ 1362          ┆ 113.15      │
    │ Downtown ┆ Pastry           ┆ 8993.26       ┆ 2762          ┆ 99.93       │
    │ Downtown ┆ Tea              ┆ 6715.67       ┆ 1795          ┆ 74.62       │
    │ Downtown ┆ Smoothie         ┆ 5804.68       ┆ 1056          ┆ 64.5        │
    └──────────┴──────────────────┴───────────────┴───────────────┴─────────────┘

    Top product by revenue at each store:
      Airport    Coffee  ($26,225.13)
      Downtown   Coffee  ($18,764.39)
      Mall       Coffee  ($18,746.75)
      Suburban   Coffee  ($18,627.65)
      University Coffee  ($18,423.16)
    ```

    **Interpretation:** All 25 store-product combinations come back in one query, and the bottom lines settle a question at a glance: Coffee is the top earner at *every* store, but the gap varies — Airport's Coffee revenue ($26,225.13) towers over its own runner-up and over every other store's Coffee (all near $18,423.16–$18,764.39), reflecting the traveler demand premium. One dtype detail: `total_units` comes back as `decimal[38,0]` because DuckDB's `SUM` over integers promotes to a wide decimal type on the way through `.pl()` — the values are exact, just displayed with a different dtype than a native Polars sum.

    *Source: `computations/module17_examples.py` — `demo_sql_crosstab()`*

### Window Functions: The 7-Day Rolling Average

Window functions compute values across a "window" of related rows *without collapsing them* — unlike `GROUP BY`, every input row survives. Here a CTE (`WITH daily_totals AS ...`) first aggregates to one row per store per day, then `AVG(...) OVER (PARTITION BY store_id ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)` averages each day with the six days before it, per store. The rolling average smooths day-to-day noise so trends become visible.

!!! example "Worked Example: Rolling Average via CTE + Window Function"

    ```python
    duckdb.register("sales_clean", sales_clean)

    rolling_avg = duckdb.sql("""
        WITH daily_totals AS (
            SELECT
                store_id,
                date,
                SUM(revenue) AS daily_revenue
            FROM sales_clean
            GROUP BY store_id, date
        )
        SELECT
            store_id,
            date,
            ROUND(daily_revenue, 2) AS daily_revenue,
            ROUND(
                AVG(daily_revenue) OVER (
                    PARTITION BY store_id
                    ORDER BY date
                    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
                ),
                2
            ) AS rolling_7d_avg
        FROM daily_totals
        ORDER BY store_id, date
    """).pl()

    print(f"Rolling average table: {rolling_avg.shape[0]} rows")
    print(rolling_avg.head(10))
    ```

    **Output:**

    ```
    Rolling average table: 450 rows

    First 10 rows (Airport, early January):
    shape: (10, 4)
    ┌──────────┬────────────┬───────────────┬────────────────┐
    │ store_id ┆ date       ┆ daily_revenue ┆ rolling_7d_avg │
    │ ---      ┆ ---        ┆ ---           ┆ ---            │
    │ str      ┆ date       ┆ f64           ┆ f64            │
    ╞══════════╪════════════╪═══════════════╪════════════════╡
    │ Airport  ┆ 2025-01-01 ┆ 666.89        ┆ 666.89         │
    │ Airport  ┆ 2025-01-02 ┆ 618.94        ┆ 642.92         │
    │ Airport  ┆ 2025-01-03 ┆ 740.26        ┆ 675.36         │
    │ Airport  ┆ 2025-01-04 ┆ 630.49        ┆ 664.15         │
    │ Airport  ┆ 2025-01-05 ┆ 519.82        ┆ 635.28         │
    │ Airport  ┆ 2025-01-06 ┆ 574.58        ┆ 625.16         │
    │ Airport  ┆ 2025-01-07 ┆ 712.25        ┆ 637.6          │
    │ Airport  ┆ 2025-01-08 ┆ 695.14        ┆ 641.64         │
    │ Airport  ┆ 2025-01-09 ┆ 579.97        ┆ 636.07         │
    │ Airport  ┆ 2025-01-10 ┆ 627.56        ┆ 619.97         │
    └──────────┴────────────┴───────────────┴────────────────┘
    ```

    **Interpretation:** The CTE collapses the product-level rows to 450 store-days; the window function then adds a column *alongside* `daily_revenue` rather than replacing it. You can verify the mechanics by hand on the first rows: on 2025-01-01 the window holds only one day, so `rolling_7d_avg` equals `daily_revenue` (666.89); on 2025-01-02 it is the mean of 666.89 and 618.94, which is 642.92. From the seventh row on, each value averages a full week. Where the raw column jumps around (519.82 one day, 712.25 two days later), the rolling column drifts gently — never leaving the band between 619.97 and 675.36 in these ten rows — and that smoothing is exactly what makes trends visible in the trend chart later in the chapter.

    *Source: `computations/module17_examples.py` — `demo_sql_rolling_average()`*

### Same Question, Two Tools

To prove Polars and DuckDB agree, here is the store revenue summary from Analysis 1 rewritten in SQL. Choosing between them is style, not correctness.

!!! example "Worked Example: The Store Summary in SQL Matches Polars"

    ```python
    duckdb.register("sales_clean", sales_clean)

    store_sql = duckdb.sql("""
        SELECT
            store_id,
            ROUND(SUM(revenue), 2)  AS total_revenue,
            ROUND(AVG(revenue), 2)  AS avg_product_rev,
            SUM(units_sold)         AS total_units
        FROM sales_clean
        GROUP BY store_id
        ORDER BY total_revenue DESC
    """).pl()

    print(store_sql)
    ```

    **Output:**

    ```
    Store summary via DuckDB SQL:
    shape: (5, 4)
    ┌────────────┬───────────────┬─────────────────┬───────────────┐
    │ store_id   ┆ total_revenue ┆ avg_product_rev ┆ total_units   │
    │ ---        ┆ ---           ┆ ---             ┆ ---           │
    │ str        ┆ f64           ┆ f64             ┆ decimal[38,0] │
    ╞════════════╪═══════════════╪═════════════════╪═══════════════╡
    │ Airport    ┆ 58279.89      ┆ 129.51          ┆ 12883         │
    │ Mall       ┆ 53549.61      ┆ 119.0           ┆ 12051         │
    │ University ┆ 53207.12      ┆ 118.24          ┆ 11610         │
    │ Downtown   ┆ 50461.89      ┆ 112.14          ┆ 11150         │
    │ Suburban   ┆ 50422.57      ┆ 112.05          ┆ 11153         │
    └────────────┴───────────────┴─────────────────┴───────────────┘
    ```

    **Interpretation:** Every figure — Airport's 58279.89 down to Suburban's 50422.57, and all the unit totals — matches the Polars `group_by` version exactly. In practice you pick whichever tool makes a given query easier to write *and read*: SQL tends to win for cross-tabulations and window functions, Polars for chained transformations and conditional logic. A capstone that uses both, each where it is strongest, reads as fluency rather than indecision.

    *Source: `computations/module17_examples.py` — `demo_sql_vs_polars()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "DuckDB needs the data exported to a database first." | `duckdb.register("name", df)` exposes the in-memory Polars DataFrame to SQL directly — no copy, no file, no server. The `.pl()` on the way out returns you to Polars. |
| "A window function is just a `GROUP BY` with extra syntax." | `GROUP BY` collapses rows (450 store-days from 2250 product rows); a window function keeps every row and adds a column computed over its window. If your result must keep daily rows *and* show a weekly average, you need a window. |
| "SQL and Polars might give slightly different numbers." | On the same data and the same logic they agree to the cent, as the side-by-side store summary shows. Differences you do observe come from differing logic (filters, null handling, rounding), never from the engine "flavoring" arithmetic. |
| "Result dtypes always survive the round trip unchanged." | DuckDB promotes integer `SUM`s to a wide decimal type, which Polars displays as `decimal[38,0]`. Values are exact; only the dtype label differs. Check dtypes after any engine hand-off. |

---

## 16.2.4 Visualizations and Interactive Elements

Visualizations translate numbers into patterns an audience can absorb quickly. A good capstone includes four to six charts, each with a clear title, labeled axes, and a written interpretation — a chart without a sentence underneath is a puzzle, not a finding. The examples use Plotly Express; `.to_pandas()` converts each Polars DataFrame on the way in, matching the convention from Module 11. Because charts render as figures rather than text, the worked examples in this section verify the *numbers behind* the charts; the chart code itself is shown for each.

### Chart 1: Total Revenue by Store

```python
import plotly.express as px

fig = px.bar(
    store_summary.to_pandas(),
    x="store_id",
    y="total_revenue",
    title="Total Revenue by Store (Q1 2025)",
    labels={"store_id": "Store Location", "total_revenue": "Total Revenue ($)"},
    color="store_id",
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig.update_layout(showlegend=False, template="plotly_white",
                  xaxis_categoryorder="total descending")
fig
```

The bar chart makes the ranking from §16.2.2 Analysis 1 legible in one glance: Airport first, then Mall and University, with Downtown and Suburban nearly tied. Just as important is what the *scale* shows — the gap between the tallest and shortest bars is modest, not a runaway lead, so location is a smaller lever than the product mix, and the per-visitor efficiency ranking runs in nearly the opposite order.

### Chart 2: Revenue by Product Category Across Stores

```python
fig = px.bar(
    cross_tab.to_pandas(),
    x="store_id",
    y="total_revenue",
    color="product_category",
    barmode="group",
    title="Revenue by Product Category Across Stores",
    labels={"store_id": "Store Location", "total_revenue": "Total Revenue ($)",
            "product_category": "Product"},
    color_discrete_sequence=px.colors.qualitative.Pastel,
)
fig.update_layout(template="plotly_white", xaxis_categoryorder="total descending",
                  legend_title_text="Product")
fig
```

Built on the §16.2.3 cross-tabulation, the grouped bars show Coffee dominating at every location while the *secondary* products vary: the Airport's Coffee bar towers over its neighbors (travelers grabbing a quick cup), University shows relatively stronger Smoothie performance, and Mall a notable Pastry component. The chart argues visually for location-specific inventory allocation.

### Chart 3: Daily Revenue Trend with Rolling Average

```python
downtown = rolling_avg.filter(pl.col("store_id") == "Downtown").to_pandas()

fig = px.line(
    downtown,
    x="date",
    y="rolling_7d_avg",
    title="Downtown Store: 7-Day Rolling Average Revenue",
    labels={"date": "Date", "rolling_7d_avg": "7-Day Rolling Avg Revenue ($)"},
)
fig.add_scatter(x=downtown["date"], y=downtown["daily_revenue"],
                mode="markers", name="Daily Revenue",
                marker=dict(size=4, opacity=0.4))
fig.update_layout(template="plotly_white")
fig
```

Filtering the §16.2.3 rolling-average table to one store keeps the trend line clean. The solid line (rolling average) drifts gently while the faint dots (daily values) scatter around it — the smoothing hides promo-day spikes and random noise so that any *sustained* upward or downward slope would stand out. In this quarter the Downtown line is essentially flat: stable demand, no seasonal drift.

### Chart 4: Customer Traffic vs. Daily Revenue

The scatter plot asks a relationship question rather than a ranking question: do busier days earn more? To draw it, the product rows must first be aggregated to store-days (summing revenue, and taking `.first()` of the repeated `customer_count` — *not* summing it).

!!! example "Worked Example: The Numbers Behind the Scatter Plot"

    ```python
    daily = (
        sales_clean
        .group_by("store_id", "date")
        .agg(
            pl.col("revenue").sum().alias("daily_revenue"),
            pl.col("customer_count").first().alias("customer_count"),
        )
    )

    fig = px.scatter(
        daily.to_pandas(),
        x="customer_count", y="daily_revenue", color="store_id",
        title="Customer Traffic vs. Daily Revenue by Store",
        labels={"customer_count": "Daily Customer Count",
                "daily_revenue": "Daily Revenue ($)", "store_id": "Store"},
        opacity=0.6,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(template="plotly_white", legend_title_text="Store")
    fig
    ```

    **Output:**

    ```
    Scatter data: 450 store-day points (5 stores x 90 days)
    Correlation between daily traffic and daily revenue: 0.47

    Per-store daily averages (the center of each scatter cluster):
    shape: (5, 4)
    ┌────────────┬─────────────┬───────────────────┬─────────────────────┐
    │ store_id   ┆ avg_traffic ┆ avg_daily_revenue ┆ revenue_per_visitor │
    │ ---        ┆ ---         ┆ ---               ┆ ---                 │
    │ str        ┆ f64         ┆ f64               ┆ f64                 │
    ╞════════════╪═════════════╪═══════════════════╪═════════════════════╡
    │ Airport    ┆ 266.8       ┆ 647.55            ┆ 2.43                │
    │ Downtown   ┆ 207.3       ┆ 560.69            ┆ 2.7                 │
    │ Mall       ┆ 192.3       ┆ 595.0             ┆ 3.09                │
    │ University ┆ 178.2       ┆ 591.19            ┆ 3.32                │
    │ Suburban   ┆ 140.4       ┆ 560.25            ┆ 3.99                │
    └────────────┴─────────────┴───────────────────┴─────────────────────┘
    ```

    **Interpretation:** Across 450 store-day points, traffic and revenue correlate positively (0.47) — busier days do earn more — but the per-store cluster centers reveal the twist the chart makes visible: the *slope* differs by store, and not in the direction you might guess. Suburban sits far left (140.4 average daily customers) yet earns $3.99 per visitor, while Airport sits far right (266.8) at just $2.43 per visitor. Revenue per visitor is *highest* at the lower-traffic stores — the same efficiency reversal from the store summary, now with a geometric explanation: Airport's cluster is farther right but not proportionally higher.

    *Source: `computations/module17_examples.py` — `demo_scatter_numbers()`*

### Chart 5: Weekday vs. Weekend Traffic Patterns

```python
fig = px.bar(
    weekend_analysis.to_pandas(),
    x="store_id",
    y="avg_traffic",
    color="period",
    barmode="group",
    title="Average Daily Traffic: Weekday vs. Weekend by Store",
    labels={"store_id": "Store Location", "avg_traffic": "Avg Daily Customer Count",
            "period": "Period"},
    color_discrete_map={"Weekday": "#4C78A8", "Weekend": "#F4A261"},
)
fig.update_layout(template="plotly_white", xaxis_categoryorder="total descending",
                  legend_title_text="Period")
fig
```

Paired bars per store make the §16.2.2 Analysis 3 pattern visible at a glance: Downtown's weekend bar drops well below its weekday bar, Mall's does the reverse, and Airport's pair is nearly even. Because revenue per product-day barely moves across these swings, the actionable signal is staffing — reduce Downtown's Saturday crew, plan for Mall's weekend peak.

### Chart 6: Promotional Impact by Store

```python
fig = px.bar(
    promo_by_store.to_pandas(),
    x="store_id",
    y="avg_revenue",
    color="promo_label",
    barmode="group",
    title="Promotional Impact on Average Revenue by Store",
    labels={"store_id": "Store Location",
            "avg_revenue": "Avg Revenue per Product-Day ($)",
            "promo_label": "Promotion"},
    color_discrete_map={"Promo": "#59A14F", "No Promo": "#E15759"},
)
fig.update_layout(template="plotly_white", xaxis_categoryorder="total descending",
                  legend_title_text="Promotion Status")
fig
```

Using the per-store promo table from §16.2.2 Analysis 4, every store shows a green (Promo) bar above its red (No Promo) bar by a similar proportion — visual evidence that the promotion mechanism works uniformly rather than benefiting only certain locations. The honest caption writes itself: promotions lift revenue everywhere; whether they lift *profit* requires cost data we do not have.

### Interactive Exploration with Marimo Widgets

A polished capstone notebook can let the reader explore the data themselves. Instead of building a separate chart for every store, you build **one chart driven by a dropdown** — the marimo pattern from Module 12: create the widgets in one cell and *return* them, then read `.value` in another cell. When the user changes a widget, marimo re-runs the downstream cell automatically; there are no callbacks and no refresh button.

```python
# Cell 1: create the widgets (returned as cross-cell exports)
stores = sales_clean["store_id"].unique().sort().to_list()

store_picker = mo.ui.dropdown(
    options=stores,
    value=stores[0],
    label="Select a store:",
)
rev_threshold = mo.ui.slider(
    start=0, stop=500, step=25, value=100,
    label="Minimum daily product revenue ($):",
)
mo.hstack([store_picker, rev_threshold], justify="start")
```

```python
# Cell 2: read .value and build the reactive chart
filtered = sales_clean.filter(
    (pl.col("store_id") == store_picker.value)
    & (pl.col("revenue") >= rev_threshold.value)
)
summary = (
    filtered
    .group_by("product_category")
    .agg(pl.col("revenue").sum().alias("total_revenue"),
         pl.col("units_sold").sum().alias("total_units"))
    .sort("total_revenue", descending=True)
)
px.bar(summary.to_pandas(), x="product_category", y="total_revenue",
       title=f"{store_picker.value}: Revenue by Product "
             f"(min ${rev_threshold.value}/day)")
```

Because a course companion page cannot host a live widget, the worked example below *simulates* one widget state — the values a user might have selected — and shows exactly what the reactive cell would compute.

!!! example "Worked Example: What the Reactive Cell Computes for One Widget State"

    ```python
    selected_store = "University"  # simulates store_picker.value
    min_revenue = 100              # simulates rev_threshold.value

    store_rows = sales_clean.filter(pl.col("store_id") == selected_store)
    filtered = store_rows.filter(pl.col("revenue") >= min_revenue)
    print(f"Rows for {selected_store}: {store_rows.shape[0]}")
    print(f"Rows kept after the filter: {filtered.shape[0]}")

    summary = (
        filtered
        .group_by("product_category")
        .agg(
            pl.col("revenue").sum().round(2).alias("total_revenue"),
            pl.col("units_sold").sum().alias("total_units"),
            pl.len().alias("days_kept"),
        )
        .sort("total_revenue", descending=True)
    )
    print(summary)
    ```

    **Output:**

    ```
    Simulated widget state:
      store_picker.value  = 'University'
      rev_threshold.value = 100

    Rows for University: 450
    Rows kept after the revenue >= $100 filter: 238

    What the reactive chart would display:
    shape: (5, 4)
    ┌──────────────────┬───────────────┬─────────────┬───────────┐
    │ product_category ┆ total_revenue ┆ total_units ┆ days_kept │
    │ ---              ┆ ---           ┆ ---         ┆ ---       │
    │ str              ┆ f64           ┆ i64         ┆ u32       │
    ╞══════════════════╪═══════════════╪═════════════╪═══════════╡
    │ Coffee           ┆ 18423.16      ┆ 4108        ┆ 90        │
    │ Sandwich         ┆ 7909.01       ┆ 1052        ┆ 64        │
    │ Smoothie         ┆ 4684.56       ┆ 846         ┆ 42        │
    │ Pastry           ┆ 4541.08       ┆ 1385        ┆ 40        │
    │ Tea              ┆ 207.42        ┆ 55          ┆ 2         │
    └──────────────────┴───────────────┴─────────────┴───────────┘
    ```

    **Interpretation:** With the dropdown on University and the slider at $100, the filter keeps 238 of the store's 450 product-day rows. The surviving mix is revealing: Coffee cleared the $100 bar on all 90 days ($18,423.16 total), Smoothie — a University specialty — on 42 days, while Tea cleared it on only 2 days ($207.42), nearly vanishing from the chart. Change either widget and marimo recomputes this table and its chart instantly; that "one chart, many views" pattern is what makes an interactive notebook feel like a dashboard.

    *Source: `computations/module17_examples.py` — `demo_widget_simulation()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "More charts make a stronger capstone." | Choosing the four to six charts that best answer the research question is an editorial decision. Dozens of charts are *possible*; a reader's attention is the scarce resource. |
| "A good chart speaks for itself." | Every chart in a capstone gets a written interpretation. The chart shows the pattern; the sentence says what it means for the business and what to do about it. |
| "Interactive widgets need callback functions or a refresh button." | In marimo, reading `widget.value` in another cell creates the dependency; changing the widget re-runs that cell automatically. Create the widget in one cell, read `.value` in another — that is the entire pattern. |
| "Summing `customer_count` per store-day is fine for the scatter plot." | The scatter aggregation uses `.first()` on `customer_count` precisely because the value repeats across the five product rows of a store-day. Summing would quintuple traffic and silently rescale the x-axis. |

---

## 16.2.5 Communicating Results

Analysis that never becomes a decision is a hobby. The last three steps of the capstone — executive summary, limitations, reflection — are pure writing, and they are weighted heavily in your assignment precisely because they are what separates an analyst from a script.

### The Executive Summary

An executive summary distills the entire analysis into a narrative a non-technical reader can absorb in two minutes. It answers the research question directly, leads with findings (not methods), attaches a number to each claim, and ends with a recommendation. It is often the *only* part a decision-maker reads.

Before writing one, gather the headline numbers in one place — pulling them fresh from the data rather than retyping them from memory prevents the classic embarrassment of a summary that contradicts its own appendix.

!!! example "Worked Example: Assembling the Headline Numbers"

    ```python
    total_revenue = sales_clean["revenue"].sum()
    print(f"Total Q1 revenue, all stores and products: ${total_revenue:,.2f}")

    store_totals = (
        sales_clean
        .group_by("store_id")
        .agg(
            pl.col("revenue").sum().round(2).alias("total_revenue"),
            pl.col("revenue_per_customer").mean().round(2).alias("rev_per_customer"),
        )
        .sort("total_revenue", descending=True)
    )
    for rank, (store, rev, _) in enumerate(store_totals.iter_rows(), start=1):
        print(f"  {rank}. {store:<10} ${rev:,.2f}")
    # ... plus the ratio, efficiency extremes, Coffee share,
    #     promo lift, and weekend swings (full code in the source file)
    ```

    **Output:**

    ```
    Headline numbers for the executive summary
    ------------------------------------------
    Total Q1 revenue, all stores and products: $265,921.08

    Store revenue ranking:
      1. Airport    $58,279.89
      2. Mall       $53,549.61
      3. University $53,207.12
      4. Downtown   $50,461.89
      5. Suburban   $50,422.57
    Top-to-bottom store revenue ratio: 1.16

    Revenue per customer (efficiency):
      highest: Suburban ($0.81 per visitor)
      lowest:  Airport ($0.49 per visitor)

    Coffee share of total revenue: 37.9%
    Promo-day lift in average revenue: +15.3%

    Weekend traffic change: Downtown -21.6%, Mall +29.9%
    ```

    **Interpretation:** These nine-or-so figures *are* the executive summary's skeleton: $265,921.08 of quarterly revenue, a store ranking whose top-to-bottom ratio is only 1.16 (volume differences are modest), an efficiency reversal ($0.81 per visitor at Suburban vs. $0.49 at Airport), one dominant product (Coffee at 37.9%), a consistent promotional lift (+15.3%), and opposite weekend swings at Downtown (-21.6%) and Mall (+29.9%). Every sentence in the summary below traces back to one of these lines — which is what "grounded in the data" means in practice.

    *Source: `computations/module17_examples.py` — `demo_executive_summary()`*

With the numbers in hand, the model summary reads like this (condensed from the teaching notebook):

> **Research question:** How do location type, product category, and day of week affect revenue and customer traffic at Brewed Awakening?
>
> **1. Location drives revenue, but efficiency reverses the ranking.** The Airport store generates the highest total revenue, yet on a revenue-per-customer basis the order flips — Suburban earns the most per visitor and Airport the least. Airport wins on sheer volume, not on how much each customer spends.
>
> **2. Coffee dominates, but the product mix should be location-specific.** Coffee leads at every store, while the secondary products vary: Smoothies outperform at the University, Pastries at the Mall. Tailoring inventory and marketing to each location's strengths could improve margins.
>
> **3. Weekend patterns require location-specific staffing.** Downtown foot traffic drops sharply on weekends while Mall traffic surges; revenue per visit stays roughly constant, so this is chiefly a staffing signal.
>
> **4. Promotions work, but profitability is unknown.** Promotional days show consistently higher revenue across all locations; without cost and margin data we cannot confirm they are net profitable.
>
> **Recommendation:** Implement location-specific strategies for staffing, inventory, and promotion rather than a one-size-fits-all approach — and investigate whether the efficient low-traffic stores could grow traffic without sacrificing their per-visitor economics.

Notice the form: findings first, one bolded claim per paragraph, numbers available on demand, and a recommendation that names *actions*, not virtues.

### Limitations & Future Work

Every analysis has boundaries, and stating them is a strength, not a confession — it tells the reader exactly how much weight your conclusions can bear. The teaching example acknowledges five:

1. **Synthetic data.** The dataset was generated to illustrate techniques; real data brings noise, inconsistencies, and edge cases that synthetic data cannot capture.
2. **No cost or margin data.** Revenue is analyzable; profit is not. The promotional finding is incomplete without promotion costs.
3. **A single quarter.** Ninety days cannot capture seasonality — summer iced drinks, holiday gift cards, back-to-school rushes.
4. **No customer demographics.** Counts without identities; segmentation by age, loyalty status, or visit frequency is impossible.
5. **No competitive data.** A competitor opening or closing nearby would move revenue in ways this dataset cannot explain.

Each limitation then suggests its own **future work**: extend to a full year, add cost data, A/B-test promotions at individual stores, build a demand-prediction model from weather/day/promo features, survey customers. Good limitation writing has this shape — *what we cannot conclude, why, and what data or method would fix it*. Vague humility ("the data could be better") earns no credit in a capstone; specific boundaries do.

### Reflection

Reflection is the final piece: what worked, what was hard, and what you would do differently. It demonstrates that you learned about the *process*, not just the subject. The teaching notebook models it honestly — the group-by workflow made exploring dimensions cheap; choosing which five or six charts to include was an editorial struggle, not a technical one; translating statistics into business language took longer than computing them; and next time the author would draft the executive summary outline *before* analyzing, to focus the exploration, and would reach for real, messy data sooner. Your own reflection should be equally concrete: name the finding that surprised you, the tool that earned its place, and the thing you would change.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "Admitting limitations weakens my report." | Stating limitations is how you control the interpretation of your work. Readers *will* find the boundaries; naming them first shows analytical maturity and keeps your credibility when they do. |
| "The executive summary is a shortened methods section." | It is findings-first prose for someone who will never read your code: claim, number, implication, recommendation. Methods live in the notebook underneath it. |
| "The reflection is filler." | It is where you demonstrate transferable judgment — tool choice, editorial decisions, what you would do differently — which is exactly what an employer reads a portfolio project for. |

---

## Reflection Questions

1. The store with the most revenue earned the least per visitor. Describe a business decision where ranking by total revenue would be the right choice, and one where ranking by revenue-per-customer would be — and what goes wrong if you pick the wrong metric.
2. Several analyses found factors that move *traffic* strongly while leaving *revenue per row* nearly flat. Why is that distinction operationally valuable, and how would you explain it to a manager who only looks at the revenue column?
3. The same store summary was computed in Polars and in DuckDB SQL with identical results. For your own capstone, how would you decide which tool to use for a given step — and what would make you use both in one notebook?
4. The teaching notebook's author says that next time they would outline the executive summary *before* doing the analysis. What are the benefits and the risks of deciding what you expect to conclude before you explore the data?
5. Of the five stated limitations (synthetic data, no margins, one quarter, no demographics, no competitive data), which one most threatens the recommendation to adopt location-specific strategies, and what specific data would you request to address it?
6. You have six charts and a board of directors with ten minutes. Which two charts from this module's set would you keep, and what would you say about each in two sentences?

---

## Your Assignment

The Module 16.2 assignment is the second half of your capstone: a complete analysis-and-presentation project worth **100 points plus a 10-point bonus**, built in a **marimo notebook (`.py` file)** and submitted to **Blackboard**. The closing reflection section is not graded separately — it counts toward participation.

The notebook supplies its own dataset: monthly activity records for a fictional **metropolitan public library system** — branches in different neighborhood settings, several program categories, and metrics for circulation (checkouts), program attendance, new card registrations, and patron satisfaction across a full year. A provided generation cell builds the data with a fixed random seed; the instructions say **do not modify it**, because the grading checks depend on the exact dataset. Your research question: *how do branch type, program category, and season affect circulation and program attendance?* — the same three-factor structure you just watched the coffee-shop example answer, transplanted to a new domain. This chapter deliberately demonstrated every technique on the coffee data so that you practice the method here and produce the library findings yourself.

**Task 1: Data Cleaning and Preparation (15 points).** Starting from the raw DataFrame, you fill the nulls that the satisfaction column contains with its median, engineer a normalized attendance-per-checkout column (a ratio scaled and rounded as specified), and create a boolean flag marking rows whose attendance exceeds the overall median — then print the null count and the resulting shape and display the head. This is the §16.2.1 Step 3 workflow exactly: `median()` + `fill_null()` from Module 10, plus the two engineered-column patterns (`with_columns()`, ratio column, threshold flag). Grading rewards the null fill (5), the ratio column (5), the flag (3), and the printed output (2).

**Task 2: Polars Group-By Analysis (15 points, 5 per summary).** Three aggregations, each assigned to a named variable: a branch performance summary, a program popularity summary, and a seasonal pattern summary, each with specified aggregation columns, rounding, and sort order. One wrinkle deserves care: like `customer_count` in the coffee data, the library's branch-level checkout totals repeat across the program rows of a branch-month, so the branch summary requires the deduplication adjustment the task text describes before summing. Everything here is §16.2.2 — including the warning in its Common Misconceptions table about summing a repeated column.

**Task 3: DuckDB SQL Queries (20 points).** Three queries against the cleaned DataFrame, each ending in `.pl()`: **3A (7 points)** ranks branch-program combinations by total attendance with a grouped, ordered, limited query; **3B (7 points)** builds a CTE of monthly branch totals and then applies a **window function** — a running `SUM(...) OVER (PARTITION BY ... ORDER BY ...)` — to produce cumulative checkouts over the year, the same CTE-plus-window pattern as §16.2.3's rolling average (a running total simply uses a different window frame); **3C (6 points)** compares branch types on average attendance, average satisfaction, and a distinct-count of branches. §16.2.3 covers all three shapes.

**Task 4: Visualizations (15 points, 5 per chart).** Three polished Plotly Express charts, each with a descriptive title, labeled axes via the `labels` parameter, appropriate colors, and the `plotly_white` template (remember `.to_pandas()`): a **horizontal bar chart** of attendance by branch, a **grouped bar chart** of average attendance by season and program (which needs one more group-by you write yourself), and a **line chart** of the cumulative checkouts from Task 3B. The chart grammar — bar orientation, `barmode="group"`, color mapping, layout templates — is demonstrated across §16.2.4's six charts.

**Task 5: Data Narrative (20 points, 5 per section).** A structured findings summary written in `mo.md()`: three key findings (branch performance, program patterns, seasonal dynamics), each citing specific numbers *from your own results*, plus one concrete, actionable recommendation for library management — the assignment's standard is "specific and actionable," naming a program, branch, or budget move, rather than a vague "improve programs." This is the executive-summary discipline of §16.2.5: claim, number, implication, action.

**Task 6: Limitations and Next Steps (15 points).** Three *distinct* limitations (9 points, 3 each) — what the analysis cannot tell us and why that matters — and three concrete follow-up analyses (6 points, 2 each), each naming the data you would need, the method you would use, and the question it would answer. §16.2.5's limitations section shows the shape: specific boundaries, not vague humility.

**Bonus: Interactive marimo Element (10 points).** One marimo UI element — a branch-selector dropdown, a season multiselect, or an attendance-threshold slider — that reactively filters data or updates a chart, with the result displayed. Grading rewards the element (3), working reactive filtering (4), and a clear display (3). The widget pattern (create in one cell, read `.value` in another) is §16.2.4's closing example.

Two standing rules from the assignment: use the underscore prefix for cell-scoped variables (loop variables, figures, temporaries) but *not* for variables returned from a cell, and put written responses inside `mo.md()` calls. Review this chapter's coffee-shop walkthrough as your worked model — then let the library data tell its own story.

---

## Chapter Summary

This module assembled every tool in the course into a single deliverable. A finished capstone follows a clear structure — acquisition, inspection, cleaning, analysis, visualization, executive summary, limitations, reflection — with narrative before and after every code cell explaining what is about to happen and what the results mean. The worked example carried a fictional coffee-shop chain through all nine steps: reproducible synthetic data (a fixed seed), a four-check inspection (schema, shape, nulls, distributions), and two engineered columns that turned raw revenue into an efficiency metric and a traffic segment.

The analysis itself was systematic rather than clever: five Polars group-bys, each answering one facet of the research question, repeatedly finding that traffic and revenue are separate levers — the busiest store earned the least per visitor, weekends and weather moved foot traffic while per-product revenue stayed flat, and promotions lifted revenue consistently everywhere. DuckDB earned its optional place where SQL reads best: a store-by-product cross-tabulation, and a CTE feeding a window function that computed a rolling average without collapsing rows — with a side-by-side proof that Polars and SQL agree to the cent on the same logic.

Presentation turned those tables into an argument: six charts, each with a title, labeled axes, and a written interpretation; one interactive chart driven by marimo widgets instead of five near-duplicates; and an executive summary assembled from headline numbers pulled fresh from the data. The chapter closed with the two most underrated sections of any analysis — limitations stated as specific boundaries with the data that would fix them, and a reflection on process. These are the sections that read as judgment, and judgment is what the capstone certifies.

---

## What's Next

There is no Module 17 — this is the end of MIS501, and the skills now compound on their own. Over sixteen modules you went from printing a first line of Python to running a complete analytical operation: core Python for logic and structure (Modules 1–8), Polars, visualization, marimo, and DuckDB for data work (9–13), web scraping and APIs for acquisition (14–15), and a two-part capstone that framed a question and delivered a defensible answer (16.1–16.2).

Where these skills go from here is wherever data meets a decision. The workflow you practiced — frame the question, acquire and inspect the data, clean it, aggregate it, visualize it, and write the story with its limitations attached — is the daily shape of analytics work in finance, operations, marketing, and management, and it transfers unchanged to whatever tools your employer happens to run. Your capstone notebook is a portfolio piece: it demonstrates not just coding ability but the capacity to take a vague business question and return actionable insight in a reproducible document, which is the rarer skill. Keep the habits that made it work — reproducible seeds and scripts, narrative around every result, honest limitations — and keep practicing on real, messy datasets, because those habits, more than any single library, are what you actually learned here. Congratulations on completing the course.
