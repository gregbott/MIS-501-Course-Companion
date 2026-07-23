"""Module 7 worked-example computations for the MIS 501 Course Companion.

Every demo_*() function below reproduces exactly one Worked Example in
docs/modules/07-dictionaries-and-sets.md. Run this script directly to print
each example's output under a separator header, in the same order the
examples appear in the chapter.

All data is self-contained literal data (no files, no network). Sets are
always printed through sorted() so the displayed output is deterministic.

References in Course Companion:
    demo_create_dictionaries()         -> Module 7, Section 7.1 (Dictionaries: Looking Up Data by Name)
    demo_access_with_get()             -> Module 7, Section 7.1 (Dictionaries: Looking Up Data by Name)
    demo_modify_dictionary()           -> Module 7, Section 7.2 (Modifying and Iterating Over Dictionaries)
    demo_merge_with_update()           -> Module 7, Section 7.2 (Modifying and Iterating Over Dictionaries)
    demo_keys_values_items()           -> Module 7, Section 7.2 (Modifying and Iterating Over Dictionaries)
    demo_membership_check()            -> Module 7, Section 7.2 (Modifying and Iterating Over Dictionaries)
    demo_regional_sales_report()       -> Module 7, Section 7.2 (Modifying and Iterating Over Dictionaries)
    demo_nested_employee_directory()   -> Module 7, Section 7.3 (Nested Dictionaries, Comprehensions, and Counting)
    demo_price_lookup_comprehension()  -> Module 7, Section 7.3 (Nested Dictionaries, Comprehensions, and Counting)
    demo_discount_comprehension()      -> Module 7, Section 7.3 (Nested Dictionaries, Comprehensions, and Counting)
    demo_counting_patterns()           -> Module 7, Section 7.3 (Nested Dictionaries, Comprehensions, and Counting)
    demo_set_deduplication()           -> Module 7, Section 7.4 (Sets and Set Operations)
    demo_set_operations()              -> Module 7, Section 7.4 (Sets and Set Operations)
    demo_repeat_customers()            -> Module 7, Section 7.4 (Sets and Set Operations)
    demo_capstone_sales_dashboard()    -> Module 7, Section 7.5 (Choosing the Right Structure & Capstone)

Last updated: 2026-07-23
"""


# ---------------------------------------------------------------------------
# Section 7.1 — Dictionaries: Looking Up Data by Name
# ---------------------------------------------------------------------------

def demo_create_dictionaries():
    """Create a dictionary with a literal, then build one key by key."""
    # A product catalog entry, created all at once with a literal
    product = {
        "name": "Wireless Mouse",
        "sku": "WM-2024-001",
        "price": 29.99,
        "in_stock": True,
        "quantity": 150,
    }

    print(f"Product: {product}")
    print(f"Number of fields: {len(product)}")
    print(f"Type: {type(product)}")
    print()

    # Building a dictionary one key at a time
    customer = {}
    customer["name"] = "Acme Corp"
    customer["industry"] = "Manufacturing"
    customer["balance"] = 15000.00
    customer["active"] = True

    print(f"Customer record: {customer}")


def demo_access_with_get():
    """Square-bracket access vs. safe access with .get()."""
    employee = {
        "name": "Sarah Chen",
        "department": "Marketing",
        "salary": 78000,
        "years": 5,
    }

    # Square bracket access — key must exist
    print(f"Name: {employee['name']}")
    print(f"Department: {employee['department']}")
    print(f"Salary: ${employee['salary']:,}")

    # Safe access with .get()
    print(f"Title: {employee.get('title', 'Not specified')}")
    print(f"Email: {employee.get('email')}")  # Returns None


# ---------------------------------------------------------------------------
# Section 7.2 — Modifying and Iterating Over Dictionaries
# ---------------------------------------------------------------------------

def demo_modify_dictionary():
    """Update a value, add a key, and remove a key with .pop()."""
    store = {
        "name": "Downtown Branch",
        "manager": "Tom Rivera",
        "monthly_revenue": 85000,
    }

    print(f"Before: {store}")

    # Update an existing value
    store["monthly_revenue"] = 92000

    # Add a new key-value pair
    store["employees"] = 12

    # Remove a key-value pair
    removed = store.pop("manager")
    print(f"Removed manager: {removed}")
    print(f"After: {store}")


def demo_merge_with_update():
    """Merge one dictionary into another with .update()."""
    base_order = {
        "order_id": "ORD-4521",
        "customer": "Bright Solutions",
        "total": 1250.00,
    }

    shipping_info = {
        "shipping_method": "Express",
        "shipping_cost": 24.99,
        "total": 1274.99,  # Updated total including shipping
    }

    print(f"Before merge: {base_order}")
    print()

    base_order.update(shipping_info)
    print("Merged order:")
    for key, value in base_order.items():
        print(f"  {key}: {value}")


def demo_keys_values_items():
    """The three dictionary views: .keys(), .values(), and .items()."""
    inventory = {
        "Laptop": 45,
        "Monitor": 120,
        "Keyboard": 200,
        "Mouse": 350,
        "Webcam": 85,
    }

    print("Keys:", list(inventory.keys()))
    print("Values:", list(inventory.values()))
    print()

    # Iterating with .items() — the most common pattern
    print("Inventory Report (LOW = fewer than 100 units)")
    print("-" * 30)
    for product, qty in inventory.items():
        status = "LOW" if qty < 100 else "OK"
        print(f"  {product:<12} {qty:>5} units  [{status}]")


def demo_membership_check():
    """Use `in` and `not in` to test whether a key exists."""
    prices = {
        "Basic Plan": 9.99,
        "Pro Plan": 29.99,
        "Enterprise": 99.99,
    }

    # Check if a plan exists before accessing it
    plan_name = "Pro Plan"
    if plan_name in prices:
        print(f"{plan_name} costs ${prices[plan_name]}")
    else:
        print(f"{plan_name} not found in pricing")

    # Check if a plan does NOT exist
    plan_name = "Student Plan"
    if plan_name not in prices:
        print(f"{plan_name} is not available")


def demo_regional_sales_report():
    """Iterate over a dictionary with .items() to build a sales report."""
    regional_sales = {
        "Northeast": 245000,
        "Southeast": 198000,
        "Midwest": 167000,
        "Southwest": 210000,
        "West": 312000,
    }

    total = sum(regional_sales.values())

    print("Regional Sales Report")
    print("=" * 45)
    for region, revenue in regional_sales.items():
        pct = revenue / total * 100
        print(f"  {region:<12}  ${revenue:>10,}  ({pct:5.1f}%)")
    print("-" * 45)
    print(f"  {'Total':<12}  ${total:>10,}")


# ---------------------------------------------------------------------------
# Section 7.3 — Nested Dictionaries, Comprehensions, and Counting
# ---------------------------------------------------------------------------

def demo_nested_employee_directory():
    """Drill into one nested record, then iterate over all of them."""
    employees = {
        "E001": {
            "name": "Alice Park",
            "department": "Engineering",
            "salary": 95000,
            "skills": ["Python", "SQL", "Tableau"],
        },
        "E002": {
            "name": "Bob Martinez",
            "department": "Marketing",
            "salary": 72000,
            "skills": ["Excel", "PowerPoint", "Analytics"],
        },
        "E003": {
            "name": "Carol Wu",
            "department": "Finance",
            "salary": 88000,
            "skills": ["Excel", "Python", "SAP"],
        },
    }

    # Accessing nested data — one bracket per level
    print(f"Employee E001: {employees['E001']['name']}")
    print(f"Department: {employees['E001']['department']}")
    print(f"Skills: {', '.join(employees['E001']['skills'])}")
    print()

    # Iterating through the nested dictionary
    print("Employee Directory")
    print("=" * 50)
    for emp_id, info in employees.items():
        print(f"  [{emp_id}] {info['name']:<16} {info['department']:<14} ${info['salary']:>8,}")

    # Calculate average salary across all records
    avg_salary = sum(info["salary"] for info in employees.values()) / len(employees)
    print(f"\n  Average salary: ${avg_salary:,.2f}")


def demo_price_lookup_comprehension():
    """Build a lookup dict from a list of tuples, then a filtered version."""
    products = [
        ("Laptop", 999.99),
        ("Monitor", 349.50),
        ("Keyboard", 79.95),
        ("Mouse", 24.99),
        ("Webcam", 64.50),
    ]

    # Create a dict from a list of tuples
    price_lookup = {name: price for name, price in products}
    print(f"Price lookup: {price_lookup}")

    # With a filter — only products over $50
    premium = {name: price for name, price in products if price > 50}
    print(f"Premium items (over $50): {premium}")


def demo_discount_comprehension():
    """Transform an existing dictionary with a comprehension (15% off)."""
    original_prices = {
        "Widget A": 45.00,
        "Widget B": 120.00,
        "Widget C": 32.00,
        "Widget D": 89.00,
    }

    sale_prices = {
        name: round(price * 0.85, 2)
        for name, price in original_prices.items()
    }

    print("15% Off Sale:")
    for name in original_prices:
        print(f"  {name}: ${original_prices[name]:.2f} → ${sale_prices[name]:.2f}")


def demo_counting_patterns():
    """Count occurrences two ways: if/else, then the .get() shortcut."""
    # Pattern 1: explicit if/else check
    orders = [
        "Northeast", "West", "Southeast", "West", "Midwest",
        "Northeast", "West", "Southwest", "Northeast", "Southeast",
        "West", "Midwest", "Northeast", "Southwest", "West",
    ]

    region_counts = {}
    for region in orders:
        if region in region_counts:
            region_counts[region] += 1
        else:
            region_counts[region] = 1

    print(f"Total orders processed: {len(orders)}")
    print("Orders by region:")
    for region, count in sorted(region_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {region:<12} {count} orders")

    # Pattern 2: the .get() shortcut — .get(key, 0) supplies 0 for new keys
    transactions = [
        {"product": "Laptop", "category": "Electronics"},
        {"product": "Desk Chair", "category": "Furniture"},
        {"product": "Monitor", "category": "Electronics"},
        {"product": "Notebook", "category": "Office Supplies"},
        {"product": "Standing Desk", "category": "Furniture"},
        {"product": "Webcam", "category": "Electronics"},
        {"product": "Pens", "category": "Office Supplies"},
        {"product": "Keyboard", "category": "Electronics"},
    ]

    category_counts = {}
    for txn in transactions:
        cat = txn["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1

    print()
    print(f"Total transactions processed: {len(transactions)}")
    print("Transactions by category:")
    for cat, count in category_counts.items():
        print(f"  {cat:<18} {count}")


# ---------------------------------------------------------------------------
# Section 7.4 — Sets and Set Operations
# ---------------------------------------------------------------------------

def demo_set_deduplication():
    """Convert a list with duplicates into a set of unique items."""
    raw_departments = [
        "Marketing", "Engineering", "Marketing", "Finance",
        "Engineering", "HR", "Marketing", "Finance", "Engineering",
    ]

    unique_departments = set(raw_departments)
    print(f"Raw list ({len(raw_departments)} items): {raw_departments}")
    # sorted() only for display — a set has no order of its own
    print(f"Unique set ({len(unique_departments)} items): {sorted(unique_departments)}")


def demo_set_operations():
    """Union, intersection, difference, and symmetric difference."""
    team_a_skills = {"Python", "SQL", "Excel", "Tableau", "R"}
    team_b_skills = {"Python", "Java", "SQL", "PowerBI", "Spark"}

    # sorted() only for display — sets are unordered, so we sort for a stable view
    print(f"Team A: {sorted(team_a_skills)}")
    print(f"Team B: {sorted(team_b_skills)}")
    print()

    # Union — all skills across both teams
    all_skills = team_a_skills | team_b_skills
    print(f"All skills (union):         {sorted(all_skills)}")

    # Intersection — skills both teams share
    shared_skills = team_a_skills & team_b_skills
    print(f"Shared skills (intersect):  {sorted(shared_skills)}")

    # Difference — skills unique to Team A
    only_a = team_a_skills - team_b_skills
    print(f"Only Team A (difference):   {sorted(only_a)}")

    # Symmetric difference — skills unique to one team
    unique_to_one = team_a_skills ^ team_b_skills
    print(f"Unique to one team (sym):   {sorted(unique_to_one)}")


def demo_repeat_customers():
    """Compare two quarters of customers with set operations."""
    q1_customers = {"Acme Corp", "Bright Solutions", "CyberTech", "DataFlow", "EcoGoods"}
    q2_customers = {"Bright Solutions", "DataFlow", "FreshStart", "GreenTech", "Acme Corp"}

    repeat_customers = q1_customers & q2_customers
    new_in_q2 = q2_customers - q1_customers
    lost_in_q2 = q1_customers - q2_customers

    # sorted() only for display — sets are unordered
    print(f"Repeat customers: {sorted(repeat_customers)}")
    print(f"New in Q2: {sorted(new_in_q2)}")
    print(f"Lost after Q1: {sorted(lost_in_q2)}")


# ---------------------------------------------------------------------------
# Section 7.5 — Choosing the Right Structure & Capstone
# ---------------------------------------------------------------------------

def demo_capstone_sales_dashboard():
    """Combine dicts, comprehensions, and sets into a sales dashboard."""
    # Raw transaction data — a list of dictionaries
    transactions = [
        {"rep": "Alice", "region": "West", "product": "Laptop", "amount": 2499.00},
        {"rep": "Bob", "region": "East", "product": "Monitor", "amount": 699.00},
        {"rep": "Alice", "region": "West", "product": "Keyboard", "amount": 159.00},
        {"rep": "Carol", "region": "East", "product": "Laptop", "amount": 2499.00},
        {"rep": "Bob", "region": "East", "product": "Webcam", "amount": 129.00},
        {"rep": "Dave", "region": "Central", "product": "Laptop", "amount": 2499.00},
        {"rep": "Alice", "region": "West", "product": "Monitor", "amount": 699.00},
        {"rep": "Carol", "region": "East", "product": "Mouse", "amount": 49.00},
        {"rep": "Dave", "region": "Central", "product": "Keyboard", "amount": 159.00},
        {"rep": "Alice", "region": "West", "product": "Webcam", "amount": 129.00},
    ]

    # 1. Total revenue by region (dictionary accumulator with .get())
    region_revenue = {}
    for txn in transactions:
        r = txn["region"]
        region_revenue[r] = region_revenue.get(r, 0) + txn["amount"]

    print("Revenue by Region")
    print("=" * 35)
    for region, rev in sorted(region_revenue.items(), key=lambda x: x[1], reverse=True):
        print(f"  {region:<10} ${rev:>10,.2f}")
    grand_total = sum(region_revenue.values())
    print(f"  {'Total':<10} ${grand_total:>10,.2f}")

    # 2. Total revenue per rep (same accumulator pattern)
    rep_revenue = {}
    for txn in transactions:
        rep = txn["rep"]
        rep_revenue[rep] = rep_revenue.get(rep, 0) + txn["amount"]

    print("\nRevenue by Sales Rep")
    print("=" * 35)
    for rep, rev in sorted(rep_revenue.items(), key=lambda x: x[1], reverse=True):
        print(f"  {rep:<10} ${rev:>10,.2f}")

    # 3. Unique products sold (set comprehension)
    products_sold = {txn["product"] for txn in transactions}
    # sorted() only for display — sets are unordered
    print(f"\nUnique products sold: {sorted(products_sold)}")
    print(f"Number of unique products: {len(products_sold)}")

    # 4. Which products do two reps have in common? (set intersection)
    alice_products = {txn["product"] for txn in transactions if txn["rep"] == "Alice"}
    bob_products = {txn["product"] for txn in transactions if txn["rep"] == "Bob"}
    shared = alice_products & bob_products
    print(f"\nProducts both Alice and Bob sell: {sorted(shared)}")


if __name__ == "__main__":
    demos = [
        ("Section 7.1", demo_create_dictionaries),
        ("Section 7.1", demo_access_with_get),
        ("Section 7.2", demo_modify_dictionary),
        ("Section 7.2", demo_merge_with_update),
        ("Section 7.2", demo_keys_values_items),
        ("Section 7.2", demo_membership_check),
        ("Section 7.2", demo_regional_sales_report),
        ("Section 7.3", demo_nested_employee_directory),
        ("Section 7.3", demo_price_lookup_comprehension),
        ("Section 7.3", demo_discount_comprehension),
        ("Section 7.3", demo_counting_patterns),
        ("Section 7.4", demo_set_deduplication),
        ("Section 7.4", demo_set_operations),
        ("Section 7.4", demo_repeat_customers),
        ("Section 7.5", demo_capstone_sales_dashboard),
    ]
    for section, demo in demos:
        print("=" * 72)
        print(f"{demo.__name__} — Module 7, {section}")
        print("=" * 72)
        demo()
        print()
