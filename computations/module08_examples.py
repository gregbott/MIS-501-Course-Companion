"""Module 8 worked-example computations for the MIS501 Course Companion.

Every demo_*() function below reproduces exactly one Worked Example in
docs/modules/08-file-io-and-json.md. Run this script directly to print
each example's output under a separator header, in the same order the
examples appear in the chapter.

All files the demos create or read live under computations/_scratch/module08/
(a sandbox folder), so the demos are self-contained, deterministic, and
re-runnable. Printed labels use bare filenames only — never absolute paths —
so the chapter's Output blocks match what a student sees when running the
same code in their own working folder.

References in Course Companion:
    demo_create_sales_log()          -> Module 8, Section 8.1 (Reading Text Files)
    demo_read_entire_file()          -> Module 8, Section 8.1 (Reading Text Files)
    demo_read_line_by_line()         -> Module 8, Section 8.1 (Reading Text Files)
    demo_parse_sales_log()           -> Module 8, Section 8.1 (Reading Text Files)
    demo_write_sales_report()        -> Module 8, Section 8.2 (Writing Text Files)
    demo_pathlib_inspection()        -> Module 8, Section 8.3 (The pathlib Module)
    demo_pathlib_shortcuts()         -> Module 8, Section 8.3 (The pathlib Module)
    demo_write_company_json()        -> Module 8, Section 8.4 (Working with JSON)
    demo_read_company_json()         -> Module 8, Section 8.4 (Working with JSON)
    demo_nested_json_navigation()    -> Module 8, Section 8.4 (Working with JSON)
    demo_json_loads_api_response()   -> Module 8, Section 8.4 (Working with JSON)
    demo_json_dumps_order()          -> Module 8, Section 8.4 (Working with JSON)
    demo_write_json_report()         -> Module 8, Section 8.4 (Working with JSON)
    demo_csv_module()                -> Module 8, Section 8.5 (CSV and the Data Pipeline)
    demo_data_pipeline()             -> Module 8, Section 8.5 (CSV and the Data Pipeline)

Last updated: 2026-07-23
"""

import csv
import json
from pathlib import Path

# Sandbox folder for every file the demos touch (created on import).
SCRATCH = Path(__file__).resolve().parent / "_scratch" / "module08"
SCRATCH.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Shared setup helpers (silent) — let each demo be self-contained even when
# it reads a file that another demo "created" in the chapter's narrative.
# ---------------------------------------------------------------------------

SALES_LOG_LINES = [
    "Date,Product,Units,Revenue",
    "2025-01-15,Widget A,120,3600.00",
    "2025-01-16,Widget B,85,4250.00",
    "2025-01-17,Widget A,95,2850.00",
    "2025-01-18,Widget C,200,6000.00",
    "2025-01-19,Widget B,110,5500.00",
]

COMPANY_DATA = {
    "company": "TechFlow Solutions",
    "founded": 2018,
    "headquarters": "Austin, TX",
    "employees": 145,
    "departments": [
        {
            "name": "Engineering",
            "head": "Maria Lopez",
            "headcount": 60,
            "budget": 2400000,
        },
        {
            "name": "Sales",
            "head": "James Carter",
            "headcount": 45,
            "budget": 1800000,
        },
        {
            "name": "Marketing",
            "head": "Priya Sharma",
            "headcount": 25,
            "budget": 900000,
        },
        {
            "name": "Operations",
            "head": "Kevin O'Brien",
            "headcount": 15,
            "budget": 600000,
        },
    ],
}


def _write_sales_log(path):
    """Write the practice sales log to the given path (no output)."""
    with open(path, "w") as f:
        for line in SALES_LOG_LINES:
            f.write(line + "\n")


def _write_company_json(path):
    """Write the company JSON file to the given path (no output)."""
    with open(path, "w") as f:
        json.dump(COMPANY_DATA, f, indent=2)


# ---------------------------------------------------------------------------
# Section 8.1 — Reading Text Files
# ---------------------------------------------------------------------------

def demo_create_sales_log():
    """Write a practice sales log file line by line with mode 'w'."""
    sample_lines = [
        "Date,Product,Units,Revenue",
        "2025-01-15,Widget A,120,3600.00",
        "2025-01-16,Widget B,85,4250.00",
        "2025-01-17,Widget A,95,2850.00",
        "2025-01-18,Widget C,200,6000.00",
        "2025-01-19,Widget B,110,5500.00",
    ]

    with open(SCRATCH / "sales_log.txt", "w") as f:
        for line in sample_lines:
            f.write(line + "\n")

    print("Created sales_log.txt with 6 lines (1 header + 5 data rows)")


def demo_read_entire_file():
    """Read the whole sales log at once with .read()."""
    _write_sales_log(SCRATCH / "sales_log.txt")

    with open(SCRATCH / "sales_log.txt", "r") as f:
        contents = f.read()

    print("Full file contents:")
    print(contents)
    print(f"Total characters: {len(contents)}")


def demo_read_line_by_line():
    """Stream the sales log one line at a time with a for loop."""
    _write_sales_log(SCRATCH / "sales_log.txt")

    print("Line-by-line reading:")
    with open(SCRATCH / "sales_log.txt", "r") as f:
        for line_num, line in enumerate(f, start=1):
            clean = line.strip()  # Remove trailing newline
            print(f"  Line {line_num}: {clean}")


def demo_parse_sales_log():
    """Parse the sales log into a list of dictionaries and total the revenue."""
    _write_sales_log(SCRATCH / "sales_log.txt")

    sales = []
    with open(SCRATCH / "sales_log.txt", "r") as f:
        header = f.readline().strip().split(",")  # First line is the header
        for line in f:
            parts = line.strip().split(",")
            record = {
                "date": parts[0],
                "product": parts[1],
                "units": int(parts[2]),
                "revenue": float(parts[3]),
            }
            sales.append(record)

    print(f"Parsed {len(sales)} records:")
    for sale in sales:
        print(
            f"  {sale['date']}  {sale['product']:<10}  "
            f"{sale['units']:>4} units  ${sale['revenue']:>9,.2f}"
        )

    total_revenue = sum(s["revenue"] for s in sales)
    print(f"\nTotal revenue: ${total_revenue:,.2f}")


# ---------------------------------------------------------------------------
# Section 8.2 — Writing Text Files
# ---------------------------------------------------------------------------

def demo_write_sales_report():
    """Write a formatted summary report with mode 'w', then read it back."""
    sales = [
        {"date": "2025-01-15", "product": "Widget A", "units": 120, "revenue": 3600.00},
        {"date": "2025-01-16", "product": "Widget B", "units": 85, "revenue": 4250.00},
        {"date": "2025-01-17", "product": "Widget A", "units": 95, "revenue": 2850.00},
        {"date": "2025-01-18", "product": "Widget C", "units": 200, "revenue": 6000.00},
        {"date": "2025-01-19", "product": "Widget B", "units": 110, "revenue": 5500.00},
    ]

    with open(SCRATCH / "sales_report.txt", "w") as f:
        f.write("Daily Sales Report\n")
        f.write("=" * 50 + "\n\n")
        for sale in sales:
            f.write(f"{sale['date']}  {sale['product']:<10}  ${sale['revenue']:>9,.2f}\n")
        total = sum(s["revenue"] for s in sales)
        f.write(f"\n{'Total':<22}  ${total:>9,.2f}\n")

    # Verify by reading it back
    with open(SCRATCH / "sales_report.txt", "r") as f:
        print(f.read())


# ---------------------------------------------------------------------------
# Section 8.3 — The pathlib Module
# ---------------------------------------------------------------------------

def demo_pathlib_inspection():
    """Build a path with / and inspect its parts and existence."""
    data_dir = SCRATCH / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    _write_sales_log(data_dir / "sales_log.txt")

    # The chapter shows Path("data") / "sales_log.txt"; here the same
    # relative path is displayed while checks run inside the sandbox.
    file_abs = data_dir / "sales_log.txt"
    file_path = file_abs.relative_to(SCRATCH)

    print(f"Path: {file_path}")
    print(f"Name: {file_path.name}")
    print(f"Stem (no extension): {file_path.stem}")
    print(f"Extension: {file_path.suffix}")
    print(f"Parent directory: {file_path.parent}")
    print(f"Exists? {file_abs.exists()}")
    print(f"Is a file? {file_abs.is_file()}")


def demo_pathlib_shortcuts():
    """Use .write_text() and .read_text() to skip open/close entirely."""
    path = SCRATCH / "quick_note.txt"
    path.write_text("This is a quick note written with pathlib.\nLine two.\n")

    content = path.read_text()
    print(f"Read back:\n{content}")


# ---------------------------------------------------------------------------
# Section 8.4 — Working with JSON
# ---------------------------------------------------------------------------

def demo_write_company_json():
    """Save a nested Python dictionary as a formatted JSON file."""
    company_data = {
        "company": "TechFlow Solutions",
        "founded": 2018,
        "headquarters": "Austin, TX",
        "employees": 145,
        "departments": [
            {
                "name": "Engineering",
                "head": "Maria Lopez",
                "headcount": 60,
                "budget": 2400000,
            },
            {
                "name": "Sales",
                "head": "James Carter",
                "headcount": 45,
                "budget": 1800000,
            },
            {
                "name": "Marketing",
                "head": "Priya Sharma",
                "headcount": 25,
                "budget": 900000,
            },
            {
                "name": "Operations",
                "head": "Kevin O'Brien",
                "headcount": 15,
                "budget": 600000,
            },
        ],
    }

    # Write JSON to file with pretty formatting
    with open(SCRATCH / "company.json", "w") as f:
        json.dump(company_data, f, indent=2)

    print("Created company.json with 4 departments")


def demo_read_company_json():
    """Load a JSON file back into a Python dictionary with json.load()."""
    _write_company_json(SCRATCH / "company.json")

    with open(SCRATCH / "company.json", "r") as f:
        data = json.load(f)

    print(f"Company: {data['company']}")
    print(f"Founded: {data['founded']}")
    print(f"Headquarters: {data['headquarters']}")
    print(f"Total employees: {data['employees']}")
    print(f"Number of departments: {len(data['departments'])}")
    print(f"Type of loaded data: {type(data)}")


def demo_nested_json_navigation():
    """Drill into nested JSON and aggregate across a list of dictionaries."""
    _write_company_json(SCRATCH / "company.json")

    with open(SCRATCH / "company.json", "r") as f:
        data = json.load(f)

    # Navigating nested JSON
    print("Department Details:")
    print("=" * 55)
    for dept in data["departments"]:
        avg_cost = dept["budget"] / dept["headcount"]
        print(
            f"  {dept['name']:<14} "
            f"Head: {dept['head']:<16} "
            f"Staff: {dept['headcount']:>3}  "
            f"Budget: ${dept['budget']:>10,}   "
            f"Average cost: ${avg_cost:,.0f}"
        )

    # Aggregation from nested data
    total_budget = sum(dept["budget"] for dept in data["departments"])
    total_staff = sum(dept["headcount"] for dept in data["departments"])
    print(f"\n  {'Totals':<14} {'':16} Staff: {total_staff:>3}  Budget: ${total_budget:>10,}")


def demo_json_loads_api_response():
    """Parse a JSON string (as if received from a web API) with json.loads()."""
    api_response = '''
    {
        "status": "success",
        "results": 3,
        "data": [
            {"id": 101, "city": "Austin", "temp_f": 78},
            {"id": 102, "city": "Denver", "temp_f": 55},
            {"id": 103, "city": "Miami", "temp_f": 88}
        ]
    }
    '''

    weather = json.loads(api_response)

    print(f"Status: {weather['status']}")
    print(f"Results: {weather['results']}")
    print()
    for city_data in weather["data"]:
        print(f"  {city_data['city']}: {city_data['temp_f']}°F")


def demo_json_dumps_order():
    """Convert a Python dictionary to a formatted JSON string with json.dumps()."""
    order = {
        "order_id": "ORD-7890",
        "customer": "Bright Solutions",
        "items": [
            {"product": "Laptop", "qty": 3, "price": 999.99},
            {"product": "Monitor", "qty": 5, "price": 349.50},
        ],
        "total": 4747.47,
        "shipped": False,
    }

    json_string = json.dumps(order, indent=2)
    print("Python dict → JSON string:")
    print(json_string)


def demo_write_json_report():
    """Build a report dictionary, save it as JSON, and read it back to verify."""
    monthly_sales = [
        {"month": "January", "revenue": 45200, "expenses": 32100, "customers": 128},
        {"month": "February", "revenue": 51800, "expenses": 35400, "customers": 145},
        {"month": "March", "revenue": 48900, "expenses": 33800, "customers": 137},
    ]

    report = {
        "report_name": "Q1 Sales Summary",
        "generated_by": "MIS501 Python Script",
        "months": monthly_sales,
        "totals": {
            "revenue": sum(m["revenue"] for m in monthly_sales),
            "expenses": sum(m["expenses"] for m in monthly_sales),
            "customers": sum(m["customers"] for m in monthly_sales),
        },
    }

    # Write to file
    with open(SCRATCH / "q1_report.json", "w") as f:
        json.dump(report, f, indent=2)

    # Read it back to verify
    with open(SCRATCH / "q1_report.json", "r") as f:
        verified = json.load(f)

    print(f"Report: {verified['report_name']}")
    print(f"Total revenue: ${verified['totals']['revenue']:,}")
    print(f"Total expenses: ${verified['totals']['expenses']:,}")
    print(f"Total customers: {verified['totals']['customers']}")
    print(f"Profit: ${verified['totals']['revenue'] - verified['totals']['expenses']:,}")


# ---------------------------------------------------------------------------
# Section 8.5 — CSV and the Data Pipeline
# ---------------------------------------------------------------------------

def demo_csv_module():
    """Write and read a CSV file with the built-in csv module."""
    employees = [
        {"name": "Alice Park", "department": "Engineering", "salary": 95000},
        {"name": "Bob Martinez", "department": "Marketing", "salary": 72000},
        {"name": "Carol Wu", "department": "Finance", "salary": 88000},
    ]

    # Write CSV
    with open(SCRATCH / "employees.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "department", "salary"])
        writer.writeheader()
        writer.writerows(employees)

    # Read CSV back
    with open(SCRATCH / "employees.csv", "r") as f:
        reader = csv.DictReader(f)
        print("CSV Contents:")
        for row in reader:
            print(f"  {row['name']:<16} {row['department']:<14} ${int(row['salary']):>8,}")


def demo_data_pipeline():
    """Read a JSON catalog, process it, and write text + JSON outputs."""
    # Step 1: simulate a product catalog from a supplier (JSON input)
    catalog_data = {
        "supplier": "Global Parts Inc.",
        "last_updated": "2025-03-01",
        "products": [
            {"sku": "GP-1001", "name": "Bolt Pack (100)", "unit_price": 12.50, "min_order": 10},
            {"sku": "GP-1002", "name": "Washer Set (50)", "unit_price": 8.75, "min_order": 20},
            {"sku": "GP-1003", "name": "Hex Nut Bag (200)", "unit_price": 15.00, "min_order": 5},
            {"sku": "GP-1004", "name": "Spring Assortment", "unit_price": 22.00, "min_order": 8},
            {"sku": "GP-1005", "name": "Bearing Kit", "unit_price": 45.00, "min_order": 3},
        ],
    }

    catalog_path = SCRATCH / "supplier_catalog.json"
    with open(catalog_path, "w") as f:
        json.dump(catalog_data, f, indent=2)

    print("Step 1: Created supplier_catalog.json (5 products)")

    # Step 2: read the catalog and calculate order costs
    with open(catalog_path, "r") as f:
        catalog = json.load(f)

    order_summary = []
    for prod in catalog["products"]:
        min_cost = prod["unit_price"] * prod["min_order"]
        order_summary.append({
            "sku": prod["sku"],
            "name": prod["name"],
            "unit_price": prod["unit_price"],
            "min_order": prod["min_order"],
            "min_order_cost": min_cost,
        })

    print("Step 2: Calculated minimum order cost for each product")

    # Step 3a: write the text report
    report_path = SCRATCH / "order_analysis.txt"
    with open(report_path, "w") as f:
        f.write(f"Supplier: {catalog['supplier']}\n")
        f.write(f"Catalog date: {catalog['last_updated']}\n")
        f.write("=" * 65 + "\n\n")
        f.write(f"{'SKU':<12} {'Product':<22} {'Unit $':>8} {'Min Qty':>8} {'Min Cost':>10}\n")
        f.write("-" * 65 + "\n")
        for item in order_summary:
            f.write(
                f"{item['sku']:<12} "
                f"{item['name']:<22} "
                f"${item['unit_price']:>7.2f} "
                f"{item['min_order']:>8} "
                f"${item['min_order_cost']:>9.2f}\n"
            )
        total_min = sum(item["min_order_cost"] for item in order_summary)
        f.write("-" * 65 + "\n")
        f.write(f"{'Total minimum order cost':>52} ${total_min:>9.2f}\n")

    # Step 3b: write the JSON output
    json_output = {
        "supplier": catalog["supplier"],
        "analysis_date": "2025-03-15",
        "products": order_summary,
        "total_minimum_order_cost": sum(item["min_order_cost"] for item in order_summary),
    }
    json_path = SCRATCH / "order_analysis.json"
    with open(json_path, "w") as f:
        json.dump(json_output, f, indent=2)

    print(f"Step 3: Wrote {report_path.name} and {json_path.name}\n")

    # Display the text report
    print(report_path.read_text())


if __name__ == "__main__":
    demos = [
        ("Section 8.1", demo_create_sales_log),
        ("Section 8.1", demo_read_entire_file),
        ("Section 8.1", demo_read_line_by_line),
        ("Section 8.1", demo_parse_sales_log),
        ("Section 8.2", demo_write_sales_report),
        ("Section 8.3", demo_pathlib_inspection),
        ("Section 8.3", demo_pathlib_shortcuts),
        ("Section 8.4", demo_write_company_json),
        ("Section 8.4", demo_read_company_json),
        ("Section 8.4", demo_nested_json_navigation),
        ("Section 8.4", demo_json_loads_api_response),
        ("Section 8.4", demo_json_dumps_order),
        ("Section 8.4", demo_write_json_report),
        ("Section 8.5", demo_csv_module),
        ("Section 8.5", demo_data_pipeline),
    ]
    for section, demo in demos:
        print("=" * 72)
        print(f"{demo.__name__} — Module 8, {section}")
        print("=" * 72)
        demo()
        print()
