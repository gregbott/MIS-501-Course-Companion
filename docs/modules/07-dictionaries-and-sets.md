# Module 7: Data Structures: Dictionaries & Sets

## Introduction

Module 6 gave you lists and tuples — collections you access by *position*. But most business data is not positional. When you look up a product, you search by SKU, not by "the third item we entered." When you check a customer's balance, you search by company name. This module introduces the **dictionary**, Python's structure for storing labeled data and retrieving it by name, and the **set**, its structure for collections of unique items. Together they cover an enormous share of everyday business programming: product catalogs, employee records, counting orders by region, deduplicating customer lists, and comparing groups ("which customers ordered in both quarters?"). They are also the shape of things to come — the JSON data you will read from files and APIs later in the course is, at heart, nested dictionaries and lists.

---

## Learning Objectives

By the end of this module, you should be able to:

1. **Create** dictionaries and access values using keys
2. **Use** common dictionary methods (`keys`, `values`, `items`, `get`, `update`, `pop`)
3. **Build** and navigate nested dictionaries
4. **Write** dictionary comprehensions to transform data
5. **Create** sets and use set operations (union, intersection, difference, symmetric difference)
6. **Choose** the right data structure — list, tuple, dictionary, or set — for a given task

---

## 7.1 Dictionaries: Looking Up Data by Name

### From Lists to Dictionaries

Lists work well when position carries meaning — the first month, the second quarter, the third invoice. But imagine a warehouse inventory: you do not care that "Widget" happens to be the *third* item in a list. You want to look up "Widget" directly and get its quantity.

That is what a **dictionary** does. It works like a real dictionary: you look up a **word** (the *key*) and get its **definition** (the *value*). In Python, the "word" can be any immutable value — in practice usually a string or a number — and the "definition" can be anything at all.

### Creating Dictionaries

A dictionary is enclosed in **curly braces** `{}`, with each key-value pair written as `key: value` and pairs separated by commas:

```python
product = {"name": "Laptop", "price": 999.99, "in_stock": True}
```

Two rules govern the parts:

- **Keys** must be unique and **hashable** — in practice strings, numbers, and tuples of those
- **Values** can be anything — strings, numbers, lists, even other dictionaries

You can also start from an empty dictionary and add entries one at a time with bracket assignment — a common pattern when data arrives gradually:

```python
customer = {}
customer["name"] = "Acme Corp"
customer["balance"] = 15000.00
```

!!! example "Worked Example: Creating a Product Catalog Entry"

    ```python
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
    ```

    **Output:**

    ```
    Product: {'name': 'Wireless Mouse', 'sku': 'WM-2024-001', 'price': 29.99, 'in_stock': True, 'quantity': 150}
    Number of fields: 5
    Type: <class 'dict'>

    Customer record: {'name': 'Acme Corp', 'industry': 'Manufacturing', 'balance': 15000.0, 'active': True}
    ```

    **Interpretation:** The product record holds 5 labeled fields of mixed types — text, a price, a boolean, a count — and `len()` reports the number of key-value pairs, not characters. The customer record shows the incremental pattern: start empty and attach fields as they become known. Note that the balance entered as `15000.00` displays as `15000.0` — Python drops the trailing zero, but the stored value is the same.

    *Source: `computations/module07_examples.py` — `demo_create_dictionaries()`*

### Accessing Values

Use **square brackets** with the key name to get a value:

```python
product["price"]     # 29.99
product["name"]      # "Wireless Mouse"
```

If the key does not exist, Python raises a `KeyError` and your program stops. To avoid this, use the `.get()` method — it returns `None` (or a default you specify) instead of crashing. This matters constantly in business data, where records are often incomplete: one employee has a title on file, another does not.

!!! example "Worked Example: Bracket Access vs. `.get()`"

    ```python
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
    ```

    **Output:**

    ```
    Name: Sarah Chen
    Department: Marketing
    Salary: $78,000
    Title: Not specified
    Email: None
    ```

    **Interpretation:** Bracket access retrieves the $78,000 salary without trouble because the key exists. The record has no `title` or `email` key, yet neither `.get()` call crashes: the first substitutes the fallback text supplied as its second argument, and the second returns `None` because no default was given. With bracket access, either lookup would have raised a `KeyError`.

    *Source: `computations/module07_examples.py` — `demo_access_with_get()`*

### `.get()` vs. Square Brackets — When to Use Each

| Approach | Missing key behavior | Use when... |
|----------|---------------------|-------------|
| `d["key"]` | Raises `KeyError` | You are certain the key exists |
| `d.get("key")` | Returns `None` | The key might be missing |
| `d.get("key", default)` | Returns `default` | You want a fallback value |

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| `d["key"]` and `d.get("key")` behave the same way. | Only when the key exists. For a missing key, brackets raise `KeyError` while `.get()` quietly returns `None` (or your default). |
| A dictionary remembers positions, so `d[0]` gets the first item. | `d[0]` looks for a *key* equal to `0`. Dictionaries are accessed by key, not by index — there is no positional lookup. |
| Adding a key that already exists creates a second entry. | Keys are unique. Assigning to an existing key **overwrites** its value; the dictionary never holds two entries with the same key. |
| Any value can be a dictionary key. | Keys must be hashable (immutable). Strings, numbers, and tuples work; lists and dictionaries cannot be keys. Values, by contrast, can be anything. |

---

## 7.2 Modifying and Iterating Over Dictionaries

Dictionaries are **mutable** — like lists, and unlike tuples, they can change after creation. You can add pairs, overwrite values, remove entries, and merge whole dictionaries together.

### Adding, Updating, and Removing Keys

The same bracket syntax that reads a value also writes one: assigning to an existing key updates it, and assigning to a new key adds it. To remove an entry, `.pop("key")` deletes it *and hands back its value* — useful when you want to log or reuse what was removed.

!!! example "Worked Example: Updating a Store Record"

    ```python
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
    ```

    **Output:**

    ```
    Before: {'name': 'Downtown Branch', 'manager': 'Tom Rivera', 'monthly_revenue': 85000}
    Removed manager: Tom Rivera
    After: {'name': 'Downtown Branch', 'monthly_revenue': 92000, 'employees': 12}
    ```

    **Interpretation:** One record absorbed three different changes: the monthly revenue was corrected from 85000 to 92000, a staff count of 12 was added as a brand-new key, and `.pop()` removed the manager entry while returning its value so the code could report who was removed. The "after" dictionary reflects all three edits.

    *Source: `computations/module07_examples.py` — `demo_modify_dictionary()`*

The modification toolkit in one table:

| Method | Purpose | Example |
|--------|---------|---------|
| `d["key"] = value` | Add or update | `d["price"] = 49.99` |
| `d.pop("key")` | Remove and return value | `old = d.pop("discount")` |
| `d.update(other)` | Merge another dict in | `d.update({"tax": 0.08})` |
| `del d["key"]` | Remove (no return) | `del d["temp"]` |

### Merging Dictionaries with `.update()`

`.update(other)` copies every key-value pair from `other` into the dictionary. Keys that already exist get the incoming value; keys that do not exist are added. This is the standard way to combine two partial records — for example, an order and its shipping details.

!!! example "Worked Example: Merging Order and Shipping Data"

    ```python
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
    ```

    **Output:**

    ```
    Before merge: {'order_id': 'ORD-4521', 'customer': 'Bright Solutions', 'total': 1250.0}

    Merged order:
      order_id: ORD-4521
      customer: Bright Solutions
      total: 1274.99
      shipping_method: Express
      shipping_cost: 24.99
    ```

    **Interpretation:** The two keys unique to the shipping record were added, while the shared `total` key was overwritten — the order total moved from $1,250.00 to $1,274.99 once the $24.99 shipping charge was folded in. `.update()` never duplicates a key; when both dictionaries define one, the incoming value wins.

    *Source: `computations/module07_examples.py` — `demo_merge_with_update()`*

### Three Views: `.keys()`, `.values()`, `.items()`

These three methods give you different views of a dictionary's contents:

- `.keys()` — all keys
- `.values()` — all values
- `.items()` — all (key, value) pairs as tuples

`.items()` is the workhorse: combined with the tuple unpacking you learned in Module 6, it lets a `for` loop receive the key and the value in the same step.

!!! example "Worked Example: Three Views of an Inventory"

    ```python
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
    ```

    **Output:**

    ```
    Keys: ['Laptop', 'Monitor', 'Keyboard', 'Mouse', 'Webcam']
    Values: [45, 120, 200, 350, 85]

    Inventory Report (LOW = fewer than 100 units)
    ------------------------------
      Laptop          45 units  [LOW]
      Monitor        120 units  [OK]
      Keyboard       200 units  [OK]
      Mouse          350 units  [OK]
      Webcam          85 units  [LOW]
    ```

    **Interpretation:** The keys and values views were wrapped in `list()` for display. In the report loop, each pass unpacks one `(product, qty)` pair, and a conditional expression flags Laptop (45 units) and Webcam (85 units) as LOW because they sit below the 100-unit line stated in the header — a two-line reorder alert built from a dictionary.

    *Source: `computations/module07_examples.py` — `demo_keys_values_items()`*

### Checking Membership with `in`

The `in` keyword tests whether a **key** exists in a dictionary:

```python
"Laptop" in inventory    # True
"Tablet" in inventory    # False
```

Note that `in` checks **keys**, not values. To search the values instead, write `value in d.values()`. Membership checks pair naturally with the `if` statements from Module 3: test before you access, and the `KeyError` never has a chance to happen.

!!! example "Worked Example: Guarding Lookups with `in`"

    ```python
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
    ```

    **Output:**

    ```
    Pro Plan costs $29.99
    Student Plan is not available
    ```

    **Interpretation:** The first check finds the plan and safely retrieves its $29.99 price with brackets. The second uses `not in` to confirm a plan is absent and reports that fact — no exception, no crash. Guarded bracket access like this is the alternative to `.get()` when you also want to *act* on the missing case.

    *Source: `computations/module07_examples.py` — `demo_membership_check()`*

### Iterating with `.items()`

The most common way to walk a dictionary is `.items()` with tuple unpacking:

```python
for key, value in my_dict.items():
    print(f"{key}: {value}")
```

Combined with `sum()` over `.values()` and the f-string formatting from Module 2, this pattern turns a raw dictionary into a finished business report.

!!! example "Worked Example: Regional Sales Report"

    ```python
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
    ```

    **Output:**

    ```
    Regional Sales Report
    =============================================
      Northeast     $   245,000  ( 21.6%)
      Southeast     $   198,000  ( 17.5%)
      Midwest       $   167,000  ( 14.8%)
      Southwest     $   210,000  ( 18.6%)
      West          $   312,000  ( 27.6%)
    ---------------------------------------------
      Total         $ 1,132,000
    ```

    **Interpretation:** `sum(regional_sales.values())` computes the $1,132,000 grand total once, before the loop; each iteration then unpacks a region and its revenue and derives that region's share. West leads at $312,000 — 27.6% of company revenue. The alignment and comma specifiers in the f-string do the column work that would otherwise require a spreadsheet.

    *Source: `computations/module07_examples.py` — `demo_regional_sales_report()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| `"x" in d` searches the dictionary's values. | `in` tests **keys**. To search values, write `x in d.values()`. |
| `d.pop()` works like `list.pop()` — no argument removes the last item. | Dictionary `.pop()` **requires the key** to remove and returns its value. (`list.pop()` defaults to the last index; dictionaries have keys, not positions.) |
| `.keys()` and `.values()` return lists. | They return lightweight *view* objects. Wrap them in `list()` when you need an actual list — as the inventory example does for printing. |
| `.update()` replaces the whole dictionary with the new one. | It **merges**: keys present in both take the incoming value; keys unique to either side all survive. |

---

## 7.3 Nested Dictionaries, Comprehensions, and Counting

### Nested Dictionaries

Values in a dictionary can be other dictionaries. This lets you represent structured, hierarchical data — a company directory where each employee ID maps to a full record with multiple fields, much like rows in a database table. Access drills down one bracket per level: `employees["E001"]["name"]`.

!!! example "Worked Example: An Employee Directory as a Nested Dictionary"

    ```python
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
    ```

    **Output:**

    ```
    Employee E001: Alice Park
    Department: Engineering
    Skills: Python, SQL, Tableau

    Employee Directory
    ==================================================
      [E001] Alice Park       Engineering    $  95,000
      [E002] Bob Martinez     Marketing      $  72,000
      [E003] Carol Wu         Finance        $  88,000

      Average salary: $85,000.00
    ```

    **Interpretation:** Record `E001` mixes value types — strings, a number, and a list of skills that `', '.join()` turns into readable text. In the directory loop, `info` is itself a dictionary, so the row format reaches into it with inner brackets. The $85,000.00 average comes from a generator expression over `.values()` — each inner record contributes its salary without any manual indexing.

    *Source: `computations/module07_examples.py` — `demo_nested_employee_directory()`*

### Navigating Nested Data Safely

When drilling into nested structures, use `.get()` at each level to avoid a `KeyError` if data is missing:

```python
# Risky — crashes if "E999" or "skills" is missing
employees["E999"]["skills"]

# Safe — returns "Unknown" if anything is missing
employees.get("E999", {}).get("skills", "Unknown")
```

The trick is the `{}` default in the middle: if the employee ID is missing, the first `.get()` returns an empty dictionary, so the second `.get()` still has something to call itself on. This chained pattern becomes second nature once you work with JSON data in Module 8.

### Dictionary Comprehensions

Just like list comprehensions in Module 6, you can build a dictionary with a compact one-liner:

```python
{key_expr: value_expr for item in iterable}
{key_expr: value_expr for item in iterable if condition}
```

The only new ingredient is the colon: a dictionary comprehension produces a `key: value` pair per iteration instead of a single element. Two everyday uses are *reshaping* data (turning a list of tuples into a lookup table) and *transforming* it (applying a price change to every value).

!!! example "Worked Example: From Tuple List to Price Lookup"

    ```python
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
    ```

    **Output:**

    ```
    Price lookup: {'Laptop': 999.99, 'Monitor': 349.5, 'Keyboard': 79.95, 'Mouse': 24.99, 'Webcam': 64.5}
    Premium items (over $50): {'Laptop': 999.99, 'Monitor': 349.5, 'Keyboard': 79.95, 'Webcam': 64.5}
    ```

    **Interpretation:** Each `(name, price)` tuple unpacks directly in the comprehension, converting a positional list into a by-name lookup table in one line. The filtered version applies an `if` clause, keeping only the four products above the $50 mark — the Mouse at $24.99 drops out. Compare this with the loop it replaces: create empty dict, loop, test, assign.

    *Source: `computations/module07_examples.py` — `demo_price_lookup_comprehension()`*

!!! example "Worked Example: A 15% Sale in One Line"

    ```python
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
    ```

    **Output:**

    ```
    15% Off Sale:
      Widget A: $45.00 → $38.25
      Widget B: $120.00 → $102.00
      Widget C: $32.00 → $27.20
      Widget D: $89.00 → $75.65
    ```

    **Interpretation:** Iterating over `.items()` inside the comprehension keeps each product's name while transforming its value, and rounding keeps the results in whole cents — Widget B drops from $120.00 to $102.00. The original dictionary is untouched; the comprehension builds a brand-new one, so both the before and after prices remain available for the report.

    *Source: `computations/module07_examples.py` — `demo_discount_comprehension()`*

### Counting with Dictionaries

A recurring business pattern is using a dictionary to **count occurrences**: orders per region, transactions per category, tickets per priority. Start with an empty dictionary and, for each item, either create its counter or increment it:

```python
counts = {}
for item in data:
    if item in counts:
        counts[item] += 1
    else:
        counts[item] = 1
```

The `if/else` exists only to handle the first time an item appears. `.get()` collapses it into a single line — `counts.get(item, 0)` returns the running count for a known item and zero for a new one:

```python
counts = {}
for item in data:
    counts[item] = counts.get(item, 0) + 1
```

!!! example "Worked Example: Counting Orders and Transactions"

    ```python
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
    ```

    **Output:**

    ```
    Total orders processed: 15
    Orders by region:
      West         5 orders
      Northeast    4 orders
      Southeast    2 orders
      Midwest      2 orders
      Southwest    2 orders

    Total transactions processed: 8
    Transactions by category:
      Electronics        4
      Furniture          2
      Office Supplies    2
    ```

    **Interpretation:** Across 15 orders, West leads with 5 — the report sorts by count using a `sorted()` key function, largest first. The second half counts categories across 8 transaction records with the `.get()` shortcut: because `.get()` supplies a default of zero for a first-seen category, the `if/else` disappears entirely, yet Electronics still tallies to 4. Both patterns produce identical results; the shortcut is simply less code.

    *Source: `computations/module07_examples.py` — `demo_counting_patterns()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| `counts[item] += 1` works even for a brand-new item. | It raises `KeyError` the first time an item appears — there is nothing to add 1 to. Use the `if/else` pattern or `counts.get(item, 0) + 1`. |
| `{x for x in items}` builds a dictionary because it uses `{}`. | Without a `key: value` colon, that is a **set** comprehension. A dictionary comprehension needs both expressions: `{k: v for ...}`. |
| One `.get()` at the top protects a whole nested lookup. | Each level needs its own guard: `d.get("a", {}).get("b", default)`. The `{}` default keeps the chain alive when the outer key is missing. |
| A comprehension modifies the dictionary it reads from. | It builds a **new** dictionary; the source is unchanged. That is why the sale example can print original and discounted prices side by side. |

---

## 7.4 Sets and Set Operations

### Creating Sets

A **set** is an unordered collection of **unique** items — think of a bag where duplicates are automatically discarded. Sets use curly braces like dictionaries, but hold bare values instead of key-value pairs:

```python
skills = {"Python", "SQL", "Excel", "Python"}   # duplicate removed
# Result: {"Python", "SQL", "Excel"}
```

Sets earn their keep in three situations:

- **Deduplication** — remove duplicates from a list in one step
- **Membership testing** — fast "is this item in the set?" checks
- **Set operations** — compare groups: what is shared, what is unique to one side

Because a set has no order of its own, this module's examples always print `sorted(my_set)` — sorting produces a stable, readable display.

!!! example "Worked Example: Deduplicating a Department List"

    ```python
    raw_departments = [
        "Marketing", "Engineering", "Marketing", "Finance",
        "Engineering", "HR", "Marketing", "Finance", "Engineering",
    ]

    unique_departments = set(raw_departments)
    print(f"Raw list ({len(raw_departments)} items): {raw_departments}")
    # sorted() only for display — a set has no order of its own
    print(f"Unique set ({len(unique_departments)} items): {sorted(unique_departments)}")
    ```

    **Output:**

    ```
    Raw list (9 items): ['Marketing', 'Engineering', 'Marketing', 'Finance', 'Engineering', 'HR', 'Marketing', 'Finance', 'Engineering']
    Unique set (4 items): ['Engineering', 'Finance', 'HR', 'Marketing']
    ```

    **Interpretation:** Passing the list to `set()` collapses 9 raw entries into 4 unique departments — every duplicate vanishes without a loop, a condition, or a counter. This one-liner answers questions like "how many distinct departments submitted expenses this month?" directly.

    *Source: `computations/module07_examples.py` — `demo_set_deduplication()`*

### Set Operations

Sets support the comparison operations of classical set theory — each available as an operator or a method:

| Operation | Symbol | Method | Meaning |
|-----------|--------|--------|---------|
| Union | `A \| B` | `A.union(B)` | All items from both |
| Intersection | `A & B` | `A.intersection(B)` | Items in both |
| Difference | `A - B` | `A.difference(B)` | Items in A but not B |
| Symmetric Diff. | `A ^ B` | `A.symmetric_difference(B)` | Items in one but not both |

These map directly onto business questions: union is "everything we cover," intersection is "what we have in common," difference is "what only we have."

!!! example "Worked Example: Comparing Team Skill Sets"

    ```python
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
    ```

    **Output:**

    ```
    Team A: ['Excel', 'Python', 'R', 'SQL', 'Tableau']
    Team B: ['Java', 'PowerBI', 'Python', 'SQL', 'Spark']

    All skills (union):         ['Excel', 'Java', 'PowerBI', 'Python', 'R', 'SQL', 'Spark', 'Tableau']
    Shared skills (intersect):  ['Python', 'SQL']
    Only Team A (difference):   ['Excel', 'R', 'Tableau']
    Unique to one team (sym):   ['Excel', 'Java', 'PowerBI', 'R', 'Spark', 'Tableau']
    ```

    **Interpretation:** One line per question: the union catalogs every skill either team offers, the intersection shows Python and SQL are the only shared skills, and the difference isolates what Team A alone contributes. The symmetric difference — everything *not* shared — is what a manager would review when deciding which cross-training to schedule.

    *Source: `computations/module07_examples.py` — `demo_set_operations()`*

### Membership Testing: Sets vs. Lists

Checking `item in my_set` is much faster than `item in my_list` for large collections: a list is scanned item by item, while a set jumps straight to the answer via hashing. If your code frequently asks "is this ID one of ours?" and order does not matter, convert the collection to a set first.

The same operations answer customer-retention questions directly, as the next example shows.

!!! example "Worked Example: Repeat, New, and Lost Customers"

    ```python
    q1_customers = {"Acme Corp", "Bright Solutions", "CyberTech", "DataFlow", "EcoGoods"}
    q2_customers = {"Bright Solutions", "DataFlow", "FreshStart", "GreenTech", "Acme Corp"}

    repeat_customers = q1_customers & q2_customers
    new_in_q2 = q2_customers - q1_customers
    lost_in_q2 = q1_customers - q2_customers

    # sorted() only for display — sets are unordered
    print(f"Repeat customers: {sorted(repeat_customers)}")
    print(f"New in Q2: {sorted(new_in_q2)}")
    print(f"Lost after Q1: {sorted(lost_in_q2)}")
    ```

    **Output:**

    ```
    Repeat customers: ['Acme Corp', 'Bright Solutions', 'DataFlow']
    New in Q2: ['FreshStart', 'GreenTech']
    Lost after Q1: ['CyberTech', 'EcoGoods']
    ```

    **Interpretation:** Three companies ordered in both quarters (the intersection), two appeared for the first time in Q2 (Q2 minus Q1), and two from Q1 did not return (Q1 minus Q2). Notice that difference is directional — swapping the operands changes "lost" into "new." This is churn analysis in three lines.

    *Source: `computations/module07_examples.py` — `demo_repeat_customers()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Sets remember insertion order like lists and dictionaries do. | Sets are **unordered** — iteration order is arbitrary and can vary. Sort for display: `sorted(my_set)`. |
| `A - B` and `B - A` give the same result. | Difference is directional: `A - B` is "in A but not B." The customer example relies on this — one direction is lost customers, the other is new ones. |
| Sets can hold any value, like lists can. | Set elements must be hashable — strings, numbers, tuples. Lists and dictionaries cannot be set members. |
| You can grab the "first" element with `my_set[0]`. | Sets do not support indexing — there is no position to index. Convert to a sorted list if you need ordered access. |

---

## 7.5 Choosing the Right Data Structure

You now have four collection types. The choice among them is a modeling decision you will make at the start of nearly every program:

| Need | Data Structure | Example |
|------|---------------|---------|
| Ordered collection, may have duplicates | **List** `[]` | Sales figures for 12 months |
| Look up values by name/key | **Dictionary** `{}` | Product catalog by SKU |
| Fixed record, cannot change | **Tuple** `()` | (latitude, longitude) coordinates |
| Unique items, no order needed | **Set** `{...}` / `set()` | Unique customer IDs |

**Watch out:** `{}` creates an empty **dictionary**, not a set. For an empty set you must write `set()` — there is no empty-set literal.

**Rule of thumb:** looking things up by name → dictionary. Need unique items → set. Order matters → list. Should never change → tuple.

### Capstone: Regional Sales Dashboard

The capstone combines everything in this module — dictionary accumulators, `.get()`, `.items()` iteration, sorting, and set operations — to turn raw transaction data (a list of dictionaries, the shape most real datasets take) into a management dashboard. It also introduces the **set comprehension**: `{expr for item in iterable}`, which works exactly like a list comprehension but produces a set of unique results.

!!! example "Worked Example: Regional Sales Dashboard"

    ```python
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
    ```

    **Output:**

    ```
    Revenue by Region
    ===================================
      West       $  3,486.00
      East       $  3,376.00
      Central    $  2,658.00
      Total      $  9,520.00

    Revenue by Sales Rep
    ===================================
      Alice      $  3,486.00
      Dave       $  2,658.00
      Carol      $  2,548.00
      Bob        $    828.00

    Unique products sold: ['Keyboard', 'Laptop', 'Monitor', 'Mouse', 'Webcam']
    Number of unique products: 5

    Products both Alice and Bob sell: ['Monitor', 'Webcam']
    ```

    **Interpretation:** The same accumulator pattern answers two different questions just by switching the grouping key: West leads regions at $3,486.00 of the $9,520.00 total, and Alice — the only rep selling in West — tops the rep table with the matching figure. The set comprehension distills ten transactions down to 5 unique products, and an intersection of two filtered comprehensions shows Monitor and Webcam are the products Alice and Bob both sold. Every technique here reappears in the assignment.

    *Source: `computations/module07_examples.py` — `demo_capstone_sales_dashboard()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| `{}` gives you an empty set, since sets use curly braces. | `{}` is an empty **dictionary**. The only way to write an empty set is `set()`. |
| A set is just "a list without duplicates," so it supports the same operations. | Sets drop ordering and indexing in exchange for uniqueness and fast membership tests. If you need positions or duplicates, you need a list. |
| Dictionaries cannot hold complex values like lists or other dictionaries. | Values can be anything. Lists of dictionaries and dictionaries of dictionaries are the standard shapes for real datasets — the capstone's transaction data is exactly that. |

---

## Reflection Questions

1. A colleague stores product prices in two parallel lists — `names` and `prices` — and matches them by position. What problems could this cause as the catalog grows, and how does a dictionary eliminate them?
2. `d["key"]` crashes on a missing key while `d.get("key")` silently returns `None`. Describe one business scenario where the crash is actually the *better* behavior, and one where the silent default is safer.
3. The counting pattern (`counts[item] = counts.get(item, 0) + 1`) appears in reporting code constantly. What business questions in your own field reduce to "count occurrences by category"?
4. When would you reach for a dictionary comprehension instead of a `for` loop that builds a dictionary — and when would the loop be the clearer choice?
5. The customer-retention example computed repeat, new, and lost customers with three set operations. What other paired-group comparisons (this month vs. last month, plan A vs. plan B) could you analyze the same way?
6. Looking at the choosing-a-structure table in §7.5, which structure would you pick to store: a company's stock price on each trading day this year? The set of countries you ship to? A GPS coordinate? Why?

---

## Your Assignment

The Module 7 assignment, **Dictionaries & Sets**, is worth **100 points plus a 10-point bonus**. You complete it in the provided marimo notebook and submit the `.py` file to Blackboard. The closing reflection section is not graded separately — it counts toward participation. As in earlier assignments, keep the underscore prefix on cell-scoped variables, and remember two tips from this module while you work: `.get(key, default)` is the safe way to read keys that may be absent, and an empty set must be created with `set()`, never `{}`.

### Task 1: Dictionary Creation and Access (10 points)

Build a restaurant's lunch menu as a dictionary mapping five dish names to their prices, then retrieve prices three ways: bracket notation for one dish, `.get()` for another, and `.get()` with a default value for a dish that is not on the menu. Finish by printing the number of menu items with `len()`. Everything here comes from §7.1.

### Task 2: Dictionary Methods (15 points)

Starting from a hotel's room-availability dictionary, display the `.keys()`, `.values()`, and `.items()` views, then walk through a day of operations: reduce one room type's count after a booking, add a new room type with `.update()`, remove a closed room type with `.pop()` (printing what was removed), and print the final inventory. The methods are covered in §7.2, including the modification-methods table.

### Task 3: Iterating and Counting (15 points)

Given a list of customer-service ratings from twenty support calls, use a `for` loop and a dictionary — not `collections.Counter` — to count how often each rating appears. Then print a formatted summary table showing each rating's count and percentage of total responses, and identify the most common rating. The counting pattern is §7.3; the `.items()` iteration and f-string report formatting follow §7.2.

### Task 4: Dictionary Comprehensions (15 points)

A company grants an across-the-board 10% raise. Write one dictionary comprehension that applies the raise to every entry in an hourly-rates dictionary (rounded to two decimal places), and a second comprehension that filters the raised rates to only employees above a $25-per-hour threshold. Print the original, raised, and filtered dictionaries. Both comprehension forms — transform and filter — are in §7.3.

### Task 5: Nested Dictionaries (20 points)

Build a grade book as a nested dictionary in which each student maps to a dictionary of courses and numeric grades. Print the grades as a formatted table, compute each student's average rounded to two decimal places, and determine which student has the highest average. Nested access and the iterate-and-aggregate pattern are demonstrated in §7.3's employee-directory example.

### Task 6: Combined Challenge — Sets + Dictionaries (25 points)

Two store locations each track inventory as a product-to-price dictionary. **Part A** uses set operations on the dictionaries' keys to find products carried at both stores, products exclusive to each store, and the full combined product range — each printed as a sorted list (§7.4). **Part B** builds a nested price-comparison dictionary for the shared products, recording each store's price and which store is cheaper (§7.3, §7.5). **Part C** prints a formatted comparison report plus a summary of how many products fall into each availability group. The capstone in §7.5 models this combination of accumulators, sets, and formatted reporting.

### Task 7: Creative Exercise — Bonus (10 points)

Design your own business scenario demonstrating dictionaries and sets. Your solution must include a dictionary with at least five entries, at least one nested dictionary or dictionary comprehension, at least one set operation, a loop over `.items()`, a summary calculation, and clearly formatted output. The notebook suggests idea seeds — streaming-genre overlaps, month-over-month inventory comparison, league standings, recipe-ingredient matching — but any scenario of your own is welcome.

### Reflection (participation credit)

Answer the notebook's five reflection prompts in your own words: when you would choose a dictionary over a list, what `.get()` does and why it is safer than brackets, how loop-built dictionaries compare with comprehensions, a real-world case where a set beats a list, and what you found most challenging. There is no wrong answer — honest reflection helps your instructor see where support is needed.

---

## Chapter Summary

Dictionaries store key-value pairs and retrieve values by name rather than position — the natural fit whenever data has labels, which in business is almost always. You create them with `{key: value}` literals or by assigning to keys one at a time, read them with brackets when a key is guaranteed or `.get(key, default)` when it is not, and modify them freely: bracket assignment adds or overwrites, `.pop()` removes and returns, `.update()` merges another dictionary in with incoming values winning on shared keys. The three views — `.keys()`, `.values()`, `.items()` — expose the contents, and `.items()` with tuple unpacking is the standard way to loop, powering everything from inventory alerts to the regional sales report.

Structure and brevity come next. Nested dictionaries model records-within-records — an employee directory, a grade book — with one bracket per level and chained `.get()` calls for safe navigation. Dictionary comprehensions build new dictionaries in a single expression, whether reshaping a tuple list into a lookup table or applying a discount across a price list. The counting pattern — `counts[item] = counts.get(item, 0) + 1` — turns any stream of categories into a frequency table and reappears throughout data work.

Sets complete the toolkit: unordered collections of unique, hashable items. `set(some_list)` deduplicates in one step, membership tests are fast, and the four operations — union, intersection, difference, symmetric difference — answer comparison questions directly, from shared team skills to repeat-versus-lost customers. Choosing among list, tuple, dictionary, and set is a modeling decision: order → list, fixed record → tuple, lookup by name → dictionary, uniqueness → set — and remember that `{}` is an empty dictionary, never an empty set. The capstone dashboard put all of it together on a list of transaction dictionaries, the exact shape you will meet again and again in real datasets.

---

## What's Next

Module 8 covers **file input/output and JSON** — reading data from files on disk instead of typing it into your program, and writing results back out. This is where the structures from this module pay off doubly: JSON, the most common data-exchange format in business systems, is essentially nested dictionaries and lists in text form. A JSON file of customer orders loads directly into the list-of-dictionaries shape you used in the §7.5 capstone, and the `.get()` navigation you practiced here is exactly how you will pull fields out of it safely. After Module 8, your programs stop depending on hand-typed data and start working with real files.
