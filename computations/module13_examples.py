"""Module 13 computation examples: DuckDB — SQL-Based Data Analysis.

Every demo function below backs one Worked Example in the Module 13 chapter of
the MIS501 Course Companion. The chapter pastes each function's stdout
verbatim, so do not edit outputs by hand — rerun this script instead.

References in Course Companion:
    demo_dataset_overview()        -> Module 13, Section 13.1 (What Is DuckDB?)
    demo_first_query()             -> Module 13, Section 13.1 (What Is DuckDB?)
    demo_select_where()            -> Module 13, Section 13.2 (SQL Essentials: SELECT, WHERE, and Calculated Columns)
    demo_calculated_columns()      -> Module 13, Section 13.2 (SQL Essentials: SELECT, WHERE, and Calculated Columns)
    demo_case_when()               -> Module 13, Section 13.2 (SQL Essentials: SELECT, WHERE, and Calculated Columns)
    demo_aggregates()              -> Module 13, Section 13.3 (Aggregation: Summary Functions, GROUP BY, and HAVING)
    demo_group_by_customer()       -> Module 13, Section 13.3 (Aggregation: Summary Functions, GROUP BY, and HAVING)
    demo_group_by_month_category() -> Module 13, Section 13.3 (Aggregation: Summary Functions, GROUP BY, and HAVING)
    demo_having()                  -> Module 13, Section 13.3 (Aggregation: Summary Functions, GROUP BY, and HAVING)
    demo_inner_join()              -> Module 13, Section 13.4 (Combining Tables: JOINs and Subqueries)
    demo_left_join()               -> Module 13, Section 13.4 (Combining Tables: JOINs and Subqueries)
    demo_three_table_join()        -> Module 13, Section 13.4 (Combining Tables: JOINs and Subqueries)
    demo_state_summary()           -> Module 13, Section 13.4 (Combining Tables: JOINs and Subqueries)
    demo_subqueries()              -> Module 13, Section 13.4 (Combining Tables: JOINs and Subqueries)
    demo_query_polars_dfs()        -> Module 13, Section 13.5 (DuckDB + Polars: The Integrated Workflow)
    demo_sql_to_polars()           -> Module 13, Section 13.5 (DuckDB + Polars: The Integrated Workflow)
    demo_in_memory_tables()        -> Module 13, Section 13.5 (DuckDB + Polars: The Integrated Workflow)
    demo_capstone_report()         -> Module 13, Section 13.5 (DuckDB + Polars: The Integrated Workflow)

Data: the three-table retail dataset from the Module 13 teaching notebook
(m13_teaching.py) — orders (20 rows), customers (9 rows), order_items
(31 rows) — embedded as CSV literals and written to
computations/_scratch/module13/ so the demos can query the files directly,
exactly as the notebook does. Deterministic — no randomness, no network.
Queries that display individual rows carry an ORDER BY (added where the
notebook relied on file order) so stdout is stable. Only bare filenames are
printed, never absolute paths.

Last updated: 2026-07-23
"""

from pathlib import Path

import duckdb
import polars as pl

SCRATCH_DIR = Path(__file__).resolve().parent / "_scratch" / "module13"

# ---------------------------------------------------------------------------
# The three-table retail dataset (verbatim values from m13_teaching.py)
# ---------------------------------------------------------------------------

ORDERS_CSV = """order_id,customer_id,order_date,total,status
ORD-001,C101,2025-01-15,245.50,Completed
ORD-002,C102,2025-01-18,189.00,Completed
ORD-003,C103,2025-01-22,512.75,Completed
ORD-004,C101,2025-02-03,78.25,Completed
ORD-005,C104,2025-02-10,1250.00,Completed
ORD-006,C102,2025-02-14,345.00,Cancelled
ORD-007,C105,2025-02-20,92.50,Completed
ORD-008,C103,2025-03-01,678.30,Completed
ORD-009,C106,2025-03-05,156.00,Completed
ORD-010,C101,2025-03-12,420.00,Completed
ORD-011,C107,2025-03-18,88.75,Completed
ORD-012,C104,2025-03-25,2100.00,Completed
ORD-013,C102,2025-04-02,445.50,Completed
ORD-014,C108,2025-04-08,67.00,Cancelled
ORD-015,C105,2025-04-15,310.25,Completed
ORD-016,C103,2025-04-22,890.00,Completed
ORD-017,C106,2025-05-01,175.50,Completed
ORD-018,C101,2025-05-10,560.00,Completed
ORD-019,C109,2025-05-18,1425.00,Completed
ORD-020,C107,2025-05-25,235.00,Completed
"""

CUSTOMERS_CSV = """customer_id,name,city,state,join_date
C101,Alice Chen,Portland,OR,2024-06-15
C102,Bob Martinez,Seattle,WA,2024-07-20
C103,Carol Johnson,Portland,OR,2024-08-10
C104,David Kim,San Francisco,CA,2024-09-01
C105,Eve Wilson,Seattle,WA,2024-10-15
C106,Frank Brown,Los Angeles,CA,2024-11-01
C107,Grace Lee,Portland,OR,2024-12-20
C108,Henry Patel,San Francisco,CA,2025-01-05
C109,Irene Davis,Los Angeles,CA,2025-02-10
"""

ITEMS_CSV = """item_id,order_id,product,category,quantity,unit_price
1,ORD-001,Wireless Mouse,Electronics,2,29.99
2,ORD-001,USB Hub,Electronics,1,45.50
3,ORD-001,Mouse Pad,Accessories,3,15.00
4,ORD-002,Desk Lamp,Office,1,89.00
5,ORD-002,Notebook Set,Office,2,25.00
6,ORD-002,Pen Pack,Office,1,25.00
7,ORD-003,Monitor Stand,Electronics,1,189.75
8,ORD-003,Cable Kit,Electronics,2,34.50
9,ORD-003,Keyboard,Electronics,1,219.50
10,ORD-004,Mouse Pad,Accessories,1,15.00
11,ORD-004,Pen Pack,Office,2,25.00
12,ORD-004,Sticky Notes,Office,3,4.75
13,ORD-005,Standing Desk,Furniture,1,899.00
14,ORD-005,Monitor Arm,Furniture,1,175.00
15,ORD-005,Cable Tray,Furniture,1,65.00
16,ORD-005,Desk Mat,Accessories,1,45.00
17,ORD-006,Headphones,Electronics,1,199.00
18,ORD-006,Phone Stand,Accessories,1,35.00
19,ORD-006,Screen Wipes,Accessories,2,12.50
20,ORD-007,Pen Pack,Office,3,25.00
21,ORD-007,Sticky Notes,Office,1,4.75
22,ORD-008,Webcam,Electronics,1,149.00
23,ORD-008,Ring Light,Electronics,1,85.00
24,ORD-008,USB Hub,Electronics,2,45.50
25,ORD-008,Desk Lamp,Office,1,89.00
26,ORD-009,Notebook Set,Office,3,25.00
27,ORD-009,Pen Pack,Office,2,25.00
28,ORD-009,Sticky Notes,Office,2,4.75
29,ORD-010,Keyboard,Electronics,1,219.50
30,ORD-010,Wireless Mouse,Electronics,1,29.99
31,ORD-010,Mouse Pad,Accessories,2,15.00
"""


def _data_dir() -> Path:
    """Silently (re)write the three CSV files; return their directory."""
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    (SCRATCH_DIR / "m13_orders.csv").write_text(ORDERS_CSV, encoding="utf-8")
    (SCRATCH_DIR / "m13_customers.csv").write_text(CUSTOMERS_CSV, encoding="utf-8")
    (SCRATCH_DIR / "m13_order_items.csv").write_text(ITEMS_CSV, encoding="utf-8")
    return SCRATCH_DIR


# ---------------------------------------------------------------------------
# Section 13.1 — What Is DuckDB?
# ---------------------------------------------------------------------------

def demo_dataset_overview():
    """Write the three CSV files and report the shape of each table."""
    d = _data_dir()
    orders = pl.read_csv(d / "m13_orders.csv")
    customers = pl.read_csv(d / "m13_customers.csv")
    order_items = pl.read_csv(d / "m13_order_items.csv")

    print(f"orders:      {orders.shape[0]} rows, {orders.shape[1]} columns")
    print(f"customers:   {customers.shape[0]} rows, {customers.shape[1]} columns")
    print(f"order_items: {order_items.shape[0]} rows, {order_items.shape[1]} columns")


def demo_first_query():
    """Query a CSV file directly with SQL, then convert the result to Polars."""
    d = _data_dir()

    result = duckdb.sql(f"""
        SELECT *
        FROM '{d / "m13_orders.csv"}'
        ORDER BY order_id
        LIMIT 5
    """)
    print("First 5 orders (queried directly from CSV):")
    print(result)

    df = duckdb.sql(f"""
        SELECT *
        FROM '{d / "m13_orders.csv"}'
    """).pl()
    print(f"Result as Polars DataFrame: {df.shape}")
    print(f"Columns: {df.columns}")


# ---------------------------------------------------------------------------
# Section 13.2 — SQL Essentials: SELECT, WHERE, and Calculated Columns
# ---------------------------------------------------------------------------

def demo_select_where():
    """SELECT specific columns, then filter rows with WHERE."""
    d = _data_dir()

    result = duckdb.sql(f"""
        SELECT order_id, customer_id, total
        FROM '{d / "m13_orders.csv"}'
        ORDER BY order_id
        LIMIT 5
    """)
    print("Selected columns:")
    print(result)

    result = duckdb.sql(f"""
        SELECT order_id, customer_id, total, status
        FROM '{d / "m13_orders.csv"}'
        WHERE total > 500
          AND status = 'Completed'
        ORDER BY order_id
    """)
    print("Orders over $500 (completed only):")
    print(result)


def demo_calculated_columns():
    """Calculated columns with AS, plus ORDER BY ... LIMIT for a top-N list."""
    d = _data_dir()

    result = duckdb.sql(f"""
        SELECT
            order_id,
            total,
            total * 0.08 AS tax,
            total * 1.08 AS total_with_tax
        FROM '{d / "m13_orders.csv"}'
        WHERE total > 300
        ORDER BY total DESC
    """)
    print("Orders over $300 with tax calculated:")
    print(result)

    result = duckdb.sql(f"""
        SELECT order_id, customer_id, total
        FROM '{d / "m13_orders.csv"}'
        WHERE status = 'Completed'
        ORDER BY total DESC
        LIMIT 5
    """)
    print("Top 5 orders by value:")
    print(result)


def demo_case_when():
    """Conditional columns with CASE WHEN: classify order sizes."""
    d = _data_dir()

    result = duckdb.sql(f"""
        SELECT
            order_id,
            total,
            CASE
                WHEN total < 100 THEN 'Small'
                WHEN total < 500 THEN 'Medium'
                WHEN total < 1000 THEN 'Large'
                ELSE 'Premium'
            END AS order_size
        FROM '{d / "m13_orders.csv"}'
        WHERE status = 'Completed'
        ORDER BY total DESC
    """)
    print("Orders classified by size:")
    print(result)


# ---------------------------------------------------------------------------
# Section 13.3 — Aggregation: Summary Functions, GROUP BY, and HAVING
# ---------------------------------------------------------------------------

def demo_aggregates():
    """Whole-table summary statistics with COUNT, SUM, AVG, MIN, MAX."""
    d = _data_dir()

    result = duckdb.sql(f"""
        SELECT
            COUNT(*) AS total_orders,
            SUM(total) AS revenue,
            AVG(total) AS avg_order,
            MIN(total) AS smallest_order,
            MAX(total) AS largest_order,
            COUNT(DISTINCT customer_id) AS unique_customers
        FROM '{d / "m13_orders.csv"}'
        WHERE status = 'Completed'
    """)
    print("Order summary (completed orders only):")
    print(result)


def demo_group_by_customer():
    """GROUP BY customer: order count, total spent, average, largest."""
    d = _data_dir()

    result = duckdb.sql(f"""
        SELECT
            customer_id,
            COUNT(*) AS order_count,
            SUM(total) AS total_spent,
            AVG(total) AS avg_order,
            MAX(total) AS largest_order
        FROM '{d / "m13_orders.csv"}'
        WHERE status = 'Completed'
        GROUP BY customer_id
        ORDER BY total_spent DESC
    """)
    print("Customer spending summary:")
    print(result)


def demo_group_by_month_category():
    """GROUP BY on a derived month column, then on product category."""
    d = _data_dir()

    result = duckdb.sql(f"""
        SELECT
            strftime(order_date::DATE, '%Y-%m') AS month,
            COUNT(*) AS order_count,
            ROUND(SUM(total), 2) AS revenue
        FROM '{d / "m13_orders.csv"}'
        WHERE status = 'Completed'
        GROUP BY month
        ORDER BY month
    """)
    print("Monthly revenue:")
    print(result)

    result = duckdb.sql(f"""
        SELECT
            category,
            COUNT(*) AS line_items,
            SUM(quantity) AS total_units,
            ROUND(SUM(quantity * unit_price), 2) AS total_revenue,
            ROUND(AVG(unit_price), 2) AS avg_price
        FROM '{d / "m13_order_items.csv"}'
        GROUP BY category
        ORDER BY total_revenue DESC
    """)
    print("Revenue by product category:")
    print(result)


def demo_having():
    """HAVING filters groups after aggregation (WHERE filters rows before)."""
    d = _data_dir()

    result = duckdb.sql(f"""
        SELECT
            customer_id,
            COUNT(*) AS order_count,
            ROUND(SUM(total), 2) AS total_spent
        FROM '{d / "m13_orders.csv"}'
        WHERE status = 'Completed'
        GROUP BY customer_id
        HAVING total_spent > 500
        ORDER BY total_spent DESC
    """)
    print("High-value customers (>$500 total):")
    print(result)

    result = duckdb.sql(f"""
        SELECT
            category,
            SUM(quantity) AS total_units,
            ROUND(SUM(quantity * unit_price), 2) AS total_revenue
        FROM '{d / "m13_order_items.csv"}'
        GROUP BY category
        HAVING total_units > 10
        ORDER BY total_revenue DESC
    """)
    print("Categories with >10 units sold:")
    print(result)


# ---------------------------------------------------------------------------
# Section 13.4 — Combining Tables: JOINs and Subqueries
# ---------------------------------------------------------------------------

def demo_inner_join():
    """INNER JOIN: attach customer names and cities to orders."""
    d = _data_dir()

    result = duckdb.sql(f"""
        SELECT
            o.order_id,
            c.name AS customer_name,
            c.city,
            o.order_date,
            o.total
        FROM '{d / "m13_orders.csv"}' AS o
        INNER JOIN '{d / "m13_customers.csv"}' AS c
            ON o.customer_id = c.customer_id
        WHERE o.status = 'Completed'
        ORDER BY o.total DESC
        LIMIT 10
    """)
    print("Top 10 orders with customer details:")
    print(result)


def demo_left_join():
    """LEFT JOIN: every customer appears, even those with no completed orders."""
    d = _data_dir()

    # COUNT(o.order_id) is deliberate: a customer with no completed orders
    # still appears (that is the point of LEFT JOIN), but their order columns
    # come back NULL. COUNT(o.order_id) skips those NULLs and reports 0 --
    # COUNT(*) would count the NULL-padded row and wrongly report 1.
    result = duckdb.sql(f"""
        SELECT
            c.customer_id,
            c.name,
            c.city,
            COUNT(o.order_id) AS order_count,
            COALESCE(SUM(o.total), 0) AS total_spent
        FROM '{d / "m13_customers.csv"}' AS c
        LEFT JOIN '{d / "m13_orders.csv"}' AS o
            ON c.customer_id = o.customer_id
            AND o.status = 'Completed'
        GROUP BY c.customer_id, c.name, c.city
        ORDER BY total_spent DESC
    """)
    print("All customers with order totals (LEFT JOIN):")
    print(result)


def demo_three_table_join():
    """Chain two INNER JOINs: orders + customers + order_items."""
    d = _data_dir()

    result = duckdb.sql(f"""
        SELECT
            c.name AS customer_name,
            o.order_id,
            i.product,
            i.category,
            i.quantity,
            i.unit_price,
            i.quantity * i.unit_price AS line_total
        FROM '{d / "m13_orders.csv"}' AS o
        INNER JOIN '{d / "m13_customers.csv"}' AS c
            ON o.customer_id = c.customer_id
        INNER JOIN '{d / "m13_order_items.csv"}' AS i
            ON o.order_id = i.order_id
        WHERE o.status = 'Completed'
        ORDER BY line_total DESC, o.order_id
        LIMIT 10
    """)
    print("Top 10 line items with customer names:")
    print(result)


def demo_state_summary():
    """Join + GROUP BY + conditional aggregation with SUM(CASE WHEN ...)."""
    d = _data_dir()

    result = duckdb.sql(f"""
        SELECT
            c.state,
            COUNT(*) AS orders,
            ROUND(SUM(o.total), 2) AS revenue,
            ROUND(AVG(o.total), 2) AS avg_order,
            SUM(CASE WHEN o.total >= 500 THEN 1 ELSE 0 END) AS large_orders
        FROM '{d / "m13_orders.csv"}' AS o
        JOIN '{d / "m13_customers.csv"}' AS c
            ON o.customer_id = c.customer_id
        WHERE o.status = 'Completed'
        GROUP BY c.state
        ORDER BY revenue DESC
    """)
    print("State summary with large-order count:")
    print(result)


def demo_subqueries():
    """A scalar subquery in WHERE, then an IN subquery for list membership."""
    d = _data_dir()

    result = duckdb.sql(f"""
        SELECT
            order_id,
            customer_id,
            total,
            (SELECT ROUND(AVG(total), 2) FROM '{d / "m13_orders.csv"}'
             WHERE status = 'Completed') AS avg_total
        FROM '{d / "m13_orders.csv"}'
        WHERE status = 'Completed'
          AND total > (SELECT AVG(total) FROM '{d / "m13_orders.csv"}'
                       WHERE status = 'Completed')
        ORDER BY total DESC
    """)
    print("Orders above the average order value:")
    print(result)

    result = duckdb.sql(f"""
        SELECT customer_id, name, city, state
        FROM '{d / "m13_customers.csv"}'
        WHERE customer_id IN (
            SELECT DISTINCT customer_id
            FROM '{d / "m13_orders.csv"}'
            WHERE total > 500
              AND status = 'Completed'
        )
        ORDER BY customer_id
    """)
    print("Customers with at least one order over $500:")
    print(result)


# ---------------------------------------------------------------------------
# Section 13.5 — DuckDB + Polars: The Integrated Workflow
# ---------------------------------------------------------------------------

def demo_query_polars_dfs():
    """Query Polars DataFrames by variable name (zero-copy replacement scan)."""
    d = _data_dir()
    orders = pl.read_csv(d / "m13_orders.csv")  # noqa: F841 (referenced in SQL)
    customers = pl.read_csv(d / "m13_customers.csv")  # noqa: F841

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


def demo_sql_to_polars():
    """Convert a DuckDB result to a Polars DataFrame with .pl()."""
    d = _data_dir()
    orders = pl.read_csv(d / "m13_orders.csv")  # noqa: F841
    customers = pl.read_csv(d / "m13_customers.csv")  # noqa: F841

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


def demo_in_memory_tables():
    """CREATE TABLE from CSV files inside an in-memory database, then query."""
    d = _data_dir()
    con = duckdb.connect()  # a private in-memory database

    con.sql(f"CREATE TABLE orders_tbl AS SELECT * FROM '{d / 'm13_orders.csv'}'")
    con.sql(f"CREATE TABLE customers_tbl AS SELECT * FROM '{d / 'm13_customers.csv'}'")
    con.sql(f"CREATE TABLE items_tbl AS SELECT * FROM '{d / 'm13_order_items.csv'}'")

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
    con.close()


def demo_capstone_report():
    """The BI report: three SQL queries -> Polars DataFrames -> summary line."""
    d = _data_dir()

    customer_ltv = duckdb.sql(f"""
        SELECT
            c.name,
            c.state,
            COUNT(DISTINCT o.order_id) AS total_orders,
            ROUND(SUM(o.total), 2) AS lifetime_value,
            ROUND(AVG(o.total), 2) AS avg_order,
            MIN(o.order_date) AS first_order,
            MAX(o.order_date) AS last_order
        FROM '{d / "m13_orders.csv"}' AS o
        INNER JOIN '{d / "m13_customers.csv"}' AS c
            ON o.customer_id = c.customer_id
        WHERE o.status = 'Completed'
        GROUP BY c.name, c.state
        ORDER BY lifetime_value DESC
    """).pl()
    print("Customer Lifetime Value Report:")
    print(customer_ltv)

    category_perf = duckdb.sql(f"""
        SELECT
            i.category,
            COUNT(DISTINCT i.order_id) AS orders_containing,
            SUM(i.quantity) AS units_sold,
            ROUND(SUM(i.quantity * i.unit_price), 2) AS revenue,
            ROUND(AVG(i.unit_price), 2) AS avg_unit_price,
            COUNT(DISTINCT i.product) AS unique_products
        FROM '{d / "m13_order_items.csv"}' AS i
        INNER JOIN '{d / "m13_orders.csv"}' AS o
            ON i.order_id = o.order_id
        WHERE o.status = 'Completed'
        GROUP BY i.category
        ORDER BY revenue DESC
    """).pl()
    print("\nCategory Performance:")
    print(category_perf)

    monthly_trend = duckdb.sql(f"""
        SELECT
            strftime(order_date::DATE, '%Y-%m') AS month,
            COUNT(*) AS orders,
            ROUND(SUM(total), 2) AS revenue,
            COUNT(DISTINCT customer_id) AS active_customers
        FROM '{d / "m13_orders.csv"}'
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


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    demos = [
        ("Section 13.1", demo_dataset_overview),
        ("Section 13.1", demo_first_query),
        ("Section 13.2", demo_select_where),
        ("Section 13.2", demo_calculated_columns),
        ("Section 13.2", demo_case_when),
        ("Section 13.3", demo_aggregates),
        ("Section 13.3", demo_group_by_customer),
        ("Section 13.3", demo_group_by_month_category),
        ("Section 13.3", demo_having),
        ("Section 13.4", demo_inner_join),
        ("Section 13.4", demo_left_join),
        ("Section 13.4", demo_three_table_join),
        ("Section 13.4", demo_state_summary),
        ("Section 13.4", demo_subqueries),
        ("Section 13.5", demo_query_polars_dfs),
        ("Section 13.5", demo_sql_to_polars),
        ("Section 13.5", demo_in_memory_tables),
        ("Section 13.5", demo_capstone_report),
    ]
    for section, demo in demos:
        print("=" * 72)
        print(f"{demo.__name__} — Module 13, {section}")
        print("=" * 72)
        demo()
        print()
