"""Module 17 computation examples: Capstone — Analysis & Presentation.

Every demo function below backs one Worked Example in the Module 17 chapter of
the MIS501 Course Companion. The chapter pastes each function's stdout
verbatim, so do not edit outputs by hand — rerun this script instead.

References in Course Companion:
    demo_generate_dataset()   -> Module 17, Section 17.1 (The Capstone Workflow: From Raw Data to Deliverable)
    demo_inspect_dataset()    -> Module 17, Section 17.1 (The Capstone Workflow: From Raw Data to Deliverable)
    demo_clean_and_engineer() -> Module 17, Section 17.1 (The Capstone Workflow: From Raw Data to Deliverable)
    demo_revenue_by_store()   -> Module 17, Section 17.2 (Analysis with Polars)
    demo_revenue_by_product() -> Module 17, Section 17.2 (Analysis with Polars)
    demo_weekend_patterns()   -> Module 17, Section 17.2 (Analysis with Polars)
    demo_promo_effect()       -> Module 17, Section 17.2 (Analysis with Polars)
    demo_weather_impact()     -> Module 17, Section 17.2 (Analysis with Polars)
    demo_sql_crosstab()       -> Module 17, Section 17.3 (Analysis with DuckDB)
    demo_sql_rolling_average()-> Module 17, Section 17.3 (Analysis with DuckDB)
    demo_sql_vs_polars()      -> Module 17, Section 17.3 (Analysis with DuckDB)
    demo_scatter_numbers()    -> Module 17, Section 17.4 (Visualizations and Interactive Elements)
    demo_widget_simulation()  -> Module 17, Section 17.4 (Visualizations and Interactive Elements)
    demo_executive_summary()  -> Module 17, Section 17.5 (Communicating Results)

Data: the synthetic "Brewed Awakening" coffee-shop-chain dataset from the
Module 17 teaching notebook (m17_teaching.py), regenerated here with the
notebook's own seed (501) and the identical sequence of random calls, so every
number matches the notebook. This demonstration dataset is deliberately
different from the Module 17 assignment's library-system dataset — the chapter
teaches the workflow, not the assignment's answers.

Charts in the chapter are built with Plotly Express; per companion convention
the demos print the numbers *behind* each chart instead of rendering figures.
Widget demos simulate marimo UI values as plain variables (module 12 rule).
Deterministic — no network access. Nothing is written to disk.

Last updated: 2026-07-23
"""

import random
from datetime import date, timedelta

import duckdb
import polars as pl


# ---------------------------------------------------------------------------
# Dataset builders (mirror m17_teaching.py exactly: same seed 501, same order
# of random calls, so every value matches the teaching notebook)
# ---------------------------------------------------------------------------

def make_sales_data():
    """Recreate the teaching notebook's synthetic coffee-shop sales dataset."""
    random.seed(501)

    stores = {
        "Downtown": {"base_traffic": 220, "base_revenue_mult": 1.3},
        "University": {"base_traffic": 180, "base_revenue_mult": 0.9},
        "Airport": {"base_traffic": 250, "base_revenue_mult": 1.5},
        "Suburban": {"base_traffic": 130, "base_revenue_mult": 0.8},
        "Mall": {"base_traffic": 170, "base_revenue_mult": 1.1},
    }

    products = {
        "Coffee": {"base_price": 4.50, "base_units": 45},
        "Tea": {"base_price": 3.75, "base_units": 20},
        "Pastry": {"base_price": 3.25, "base_units": 30},
        "Sandwich": {"base_price": 7.50, "base_units": 15},
        "Smoothie": {"base_price": 5.50, "base_units": 12},
    }

    days = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday",
    ]

    weather_options = ["Sunny", "Cloudy", "Rainy"]
    weather_weights = [0.50, 0.30, 0.20]

    # Dates for Q1 2025 (Jan 1 - Mar 31)
    start = date(2025, 1, 1)
    all_dates = [start + timedelta(days=d) for d in range(90)]

    rows = []
    for date_val in all_dates:
        # Day of week (0 = Monday in Python)
        dow_index = date_val.weekday()
        day_name = days[dow_index]
        is_weekend = dow_index >= 5

        # Weather for the day
        weather = random.choices(
            weather_options,
            weights=weather_weights,
            k=1,
        )[0]

        # Promo active ~20% of days
        promo = random.random() < 0.20

        for store_name, store_info in stores.items():
            base_traffic = store_info["base_traffic"]

            # Weekend adjustments vary by store type
            if is_weekend:
                if store_name == "Downtown":
                    traffic_adj = -0.25  # office workers gone
                elif store_name == "University":
                    traffic_adj = -0.15  # fewer students
                elif store_name == "Airport":
                    traffic_adj = 0.10  # leisure travelers
                elif store_name == "Mall":
                    traffic_adj = 0.30  # shoppers
                else:
                    traffic_adj = 0.15  # suburban families
            else:
                traffic_adj = 0.0

            # Weather effect on traffic
            weather_traffic = {
                "Sunny": 0.05,
                "Cloudy": 0.0,
                "Rainy": -0.10,
            }[weather]

            # Promo effect
            promo_mult = 1.15 if promo else 1.0

            day_traffic = int(
                base_traffic
                * (1.0 + traffic_adj)
                * (1.0 + weather_traffic)
                * promo_mult
                * random.uniform(0.85, 1.15)
            )
            day_traffic = max(50, day_traffic)

            for prod_name, prod_info in products.items():
                base_units = prod_info["base_units"]
                price = prod_info["base_price"]

                # Product-level adjustments
                if store_name == "Airport" and prod_name == "Coffee":
                    prod_mult = 1.4  # travelers need coffee
                elif store_name == "University" and prod_name == "Smoothie":
                    prod_mult = 1.5  # students like smoothies
                elif store_name == "Mall" and prod_name == "Pastry":
                    prod_mult = 1.3  # mall snacking
                else:
                    prod_mult = 1.0

                units = int(
                    base_units
                    * prod_mult
                    * promo_mult
                    * random.uniform(0.75, 1.25)
                )
                units = max(2, units)

                revenue = round(units * price * random.uniform(0.95, 1.05), 2)

                rows.append({
                    "store_id": store_name,
                    "date": date_val,
                    "day_of_week": day_name,
                    "product_category": prod_name,
                    "units_sold": units,
                    "revenue": revenue,
                    "customer_count": day_traffic,
                    "weather": weather,
                    "is_weekend": is_weekend,
                    "promo_active": promo,
                })

    return pl.DataFrame(rows)


def make_sales_clean():
    """The cleaned dataset: raw data plus the two engineered columns."""
    sales_data = make_sales_data()
    median_traffic = sales_data.select(
        pl.col("customer_count").median()
    ).item()
    return sales_data.with_columns(
        (pl.col("revenue") / pl.col("customer_count"))
        .round(2)
        .alias("revenue_per_customer"),
        (pl.col("customer_count") > median_traffic).alias("is_high_traffic"),
    )


def make_weekend_analysis():
    """Weekday-vs-weekend averages per store (teaching notebook Analysis 4.3)."""
    return (
        make_sales_clean()
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


def weekend_traffic_changes():
    """Percent change in avg traffic, weekend vs. weekday, per store."""
    return (
        make_weekend_analysis()
        .select("store_id", "period", "avg_traffic")
        .pivot(on="period", index="store_id", values="avg_traffic")
        .with_columns(
            ((pl.col("Weekend") / pl.col("Weekday") - 1) * 100)
            .round(1)
            .alias("traffic_change_pct"),
        )
        .sort("store_id")
    )


# ---------------------------------------------------------------------------
# Section 17.1 — The Capstone Workflow: From Raw Data to Deliverable
# ---------------------------------------------------------------------------

def demo_generate_dataset():
    """Step 1: generate the synthetic coffee-shop dataset (seed 501)."""
    sales_data = make_sales_data()

    print("Random seed: 501")
    print("Coverage: 90 days x 5 stores x 5 product categories")
    print(f"Dataset shape: {sales_data.shape[0]} rows x {sales_data.shape[1]} columns")
    date_min = sales_data.select(pl.col("date").min()).item()
    date_max = sales_data.select(pl.col("date").max()).item()
    print(f"Date range: {date_min} to {date_max}")

    print("\nFirst 10 rows (selected columns):")
    print(
        sales_data.head(10).select(
            "store_id", "date", "product_category",
            "units_sold", "revenue", "customer_count",
        )
    )


def demo_inspect_dataset():
    """Step 2: schema, null counts, and summary statistics."""
    sales_data = make_sales_data()

    print("Schema (column -> dtype):")
    for name, dtype in sales_data.schema.items():
        print(f"  {name}: {dtype}")

    print("\nNull values per column:")
    for name, count in zip(sales_data.columns, sales_data.null_count().row(0)):
        print(f"  {name}: {count}")

    print("\nSummary statistics for the numeric columns:")
    print(sales_data.select("units_sold", "revenue", "customer_count").describe())


def demo_clean_and_engineer():
    """Step 3: median-based threshold and two engineered columns."""
    sales_data = make_sales_data()

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
    print("\nFirst 5 rows (key columns):")
    print(
        sales_clean.head(5).select(
            "store_id", "product_category", "revenue", "customer_count",
            "revenue_per_customer", "is_high_traffic",
        )
    )


# ---------------------------------------------------------------------------
# Section 17.2 — Analysis with Polars
# ---------------------------------------------------------------------------

def demo_revenue_by_store():
    """Analysis 4.1: total revenue and per-customer efficiency by store."""
    sales_clean = make_sales_clean()

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
    print("Store summary (sorted by total revenue):")
    print(store_summary)


def demo_revenue_by_product():
    """Analysis 4.2: revenue contribution by product category."""
    sales_clean = make_sales_clean()

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
            (pl.col("total_revenue")
             / pl.col("total_revenue").sum()
             * 100)
            .round(1)
            .alias("pct_of_total"),
            pl.col("total_revenue").round(2),
            pl.col("avg_revenue").round(2),
        )
    )
    print("Product summary (sorted by total revenue):")
    print(product_summary)


def demo_weekend_patterns():
    """Analysis 4.3: weekday vs. weekend revenue and traffic by store."""
    weekend_analysis = make_weekend_analysis()

    print("Weekday vs. weekend averages by store:")
    print(weekend_analysis)

    print("\nWeekend traffic change vs. weekday:")
    for store, change in weekend_traffic_changes().select(
        "store_id", "traffic_change_pct"
    ).iter_rows():
        print(f"  {store:<10} {change:+.1f}%")


def demo_promo_effect():
    """Analysis 4.4: promotional effect, overall and per store."""
    sales_clean = make_sales_clean()

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
            .then(pl.lit("Promo Day"))
            .otherwise(pl.lit("Regular Day"))
            .alias("day_type"),
            pl.col("avg_revenue").round(2),
            pl.col("avg_units").round(1),
            pl.col("avg_traffic").round(1),
        )
    )
    print("Promotional effect (all stores pooled):")
    print(promo_effect)

    regular_avg = promo_effect.filter(~pl.col("promo_active"))["avg_revenue"].item()
    promo_avg = promo_effect.filter(pl.col("promo_active"))["avg_revenue"].item()
    lift_pct = (promo_avg / regular_avg - 1) * 100
    print(f"\nPromo-day lift in average revenue: {lift_pct:+.1f}%")

    promo_by_store = (
        sales_clean
        .group_by("store_id", "promo_active")
        .agg(
            pl.col("revenue").mean().alias("avg_revenue"),
        )
        .with_columns(
            pl.when(pl.col("promo_active"))
            .then(pl.lit("Promo"))
            .otherwise(pl.lit("No Promo"))
            .alias("promo_label"),
            pl.col("avg_revenue").round(2),
        )
        .sort("store_id", "promo_active")
        .select("store_id", "promo_label", "avg_revenue")
    )
    print("\nAverage revenue per product-day, by store and promo status:")
    print(promo_by_store)


def demo_weather_impact():
    """Analysis 4.5: weather effect on traffic and revenue."""
    sales_clean = make_sales_clean()

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
    print("Weather summary (sorted by average traffic):")
    print(weather_summary)

    sunny = weather_summary.filter(pl.col("weather") == "Sunny")["avg_traffic"].item()
    rainy = weather_summary.filter(pl.col("weather") == "Rainy")["avg_traffic"].item()
    swing = (sunny / rainy - 1) * 100
    print(f"\nSunny-vs-rainy traffic swing: {swing:+.1f}%")


# ---------------------------------------------------------------------------
# Section 17.3 — Analysis with DuckDB
# ---------------------------------------------------------------------------

def demo_sql_crosstab():
    """Analysis 5.1: store x product cross-tabulation in SQL."""
    sales_clean = make_sales_clean()
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

    print(f"Cross-tabulation: {cross_tab.shape[0]} rows (5 stores x 5 products)")
    print("\nFirst 10 rows (Airport and Downtown):")
    print(cross_tab.head(10))

    print("\nTop product by revenue at each store:")
    top_per_store = (
        cross_tab
        .sort("total_revenue", descending=True)
        .group_by("store_id", maintain_order=True)
        .first()
        .sort("store_id")
    )
    for store, product, rev in top_per_store.select(
        "store_id", "product_category", "total_revenue"
    ).iter_rows():
        print(f"  {store:<10} {product}  (${rev:,.2f})")


def demo_sql_rolling_average():
    """Analysis 5.2: 7-day rolling average via a CTE plus window function."""
    sales_clean = make_sales_clean()
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
    print("\nFirst 10 rows (Airport, early January):")
    print(rolling_avg.head(10))


def demo_sql_vs_polars():
    """Tool choice: the store summary computed in SQL matches Polars."""
    sales_clean = make_sales_clean()
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

    print("Store summary via DuckDB SQL:")
    print(store_sql)


# ---------------------------------------------------------------------------
# Section 17.4 — Visualizations and Interactive Elements
# ---------------------------------------------------------------------------

def demo_scatter_numbers():
    """Numbers behind Chart 4: the traffic-vs-revenue scatter plot."""
    sales_clean = make_sales_clean()

    daily = (
        sales_clean
        .group_by("store_id", "date")
        .agg(
            pl.col("revenue").sum().alias("daily_revenue"),
            pl.col("customer_count").first().alias("customer_count"),
        )
    )
    print(f"Scatter data: {daily.shape[0]} store-day points "
          f"({daily['store_id'].n_unique()} stores x 90 days)")

    corr = daily.select(
        pl.corr("customer_count", "daily_revenue")
    ).item()
    print(f"Correlation between daily traffic and daily revenue: {corr:.2f}")

    print("\nPer-store daily averages (the center of each scatter cluster):")
    cluster_centers = (
        daily
        .group_by("store_id")
        .agg(
            pl.col("customer_count").mean().round(1).alias("avg_traffic"),
            pl.col("daily_revenue").mean().round(2).alias("avg_daily_revenue"),
        )
        .with_columns(
            (pl.col("avg_daily_revenue") / pl.col("avg_traffic"))
            .round(2)
            .alias("revenue_per_visitor"),
        )
        .sort("avg_traffic", descending=True)
    )
    print(cluster_centers)


def demo_widget_simulation():
    """Step 6B: simulate the store dropdown and revenue-threshold slider."""
    sales_clean = make_sales_clean()

    selected_store = "University"  # simulates store_picker.value
    min_revenue = 100              # simulates rev_threshold.value

    print("Simulated widget state:")
    print(f"  store_picker.value  = '{selected_store}'")
    print(f"  rev_threshold.value = {min_revenue}")

    store_rows = sales_clean.filter(pl.col("store_id") == selected_store)
    filtered = store_rows.filter(pl.col("revenue") >= min_revenue)
    print(f"\nRows for {selected_store}: {store_rows.shape[0]}")
    print(f"Rows kept after the revenue >= ${min_revenue} filter: {filtered.shape[0]}")

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
    print("\nWhat the reactive chart would display:")
    print(summary)


# ---------------------------------------------------------------------------
# Section 17.5 — Communicating Results
# ---------------------------------------------------------------------------

def demo_executive_summary():
    """Step 7: the headline numbers an executive summary is built from."""
    sales_clean = make_sales_clean()

    total_revenue = sales_clean["revenue"].sum()
    print("Headline numbers for the executive summary")
    print("------------------------------------------")
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
    print("\nStore revenue ranking:")
    for rank, (store, rev, _) in enumerate(store_totals.iter_rows(), start=1):
        print(f"  {rank}. {store:<10} ${rev:,.2f}")

    top_rev = store_totals["total_revenue"][0]
    bottom_rev = store_totals["total_revenue"][-1]
    print(f"Top-to-bottom store revenue ratio: {top_rev / bottom_rev:.2f}")

    by_eff = store_totals.sort("rev_per_customer", descending=True)
    eff_top_store = by_eff["store_id"][0]
    eff_top_val = by_eff["rev_per_customer"][0]
    eff_bot_store = by_eff["store_id"][-1]
    eff_bot_val = by_eff["rev_per_customer"][-1]
    print("\nRevenue per customer (efficiency):")
    print(f"  highest: {eff_top_store} (${eff_top_val:.2f} per visitor)")
    print(f"  lowest:  {eff_bot_store} (${eff_bot_val:.2f} per visitor)")

    coffee_share = (
        sales_clean
        .group_by("product_category")
        .agg(pl.col("revenue").sum().alias("rev"))
        .with_columns((pl.col("rev") / pl.col("rev").sum() * 100).round(1).alias("pct"))
        .filter(pl.col("product_category") == "Coffee")["pct"]
        .item()
    )
    print(f"\nCoffee share of total revenue: {coffee_share}%")

    promo_avgs = (
        sales_clean
        .group_by("promo_active")
        .agg(pl.col("revenue").mean().round(2).alias("avg_revenue"))
        .sort("promo_active")
    )
    lift = (promo_avgs["avg_revenue"][1] / promo_avgs["avg_revenue"][0] - 1) * 100
    print(f"Promo-day lift in average revenue: {lift:+.1f}%")

    changes = weekend_traffic_changes()
    downtown = changes.filter(pl.col("store_id") == "Downtown")["traffic_change_pct"].item()
    mall = changes.filter(pl.col("store_id") == "Mall")["traffic_change_pct"].item()
    print(f"\nWeekend traffic change: Downtown {downtown:+.1f}%, Mall {mall:+.1f}%")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    demos = [
        demo_generate_dataset,
        demo_inspect_dataset,
        demo_clean_and_engineer,
        demo_revenue_by_store,
        demo_revenue_by_product,
        demo_weekend_patterns,
        demo_promo_effect,
        demo_weather_impact,
        demo_sql_crosstab,
        demo_sql_rolling_average,
        demo_sql_vs_polars,
        demo_scatter_numbers,
        demo_widget_simulation,
        demo_executive_summary,
    ]

    for demo in demos:
        print("=" * 70)
        print(f"# {demo.__name__}")
        print("=" * 70)
        demo()
        print()
