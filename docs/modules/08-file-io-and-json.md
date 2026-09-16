# Module 8: File I/O & Working with JSON

## Introduction

Every module so far has worked with data typed directly into a notebook — a few prices here, a small dictionary there. Real business data does not arrive that way. It lives in **files**: CSV exports from Excel, JSON responses from web APIs, text logs from servers, configuration files for applications. **File I/O** (input/output) is the bridge between your Python code and that outside world. Once you can read a file, you can process thousands of records without typing a single one by hand; once you can write a file, your analysis can produce reports and datasets that other people — and other programs — consume. This module covers the two formats you will meet constantly in business settings: plain **text files** (logs, reports, CSV) and **JSON files** (structured, nested data from APIs and configuration systems). It closes with a small but complete data pipeline: read a supplier's JSON catalog, compute order costs, and write both a human-readable report and a machine-readable JSON output.

---

## Learning Objectives

By the end of this module, you should be able to:

1. **Read** and **write** text files using Python's built-in `open()` function
2. **Use** context managers (the `with` statement) to handle files safely
3. **Navigate** the file system with the `pathlib` module
4. **Explain** the structure of JSON data and how it maps to Python types
5. **Read** and **write** JSON files with the `json` module
6. **Navigate** and extract data from nested JSON structures

---

## 8.1 Reading Text Files

The built-in `open()` function opens a file and returns a file object you can read from or write to. Its second argument is the **mode**, which declares what you intend to do:

| Mode | Meaning | Creates file? |
|------|---------|---------------|
| `"r"` | Read (default) | No — errors if missing |
| `"w"` | Write (overwrite) | Yes |
| `"a"` | Append (add to end) | Yes |

### The Context Manager: `with`

**Always** open files with a **context manager** — the `with` statement. It automatically closes the file when the block ends, even if an error occurs partway through:

```python
with open("data.txt", "r") as f:
    contents = f.read()
# file is automatically closed here
```

Without `with`, a forgotten `close()` call can leave the file locked or leave written data stuck in a buffer that never reaches the disk. With `with`, cleanup is guaranteed. Every example in this module — and every task in the assignment — uses this pattern.

!!! note "Where do these files go?"

    The code in this chapter uses bare filenames like `sales_log.txt`, which Python places in the *current working folder*. The companion's verification scripts run every example inside a sandbox folder (`computations/_scratch/module08/`) so the book's code is re-runnable without scattering files through the repository. When you run the same code yourself, the files appear in whatever folder your notebook runs from; the module's teaching notebook uses `tempfile.gettempdir()` to pick a temporary folder that exists on any operating system.

Before we can practice reading, we need a file to read. The demo below writes a small sales log — one line per day — using mode `"w"`. (Writing is covered in depth in §8.2; here it just sets the stage.)

!!! example "Worked Example: Creating a Practice File"

    ```python
    sample_lines = [
        "Date,Product,Units,Revenue",
        "2025-01-15,Widget A,120,3600.00",
        "2025-01-16,Widget B,85,4250.00",
        "2025-01-17,Widget A,95,2850.00",
        "2025-01-18,Widget C,200,6000.00",
        "2025-01-19,Widget B,110,5500.00",
    ]

    with open("sales_log.txt", "w") as f:
        for line in sample_lines:
            f.write(line + "\n")

    print("Created sales_log.txt with 6 lines (1 header + 5 data rows)")
    ```

    **Output:**

    ```
    Created sales_log.txt with 6 lines (1 header + 5 data rows)
    ```

    **Interpretation:** Mode `"w"` created the file, and each `f.write()` call added one line. Note the explicit `"\n"` — unlike `print()`, the `write()` method does not add a newline for you. The result is a 6-line file: 1 header row naming the columns plus 5 data rows.

    *Source: `computations/module08_examples.py` — `demo_create_sales_log()`*

### Reading a Whole File at Once

The `.read()` method returns the entire file as one string — the simplest approach when the file is small.

!!! example "Worked Example: Reading an Entire File with `.read()`"

    ```python
    with open("sales_log.txt", "r") as f:
        contents = f.read()

    print("Full file contents:")
    print(contents)
    print(f"Total characters: {len(contents)}")
    ```

    **Output:**

    ```
    Full file contents:
    Date,Product,Units,Revenue
    2025-01-15,Widget A,120,3600.00
    2025-01-16,Widget B,85,4250.00
    2025-01-17,Widget A,95,2850.00
    2025-01-18,Widget C,200,6000.00
    2025-01-19,Widget B,110,5500.00

    Total characters: 185
    ```

    **Interpretation:** One `.read()` call returned the whole file as a single string of 185 characters — including the invisible newline character that ends each line, which is why printing the string reproduces the file's layout exactly. Convenient for small files, but the entire file must fit in memory at once.

    *Source: `computations/module08_examples.py` — `demo_read_entire_file()`*

### Reading Line by Line

For large files, reading everything at once can use too much memory. Instead, read **line by line** — these two approaches **stream** the file, holding just one line in memory at a time:

- `.readline()` — reads one line each time you call it
- **Iterating directly** (`for line in f:`) — the most Pythonic approach

There is also `.readlines()`, which returns a list of *all* lines — but it loads the whole file into memory, the same cost as `.read()`, so it does **not** help with large files.

!!! example "Worked Example: Reading Line by Line"

    ```python
    print("Line-by-line reading:")
    with open("sales_log.txt", "r") as f:
        for line_num, line in enumerate(f, start=1):
            clean = line.strip()  # Remove trailing newline
            print(f"  Line {line_num}: {clean}")
    ```

    **Output:**

    ```
    Line-by-line reading:
      Line 1: Date,Product,Units,Revenue
      Line 2: 2025-01-15,Widget A,120,3600.00
      Line 3: 2025-01-16,Widget B,85,4250.00
      Line 4: 2025-01-17,Widget A,95,2850.00
      Line 5: 2025-01-18,Widget C,200,6000.00
      Line 6: 2025-01-19,Widget B,110,5500.00
    ```

    **Interpretation:** The file object itself is iterable — each pass through the loop delivers the next line, so only one line lives in memory at a time. `enumerate(f, start=1)` numbers the lines as they arrive, and `.strip()` removes the trailing newline each line carries; without it, every `print()` would produce a blank line after each row.

    *Source: `computations/module08_examples.py` — `demo_read_line_by_line()`*

### From Lines to Records

Reading lines is only half the job — a business analysis needs the *values* inside them. The pattern below appears constantly: read the header line with `.readline()`, then split each remaining line on its delimiter and convert the text pieces to proper types. The result is a list of dictionaries, the same structure you built by hand in Module 7.

!!! example "Worked Example: Parsing the Sales Log into Records"

    ```python
    sales = []

    with open("sales_log.txt", "r") as f:
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
    ```

    **Output:**

    ```
    Parsed 5 records:
      2025-01-15  Widget A     120 units  $ 3,600.00
      2025-01-16  Widget B      85 units  $ 4,250.00
      2025-01-17  Widget A      95 units  $ 2,850.00
      2025-01-18  Widget C     200 units  $ 6,000.00
      2025-01-19  Widget B     110 units  $ 5,500.00
    
    Total revenue: $22,200.00
    ```

    **Interpretation:** The consumed header line leaves only the 5 data rows for the loop, and each becomes a dictionary with real types: `int()` turns the text `"120"` into a number you can add, and `float()` does the same for revenue. Once the file is a list of dictionaries, everything from the data-structures modules applies — here a generator expression sums the revenue to $22,200.00.

    *Source: `computations/module08_examples.py` — `demo_parse_sales_log()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Opening a file with mode `"r"` creates it if it is missing. | `"r"` raises an error when the file does not exist. Only `"w"` and `"a"` create files. |
| `.readlines()` is the memory-safe way to handle big files. | `.readlines()` loads *every* line into a list at once — the same memory cost as `.read()`. Iterating with `for line in f:` is the streaming approach. |
| Lines read from a file arrive as clean strings. | Every line keeps its trailing `"\n"` newline character. Call `.strip()` before comparing, splitting, or printing. |
| Numbers read from a file are numbers. | Everything read from a text file is a **string**, including `"120"` and `"3600.00"`. Convert with `int()` or `float()` before doing arithmetic. |
| You only need `close()` if the program crashes. | It is the other way around: the `with` statement guarantees the file is closed *especially* when something goes wrong mid-block. Manual `close()` calls are exactly what crashes skip. |

---

## 8.2 Writing Text Files

Use mode `"w"` to create a new file (or overwrite an existing one) and mode `"a"` to append to an existing file:

```python
# Write (creates or overwrites)
with open("report.txt", "w") as f:
    f.write("Sales Report\n")
    f.write("============\n")

# Append (adds to end)
with open("report.txt", "a") as f:
    f.write("Total: $22,200.00\n")
```

**Warning:** Mode `"w"` **destroys** existing contents the moment the file is opened. If you want to add to a file — a daily log, for example — use `"a"`.

Writing shines when your code produces something a manager can read. The example below turns the parsed sales data into a formatted report file, then reads it back to verify what landed on disk — a habit worth keeping, because the file on disk is what your audience will actually see.

!!! example "Worked Example: Writing a Formatted Sales Report"

    ```python
    sales = [
        {"date": "2025-01-15", "product": "Widget A", "units": 120, "revenue": 3600.00},
        {"date": "2025-01-16", "product": "Widget B", "units": 85, "revenue": 4250.00},
        {"date": "2025-01-17", "product": "Widget A", "units": 95, "revenue": 2850.00},
        {"date": "2025-01-18", "product": "Widget C", "units": 200, "revenue": 6000.00},
        {"date": "2025-01-19", "product": "Widget B", "units": 110, "revenue": 5500.00},
    ]

    with open("sales_report.txt", "w") as f:
        f.write("Daily Sales Report\n")
        f.write("=" * 50 + "\n\n")
        for sale in sales:
            f.write(f"{sale['date']}  {sale['product']:<10}  ${sale['revenue']:>9,.2f}\n")
        total = sum(s["revenue"] for s in sales)
        f.write(f"\n{'Total':<22}  ${total:>9,.2f}\n")

    # Verify by reading it back
    with open("sales_report.txt", "r") as f:
        print(f.read())
    ```

    **Output:**

    ```
    Daily Sales Report
    ==================================================
    
    2025-01-15  Widget A    $ 3,600.00
    2025-01-16  Widget B    $ 4,250.00
    2025-01-17  Widget A    $ 2,850.00
    2025-01-18  Widget C    $ 6,000.00
    2025-01-19  Widget B    $ 5,500.00
    
    Total                   $22,200.00
    ```

    **Interpretation:** Everything you learned about f-string formatting earlier in the course works inside `f.write()` — left-aligned product names and right-aligned dollar amounts produce clean columns, and the grand total of $22,200.00 lines up under the daily figures. The read-back at the end confirms the file contains exactly the report intended.

    *Source: `computations/module08_examples.py` — `demo_write_sales_report()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Mode `"w"` adds new content to an existing file. | `"w"` erases the file's contents the instant it opens. To add to the end, use `"a"` (append). |
| `f.write()` adds a newline automatically, like `print()`. | `write()` outputs exactly the string you give it. Without an explicit `"\n"`, everything runs together on one line. |
| A file opened for reading can also be written. | The mode is a contract: `"r"` objects to writes, `"w"`/`"a"` object to reads. Open the file again in the mode you need. |
| What you `write()` is instantly on disk. | Written data may sit in a buffer until the file is closed. This is another reason the `with` block matters — it closes the file and flushes the buffer for you. |

---

## 8.3 The `pathlib` Module

So far, file locations have been plain strings. The `pathlib` module provides an object-oriented way to work with paths — and its `/` operator joins path pieces using the **correct separator for the operating system you are on** (Windows uses `\`, Mac/Linux use `/`), so you never hard-code separators yourself:

```python
from pathlib import Path

data_dir = Path("data")
file_path = data_dir / "sales_log.txt"   # / joins with the OS separator
```

One thing `pathlib` does **not** do is invent a valid starting folder. A path like `/tmp` is a normal absolute path on Mac/Linux, but on Windows it is *not* absolute and may not exist. For a temporary folder that works on every OS, ask Python for one with `tempfile.gettempdir()` — the teaching notebook stores that in its `work_dir` variable and joins filenames onto it.

### Inspecting a Path

A `Path` object knows how to take itself apart: the filename, the extension, the folder it sits in, and whether it actually exists on disk. Here the sales log from §8.1 has been placed inside a `data` folder first.

!!! example "Worked Example: Inspecting a Path's Parts"

    ```python
    from pathlib import Path

    data_dir = Path("data")
    file_path = data_dir / "sales_log.txt"

    print(f"Path: {file_path}")
    print(f"Name: {file_path.name}")
    print(f"Stem (no extension): {file_path.stem}")
    print(f"Extension: {file_path.suffix}")
    print(f"Parent directory: {file_path.parent}")
    print(f"Exists? {file_path.exists()}")
    print(f"Is a file? {file_path.is_file()}")
    ```

    **Output:**

    ```
    Path: data/sales_log.txt
    Name: sales_log.txt
    Stem (no extension): sales_log
    Extension: .txt
    Parent directory: data
    Exists? True
    Is a file? True
    ```

    **Interpretation:** The properties decompose the path without touching the disk — `.name`, `.stem`, `.suffix`, and `.parent` are pure string surgery. Only `.exists()` and `.is_file()` actually check the file system, which makes them the polite way to test for a file before opening it in mode `"r"`.

    *Source: `computations/module08_examples.py` — `demo_pathlib_inspection()`*

### Useful `pathlib` Operations

| Operation | Purpose | Example |
|-----------|---------|---------|
| `Path("dir") / "file.txt"` | Join paths | Cross-platform path building |
| `.exists()` | Check if path exists | Avoid errors before reading |
| `.is_file()` / `.is_dir()` | Check type | Distinguish files from folders |
| `.name` | File name with extension | `"report.csv"` |
| `.stem` | File name without extension | `"report"` |
| `.suffix` | Extension | `".csv"` |
| `.parent` | Parent directory | `Path("data")` |
| `.read_text()` | Read entire file | Shortcut for open/read/close |
| `.write_text()` | Write entire file | Shortcut for open/write/close |

The last two rows deserve a demonstration: for simple whole-file reads and writes, `pathlib` collapses the open/operate/close dance into a single method call.

!!! example "Worked Example: `write_text()` and `read_text()` Shortcuts"

    ```python
    from pathlib import Path

    path = Path("quick_note.txt")
    path.write_text("This is a quick note written with pathlib.\nLine two.\n")

    content = path.read_text()
    print(f"Read back:\n{content}")
    ```

    **Output:**

    ```
    Read back:
    This is a quick note written with pathlib.
    Line two.
    ```

    **Interpretation:** `.write_text()` opened the file, wrote the string, and closed it — one call instead of a `with` block. `.read_text()` did the same in reverse. These shortcuts are ideal for small whole-file operations; for line-by-line streaming or appending, the `open()` patterns from earlier in the module remain the right tools.

    *Source: `computations/module08_examples.py` — `demo_pathlib_shortcuts()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Building paths by gluing strings (`folder + "/" + name`) is fine. | It breaks the moment the code runs on an OS with a different separator. The `/` operator on `Path` objects inserts the correct one automatically. |
| `/tmp/` works as a temp folder on every computer. | On Windows, `/tmp` is not an absolute path and may not exist. `tempfile.gettempdir()` returns a real temp folder on any OS. |
| A `Path` object must point to a file that exists. | A `Path` is just a description of a location. It can name a file you are *about to create* — that is exactly what `.exists()` is for. |
| `.exists()` returning `False` means something went wrong. | It is an ordinary question with an ordinary answer. Checking before reading is how you *avoid* errors. |

---

## 8.4 Working with JSON

**JSON** (JavaScript Object Notation) is the most common format for structured data on the web. If you have ever used a web API — and in Module 15 you will — the data came back as JSON.

### What JSON Looks Like

JSON looks almost identical to Python dictionaries and lists:

```json
{
    "name": "Acme Corp",
    "founded": 2010,
    "active": true,
    "departments": ["Sales", "Engineering", "Marketing"]
}
```

The mapping between the two worlds is direct:

| JSON | Python |
|------|--------|
| `{}` object | `dict` |
| `[]` array | `list` |
| `"string"` | `str` |
| `123` / `45.6` | `int` / `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

Two differences trip up beginners: JSON spells its booleans lowercase (`true`, `false`) and uses `null` where Python uses `None`. The `json` module translates in both directions, so you never write those literals in Python code.

### The `json` Module's Four Functions

Python's built-in `json` module converts between JSON text and Python objects:

- `json.load(file)` — read from an open file
- `json.loads(string)` — parse a JSON string
- `json.dump(data, file)` — write to a file
- `json.dumps(data)` — convert to a JSON string

The pattern behind the names: `dump`/`load` work with **files**, and the trailing **s** in `loads`/`dumps` means **string**.

### Writing and Reading JSON Files

We start by saving a nested Python dictionary — a company with a list of departments — as a JSON file. The `indent=2` argument formats the output with line breaks and indentation so humans can read it.

!!! example "Worked Example: Writing a JSON File with `json.dump()`"

    ```python
    import json

    company_data = {
        "company": "TechFlow Solutions",
        "founded": 2018,
        "headquarters": "Austin, TX",
        "employees": 145,
        "departments": [
            {"name": "Engineering", "head": "Maria Lopez", "headcount": 60, "budget": 2400000},
            {"name": "Sales", "head": "James Carter", "headcount": 45, "budget": 1800000},
            {"name": "Marketing", "head": "Priya Sharma", "headcount": 25, "budget": 900000},
            {"name": "Operations", "head": "Kevin O'Brien", "headcount": 15, "budget": 600000},
        ],
    }

    # Write JSON to file with pretty formatting
    with open("company.json", "w") as f:
        json.dump(company_data, f, indent=2)

    print("Created company.json with 4 departments")
    ```

    **Output:**

    ```
    Created company.json with 4 departments
    ```

    **Interpretation:** `json.dump()` serialized the whole nested structure — the dictionary, its list of 4 department dictionaries, strings, and numbers — into standards-compliant JSON text in one call. No loops, no manual formatting: the module handles quoting, commas, and nesting.

    *Source: `computations/module08_examples.py` — `demo_write_company_json()`*

Reading it back is just as direct: `json.load()` parses the file and hands you ordinary Python objects.

!!! example "Worked Example: Reading a JSON File with `json.load()`"

    ```python
    import json

    with open("company.json", "r") as f:
        data = json.load(f)

    print(f"Company: {data['company']}")
    print(f"Founded: {data['founded']}")
    print(f"Headquarters: {data['headquarters']}")
    print(f"Total employees: {data['employees']}")
    print(f"Number of departments: {len(data['departments'])}")
    print(f"Type of loaded data: {type(data)}")
    ```

    **Output:**

    ```
    Company: TechFlow Solutions
    Founded: 2018
    Headquarters: Austin, TX
    Total employees: 145
    Number of departments: 4
    Type of loaded data: <class 'dict'>
    ```

    **Interpretation:** The loaded result is a plain Python `dict` — the founding year 2018 came back as an `int`, the 145 employees as an `int`, and the 4 departments as a `list`. Every dictionary and list skill from the data-structures modules applies immediately; nothing about the data is "special" once it is loaded.

    *Source: `computations/module08_examples.py` — `demo_read_company_json()`*

### Navigating Nested JSON

Real-world JSON is usually nested — dictionaries inside lists inside dictionaries. The key skill is chaining access operations:

```python
data["departments"][0]["name"]     # First department's name
data["departments"][2]["budget"]   # Third department's budget
```

Think of it as following a path: start at the top, then drill down one level at a time. And because the nested pieces are ordinary lists and dictionaries, loops and aggregations work exactly as they did in Modules 6 and 7.

!!! example "Worked Example: Department Analysis from Nested JSON"

    ```python
    import json

    with open("company.json", "r") as f:
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
    ```

    **Output:**

    ```
    Department Details:
    =======================================================
      Engineering    Head: Maria Lopez      Staff:  60  Budget: $ 2,400,000   Average cost: $40,000
      Sales          Head: James Carter     Staff:  45  Budget: $ 1,800,000   Average cost: $40,000
      Marketing      Head: Priya Sharma     Staff:  25  Budget: $   900,000   Average cost: $36,000
      Operations     Head: Kevin O'Brien    Staff:  15  Budget: $   600,000   Average cost: $40,000
    
      Totals                          Staff: 145  Budget: $ 5,700,000
    ```

    **Interpretation:** Each pass through the loop holds one department dictionary, so `dept["budget"] / dept["headcount"]` computes a per-person cost — $40,000 in three departments, $36,000 in Marketing. The generator expressions then aggregate *across* the nesting: 145 staff and a $5,700,000 combined budget, matching the company-level employee count from the previous example.

    *Source: `computations/module08_examples.py` — `demo_nested_json_navigation()`*

### JSON Strings: `loads()` and `dumps()`

Sometimes JSON arrives as a **string** rather than a file — most commonly as the body of a web API response. `json.loads()` (load **s**tring) parses it, and `json.dumps()` (dump **s**tring) goes the other way.

!!! example "Worked Example: Parsing a JSON String from an API"

    ```python
    import json

    # Parsing a JSON string (as if received from an API)
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
    ```

    **Output:**

    ```
    Status: success
    Results: 3
    
      Austin: 78°F
      Denver: 55°F
      Miami: 88°F
    ```

    **Interpretation:** One `json.loads()` call turned the raw response text into a dictionary with a list of city readings inside. The `results` field reports 3 readings, and the loop confirms it — Austin at 78°F, Denver at 55°F, Miami at 88°F. This is a preview of the REST-APIs module later in the course, where strings like this arrive from live web services.

    *Source: `computations/module08_examples.py` — `demo_json_loads_api_response()`*

!!! example "Worked Example: Converting Python Data to a JSON String"

    ```python
    import json

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
    ```

    **Output:**

    ```
    Python dict → JSON string:
    {
      "order_id": "ORD-7890",
      "customer": "Bright Solutions",
      "items": [
        {
          "product": "Laptop",
          "qty": 3,
          "price": 999.99
        },
        {
          "product": "Monitor",
          "qty": 5,
          "price": 349.5
        }
      ],
      "total": 4747.47,
      "shipped": false
    }
    ```

    **Interpretation:** `json.dumps()` produced a formatted string ready to send to an API or store in a database. Notice the translations at the boundary: Python's `False` became JSON's lowercase `false`, and the float printed as `349.5` — JSON stores the *value*, not the trailing zero of the display format. Presentation formatting stays the job of f-strings on the Python side.

    *Source: `computations/module08_examples.py` — `demo_json_dumps_order()`*

### Building and Saving a JSON Report

Writing JSON files is how your analysis hands structured results to other programs. The example below builds a quarterly report — including a nested `totals` dictionary computed on the fly — saves it with `json.dump()`, then immediately reads it back to verify the round trip.

!!! example "Worked Example: Writing and Verifying a JSON Report"

    ```python
    import json

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
    with open("q1_report.json", "w") as f:
        json.dump(report, f, indent=2)

    # Read it back to verify
    with open("q1_report.json", "r") as f:
        verified = json.load(f)

    print(f"Report: {verified['report_name']}")
    print(f"Total revenue: ${verified['totals']['revenue']:,}")
    print(f"Total expenses: ${verified['totals']['expenses']:,}")
    print(f"Total customers: {verified['totals']['customers']}")
    print(f"Profit: ${verified['totals']['revenue'] - verified['totals']['expenses']:,}")
    ```

    **Output:**

    ```
    Report: Q1 Sales Summary
    Total revenue: $145,900
    Total expenses: $101,300
    Total customers: 410
    Profit: $44,600
    ```

    **Interpretation:** The round trip — build, `dump`, `load`, verify — proves the file on disk carries the full analysis: $145,900 revenue against $101,300 in expenses across 410 customers, for a $44,600 profit computed from the reloaded values. Chained access like `verified['totals']['revenue']` is the nested-navigation skill again, now applied to data your own code produced.

    *Source: `computations/module08_examples.py` — `demo_write_json_report()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| You can write `true`, `false`, or `null` in Python code. | Those are JSON spellings. In Python they are `True`, `False`, and `None` — the `json` module translates automatically at the boundary. |
| `json.load()` and `json.loads()` are interchangeable. | `load()` takes an open **file**; `loads()` takes a **string**. The trailing `s` means string — same for `dump()` vs `dumps()`. |
| Loading JSON produces a special "JSON object" needing special methods. | You get plain Python dicts, lists, strings, and numbers. Every skill from Modules 6 and 7 applies unchanged. |
| JSON keys can be numbers or any other type. | JSON object keys must be **strings**. When you dump a dict, non-string keys get converted, which can surprise you on the way back in. |
| `indent=2` changes the data. | Indentation is cosmetic whitespace for human readers. The parsed data is identical with or without it. |

---

## 8.5 CSV and the Data Pipeline

### CSV: A Brief Introduction

**CSV** (Comma-Separated Values) is the simplest tabular data format — one row per line, columns separated by commas. You already parsed one manually in §8.1: the sales log was CSV all along.

```
Name,Department,Salary
Alice Park,Engineering,95000
Bob Martinez,Marketing,72000
```

Python's built-in `csv` module handles the parsing details (including tricky cases like commas inside quoted values) so you do not split strings by hand. Its `DictWriter` and `DictReader` classes map each row to a dictionary keyed by the header.

!!! example "Worked Example: Writing and Reading CSV with the `csv` Module"

    ```python
    import csv

    employees = [
        {"name": "Alice Park", "department": "Engineering", "salary": 95000},
        {"name": "Bob Martinez", "department": "Marketing", "salary": 72000},
        {"name": "Carol Wu", "department": "Finance", "salary": 88000},
    ]

    # Write CSV
    with open("employees.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "department", "salary"])
        writer.writeheader()
        writer.writerows(employees)

    # Read CSV back
    with open("employees.csv", "r") as f:
        reader = csv.DictReader(f)
        print("CSV Contents:")
        for row in reader:
            print(f"  {row['name']:<16} {row['department']:<14} ${int(row['salary']):>8,}")
    ```

    **Output:**

    ```
    CSV Contents:
      Alice Park       Engineering    $  95,000
      Bob Martinez     Marketing      $  72,000
      Carol Wu         Finance        $  88,000
    ```

    **Interpretation:** `DictWriter` wrote the header row and the data rows from the list of dictionaries; `DictReader` reversed the trip, yielding one dictionary per row keyed by the header names. Note the `int(row['salary'])` conversion — CSV, like any text format, delivers strings. In the next module, Polars will read files like this into a DataFrame with a single line and handle the type conversion for you.

    *Source: `computations/module08_examples.py` — `demo_csv_module()`*

### Capstone: Read → Process → Write

Everything in this module combines into the fundamental shape of data work — a **pipeline**: read an input file, process the data, write output files. The example below simulates receiving a supplier's product catalog as JSON, computes the minimum order cost for each product, and writes *two* outputs: a text report for humans and a JSON file for downstream programs.

!!! example "Worked Example: A Complete Data Pipeline"

    ```python
    import json
    from pathlib import Path

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

    catalog_path = Path("supplier_catalog.json")
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
    report_path = Path("order_analysis.txt")
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
    json_path = Path("order_analysis.json")
    with open(json_path, "w") as f:
        json.dump(json_output, f, indent=2)

    print(f"Step 3: Wrote {report_path.name} and {json_path.name}\n")

    # Display the text report
    print(report_path.read_text())
    ```

    **Output:**

    ```
    Step 1: Created supplier_catalog.json (5 products)
    Step 2: Calculated minimum order cost for each product
    Step 3: Wrote order_analysis.txt and order_analysis.json
    
    Supplier: Global Parts Inc.
    Catalog date: 2025-03-01
    =================================================================
    
    SKU          Product                  Unit $  Min Qty   Min Cost
    -----------------------------------------------------------------
    GP-1001      Bolt Pack (100)        $  12.50       10 $   125.00
    GP-1002      Washer Set (50)        $   8.75       20 $   175.00
    GP-1003      Hex Nut Bag (200)      $  15.00        5 $    75.00
    GP-1004      Spring Assortment      $  22.00        8 $   176.00
    GP-1005      Bearing Kit            $  45.00        3 $   135.00
    -----------------------------------------------------------------
                                Total minimum order cost $   686.00
    ```

    **Interpretation:** The pipeline read a nested JSON catalog of 5 products, enriched each record with a computed `min_order_cost` (unit price times minimum quantity — from $75.00 for hex nuts up to $176.00 for the spring assortment), and produced a $686.00 total minimum order. The same analysis left disk twice: a formatted text report a purchasing manager can read, and a JSON file the next program in the chain can `json.load()`. That read → process → write shape is the skeleton of every data workflow in the rest of this course.

    *Source: `computations/module08_examples.py` — `demo_data_pipeline()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| CSV is an Excel file format. | CSV is plain text that Excel happens to open. Any text editor — or two lines of Python — can read it. |
| You will always parse CSV by hand with `split(",")`. | Hand-splitting breaks on quoted commas. The `csv` module handles the edge cases now, and Polars (Module 9) replaces both with one `read_csv()` call. |
| A "data pipeline" requires special infrastructure. | At its core, a pipeline is read → process → write, built entirely from `open()`, `json`, loops, and functions you already know. Tools add scale, not a different idea. |

---

## Reflection Questions

1. `.read()` returns the whole file as one string, while `for line in f:` streams it one line at a time. For a server log measured in gigabytes, why does that difference matter — and why does it barely matter for the small files in this module?
2. A script opens a report file, writes half the rows, and then crashes on a bad record. Explain what the `with` statement guarantees in that moment that a plain `open()`/`close()` pair does not.
3. A teammate hard-codes `"C:\\reports\\output.txt"` in a script that must also run on your Mac. Which `pathlib` and `tempfile` tools from §8.3 fix this, and what does each contribute?
4. Compare JSON to a plain text report of the same analysis. When is JSON the better choice for storing data, and when is a simple text file sufficient? Who — or what — is the "reader" in each case?
5. Mode `"w"` silently destroys an existing file. Describe a business scenario where confusing `"w"` with `"a"` would cause real damage, and a habit from this module that guards against it.
6. The capstone pipeline wrote the same analysis to disk twice — once as text, once as JSON. Why produce both? What downstream consumer does each output serve?

---

## Your Assignment

The Module 8 assignment, **File I/O & Working with JSON**, is worth **100 points plus a 10-point bonus**. You complete it in the provided marimo notebook and submit the `.py` file to Blackboard. The closing reflection section is not graded separately — it counts toward participation. Two ground rules from the notebook's instructions: every file must be opened with a **context manager** (`with` statement), and file paths use the temp folder specified in the notebook so your code runs on any machine. Several tasks include a setup cell that creates the input file for you — run it, but do not modify it.

### Task 1: Reading a Text File (10 points)

A setup cell writes a weekly expense log — one category and amount per line, separated by a comma. Open the file with a context manager, parse each line into its category and amount, print each expense with aligned formatting, and finish with the total. This is the read → strip → split → convert pattern from §8.1.

### Task 2: Writing a Text File (15 points)

Starting from a provided list of employee attendance dictionaries, write a formatted attendance report to a text file: a header, one line per employee showing days present, days absent, and an attendance percentage, plus the overall average percentage. Then read the file back and print its contents. Writing and the read-back verification habit come from §8.2; the percentage arithmetic and f-string alignment draw on Module 2.

### Task 3: Pathlib Operations (15 points)

Create `Path` objects for three given file paths and, for each, print its `.name`, `.stem`, `.suffix`, and `.parent`, then check `.exists()`. Finish by creating a notes file with `.write_text()` and reading it back with `.read_text()`. Everything you need is the property tour and shortcut methods in §8.3.

### Task 4: Reading JSON (15 points)

A setup cell saves a restaurant menu as JSON, organized by category with a name, price, and vegetarian flag on each item. Load it with `json.load()`, print every vegetarian item under its category with its price, count them, and compute the average price per category. Loading is covered in §8.4; the category loop is nested-JSON navigation from the same section.

### Task 5: Navigating Nested JSON (20 points)

A setup cell writes a deeply nested school schedule: teachers, each with classes, each class with a room, time, and student list. Extract the unique room numbers using a set, count total students per teacher across their classes, and identify the teacher with the most students. This combines the nested navigation of §8.4 with the sets and dictionary-accumulator patterns from Module 7.

### Task 6: Building a Data Pipeline (25 points)

From a JSON file of quarterly sales figures per salesperson, build a full pipeline: read the input, compute each person's annual total and quarterly average, then write two outputs — a formatted text summary report (including team totals and the top performer) and an enriched JSON file that adds the computed fields to each record. Read back and print both outputs. This is the capstone pattern of §8.5, using the writing skills of §8.2 and the JSON round trip of §8.4.

### Task 7: Creative Exercise — Bonus (10 points)

Design your own business scenario demonstrating file I/O and JSON. It must include at least one text-file read or write, at least one JSON-file read or write, a context manager, navigation of a nested data structure, a summary calculation, and clear formatted output. The notebook suggests directions — a fitness tracker, a library catalog, a project dashboard, a budget tracker — but the scenario is yours.

### Reflection (participation credit)

Answer the notebook's five reflection prompts in your own words: `.read()` versus line-by-line iteration, why context managers matter, what `pathlib` adds over plain strings, when JSON beats plain text (and vice versa), and what challenged you most. There is no wrong answer — honest reflection helps your instructor see where support is needed.

---

## Chapter Summary

File I/O is the bridge between your code and the outside world. The `open()` function with a mode — `"r"` to read, `"w"` to overwrite, `"a"` to append — gives access to text files, and the `with` statement wraps every file operation so the file is closed properly even when something goes wrong. Small files can be swallowed whole with `.read()`; large ones should be streamed line by line, stripping the trailing newline from each line and converting text fields to real types before doing arithmetic. Writing reverses the flow: `f.write()` puts exactly the string you give it on disk (newlines included only if you add them), and reading a report back after writing it is a cheap way to verify what your audience will actually see.

The `pathlib` module replaces fragile string paths with `Path` objects: the `/` operator joins path pieces with the correct separator for any operating system, properties like `.name`, `.stem`, `.suffix`, and `.parent` take a path apart, `.exists()` checks the disk before you commit to reading, and `.write_text()`/`.read_text()` collapse simple whole-file operations into one call. For temporary locations that work everywhere, `tempfile.gettempdir()` beats hard-coding a folder.

JSON is the lingua franca of structured data on the web, and it maps directly onto Python: objects to dicts, arrays to lists, `true`/`false`/`null` to `True`/`False`/`None`. Four functions cover every direction of travel — `json.load()` and `json.dump()` for files, `json.loads()` and `json.dumps()` for strings — and once loaded, nested JSON is navigated by chaining `["key"]` and `[index]` access, which means every dictionary and list technique from Modules 6 and 7 transfers unchanged. CSV rounds out the formats: the simplest tabular text, readable today with the `csv` module and, starting next module, with a single Polars call. The capstone pipeline — read an input file, process the records, write text and JSON outputs — is the shape that data work takes from here forward.

---

## What's Next

Module 9 introduces **Polars**, a fast data analysis library that reads CSV, JSON, and Parquet files into **DataFrames** — and everything in this module set it up. The sales log you parsed by hand with `strip()` and `split()`, converting each field's type yourself, becomes a one-line `pl.read_csv()` with types inferred automatically. The file paths come from `pathlib`, the JSON structures you navigated become columns you can filter and aggregate with simple expressions, and the read → process → write pipeline stays the same shape — only the "process" step gains industrial-strength tools for selecting, sorting, and summarizing thousands of rows at once.
