"""Module 10 computation examples: Polars — Transformations & Aggregations.

Every demo function below backs one Worked Example in the Module 10 chapter of
the MIS 501 Course Companion. The chapter pastes each function's stdout
verbatim, so do not edit outputs by hand — rerun this script instead.

References in Course Companion:
    demo_add_total_column()      -> Module 10, Section 10.1 (Transforming Columns: Adding, Renaming, and Casting)
    demo_multiple_columns()      -> Module 10, Section 10.1 (Transforming Columns: Adding, Renaming, and Casting)
    demo_rename_columns()        -> Module 10, Section 10.1 (Transforming Columns: Adding, Renaming, and Casting)
    demo_cast_types()            -> Module 10, Section 10.1 (Transforming Columns: Adding, Renaming, and Casting)
    demo_group_by_single()       -> Module 10, Section 10.2 (Group-By Aggregations)
    demo_group_by_multiple()     -> Module 10, Section 10.2 (Group-By Aggregations)
    demo_customer_summary()      -> Module 10, Section 10.2 (Group-By Aggregations)
    demo_left_join()             -> Module 10, Section 10.3 (Joining DataFrames)
    demo_join_then_group()       -> Module 10, Section 10.3 (Joining DataFrames)
    demo_null_detection()        -> Module 10, Section 10.4 (Handling Null Values)
    demo_fill_null()             -> Module 10, Section 10.4 (Handling Null Values)
    demo_remove_nulls()          -> Module 10, Section 10.4 (Handling Null Values)
    demo_pipeline_enrich()       -> Module 10, Section 10.5 (Method Chaining: The End-to-End Pipeline)
    demo_pipeline_summaries()    -> Module 10, Section 10.5 (Method Chaining: The End-to-End Pipeline)
    demo_pipeline_write_report() -> Module 10, Section 10.5 (Method Chaining: The End-to-End Pipeline)

Data: the 12-order dataset from the Module 10 teaching notebook
(m10_teaching.py), embedded as literals so the script is self-contained.
Deterministic — no randomness, no network. File output goes to
computations/_scratch/module10/ (relative paths only).

Last updated: 2026-07-23
"""

from pathlib import Path

import polars as pl

SCRATCH_DIR = Path(__file__).parent / "_scratch" / "module10"


def make_orders():
    """The 12-order sales dataset used throughout the module."""
    return pl.DataFrame(
        {
            "order_id": [
                "ORD-001", "ORD-002", "ORD-003", "ORD-004", "ORD-005", "ORD-006",
                "ORD-007", "ORD-008", "ORD-009", "ORD-010", "ORD-011", "ORD-012",
            ],
            "customer": [
                "Acme Corp", "Bright Solutions", "CyberTech", "Acme Corp",
                "DataFlow Inc", "Bright Solutions", "EcoGoods", "DataFlow Inc",
                "CyberTech", "Acme Corp", "EcoGoods", "Bright Solutions",
            ],
            "product": [
                "Laptop", "Monitor", "Keyboard", "Mouse", "Laptop", "Webcam",
                "Keyboard", "Monitor", "Mouse", "Webcam", "Laptop", "Keyboard",
            ],
            "category": [
                "Electronics", "Electronics", "Accessories", "Accessories",
                "Electronics", "Electronics", "Accessories", "Electronics",
                "Accessories", "Electronics", "Electronics", "Accessories",
            ],
            "quantity": [3, 5, 20, 50, 2, 10, 15, 8, 30, 5, 1, 25],
            "unit_price": [
                999.99, 349.50, 79.95, 24.99, 999.99, 64.50,
                79.95, 349.50, 24.99, 64.50, 999.99, 79.95,
            ],
            "region": [
                "West", "East", "West", "West", "Central", "East",
                "East", "Central", "West", "West", "East", "East",
            ],
            "order_date": [
                "2025-01-05", "2025-01-08", "2025-01-10", "2025-01-12",
                "2025-01-15", "2025-01-18", "2025-01-20", "2025-01-22",
                "2025-01-25", "2025-01-28", "2025-02-01", "2025-02-03",
            ],
        }
    )


def make_orders_with_total():
    """Orders plus the computed 'total' column (quantity * unit_price)."""
    return make_orders().with_columns(
        (pl.col("quantity") * pl.col("unit_price")).round(2).alias("total"),
    )


def make_customers():
    """The customer-attributes lookup table used in the join demos."""
    return pl.DataFrame(
        {
            "customer": [
                "Acme Corp", "Bright Solutions", "CyberTech",
                "DataFlow Inc", "EcoGoods",
            ],
            "industry": [
                "Manufacturing", "Consulting", "Technology",
                "Analytics", "Retail",
            ],
            "tier": ["Gold", "Silver", "Gold", "Bronze", "Silver"],
        }
    )


def make_products_with_nulls():
    """A small product table containing missing values."""
    return pl.DataFrame(
        {
            "product": ["Laptop", "Monitor", "Keyboard", "Mouse", "Webcam"],
            "price": [999.99, 349.50, None, 24.99, None],
            "rating": [4.5, None, 4.2, 3.8, 4.0],
            "stock": [45, 120, 200, None, 85],
        }
    )


# ---------------------------------------------------------------------------
# Section 10.1 — Transforming Columns: Adding, Renaming, and Casting
# ---------------------------------------------------------------------------

def demo_add_total_column():
    """Build the orders data, then add a computed 'total' column."""
    orders = make_orders()

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


def demo_multiple_columns():
    """Add several computed columns in a single with_columns() call."""
    orders = make_orders()

    enriched = orders.with_columns(
        (pl.col("quantity") * pl.col("unit_price")).round(2).alias("total"),
        (pl.col("quantity") * pl.col("unit_price") * 0.08).round(2).alias("tax"),
        pl.col("product").str.to_uppercase().alias("product_upper"),
    )

    print(enriched.select("order_id", "product", "product_upper", "total", "tax").head(5))


def demo_rename_columns():
    """Rename columns without touching the values."""
    orders = make_orders()

    renamed = orders.rename(
        {
            "unit_price": "price",
            "order_date": "date",
        }
    )

    print(f"Before: {orders.columns}")
    print(f"After:  {renamed.columns}")


def demo_cast_types():
    """Cast the order_date column from String to a real Date type."""
    orders = make_orders()

    print(f"order_date type before: {orders.schema['order_date']}")

    orders_typed = orders.with_columns(
        pl.col("order_date").str.to_date("%Y-%m-%d").alias("order_date"),
    )

    print(f"order_date type after:  {orders_typed.schema['order_date']}")
    print(orders_typed.select("order_id", "order_date").head(5))


# ---------------------------------------------------------------------------
# Section 10.2 — Group-By Aggregations
# ---------------------------------------------------------------------------

def demo_group_by_single():
    """Group by one column: revenue by region, then revenue by category."""
    orders = make_orders_with_total()

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


def demo_group_by_multiple():
    """Group by two columns: region AND category."""
    orders = make_orders_with_total()

    by_region_cat = orders.group_by("region", "category").agg(
        pl.col("total").sum().alias("revenue"),
        pl.len().alias("num_orders"),
    ).sort("region", "revenue", descending=[False, True])

    print("Revenue by Region and Category:")
    print(by_region_cat)


def demo_customer_summary():
    """One group_by with five different aggregation functions."""
    orders = make_orders_with_total()

    customer_summary = orders.group_by("customer").agg(
        pl.col("total").sum().alias("total_spent"),
        pl.col("total").mean().round(2).alias("avg_order"),
        pl.len().alias("num_orders"),
        pl.col("product").n_unique().alias("unique_products"),
        pl.col("total").max().alias("largest_order"),
    ).sort("total_spent", descending=True)

    print("Customer Summary:")
    print(customer_summary)


# ---------------------------------------------------------------------------
# Section 10.3 — Joining DataFrames
# ---------------------------------------------------------------------------

def demo_left_join():
    """Left-join customer attributes onto each order."""
    orders = make_orders_with_total()
    customers = make_customers()

    print("Customer Info:")
    print(customers)

    enriched = orders.join(
        customers,
        on="customer",
        how="left",
    )

    print("\nOrders with customer info (first 6 rows):")
    print(enriched.select("order_id", "customer", "industry", "tier", "product", "total").head(6))


def demo_join_then_group():
    """Join first, then aggregate: revenue by customer tier."""
    orders = make_orders_with_total()
    customers = make_customers()

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


# ---------------------------------------------------------------------------
# Section 10.4 — Handling Null Values
# ---------------------------------------------------------------------------

def demo_null_detection():
    """Show a table with missing values and count the nulls per column."""
    products = make_products_with_nulls()

    print("Dataset with nulls:")
    print(products)
    print("\nNull counts per column:")
    print(products.null_count())


def demo_fill_null():
    """Replace nulls with defaults: constants and a computed mean."""
    products = make_products_with_nulls()

    filled = products.with_columns(
        pl.col("price").fill_null(0).alias("price"),
        pl.col("rating").fill_null(pl.col("rating").mean()).alias("rating"),
        pl.col("stock").fill_null(0).alias("stock"),
    )

    print("After filling nulls:")
    print(filled)


def demo_remove_nulls():
    """Keep rows with valid prices, then drop every row containing any null."""
    products = make_products_with_nulls()

    valid_prices = products.filter(pl.col("price").is_not_null())
    print("Rows with valid prices:")
    print(valid_prices)

    clean = products.drop_nulls()
    print(f"\nOriginal rows: {products.shape[0]}, After drop_nulls: {clean.shape[0]}")
    print(clean)


# ---------------------------------------------------------------------------
# Section 10.5 — Method Chaining: The End-to-End Pipeline
# ---------------------------------------------------------------------------

def demo_pipeline_enrich():
    """Pipeline step 1: compute totals and tax, fix dates, join customer info."""
    orders = make_orders()
    customers = make_customers()

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


def demo_pipeline_summaries():
    """Pipeline step 2: tier summary and top-customer report from the enriched data."""
    orders = make_orders()
    customers = make_customers()

    analysis = (
        orders
        .with_columns(
            (pl.col("quantity") * pl.col("unit_price")).round(2).alias("total"),
        )
        .join(customers, on="customer", how="left")
    )

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


def demo_pipeline_write_report():
    """Pipeline step 3: build the product report, write it to CSV, read it back."""
    orders = make_orders()

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

    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    report_path = SCRATCH_DIR / "product_performance.csv"
    product_perf.write_csv(report_path)
    print(f"\nWrote product performance report ({product_perf.shape[0]} products) to product_performance.csv")

    verified = pl.read_csv(report_path)
    print("\nRead back from CSV to verify:")
    print(verified)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    demos = [
        demo_add_total_column,
        demo_multiple_columns,
        demo_rename_columns,
        demo_cast_types,
        demo_group_by_single,
        demo_group_by_multiple,
        demo_customer_summary,
        demo_left_join,
        demo_join_then_group,
        demo_null_detection,
        demo_fill_null,
        demo_remove_nulls,
        demo_pipeline_enrich,
        demo_pipeline_summaries,
        demo_pipeline_write_report,
    ]

    for demo in demos:
        print("=" * 70)
        print(f"# {demo.__name__}")
        print("=" * 70)
        demo()
        print()
