"""Module 9 computation examples: Introduction to Polars.

Every demo function below backs one Worked Example in the Module 9 chapter of
the MIS 501 Course Companion. The chapter pastes each function's stdout
verbatim, so do not edit outputs by hand — rerun this script instead.

References in Course Companion:
    demo_create_dataframe()   -> Module 9, Section 9.1 (Why Polars? DataFrames and Series)
    demo_series()             -> Module 9, Section 9.1 (Why Polars? DataFrames and Series)
    demo_inspect_dataframe()  -> Module 9, Section 9.1 (Why Polars? DataFrames and Series)
    demo_read_csv()           -> Module 9, Section 9.2 (Reading Data from Files)
    demo_read_json()          -> Module 9, Section 9.2 (Reading Data from Files)
    demo_select_columns()     -> Module 9, Section 9.3 (Selecting Columns with select())
    demo_select_expressions() -> Module 9, Section 9.3 (Selecting Columns with select())
    demo_filter_rows()        -> Module 9, Section 9.4 (Filtering Rows with filter())
    demo_filter_strings()     -> Module 9, Section 9.4 (Filtering Rows with filter())
    demo_filter_is_in()       -> Module 9, Section 9.4 (Filtering Rows with filter())
    demo_sort_salary()        -> Module 9, Section 9.5 (Sorting, Writing, and Chaining Pipelines)
    demo_sort_multi_column()  -> Module 9, Section 9.5 (Sorting, Writing, and Chaining Pipelines)
    demo_write_csv()          -> Module 9, Section 9.5 (Sorting, Writing, and Chaining Pipelines)
    demo_chained_pipeline()   -> Module 9, Section 9.5 (Sorting, Writing, and Chaining Pipelines)
    demo_capstone_pipeline()  -> Module 9, Section 9.5 (Sorting, Writing, and Chaining Pipelines)

Data: the 10-employee HR dataset and 6-record sales JSON from the Module 9
teaching notebook (m09_teaching.py), embedded as literals so the script is
self-contained. Deterministic — no randomness, no network. File output goes
to computations/_scratch/module09/ (stdout shows bare filenames only, never
absolute paths).

Last updated: 2026-07-23
"""

import json
from pathlib import Path

import polars as pl

SCRATCH_DIR = Path(__file__).resolve().parent / "_scratch" / "module09"

EMPLOYEES_CSV = """employee_id,name,department,hire_date,salary,performance_score
E101,Alice Park,Engineering,2020-03-15,95000,4.2
E102,Bob Martinez,Marketing,2019-07-01,72000,3.8
E103,Carol Wu,Finance,2021-01-10,88000,4.5
E104,David Chen,Engineering,2022-06-20,85000,3.9
E105,Eva Lopez,Marketing,2020-11-05,76000,4.1
E106,Frank Kim,Finance,2018-04-18,92000,4.3
E107,Grace Patel,Engineering,2023-02-14,82000,3.7
E108,Henry Okafor,Operations,2019-09-30,68000,4.0
E109,Iris Tanaka,Operations,2021-08-22,71000,3.6
E110,Jack Rivera,Marketing,2020-05-12,74000,4.4
"""


def _employees_csv_path() -> Path:
    """Silently write the sample employees CSV to scratch and return its path.

    The doc shows students the simple path ``employees.csv``; the demos read
    the same content from the scratch directory so the script is standalone.
    """
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    path = SCRATCH_DIR / "employees.csv"
    path.write_text(EMPLOYEES_CSV, encoding="utf-8")
    return path


def make_products() -> pl.DataFrame:
    """The 5-product catalog used in the DataFrame-creation demos."""
    return pl.DataFrame(
        {
            "product": ["Laptop", "Monitor", "Keyboard", "Mouse", "Webcam"],
            "category": [
                "Electronics", "Electronics", "Accessories",
                "Accessories", "Electronics",
            ],
            "price": [999.99, 349.50, 79.95, 24.99, 64.50],
            "units_sold": [45, 120, 200, 350, 85],
        }
    )


# ---------------------------------------------------------------------------
# Section 9.1 — Why Polars? DataFrames and Series
# ---------------------------------------------------------------------------

def demo_create_dataframe():
    """Import Polars, print its version, and build a DataFrame from a dict."""
    print(f"Polars version: {pl.__version__}")
    print()

    products = make_products()
    print("Product DataFrame:")
    print(products)


def demo_series():
    """Create a Series (a single column) and compute basic statistics."""
    revenue = pl.Series("monthly_revenue", [42000, 51000, 38000, 47000, 55000])

    print(revenue)
    print(f"Dtype: {revenue.dtype}")
    print(f"Length: {len(revenue)}")
    print(f"Sum: ${revenue.sum():,}")
    print(f"Mean: ${revenue.mean():,.2f}")


def demo_inspect_dataframe():
    """Inspect a DataFrame: shape, columns, schema, and describe()."""
    products = make_products()

    print(f"Shape: {products.shape}")
    print(f"Columns: {products.columns}")
    print(f"Schema: {products.schema}")
    print()
    print("Summary statistics (describe):")
    print(products.describe())


# ---------------------------------------------------------------------------
# Section 9.2 — Reading Data from Files
# ---------------------------------------------------------------------------

def demo_read_csv():
    """Create the sample employees CSV, then read it with pl.read_csv()."""
    csv_path = _employees_csv_path()
    print("Created employees.csv with 10 employee records")
    print()

    employees = pl.read_csv(csv_path)
    print(f"Shape: {employees.shape}")
    print(f"Columns: {employees.columns}")
    print()
    print(employees)


def demo_read_json():
    """Create a sample JSON file of sales records, then read it with pl.read_json()."""
    sales_data = [
        {"date": "2025-01-15", "region": "West", "product": "Laptop", "units": 12, "revenue": 11999.88},
        {"date": "2025-01-15", "region": "East", "product": "Monitor", "units": 25, "revenue": 8737.50},
        {"date": "2025-01-16", "region": "West", "product": "Keyboard", "units": 50, "revenue": 3997.50},
        {"date": "2025-01-16", "region": "East", "product": "Laptop", "units": 8, "revenue": 7999.92},
        {"date": "2025-01-17", "region": "Central", "product": "Mouse", "units": 100, "revenue": 2499.00},
        {"date": "2025-01-17", "region": "West", "product": "Webcam", "units": 30, "revenue": 1935.00},
    ]

    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    json_path = SCRATCH_DIR / "sales.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(sales_data, f, indent=2)
    print("Created sales.json with 6 records")
    print()

    sales = pl.read_json(json_path)
    print(f"Shape: {sales.shape}")
    print(sales)


# ---------------------------------------------------------------------------
# Section 9.3 — Selecting Columns with select()
# ---------------------------------------------------------------------------

def demo_select_columns():
    """Select specific columns by name."""
    employees = pl.read_csv(_employees_csv_path())

    selected = employees.select("name", "department", "salary")
    print(selected)


def demo_select_expressions():
    """Select with pl.col() expressions: transform, round, and alias columns."""
    employees = pl.read_csv(_employees_csv_path())

    result = employees.select(
        pl.col("name"),
        pl.col("department"),
        pl.col("salary").alias("annual_salary"),
        (pl.col("salary") / 12).round(2).alias("monthly_salary"),
        (pl.col("salary") / 52).round(2).alias("weekly_salary"),
    )
    print(result)


# ---------------------------------------------------------------------------
# Section 9.4 — Filtering Rows with filter()
# ---------------------------------------------------------------------------

def demo_filter_rows():
    """Filter with a comparison, then combine two conditions with &."""
    employees = pl.read_csv(_employees_csv_path())

    high_earners = employees.filter(pl.col("salary") > 80000)
    print("High earners (salary > $80,000):")
    print(high_earners.select("name", "department", "salary", "performance_score"))
    print()

    top_engineers = employees.filter(
        (pl.col("department") == "Engineering")
        & (pl.col("performance_score") >= 4.0)
    )
    print("Engineering employees with performance >= 4.0:")
    print(top_engineers.select("name", "department", "salary", "performance_score"))


def demo_filter_strings():
    """Filter rows using a string method inside the condition."""
    employees = pl.read_csv(_employees_csv_path())

    result = employees.filter(pl.col("name").str.contains("P"))
    print("Employees with a capital 'P' in their name:")
    print(result.select("name", "department"))


def demo_filter_is_in():
    """Filter for multiple values: | conditions versus is_in()."""
    employees = pl.read_csv(_employees_csv_path())

    with_or = employees.filter(
        (pl.col("department") == "Marketing")
        | (pl.col("department") == "Finance")
    )
    print("Marketing or Finance employees (two conditions with |):")
    print(with_or.select("name", "department", "salary"))
    print()

    with_is_in = employees.filter(pl.col("department").is_in(["Marketing", "Finance"]))
    print("Same rows with is_in():")
    print(with_is_in.select("name", "department", "salary"))


# ---------------------------------------------------------------------------
# Section 9.5 — Sorting, Writing, and Chaining Pipelines
# ---------------------------------------------------------------------------

def demo_sort_salary():
    """Sort by salary descending, then preview the top rows with head()."""
    employees = pl.read_csv(_employees_csv_path())

    by_salary = employees.sort("salary", descending=True)
    print("Employees by salary (highest first):")
    print(by_salary.select("name", "department", "salary"))
    print()

    print("Top 3 earners:")
    print(by_salary.head(3).select("name", "salary"))


def demo_sort_multi_column():
    """Sort by department ascending, then salary descending within each."""
    employees = pl.read_csv(_employees_csv_path())

    result = employees.sort(
        "department",
        "salary",
        descending=[False, True],
    )
    print("By department (A-Z), then salary (high to low) within each:")
    print(result.select("name", "department", "salary"))


def demo_write_csv():
    """Filter the engineers, write them to a CSV, and read it back to verify."""
    employees = pl.read_csv(_employees_csv_path())

    engineers = employees.filter(pl.col("department") == "Engineering")
    out_path = SCRATCH_DIR / "engineers.csv"
    engineers.write_csv(out_path)

    verified = pl.read_csv(out_path)
    print(f"Wrote {verified.shape[0]} engineering records to engineers.csv")
    print()
    print("Read back from engineers.csv to verify:")
    print(verified.select("employee_id", "name", "salary", "performance_score"))


def demo_chained_pipeline():
    """Chain filter -> select -> sort into a single readable pipeline."""
    employees = pl.read_csv(_employees_csv_path())

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


def demo_capstone_pipeline():
    """Capstone: overview, department counts, and the raise-candidates pipeline."""
    employees = pl.read_csv(_employees_csv_path())

    print("=== Employee Dataset Overview ===")
    print(f"Total employees: {employees.shape[0]}")
    print(f"Columns: {employees.columns}")
    print()

    dept_counts = (
        employees
        .select("department")
        .to_series()
        .value_counts()
        # tiebreak on the department name so ties print in a stable order
        .sort("count", "department", descending=[True, False])
    )
    print("Employees per department:")
    for dept, count in dept_counts.iter_rows():
        print(f"  {dept:<14} {count} employees")
    print()

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

    out_path = SCRATCH_DIR / "raise_candidates.csv"
    raise_candidates.write_csv(out_path)
    print(f"Wrote {raise_candidates.shape[0]} raise candidates to raise_candidates.csv")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    demos = [
        demo_create_dataframe,
        demo_series,
        demo_inspect_dataframe,
        demo_read_csv,
        demo_read_json,
        demo_select_columns,
        demo_select_expressions,
        demo_filter_rows,
        demo_filter_strings,
        demo_filter_is_in,
        demo_sort_salary,
        demo_sort_multi_column,
        demo_write_csv,
        demo_chained_pipeline,
        demo_capstone_pipeline,
    ]

    for demo in demos:
        print("=" * 70)
        print(f"# {demo.__name__}")
        print("=" * 70)
        demo()
        print()
