"""
Module 14: Web Scraping - Worked Example Computations

This script reproduces every worked-example output in the Module 14 chapter
of the MIS501 Course Companion. Run with:

    pixi run -e compute python computations/module14_examples.py

DETERMINISM / OFFLINE NOTE: The teaching notebook makes two live requests to
httpbin.org (`requests.get`); every other demo already works on HTML strings
created in Python. These demos make NO network calls:

- SAMPLE_HTTPBIN_HTML mirrors the page https://httpbin.org/html returns (a
  Moby-Dick excerpt), so the request demos process an embedded page instead
  of a live response.
- MAIN_PAGE_HTML, ENGINEERING_HTML, MARKETING_HTML, FINANCE_HTML, and
  OPERATIONS_HTML reproduce the notebook's fictional Acme Corporation
  employee directory exactly. DEPARTMENT_PAGES maps department URLs to
  their pages, simulating multi-page navigation without a network.

The `requests` library is imported ONLY for its exception classes so the
robust-fetch demo uses the exact `except` clause the notebook teaches; no
request is ever sent. BeautifulSoup uses Python's built-in "html.parser".

References in Course Companion:
- demo_requests_basics()            -> Module 14, Section 14.1 (The requests Library)
- demo_soup_object()                -> Module 14, Section 14.2 (Creating a BeautifulSoup Object)
- demo_find_and_find_all()          -> Module 14, Section 14.2 (Finding Elements)
- demo_text_extraction()            -> Module 14, Section 14.2 (Extracting Text)
- demo_extract_attributes()         -> Module 14, Section 14.2 (Extracting Attributes)
- demo_table_scraping_pattern()     -> Module 14, Section 14.3 (Working with Tables)
- demo_css_selectors()              -> Module 14, Section 14.3 (CSS Selectors)
- demo_tree_navigation()            -> Module 14, Section 14.3 (Navigating the Tree)
- demo_table_to_dataframe()         -> Module 14, Section 14.4 (Building and Cleaning a Scraped DataFrame)
- demo_multi_page_scrape()          -> Module 14, Section 14.4 (Scraping Multiple Pages)
- demo_fetch_page_function()        -> Module 14, Section 14.5 (A Robust Fetch Function)
- demo_scrape_table_function()      -> Module 14, Section 14.5 (Reusable Table Scraper Function)
- demo_capstone_scrape_and_clean()  -> Module 14, Section 14.5 (Capstone: Scrape and Clean)
- demo_capstone_analysis()          -> Module 14, Section 14.5 (Capstone: Analyze the Directory)

Last updated: 2026-07-23
"""

import time

import polars as pl
import requests  # imported for its exception classes only — no network calls
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Embedded sample pages
# ---------------------------------------------------------------------------

# Mirrors the page returned by GET https://httpbin.org/html (a Moby-Dick
# excerpt), so the request demos are reproducible offline.
SAMPLE_HTTPBIN_HTML = """<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
      <h1>Herman Melville - Moby-Dick</h1>

      <div>
        <p>
          Availing himself of the mild, summer-cool weather that now reigned in these latitudes, and in preparation for the peculiarly active pursuits shortly to be anticipated, Perth, the begrimed, blistered old blacksmith, had not removed his portable forge to the hold again, after concluding his contributory work for Ahab's leg, but still retained it on deck, fast lashed to ringbolts by the foremast; being now almost incessantly invoked by the headsmen, and harpooneers, and bowsmen to do some little job for them; altering, or repairing, or new shaping their various weapons and boat furniture.
        </p>
      </div>
  </body>
</html>"""

# --- The Acme Corp employee directory (identical to the teaching notebook) ---

# Main directory page — lists all departments
MAIN_PAGE_HTML = """
<html>
<head><title>Acme Corp - Employee Directory</title></head>
<body>
    <h1 id="page-title">Acme Corporation Employee Directory</h1>
    <p class="subtitle">Browse departments to view employee rosters</p>

    <div class="department-list">
        <div class="dept-card" id="eng-card">
            <h2><a href="/departments/engineering">Engineering</a></h2>
            <p class="dept-summary">Builds and maintains our software platform</p>
            <span class="headcount">Headcount: 8</span>
        </div>

        <div class="dept-card" id="mkt-card">
            <h2><a href="/departments/marketing">Marketing</a></h2>
            <p class="dept-summary">Drives brand awareness and customer acquisition</p>
            <span class="headcount">Headcount: 6</span>
        </div>

        <div class="dept-card" id="fin-card">
            <h2><a href="/departments/finance">Finance</a></h2>
            <p class="dept-summary">Manages budgets, forecasting, and compliance</p>
            <span class="headcount">Headcount: 5</span>
        </div>

        <div class="dept-card" id="ops-card">
            <h2><a href="/departments/operations">Operations</a></h2>
            <p class="dept-summary">Coordinates logistics and internal processes</p>
            <span class="headcount">Headcount: 6</span>
        </div>
    </div>

    <footer>
        <p class="updated">Last updated: 2025-09-01</p>
    </footer>
</body>
</html>
"""

ENGINEERING_HTML = """
<html>
<head><title>Acme Corp - Engineering</title></head>
<body>
    <h1>Engineering Department</h1>
    <p class="dept-description">The Engineering team builds and maintains
    Acme's core software platform, data pipelines, and cloud infrastructure.</p>

    <table class="employee-table" id="eng-table">
        <thead>
            <tr>
                <th>Name</th>
                <th>Title</th>
                <th>Salary</th>
                <th>Years</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>Raj Patel</td><td>VP of Engineering</td><td>$185,000</td><td>12</td></tr>
            <tr><td>Lina Zhang</td><td>Senior Software Engineer</td><td>$155,000</td><td>8</td></tr>
            <tr><td>Marcus Johnson</td><td>Senior Software Engineer</td><td>$150,000</td><td>7</td></tr>
            <tr><td>Sofia Rivera</td><td>Data Engineer</td><td>$140,000</td><td>5</td></tr>
            <tr><td>James O'Brien</td><td>Software Engineer</td><td>$120,000</td><td>3</td></tr>
            <tr><td>Aisha Kwame</td><td>Software Engineer</td><td>$115,000</td><td>2</td></tr>
            <tr><td>Noah Fischer</td><td>DevOps Engineer</td><td>$135,000</td><td>4</td></tr>
            <tr><td>Priya Sharma</td><td>Junior Developer</td><td>$85,000</td><td>1</td></tr>
        </tbody>
    </table>

    <p class="team-note">Team lead: <a href="mailto:raj.patel@acme.com">Raj Patel</a></p>
</body>
</html>
"""

MARKETING_HTML = """
<html>
<head><title>Acme Corp - Marketing</title></head>
<body>
    <h1>Marketing Department</h1>
    <p class="dept-description">The Marketing team drives brand awareness,
    manages campaigns, and leads customer acquisition efforts.</p>

    <table class="employee-table" id="mkt-table">
        <thead>
            <tr>
                <th>Name</th>
                <th>Title</th>
                <th>Salary</th>
                <th>Years</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>Diana Torres</td><td>VP of Marketing</td><td>$175,000</td><td>10</td></tr>
            <tr><td>Kevin Wu</td><td>Brand Manager</td><td>$120,000</td><td>6</td></tr>
            <tr><td>Rachel Green</td><td>Content Strategist</td><td>$105,000</td><td>4</td></tr>
            <tr><td>Tom Bradley</td><td>Digital Marketing Specialist</td><td>$95,000</td><td>3</td></tr>
            <tr><td>Yuki Tanaka</td><td>Social Media Manager</td><td>$90,000</td><td>2</td></tr>
            <tr><td>Emma Clarke</td><td>Marketing Coordinator</td><td>$72,000</td><td>1</td></tr>
        </tbody>
    </table>

    <p class="team-note">Team lead: <a href="mailto:diana.torres@acme.com">Diana Torres</a></p>
</body>
</html>
"""

FINANCE_HTML = """
<html>
<head><title>Acme Corp - Finance</title></head>
<body>
    <h1>Finance Department</h1>
    <p class="dept-description">The Finance team manages corporate budgets,
    financial forecasting, regulatory compliance, and investor relations.</p>

    <table class="employee-table" id="fin-table">
        <thead>
            <tr>
                <th>Name</th>
                <th>Title</th>
                <th>Salary</th>
                <th>Years</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>Robert Nguyen</td><td>CFO</td><td>$195,000</td><td>15</td></tr>
            <tr><td>Laura Kim</td><td>Financial Analyst</td><td>$110,000</td><td>5</td></tr>
            <tr><td>Ethan Brown</td><td>Senior Accountant</td><td>$105,000</td><td>6</td></tr>
            <tr><td>Megan Foster</td><td>Budget Analyst</td><td>$95,000</td><td>3</td></tr>
            <tr><td>Andre Williams</td><td>Compliance Officer</td><td>$115,000</td><td>4</td></tr>
        </tbody>
    </table>

    <p class="team-note">Team lead: <a href="mailto:robert.nguyen@acme.com">Robert Nguyen</a></p>
</body>
</html>
"""

OPERATIONS_HTML = """
<html>
<head><title>Acme Corp - Operations</title></head>
<body>
    <h1>Operations Department</h1>
    <p class="dept-description">The Operations team coordinates logistics,
    vendor management, facilities, and internal process improvement.</p>

    <table class="employee-table" id="ops-table">
        <thead>
            <tr>
                <th>Name</th>
                <th>Title</th>
                <th>Salary</th>
                <th>Years</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>Sandra Lopez</td><td>VP of Operations</td><td>$170,000</td><td>11</td></tr>
            <tr><td>Chris Park</td><td>Supply Chain Manager</td><td>$115,000</td><td>7</td></tr>
            <tr><td>Hannah Davis</td><td>Logistics Coordinator</td><td>$82,000</td><td>3</td></tr>
            <tr><td>Omar Hassan</td><td>Facilities Manager</td><td>$90,000</td><td>5</td></tr>
            <tr><td>Jenny Liu</td><td>Process Analyst</td><td>$98,000</td><td>4</td></tr>
            <tr><td>Brian Kelly</td><td>Operations Associate</td><td>$70,000</td><td>1</td></tr>
        </tbody>
    </table>

    <p class="team-note">Team lead: <a href="mailto:sandra.lopez@acme.com">Sandra Lopez</a></p>
</body>
</html>
"""

# Simulates the website: department URL -> page HTML (what requests.get()
# would return from each department page).
DEPARTMENT_PAGES = {
    "/departments/engineering": ENGINEERING_HTML,
    "/departments/marketing": MARKETING_HTML,
    "/departments/finance": FINANCE_HTML,
    "/departments/operations": OPERATIONS_HTML,
}

# Small snippet for the text-extraction demo (nested <strong> inside a span)
TEXT_EXTRACTION_HTML = """
<div class="employee">
    <span class="name">  Raj Patel  </span>
    <span class="title">VP of <strong>Engineering</strong></span>
</div>
"""


# ---------------------------------------------------------------------------
# 14.1 Web Scraping and How the Web Works
# ---------------------------------------------------------------------------

def demo_requests_basics():
    """
    The notebook's live requests.get("https://httpbin.org/html") demo,
    reproduced offline: the response fields shown are exactly what the
    live call returns, with the body served from SAMPLE_HTTPBIN_HTML.
    """
    status_code = 200                          # what httpbin.org/html returns
    content_type = "text/html; charset=utf-8"  # its Content-Type header
    html = SAMPLE_HTTPBIN_HTML                 # its response body

    print(f"Status code: {status_code}")
    print(f"Content type: {content_type}")
    print(f"Content length: {len(html)} characters")
    print()
    print("First 300 characters of HTML:")
    print(html[:300])


# ---------------------------------------------------------------------------
# 14.2 Parsing HTML with BeautifulSoup
# ---------------------------------------------------------------------------

def demo_soup_object():
    """Create a BeautifulSoup object from the main directory page."""
    main_soup = BeautifulSoup(MAIN_PAGE_HTML, "html.parser")

    # The soup object represents the entire document
    print(f"Type: {type(main_soup)}")
    print(f"Title tag: {main_soup.title}")
    print(f"Title text: {main_soup.title.string}")


def demo_find_and_find_all():
    """find() vs. find_all(), then searching by CSS class and by ID."""
    main_soup = BeautifulSoup(MAIN_PAGE_HTML, "html.parser")

    # find() returns the FIRST match
    first_h2 = main_soup.find("h2")
    print(f"First <h2> tag: {first_h2}")
    print(f"Text inside:   {first_h2.get_text()}")
    print()

    # find_all() returns ALL matches as a list
    all_h2 = main_soup.find_all("h2")
    print(f"All <h2> tags ({len(all_h2)} found):")
    for tag in all_h2:
        print(f"  - {tag.get_text()}")
    print()

    # Search by CSS class (class_ because class is reserved in Python)
    dept_cards = main_soup.find_all("div", class_="dept-card")
    print(f"Department cards found: {len(dept_cards)}")
    print()
    for card in dept_cards:
        name = card.find("h2").get_text()
        summary = card.find("p", class_="dept-summary").get_text()
        print(f"  {name}: {summary}")
    print()

    # Search by ID — find() returns the FIRST match. IDs are supposed to be
    # unique on a page, but real-world pages break that rule.
    eng_card = main_soup.find("div", id="eng-card")
    print("Found element with id='eng-card':")
    print(f"  Department: {eng_card.find('h2').get_text()}")
    # The span's own text already reads "Headcount: N", so print it as-is
    print(f"  {eng_card.find('span', class_='headcount').get_text()}")


def demo_text_extraction():
    """Compare .get_text(), .get_text(strip=True), separators, and .string."""
    soup = BeautifulSoup(TEXT_EXTRACTION_HTML, "html.parser")
    name_tag = soup.find("span", class_="name")
    title_tag = soup.find("span", class_="title")

    print("Extracting from <span class='name'>:")
    print(f"  .get_text()            = '{name_tag.get_text()}'")
    print(f"  .get_text(strip=True)  = '{name_tag.get_text(strip=True)}'")
    print(f"  .string                = '{name_tag.string}'")
    print()
    print("Extracting from <span class='title'> (has a nested <strong> tag):")
    print(f"  .get_text()                = '{title_tag.get_text()}'")
    # strip=True strips each text node separately and joins with NOTHING,
    # so "VP of " and "Engineering" get glued into "VP ofEngineering".
    print(f"  .get_text(strip=True)      = '{title_tag.get_text(strip=True)}'")
    print(f"  .get_text(' ', strip=True) = '{title_tag.get_text(' ', strip=True)}'")
    # .string is None here because this tag has more than one child (the
    # text "VP of " AND the <strong> tag).
    print(f"  .string                    = {title_tag.string}")


def demo_extract_attributes():
    """Extract href, id, and other attributes from tags."""
    main_soup = BeautifulSoup(MAIN_PAGE_HTML, "html.parser")

    # Extract href attributes from all links
    links = main_soup.find_all("a")
    print(f"Found {len(links)} links on the main page:")
    print()
    for link in links:
        text = link.get_text(strip=True)
        href = link["href"]
        print(f"  Text: {text:20s}  href: {href}")
    print()

    # Extract multiple attributes from department cards
    cards = main_soup.find_all("div", class_="dept-card")
    print("Department card IDs and their links:")
    print()
    for card in cards:
        card_id = card.get("id")
        link = card.find("a")
        dept_name = link.get_text(strip=True)
        dept_url = link["href"]
        print(f"  id={card_id:10s}  name={dept_name:15s}  url={dept_url}")


# ---------------------------------------------------------------------------
# 14.3 Tables, CSS Selectors, and Tree Navigation
# ---------------------------------------------------------------------------

def demo_table_scraping_pattern():
    """The four-step table pattern: table -> headers -> rows -> cells."""
    eng_soup = BeautifulSoup(ENGINEERING_HTML, "html.parser")

    # Step 1: Find the table
    table = eng_soup.find("table", class_="employee-table")
    print(f"Found table with id: {table.get('id')}")

    # Step 2: Extract column headers from <th> tags
    headers = [
        th.get_text(strip=True)
        for th in table.find_all("th")
    ]
    print(f"Column headers: {headers}")

    # Step 3: Extract data rows from <tbody>
    rows = table.find("tbody").find_all("tr")
    print(f"Data rows found: {len(rows)}")

    # Step 4: Extract cell text from each row
    print("\nEmployee data:")
    for row in rows:
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        print(f"  {cells}")


def demo_css_selectors():
    """select() and select_one() on the main page and the employee table."""
    main_soup = BeautifulSoup(MAIN_PAGE_HTML, "html.parser")

    # Select all department cards
    cards = main_soup.select("div.dept-card")
    print(f"div.dept-card: {len(cards)} matches")

    # Select by ID
    eng = main_soup.select_one("#eng-card")
    print(f"#eng-card: {eng.find('h2').get_text(strip=True)}")

    # Select all links inside department cards
    links = main_soup.select("div.dept-card a")
    print("\nLinks inside dept-cards:")
    for link in links:
        print(f"  {link.get_text(strip=True)} -> {link['href']}")

    # CSS selectors for table data
    eng_soup = BeautifulSoup(ENGINEERING_HTML, "html.parser")

    # Select all <td> cells inside the employee table
    all_cells = eng_soup.select("table.employee-table tbody td")
    print(f"\nTotal <td> cells: {len(all_cells)}")

    # Select all rows, then extract cells per row
    rows = eng_soup.select("table.employee-table tbody > tr")
    print("\nFirst 3 employees (via CSS selectors):")
    for row in rows[:3]:
        cells = [td.get_text(strip=True) for td in row.select("td")]
        print(f"  {cells}")


def demo_tree_navigation():
    """.parent, .children, find_next(), and find_parent() on the tree."""
    eng_soup = BeautifulSoup(ENGINEERING_HTML, "html.parser")

    # Start from the table
    table = eng_soup.find("table")

    # .parent tells you what contains an element
    print(f"Table's parent tag: <{table.parent.name}>")

    # .children gives direct child nodes — filter on .name to keep only
    # real elements (whitespace between tags shows up as text nodes)
    children = [
        child.name
        for child in table.children
        if child.name is not None
    ]
    print(f"Table's direct children: {children}")

    # find_next() finds the next occurrence after a given element
    h1 = eng_soup.find("h1")
    next_p = h1.find_next("p")
    print(f"\nFirst <p> after <h1>: {next_p.get_text(strip=True)[:60]}...")

    # find_parent() walks up the tree
    first_td = eng_soup.find("td")
    parent_row = first_td.find_parent("tr")
    cells = [td.get_text(strip=True) for td in parent_row.find_all("td")]
    print(f"Parent row of first <td>: {cells}")


# ---------------------------------------------------------------------------
# 14.4 From Scraped HTML to Polars DataFrames
# ---------------------------------------------------------------------------

def demo_table_to_dataframe():
    """Parse one department page into a Polars DataFrame, then clean it."""
    soup = BeautifulSoup(ENGINEERING_HTML, "html.parser")
    table = soup.find("table", class_="employee-table")

    # Extract column headers
    headers = [
        th.get_text(strip=True)
        for th in table.find_all("th")
    ]

    # Extract rows as a list of dictionaries
    employees = []
    for row in table.find("tbody").find_all("tr"):
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        # Zip headers with cell values to create a dict
        employee = dict(zip(headers, cells))
        employees.append(employee)

    # Create a Polars DataFrame
    eng_df = pl.DataFrame(employees)
    print("Engineering department as a Polars DataFrame:")
    print(eng_df)

    # Clean the data: "$185,000" -> 185000, "12" -> 12
    eng_clean = eng_df.with_columns(
        pl.col("Salary")
        .str.replace_all(r"[\$,]", "")
        .cast(pl.Int64)
        .alias("Salary"),
        pl.col("Years")
        .cast(pl.Int64)
        .alias("Years"),
    )

    print("\nCleaned DataFrame (salary as integer, years as integer):")
    print(eng_clean)


def demo_multi_page_scrape():
    """Index page -> department links -> scrape each page -> one DataFrame."""
    main_soup = BeautifulSoup(MAIN_PAGE_HTML, "html.parser")

    # Step 1: Extract department URLs from the main page
    dept_links = main_soup.select("div.dept-card a")
    urls = [
        (link.get_text(strip=True), link["href"])
        for link in dept_links
    ]

    print("Department links found:")
    for name, url in urls:
        print(f"  {name} -> {url}")

    # Step 2: Scrape each department page
    all_employees = []
    for dept_name, dept_url in urls:
        # In real code: response = requests.get(base_url + dept_url)
        # Here we look up the HTML from our dictionary
        html = DEPARTMENT_PAGES[dept_url]
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", class_="employee-table")

        headers = [
            th.get_text(strip=True)
            for th in table.find_all("th")
        ]

        for row in table.find("tbody").find_all("tr"):
            cells = [
                td.get_text(strip=True)
                for td in row.find_all("td")
            ]
            employee = dict(zip(headers, cells))
            # Add the department name so we know which page it came from
            employee["Department"] = dept_name
            all_employees.append(employee)

    # Step 3: Build the combined DataFrame, then clean it
    employees_raw = pl.DataFrame(all_employees)
    print(f"\nCombined DataFrame: {employees_raw.shape[0]} employees "
          f"from {len(urls)} departments")

    employees = employees_raw.with_columns(
        pl.col("Salary")
        .str.replace_all(r"[\$,]", "")
        .cast(pl.Int64)
        .alias("Salary"),
        pl.col("Years")
        .cast(pl.Int64)
        .alias("Years"),
    )

    print(f"Cleaned employee directory: {employees.shape[0]} rows, "
          f"{employees.shape[1]} columns")
    print(f"Departments: {employees['Department'].unique(maintain_order=True).to_list()}")
    print(f"Salary range: ${employees['Salary'].min():,} – ${employees['Salary'].max():,}")
    print(employees.head(5))


# ---------------------------------------------------------------------------
# 14.5 Robust, Reusable Scraping Workflows
# ---------------------------------------------------------------------------

def demo_fetch_page_function():
    """
    The notebook's robust fetch_page() helper: user-agent header, timeout,
    status check, exception handling, and a rate-limiting delay. The
    transport is offline (serves SAMPLE_HTTPBIN_HTML); the handling logic
    is exactly the notebook's.
    """
    class _OfflineResponse:
        def __init__(self, status_code, text):
            self.status_code = status_code
            self.text = text

    def sample_get(url, headers=None, timeout=10):
        """Offline transport: serves the embedded httpbin sample page."""
        if url == "https://httpbin.org/html":
            return _OfflineResponse(200, SAMPLE_HTTPBIN_HTML)
        return _OfflineResponse(404, "")

    def fetch_page(url, delay=1.0):
        """Fetch a page with error handling and rate limiting."""
        headers = {
            "User-Agent": "MIS501-CourseProject/1.0 (student@university.edu)"
        }
        try:
            response = sample_get(          # notebook: requests.get(
                url,
                headers=headers,
                timeout=10,
            )
            if response.status_code == 200:
                return response.text
            else:
                print(f"  Warning: {url} returned status {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"  Error fetching {url}: {e}")
            return None
        finally:
            # Rate limit: wait before the next request
            time.sleep(delay)

    html = fetch_page("https://httpbin.org/html")
    if html:
        print(f"Successfully fetched page: {len(html)} characters")
    else:
        print("Could not fetch page (network may be unavailable)")


def demo_scrape_table_function():
    """A reusable scrape_table() utility, then applied to all departments."""
    def scrape_table(html, table_selector="table", extra_columns=None):
        """Parse an HTML table into a Polars DataFrame.

        Parameters
        ----------
        html : str
            Raw HTML string containing a table.
        table_selector : str
            CSS selector to locate the table (default: first <table>).
        extra_columns : dict or None
            Additional columns to add to every row.
        """
        soup = BeautifulSoup(html, "html.parser")
        table = soup.select_one(table_selector)

        if table is None:
            return pl.DataFrame()

        # Extract headers
        headers = [
            th.get_text(strip=True)
            for th in table.find_all("th")
        ]

        # Extract rows.
        # We use find_all("tr"), NOT select("tbody > tr"): <tbody> is
        # optional in HTML source, so requiring it would return nothing on
        # any table whose source omits it. The header row (which has <th>,
        # not <td>) produces an empty cells list and is skipped below.
        records = []
        for row in table.find_all("tr"):
            cells = [
                td.get_text(strip=True)
                for td in row.find_all("td")
            ]
            if cells and len(cells) == len(headers):
                record = dict(zip(headers, cells))
                if extra_columns:
                    record.update(extra_columns)
                records.append(record)

        return pl.DataFrame(records)

    # Test the function on a minimal table.
    # Note this HTML has NO <tbody> in the source — proof that
    # find_all("tr") handles tables the browser would have "fixed" for you.
    print("Testing scrape_table() on a minimal table (no <tbody> in source):")
    test_df = scrape_table(
        html="<table><tr><th>A</th><th>B</th></tr>"
             "<tr><td>1</td><td>2</td></tr></table>",
    )
    print(test_df)

    # Use the reusable function to scrape all departments
    main_soup = BeautifulSoup(MAIN_PAGE_HTML, "html.parser")
    dept_links = main_soup.select("div.dept-card a")

    all_dfs = []
    print()
    for link in dept_links:
        name = link.get_text(strip=True)
        url = link["href"]
        html = DEPARTMENT_PAGES[url]

        df = scrape_table(
            html=html,
            table_selector="table.employee-table",
            extra_columns={"Department": name},
        )
        all_dfs.append(df)
        print(f"  {name}: {df.shape[0]} employees")

    # Combine all department DataFrames
    employees_v2 = pl.concat(all_dfs)
    print(f"\nCombined: {employees_v2.shape[0]} employees")


# --- Capstone helpers (shared by the two capstone demos) -------------------

def _capstone_dept_info():
    """Capstone Step 1: department metadata from the main page."""
    main_soup = BeautifulSoup(MAIN_PAGE_HTML, "html.parser")
    dept_cards = main_soup.select("div.dept-card")

    dept_info = []
    for card in dept_cards:
        dept_info.append({
            "Department": card.select_one("h2").get_text(strip=True),
            "Description": card.select_one("p.dept-summary").get_text(strip=True),
            "URL": card.select_one("a")["href"],
            "Headcount": int(
                card.select_one("span.headcount")
                .get_text(strip=True)
                .split(": ")[1]
            ),
        })
    return dept_info


def _capstone_clean_df():
    """Capstone Steps 2-3: scrape every department page and clean the data."""
    dept_info = _capstone_dept_info()

    all_employees = []
    for dept in dept_info:
        html = DEPARTMENT_PAGES[dept["URL"]]
        soup = BeautifulSoup(html, "html.parser")

        # Also grab the team lead email from the mailto: link
        team_note = soup.select_one("p.team-note a")
        lead_email = (
            team_note["href"].replace("mailto:", "") if team_note else "N/A"
        )

        table = soup.select_one("table.employee-table")
        headers = [th.get_text(strip=True) for th in table.find_all("th")]

        for row in table.select("tbody > tr"):
            cells = [td.get_text(strip=True) for td in row.find_all("td")]
            employee = dict(zip(headers, cells))
            employee["Department"] = dept["Department"]
            employee["Dept_Lead_Email"] = lead_email
            all_employees.append(employee)

    capstone_raw = pl.DataFrame(all_employees)

    capstone_df = (
        capstone_raw
        .with_columns(
            pl.col("Salary")
            .str.replace_all(r"[\$,]", "")
            .cast(pl.Int64)
            .alias("Salary"),
            pl.col("Years")
            .cast(pl.Int64)
            .alias("Years"),
        )
        .with_columns(
            # Create a seniority level based on years of service
            pl.when(pl.col("Years") >= 10)
            .then(pl.lit("Senior (10+ yr)"))
            .when(pl.col("Years") >= 5)
            .then(pl.lit("Mid (5-9 yr)"))
            .when(pl.col("Years") >= 2)
            .then(pl.lit("Junior (2-4 yr)"))
            .otherwise(pl.lit("Entry (<2 yr)"))
            .alias("Seniority"),
        )
    )
    return capstone_raw, capstone_df


def demo_capstone_scrape_and_clean():
    """Capstone Steps 1-3: metadata, all employee tables, cleaned columns."""
    # Step 1: Department metadata from the main page
    dept_info = _capstone_dept_info()
    dept_metadata = pl.DataFrame(dept_info)
    print("Department metadata:")
    print(dept_metadata)

    # Steps 2-3: Scrape every department page, then clean
    capstone_raw, capstone_df = _capstone_clean_df()
    print(f"\nRaw scraped data: {capstone_raw.shape[0]} rows, "
          f"{capstone_raw.shape[1]} columns")

    print(f"Cleaned DataFrame: {capstone_df.shape}")
    print(f"Columns: {capstone_df.columns}")
    print(capstone_df.select("Name", "Salary", "Years", "Seniority").head(4))


def demo_capstone_analysis():
    """Capstone Steps 4-5: summaries plus the dashboard's headline numbers."""
    _, capstone_df = _capstone_clean_df()

    # Department-level summary
    dept_summary = (
        capstone_df
        .group_by("Department")
        .agg(
            pl.len().alias("Headcount"),
            pl.col("Salary").mean().round(0).cast(pl.Int64).alias("Avg_Salary"),
            pl.col("Salary").median().alias("Median_Salary"),
            pl.col("Salary").min().alias("Min_Salary"),
            pl.col("Salary").max().alias("Max_Salary"),
            pl.col("Years").mean().round(1).alias("Avg_Years"),
        )
        .sort("Avg_Salary", descending=True)
    )
    print("Department Compensation Summary:")
    print(dept_summary)

    # Seniority-level summary
    seniority_summary = (
        capstone_df
        .group_by("Seniority")
        .agg(
            pl.len().alias("Count"),
            pl.col("Salary").mean().round(0).cast(pl.Int64).alias("Avg_Salary"),
            pl.col("Salary").min().alias("Min_Salary"),
            pl.col("Salary").max().alias("Max_Salary"),
        )
        .sort("Avg_Salary", descending=True)
    )
    print("\nCompensation by Seniority Level:")
    print(seniority_summary)

    # The dashboard's summary line (the numbers behind the charts)
    print(
        f"\nSummary: {capstone_df.shape[0]} employees across "
        f"{capstone_df['Department'].n_unique()} departments | "
        f"Salary range: ${capstone_df['Salary'].min():,} – "
        f"${capstone_df['Salary'].max():,} | "
        f"Average: ${capstone_df['Salary'].mean():,.0f}"
    )


# ---------------------------------------------------------------------------
# Runner — demos in chapter order
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    demos = [
        ("14.1", demo_requests_basics),
        ("14.2", demo_soup_object),
        ("14.2", demo_find_and_find_all),
        ("14.2", demo_text_extraction),
        ("14.2", demo_extract_attributes),
        ("14.3", demo_table_scraping_pattern),
        ("14.3", demo_css_selectors),
        ("14.3", demo_tree_navigation),
        ("14.4", demo_table_to_dataframe),
        ("14.4", demo_multi_page_scrape),
        ("14.5", demo_fetch_page_function),
        ("14.5", demo_scrape_table_function),
        ("14.5", demo_capstone_scrape_and_clean),
        ("14.5", demo_capstone_analysis),
    ]

    for section, demo in demos:
        print("=" * 72)
        print(f"[{section}] {demo.__name__}")
        print("=" * 72)
        demo()
        print()

    print("=" * 72)
    print("All Module 14 demonstrations complete.")
    print("=" * 72)
