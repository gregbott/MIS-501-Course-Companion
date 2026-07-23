# Module 14: Web Scraping

## Introduction

Every module so far assumed the data was already sitting in a file or a database. Real analysis projects rarely start that way: the competitor prices you want to track, the supplier directory you need to consolidate, or the market listings you want to study often exist only as **web pages built for human eyes**. Web scraping is the skill of turning those pages back into structured data — you write Python that downloads a page's HTML, locates the elements that hold the values you care about, and loads them into a Polars DataFrame you can analyze with everything from Modules 9–13. This module teaches that entire workflow — `requests` to fetch, BeautifulSoup to parse, Polars to analyze — along with the ethical and practical ground rules that separate a responsible scraper from a nuisance. To keep practice safe and reproducible, you will scrape a fictional company directory built from HTML strings created in Python; the techniques are identical whether the HTML comes from `requests.get()` or a string.

---

## Learning Objectives

By the end of this module, you should be able to:

1. **Explain** what web scraping is, when it is appropriate to use, and the ethical rules that govern it
2. **Fetch** web page content using the `requests` library and interpret HTTP status codes
3. **Parse** HTML documents using BeautifulSoup and Python's built-in `"html.parser"`
4. **Extract** text, attributes, and links from HTML elements
5. **Navigate** HTML structure using tags, classes, CSS selectors, and tree relationships
6. **Build** a complete scraping workflow that produces a clean Polars DataFrame ready for analysis

---

## 14.1 Web Scraping and How the Web Works

**Web scraping** is the process of extracting data from web pages programmatically. Instead of manually copying information from a website, you write Python code that downloads the page and pulls out the data you need.

**When to use web scraping:**

- The data you need is publicly available on a website
- No API (Application Programming Interface) is available
- You need to collect data from many pages that would be tedious to copy by hand

### Ethics and Legality Before You Scrape

Scraping touches someone else's server and someone else's content, so it comes with obligations. Before scraping any real site:

- **Check `robots.txt`** — most websites publish a file at `example.com/robots.txt` that specifies which pages automated tools may access
- **Respect rate limits** — add delays between requests so you do not overload the server
- **Read the Terms of Service** — some sites explicitly prohibit scraping
- **Do not scrape personal data** without a lawful basis
- **Prefer APIs when available** — they are more reliable, faster, and explicitly permitted

In this module we practice scraping techniques on HTML strings we create ourselves, so there are no ethical concerns. In Module 15 you will learn to use REST APIs, which are the preferred approach when they exist.

### How the Web Works (In Thirty Seconds)

When you type a URL into your browser:

1. Your browser sends an **HTTP GET request** to the server
2. The server returns an **HTML document** (a text file with tags)
3. Your browser **renders** the HTML into the page you see

Web scraping follows the same steps, except Python does them:

1. `requests.get(url)` sends the HTTP GET request
2. The response's `.text` attribute contains the raw HTML
3. BeautifulSoup parses the HTML so you can extract data

The key insight: **what you see in a browser is usually just formatted HTML** — and if the data is in the HTML the server sends back, you can scrape it. One caveat: some sites build their content with JavaScript *after* the page loads, and `requests` only ever sees the initial HTML, not anything JavaScript adds later. That is the number-one reason a beginner's first real scrape comes back empty. (Tools like Selenium or Playwright can render those pages, but they are beyond this module.)

### The `requests` Library

The `requests` library sends HTTP requests and returns responses. The most common method is `requests.get(url)`:

```python
response = requests.get("https://example.com")
response.status_code   # 200 means success
response.text          # the HTML content as a string
response.headers       # metadata about the response
```

**Common status codes:**

| Code | Meaning |
|------|---------|
| 200 | OK — request succeeded |
| 301 | Moved permanently — page has a new URL |
| 403 | Forbidden — you do not have permission |
| 404 | Not found — page does not exist |
| 429 | Too many requests — you are being rate-limited |
| 500 | Server error — something broke on their end |

The course notebook makes one quick live request to `httpbin.org` (a free testing service for HTTP requests) so you can see `requests` in action, then switches to HTML strings created in Python so nothing depends on a website being reachable during class. Note the `timeout` and the `try`/`except` in the example below: a live request can hang or fail, so we never call `requests.get()` without them.

!!! example "Worked Example: Fetching a Page with requests"

    ```python
    import requests

    # httpbin.org/html returns a small sample page (a Moby-Dick excerpt)
    try:
        response = requests.get("https://httpbin.org/html", timeout=10)

        print(f"Status code: {response.status_code}")
        print(f"Content type: {response.headers.get('Content-Type', 'unknown')}")
        print(f"Content length: {len(response.text)} characters")
        print()
        print("First 300 characters of HTML:")
        print(response.text[:300])
    except requests.exceptions.RequestException as e:
        print(f"Could not reach httpbin.org ({e}).")
    ```

    **Output:**

    ```
    Status code: 200
    Content type: text/html; charset=utf-8
    Content length: 765 characters

    First 300 characters of HTML:
    <!DOCTYPE html>
    <html>
      <head>
      </head>
      <body>
          <h1>Herman Melville - Moby-Dick</h1>

          <div>
            <p>
              Availing himself of the mild, summer-cool weather that now reigned in these latitudes, and in preparation for the peculiarly active pursuits shortly to be anticipated, Per
    ```

    **Interpretation:** The status code 200 confirms the request succeeded, the `Content-Type` header tells you the body is HTML text, and `.text` holds the entire page as one Python string — 765 characters here. What arrives is raw markup, not the rendered page a browser shows, which is exactly why the next step is a parser.

    *Note: output produced from an embedded sample page so results are reproducible offline.*

    *Source: `computations/module14_examples.py` — `demo_requests_basics()`*

### HTML Basics for Scraping

HTML uses **tags** to structure content. Every tag has an opening `<tag>` and a closing `</tag>`. Tags can have **attributes** like `class`, `id`, and `href`.

Here is the HTML you need to know for scraping:

| Tag | Purpose | Example |
|-----|---------|---------|
| `<h1>` to `<h6>` | Headings | `<h1>Company Directory</h1>` |
| `<p>` | Paragraph | `<p>Welcome to our site.</p>` |
| `<a>` | Link | `<a href="/about">About Us</a>` |
| `<div>` | Container/section | `<div class="dept">...</div>` |
| `<span>` | Inline container | `<span class="title">Manager</span>` |
| `<table>` | Table | `<table>...</table>` |
| `<tr>` | Table row | `<tr>...</tr>` |
| `<th>` | Table header cell | `<th>Name</th>` |
| `<td>` | Table data cell | `<td>Alice Chen</td>` |
| `<ul>`, `<li>` | List | `<ul><li>Item</li></ul>` |

**Attributes** provide extra information:

- `class="dept-card"` — groups elements by style/purpose
- `id="engineering"` — unique identifier for one element
- `href="/page"` — link destination (on `<a>` tags)

Here is a small HTML snippet worth studying line by line — this is what `response.text` actually looks like:

```python
sample_html = """
<html>
<head><title>Sample Page</title></head>
<body>
    <h1 id="main-title">Welcome</h1>
    <p class="intro">This is a <strong>sample</strong> page.</p>
    <a href="/about" class="nav-link">About Us</a>
    <a href="/contact" class="nav-link">Contact</a>
</body>
</html>
"""
```

Everything a scraper needs is visible in the source: the `<h1>` carries an `id`, the paragraph and links carry `class` attributes, and each `<a>` tag stores its destination in `href`. Scraping is the craft of describing which of these tags you want and pulling out their text or attributes.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "If I can see it in my browser, `requests.get()` will return it." | Some sites build content with JavaScript *after* the page loads. `requests` only sees the initial HTML — the number-one reason a beginner's first real scrape comes back empty. |
| "Getting a response back means the request worked." | The server can respond with an error: 403 forbidden, 404 not found, 429 rate-limited, 500 server error. Always check `response.status_code` before parsing. |
| "If data is publicly visible, scraping it is automatically allowed." | Check `robots.txt`, respect rate limits, read the Terms of Service, and never scrape personal data without a lawful basis. |
| "Scraping is the standard way programs get web data." | Scraping is the fallback. When an API exists it is more reliable, faster, and explicitly permitted — Module 15 covers APIs for exactly this reason. |

---

## 14.2 Parsing HTML with BeautifulSoup

### The Dataset: Acme Corp Employee Directory

For this module, we scrape a fictional **company employee directory** for Acme Corporation. The directory has a **main page** listing departments with links and summaries, and **department pages** with employee tables (name, title, salary, years of service) for four departments: Engineering, Marketing, Finance, and Operations. We create these as Python strings — the same HTML that `requests.get()` would return from a real website.

```python
main_page_html = """
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
        <!-- ... identical dept-card divs for Marketing (id="mkt-card"),
             Finance (id="fin-card"), and Operations (id="ops-card") ... -->
    </div>

    <footer>
        <p class="updated">Last updated: 2025-09-01</p>
    </footer>
</body>
</html>
"""
```

Each department page follows the same shape — a heading, a description paragraph, an employee table, and a team-lead link:

```python
engineering_html = """
<html>
<head><title>Acme Corp - Engineering</title></head>
<body>
    <h1>Engineering Department</h1>
    <p class="dept-description">The Engineering team builds and maintains
    Acme's core software platform, data pipelines, and cloud infrastructure.</p>

    <table class="employee-table" id="eng-table">
        <thead>
            <tr><th>Name</th><th>Title</th><th>Salary</th><th>Years</th></tr>
        </thead>
        <tbody>
            <tr><td>Raj Patel</td><td>VP of Engineering</td><td>$185,000</td><td>12</td></tr>
            <tr><td>Lina Zhang</td><td>Senior Software Engineer</td><td>$155,000</td><td>8</td></tr>
            <!-- ... six more employee rows ... -->
        </tbody>
    </table>

    <p class="team-note">Team lead: <a href="mailto:raj.patel@acme.com">Raj Patel</a></p>
</body>
</html>
"""

# marketing_html, finance_html, and operations_html follow the same structure.
# A dictionary simulates the website: URL -> the HTML that requests.get()
# would return from that URL.
department_pages = {
    "/departments/engineering": engineering_html,
    "/departments/marketing": marketing_html,
    "/departments/finance": finance_html,
    "/departments/operations": operations_html,
}
```

### Creating a BeautifulSoup Object

BeautifulSoup turns an HTML string into a Python object you can search and navigate. You create a soup object by passing the HTML string and the parser to use:

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_string, "html.parser")
```

- `html_string` — the raw HTML (from `response.text` or a string)
- `"html.parser"` — Python's built-in HTML parser (no extra install)

Once you have a soup object, you can search for tags, extract text, and navigate the document tree.

!!! example "Worked Example: Creating a Soup Object"

    ```python
    from bs4 import BeautifulSoup

    # Parse the main directory page
    main_soup = BeautifulSoup(main_page_html, "html.parser")

    # The soup object represents the entire document
    print(f"Type: {type(main_soup)}")
    print(f"Title tag: {main_soup.title}")
    print(f"Title text: {main_soup.title.string}")
    ```

    **Output:**

    ```
    Type: <class 'bs4.BeautifulSoup'>
    Title tag: <title>Acme Corp - Employee Directory</title>
    Title text: Acme Corp - Employee Directory
    ```

    **Interpretation:** The soup object is the whole document, searchable from the top. `main_soup.title` returns the tag itself — angle brackets and all — while `.string` on that tag returns just the readable text. This tag-versus-text distinction runs through everything BeautifulSoup does.

    *Source: `computations/module14_examples.py` — `demo_soup_object()`*

### Finding Elements: `find()` and `find_all()`

These are the two most important methods in BeautifulSoup:

- **`soup.find(tag)`** — returns the **first** matching element
- **`soup.find_all(tag)`** — returns a **list** of all matching elements

You can search by:

- **Tag name:** `soup.find("h1")`
- **CSS class:** `soup.find("div", class_="dept-card")`
- **ID:** `soup.find("div", id="eng-card")`
- **Attributes dict:** `soup.find("span", attrs={"class": "headcount"})`

Note the underscore in `class_=` — `class` is a reserved word in Python, so BeautifulSoup uses `class_` instead.

!!! example "Worked Example: find() and find_all() in Action"

    ```python
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

    # Search by ID — find() returns the FIRST match. IDs are supposed to
    # be unique on a page, but real-world pages break that rule.
    eng_card = main_soup.find("div", id="eng-card")
    print("Found element with id='eng-card':")
    print(f"  Department: {eng_card.find('h2').get_text()}")
    print(f"  {eng_card.find('span', class_='headcount').get_text()}")
    ```

    **Output:**

    ```
    First <h2> tag: <h2><a href="/departments/engineering">Engineering</a></h2>
    Text inside:   Engineering

    All <h2> tags (4 found):
      - Engineering
      - Marketing
      - Finance
      - Operations

    Department cards found: 4

      Engineering: Builds and maintains our software platform
      Marketing: Drives brand awareness and customer acquisition
      Finance: Manages budgets, forecasting, and compliance
      Operations: Coordinates logistics and internal processes

    Found element with id='eng-card':
      Department: Engineering
      Headcount: 8
    ```

    **Interpretation:** `find()` stops at the first `<h2>` while `find_all()` returns all 4 as a list to loop over. Searching by `class_="dept-card"` isolates the 4 repeating card containers, and searching *within* each card scopes the inner `find()` calls to that card only — the pattern behind almost every list-of-items scrape. The ID search pinpoints one specific card and reads its headcount text directly.

    *Source: `computations/module14_examples.py` — `demo_find_and_find_all()`*

!!! question "Try It Yourself: Page Title and Last-Updated Date"

    Use `find()` or `find_all()` on `main_soup` to extract:

    1. The page title (text of the `<h1>` tag)
    2. The "Last updated" date from the footer paragraph

### Extracting Text

Once you have found an element, you need to extract its text content. BeautifulSoup gives you several ways:

| Method | Returns | Strips whitespace? |
|--------|---------|-------------------|
| `.get_text()` | All text inside the tag (including children) | No (by default) |
| `.get_text(strip=True)` | Same, with each text node stripped | Yes |
| `.get_text(" ", strip=True)` | Same, but joins nested text with a space | Yes |
| `.string` | Text if the tag has exactly one child; `None` if it has several | No |
| `.text` | Same as `.get_text()` | No |

**Rule of thumb:** Use `.get_text(" ", strip=True)` for most cases. The space argument tells BeautifulSoup to join the text of nested tags with a space, so word boundaries survive. Plain `.get_text(strip=True)` strips each piece of text separately and joins them with *nothing*, which can glue words together across nested tags — the demo below shows it happening.

!!! example "Worked Example: Text Extraction Methods Compared"

    ```python
    html = """
    <div class="employee">
        <span class="name">  Raj Patel  </span>
        <span class="title">VP of <strong>Engineering</strong></span>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    name_tag = soup.find("span", class_="name")
    title_tag = soup.find("span", class_="title")

    print("Extracting from <span class='name'>:")
    print(f"  .get_text()            = '{name_tag.get_text()}'")
    print(f"  .get_text(strip=True)  = '{name_tag.get_text(strip=True)}'")
    print(f"  .string                = '{name_tag.string}'")
    print()
    print("Extracting from <span class='title'> (has a nested <strong> tag):")
    print(f"  .get_text()                = '{title_tag.get_text()}'")
    print(f"  .get_text(strip=True)      = '{title_tag.get_text(strip=True)}'")
    print(f"  .get_text(' ', strip=True) = '{title_tag.get_text(' ', strip=True)}'")
    print(f"  .string                    = {title_tag.string}")
    ```

    **Output:**

    ```
    Extracting from <span class='name'>:
      .get_text()            = '  Raj Patel  '
      .get_text(strip=True)  = 'Raj Patel'
      .string                = '  Raj Patel  '

    Extracting from <span class='title'> (has a nested <strong> tag):
      .get_text()                = 'VP of Engineering'
      .get_text(strip=True)      = 'VP ofEngineering'
      .get_text(' ', strip=True) = 'VP of Engineering'
      .string                    = None
    ```

    **Interpretation:** Watch the strip trap: `.get_text(strip=True)` strips each text node separately and joins them with nothing, gluing "VP of " and "Engineering" into "VP ofEngineering". Passing a separator — `.get_text(" ", strip=True)` — keeps the word boundary. And `.string` returns `None` on the title span because that tag has more than one child (the text plus the `<strong>` tag); it only returns text when there is exactly one.

    *Source: `computations/module14_examples.py` — `demo_text_extraction()`*

### Extracting Attributes

HTML attributes (like `href`, `class`, `id`) are accessed like dictionary keys on the tag object:

```python
link = soup.find("a")
link["href"]         # the URL
link["class"]        # list of CSS classes
link.get("id")       # returns None if attribute missing (safe)
```

Use `tag["attr"]` when you know the attribute exists. Use `tag.get("attr")` when it might be missing — this avoids a `KeyError`.

!!! example "Worked Example: Extracting Links and Attributes"

    ```python
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
    ```

    **Output:**

    ```
    Found 4 links on the main page:

      Text: Engineering           href: /departments/engineering
      Text: Marketing             href: /departments/marketing
      Text: Finance               href: /departments/finance
      Text: Operations            href: /departments/operations

    Department card IDs and their links:

      id=eng-card    name=Engineering      url=/departments/engineering
      id=mkt-card    name=Marketing        url=/departments/marketing
      id=fin-card    name=Finance          url=/departments/finance
      id=ops-card    name=Operations       url=/departments/operations
    ```

    **Interpretation:** Each link yields two separate things: its visible text via `get_text()` and its destination via `link["href"]`. The card loop combines `card.get("id")` (safe even if an id were missing) with a scoped `find()` for the link inside. Collecting URLs like this is step one of every multi-page scrape — the hrefs harvested here drive the multi-page workflow later in the module.

    *Source: `computations/module14_examples.py` — `demo_extract_attributes()`*

!!! question "Try It Yourself: Department Headcounts"

    Extract the headcount from each department card on the main page. Build a dictionary mapping department name to headcount number.

    Hint: The headcount text looks like `"Headcount: 8"` — you will need to split the string and convert to an integer.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "I can write `soup.find('div', class='dept-card')`." | `class` is a reserved word in Python. BeautifulSoup uses `class_` (with a trailing underscore) for class searches. |
| "`.string` always returns the tag's text." | `.string` returns `None` whenever a tag has more than one child. Use `.get_text()` when nesting is possible. |
| "`.get_text(strip=True)` just trims the ends." | It strips each text node separately and joins them with *nothing*, which can glue words together across nested tags. Use `.get_text(" ", strip=True)` to keep word boundaries. |
| "`find()` by id returns *the* element with that id." | It returns the *first* match. IDs are supposed to be unique, but real-world pages break that rule. |
| "`tag['attr']` is always safe." | A missing attribute raises `KeyError`. Use `tag.get("attr")`, which returns `None`, when the attribute might not exist. |

---

## 14.3 Tables, CSS Selectors, and Tree Navigation

### Working with Tables

HTML tables are the most common structure you will scrape for data analysis. The pattern is always the same:

1. Find the `<table>` element
2. Find all `<tr>` (table row) elements inside it
3. For each row, find all `<td>` (table data) cells
4. Extract the text from each cell

```
<table>
    <thead>
        <tr><th>Name</th><th>Title</th></tr>     ← header row
    </thead>
    <tbody>
        <tr><td>Raj</td><td>VP</td></tr>         ← data rows
        <tr><td>Lina</td><td>Engineer</td></tr>
    </tbody>
</table>
```

The header row uses `<th>` tags. Data rows use `<td>` tags.

!!! example "Worked Example: The Table Scraping Pattern"

    ```python
    # Parse the Engineering department page
    eng_soup = BeautifulSoup(engineering_html, "html.parser")

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
    ```

    **Output:**

    ```
    Found table with id: eng-table
    Column headers: ['Name', 'Title', 'Salary', 'Years']
    Data rows found: 8

    Employee data:
      ['Raj Patel', 'VP of Engineering', '$185,000', '12']
      ['Lina Zhang', 'Senior Software Engineer', '$155,000', '8']
      ['Marcus Johnson', 'Senior Software Engineer', '$150,000', '7']
      ['Sofia Rivera', 'Data Engineer', '$140,000', '5']
      ["James O'Brien", 'Software Engineer', '$120,000', '3']
      ['Aisha Kwame', 'Software Engineer', '$115,000', '2']
      ['Noah Fischer', 'DevOps Engineer', '$135,000', '4']
      ['Priya Sharma', 'Junior Developer', '$85,000', '1']
    ```

    **Interpretation:** Four steps turn markup into rows: locate the table, read the `<th>` headers, collect the `<tr>` rows, and pull the `<td>` text from each. All 8 employees come out as lists of strings — note that `'$185,000'` and `'12'` are *text*, not numbers. Converting them is the cleaning step covered in the next section.

    *Source: `computations/module14_examples.py` — `demo_table_scraping_pattern()`*

### CSS Selectors: `select()` and `select_one()`

CSS selectors are an alternative to `find()` / `find_all()`. They use the same syntax that web developers use in CSS stylesheets, which makes them compact and expressive.

| Selector | Meaning | Example |
|----------|---------|---------|
| `tag` | Elements by tag name | `"h1"` |
| `.class` | Elements by class | `".dept-card"` |
| `#id` | Element by ID | `"#eng-card"` |
| `tag.class` | Tag with specific class | `"div.dept-card"` |
| `parent child` | Descendants | `"table td"` |
| `parent > child` | Direct children only | `"tbody > tr"` |
| `tag[attr]` | Tag with attribute | `"a[href]"` |

- **`soup.select("selector")`** — returns all matches (like `find_all`)
- **`soup.select_one("selector")`** — returns first match (like `find`)

!!! example "Worked Example: CSS Selectors in Action"

    ```python
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
    eng_soup = BeautifulSoup(engineering_html, "html.parser")

    # Select all <td> cells inside the employee table
    all_cells = eng_soup.select("table.employee-table tbody td")
    print(f"\nTotal <td> cells: {len(all_cells)}")

    # Select all rows, then extract cells per row
    rows = eng_soup.select("table.employee-table tbody > tr")
    print("\nFirst 3 employees (via CSS selectors):")
    for row in rows[:3]:
        cells = [td.get_text(strip=True) for td in row.select("td")]
        print(f"  {cells}")
    ```

    **Output:**

    ```
    div.dept-card: 4 matches
    #eng-card: Engineering

    Links inside dept-cards:
      Engineering -> /departments/engineering
      Marketing -> /departments/marketing
      Finance -> /departments/finance
      Operations -> /departments/operations

    Total <td> cells: 32

    First 3 employees (via CSS selectors):
      ['Raj Patel', 'VP of Engineering', '$185,000', '12']
      ['Lina Zhang', 'Senior Software Engineer', '$155,000', '8']
      ['Marcus Johnson', 'Senior Software Engineer', '$150,000', '7']
    ```

    **Interpretation:** One selector string replaces a chain of `find()` calls: `"div.dept-card a"` reads as "links anywhere inside dept-cards" and returns all 4 in a single call, while `"table.employee-table tbody td"` grabs all 32 data cells at once. The descendant combinators (`parent child` and `parent > child`) do the scoping that nested loops did in the previous example — same results, more compact code.

    *Source: `computations/module14_examples.py` — `demo_css_selectors()`*

!!! question "Try It Yourself: Department Summaries via Selectors"

    Use CSS selectors to extract all department summary paragraphs (`<p class="dept-summary">`) from the main page. Print each department name alongside its summary.

    Hint: You can combine selectors to target elements within a container, e.g., `"div.dept-card h2"` selects `<h2>` inside `.dept-card`.

### Navigating the Tree

BeautifulSoup represents HTML as a tree. Every element has relationships with other elements:

- **`.parent`** — the element that contains this one
- **`.children`** — iterator over direct child **nodes**, including the whitespace text *between* tags (which is why the code below filters on `.name` to keep only real elements)
- **`.next_sibling`** / **`.previous_sibling`** — the next/previous *node* at the same level, which is often a whitespace string rather than a tag; use **`.find_next_sibling()`** / **`.find_previous_sibling()`** when you want the next/previous *element*
- **`.find_next(tag)`** — the next occurrence of a tag after this one
- **`.find_parent(tag)`** — walk up the tree to find an ancestor

Tree navigation is useful when the element you want is not directly searchable but is near an element that is.

!!! example "Worked Example: Navigating the Tree"

    ```python
    eng_soup = BeautifulSoup(engineering_html, "html.parser")

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
    ```

    **Output:**

    ```
    Table's parent tag: <body>
    Table's direct children: ['thead', 'tbody']

    First <p> after <h1>: The Engineering team builds and maintains
        Acme's core so...
    Parent row of first <td>: ['Raj Patel', 'VP of Engineering', '$185,000', '12']
    ```

    **Interpretation:** The tree runs both ways: `.parent` and `find_parent()` climb upward (from a lone `<td>` back to its full row), while `find_next()` moves forward through the document (from the heading to the description paragraph that follows it). Notice the description text keeps the internal line break from the source HTML — scraped text preserves whatever whitespace the author typed, another reason cleaning comes next.

    *Source: `computations/module14_examples.py` — `demo_tree_navigation()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "CSS selectors and `find_all()` are different systems that find different things." | They locate the same elements. `select("div.dept-card a")` equals a nested `find_all()` loop — choose whichever reads more clearly. |
| "`.next_sibling` gives me the next tag." | It gives the next *node*, which is often the whitespace text between tags. Use `.find_next_sibling()` to get the next element. |
| "`.children` yields only the child tags." | It also yields whitespace text nodes between tags. Filter on `child.name is not None` to keep only real elements. |
| "`select_one()` returns a list like `select()`." | `select_one()` returns a single tag (or `None`), mirroring `find()`; `select()` returns a list, mirroring `find_all()`. |

---

## 14.4 From Scraped HTML to Polars DataFrames

Now we combine everything: parse HTML, extract table data, and build a Polars DataFrame. This is the core skill of web scraping for data analysis.

**The pattern:**

1. Parse the HTML with BeautifulSoup
2. Find the table and extract headers
3. Loop over rows, extract cell text into a list of dictionaries
4. Pass the list of dictionaries to `pl.DataFrame()`

### Building and Cleaning a Scraped DataFrame

One more thing before the code: everything scraped from HTML arrives as *text*, so a value like `"$185,000"` cannot be averaged or summed. After building the DataFrame, a cleaning step strips the formatting characters with a regular expression (Module 5) and casts the columns to integer types.

!!! example "Worked Example: HTML Table to Polars DataFrame"

    ```python
    import polars as pl

    # Parse one department page into a Polars DataFrame
    soup = BeautifulSoup(engineering_html, "html.parser")
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
    ```

    **Output:**

    ```
    Engineering department as a Polars DataFrame:
    shape: (8, 4)
    ┌────────────────┬──────────────────────────┬──────────┬───────┐
    │ Name           ┆ Title                    ┆ Salary   ┆ Years │
    │ ---            ┆ ---                      ┆ ---      ┆ ---   │
    │ str            ┆ str                      ┆ str      ┆ str   │
    ╞════════════════╪══════════════════════════╪══════════╪═══════╡
    │ Raj Patel      ┆ VP of Engineering        ┆ $185,000 ┆ 12    │
    │ Lina Zhang     ┆ Senior Software Engineer ┆ $155,000 ┆ 8     │
    │ Marcus Johnson ┆ Senior Software Engineer ┆ $150,000 ┆ 7     │
    │ Sofia Rivera   ┆ Data Engineer            ┆ $140,000 ┆ 5     │
    │ James O'Brien  ┆ Software Engineer        ┆ $120,000 ┆ 3     │
    │ Aisha Kwame    ┆ Software Engineer        ┆ $115,000 ┆ 2     │
    │ Noah Fischer   ┆ DevOps Engineer          ┆ $135,000 ┆ 4     │
    │ Priya Sharma   ┆ Junior Developer         ┆ $85,000  ┆ 1     │
    └────────────────┴──────────────────────────┴──────────┴───────┘

    Cleaned DataFrame (salary as integer, years as integer):
    shape: (8, 4)
    ┌────────────────┬──────────────────────────┬────────┬───────┐
    │ Name           ┆ Title                    ┆ Salary ┆ Years │
    │ ---            ┆ ---                      ┆ ---    ┆ ---   │
    │ str            ┆ str                      ┆ i64    ┆ i64   │
    ╞════════════════╪══════════════════════════╪════════╪═══════╡
    │ Raj Patel      ┆ VP of Engineering        ┆ 185000 ┆ 12    │
    │ Lina Zhang     ┆ Senior Software Engineer ┆ 155000 ┆ 8     │
    │ Marcus Johnson ┆ Senior Software Engineer ┆ 150000 ┆ 7     │
    │ Sofia Rivera   ┆ Data Engineer            ┆ 140000 ┆ 5     │
    │ James O'Brien  ┆ Software Engineer        ┆ 120000 ┆ 3     │
    │ Aisha Kwame    ┆ Software Engineer        ┆ 115000 ┆ 2     │
    │ Noah Fischer   ┆ DevOps Engineer          ┆ 135000 ┆ 4     │
    │ Priya Sharma   ┆ Junior Developer         ┆ 85000  ┆ 1     │
    └────────────────┴──────────────────────────┴────────┴───────┘
    ```

    **Interpretation:** `dict(zip(headers, cells))` pairs each header with its cell value, and the resulting list of dictionaries drops straight into `pl.DataFrame()` — but look at the first dtype row: every column is `str`, including Salary and Years. The cleaning pass fixes that: the regex `[\$,]` matches dollar signs and commas, `replace_all` removes them, and `.cast(pl.Int64)` converts the survivors, so `$185,000` becomes `185000` with dtype `i64`. Scrape, then clean, is a two-step habit worth internalizing.

    *Source: `computations/module14_examples.py` — `demo_table_to_dataframe()`*

### Scraping Multiple Pages

Real scraping workflows involve multiple pages. The pattern is:

1. Scrape the index/listing page to get links
2. Visit each link and scrape its data
3. Combine all data into one DataFrame

We simulate this by scraping the main page for department links, then scraping each department page. In a real scenario, step 2 would use `requests.get(url)` for each link — here the `department_pages` dictionary plays the role of the website.

!!! example "Worked Example: A Multi-Page Scraping Workflow"

    ```python
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
        html = department_pages[dept_url]
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
    ```

    **Output:**

    ```
    Department links found:
      Engineering -> /departments/engineering
      Marketing -> /departments/marketing
      Finance -> /departments/finance
      Operations -> /departments/operations

    Combined DataFrame: 25 employees from 4 departments
    Cleaned employee directory: 25 rows, 5 columns
    Departments: ['Engineering', 'Marketing', 'Finance', 'Operations']
    Salary range: $70,000 – $195,000
    shape: (5, 5)
    ┌────────────────┬──────────────────────────┬────────┬───────┬─────────────┐
    │ Name           ┆ Title                    ┆ Salary ┆ Years ┆ Department  │
    │ ---            ┆ ---                      ┆ ---    ┆ ---   ┆ ---         │
    │ str            ┆ str                      ┆ i64    ┆ i64   ┆ str         │
    ╞════════════════╪══════════════════════════╪════════╪═══════╪═════════════╡
    │ Raj Patel      ┆ VP of Engineering        ┆ 185000 ┆ 12    ┆ Engineering │
    │ Lina Zhang     ┆ Senior Software Engineer ┆ 155000 ┆ 8     ┆ Engineering │
    │ Marcus Johnson ┆ Senior Software Engineer ┆ 150000 ┆ 7     ┆ Engineering │
    │ Sofia Rivera   ┆ Data Engineer            ┆ 140000 ┆ 5     ┆ Engineering │
    │ James O'Brien  ┆ Software Engineer        ┆ 120000 ┆ 3     ┆ Engineering │
    └────────────────┴──────────────────────────┴────────┴───────┴─────────────┘
    ```

    **Interpretation:** One index page and 4 department pages become a single tidy dataset: 25 employees, 5 columns, salaries spanning $70,000 – $195,000. The added `Department` column records which page each row came from — without it, the combined rows would lose their origin. The first 5 rows previewed are all Engineering because pages were scraped in link order.

    *Source: `computations/module14_examples.py` — `demo_multi_page_scrape()`*

!!! question "Try It Yourself: Analyzing the Employee Directory"

    Using the `employees` DataFrame, answer these questions with Polars:

    1. Which department has the highest average salary?
    2. Who are the top 3 highest-paid employees across all departments?

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "Once it is in a DataFrame, the data is ready for analysis." | Every value scraped from HTML is a string — `"$185,000"` and `"12"` included. Strip formatting and cast dtypes before any math. |
| "Each page needs its own custom parsing code." | Pages that share a template share a parse. Write the extraction once, loop it over the URLs, and tag each row with its source page. |
| "Combining pages is a separate, hard step." | If every page yields dictionaries with the same keys, one growing list feeds a single `pl.DataFrame()` call — the combining is free. |

---

## 14.5 Robust, Reusable Scraping Workflows

### Real-World Considerations

When scraping live websites (not local HTML strings), keep these practices in mind:

**1. Rate limiting.** Add a delay between requests to avoid overwhelming the server:

```python
import time

for url in urls:
    response = requests.get(url)
    # process the page...
    time.sleep(1)  # wait 1 second between requests
```

**2. Error handling.** Check the status code before parsing:

```python
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    # parse the page...
else:
    print(f"Failed to fetch {url}: status {response.status_code}")
```

**3. User-Agent headers.** Some sites block requests that do not identify themselves. Set a descriptive user-agent header:

```python
headers = {"User-Agent": "MIS501-CourseProject/1.0 (student@university.edu)"}
response = requests.get(url, headers=headers)
```

**4. Checking `robots.txt`.** Before scraping any site, check `https://example.com/robots.txt` to see what paths are allowed or disallowed for automated access.

**5. Handling missing data.** Real web pages are messy. Always use `.get()` for attributes and check for `None` before extracting text:

```python
tag = soup.find("span", class_="price")
price = tag.get_text(strip=True) if tag else "N/A"
```

The `fetch_page()` helper below combines the first three practices — headers, error handling, and rate limiting — into one function you can reuse in any project.

!!! example "Worked Example: A Robust Fetch Function"

    ```python
    import time

    def fetch_page(url, delay=1.0):
        """Fetch a page with error handling and rate limiting."""
        headers = {
            "User-Agent": "MIS501-CourseProject/1.0 (student@university.edu)"
        }
        try:
            response = requests.get(
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

    # Test with httpbin
    html = fetch_page("https://httpbin.org/html")
    if html:
        print(f"Successfully fetched page: {len(html)} characters")
    else:
        print("Could not fetch page (network may be unavailable)")
    ```

    **Output:**

    ```
    Successfully fetched page: 765 characters
    ```

    **Interpretation:** The function identifies itself with a descriptive user-agent, refuses to hang forever thanks to the timeout, turns bad status codes and network exceptions into a `None` return instead of a crash, and — because the delay sits in a `finally` block — pauses after *every* request, success or failure. Callers just check whether they got HTML back; here they did, 765 characters of it.

    *Note: output produced from an embedded sample page so results are reproducible offline.*

    *Source: `computations/module14_examples.py` — `demo_fetch_page_function()`*

### A Reusable Table Scraper

Since scraping HTML tables is so common, it pays to write a reusable function that handles the entire process: find the table, extract headers, extract rows, and return a Polars DataFrame. This is the kind of utility you would keep in your own library and reuse across projects.

**Watch out for `<tbody>`:** every browser automatically inserts a `<tbody>` element into a table, so your browser's inspector *always* shows one — but `<tbody>` is optional in the actual HTML source, and Python's `html.parser` will not add it for you. That is why the function below loops over `find_all("tr")` instead of the tempting `select("tbody > tr")`: the selector version would silently return an empty DataFrame on any table whose source happens to omit `<tbody>`.

!!! example "Worked Example: A Reusable scrape_table() Function"

    ```python
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
    dept_links = main_soup.select("div.dept-card a")

    all_dfs = []
    print()
    for link in dept_links:
        name = link.get_text(strip=True)
        url = link["href"]
        html = department_pages[url]

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
    ```

    **Output:**

    ```
    Testing scrape_table() on a minimal table (no <tbody> in source):
    shape: (1, 2)
    ┌─────┬─────┐
    │ A   ┆ B   │
    │ --- ┆ --- │
    │ str ┆ str │
    ╞═════╪═════╡
    │ 1   ┆ 2   │
    └─────┴─────┘

      Engineering: 8 employees
      Marketing: 6 employees
      Finance: 5 employees
      Operations: 6 employees

    Combined: 25 employees
    ```

    **Interpretation:** The minimal test proves the `<tbody>` defense works — the source omits `<tbody>` entirely, yet the function still returns the data row because it loops over every `<tr>` and lets the length guard drop the header row. Applied to the directory, each department page collapses to one `scrape_table()` call, `extra_columns` tags rows with their department, and `pl.concat()` stacks all 25 employees into one DataFrame.

    *Source: `computations/module14_examples.py` — `demo_scrape_table_function()`*

### Capstone: Complete Company Directory Analysis

The capstone brings together everything from this module in a complete scraping-to-analysis workflow:

1. **Scrape** the main page for department metadata
2. **Scrape** each department page for employee data
3. **Clean** the data (convert salary strings, parse years)
4. **Analyze** with Polars
5. **Visualize** with Plotly Express

**Business question:** *How does compensation vary across departments and seniority levels at Acme Corporation?*

!!! example "Worked Example: Capstone — Scrape and Clean the Directory"

    ```python
    # --- Step 1: Scrape department metadata from the main page ---
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

    dept_metadata = pl.DataFrame(dept_info)
    print("Department metadata:")
    print(dept_metadata)

    # --- Step 2: Scrape all employee tables (plus each team lead's email) ---
    all_employees = []
    for dept in dept_info:
        html = department_pages[dept["URL"]]
        soup = BeautifulSoup(html, "html.parser")

        # Grab the team lead email from the mailto: link
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
    print(f"\nRaw scraped data: {capstone_raw.shape[0]} rows, "
          f"{capstone_raw.shape[1]} columns")

    # --- Step 3: Clean the data and add a seniority level ---
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

    print(f"Cleaned DataFrame: {capstone_df.shape}")
    print(f"Columns: {capstone_df.columns}")
    print(capstone_df.select("Name", "Salary", "Years", "Seniority").head(4))
    ```

    **Output:**

    ```
    Department metadata:
    shape: (4, 4)
    ┌─────────────┬─────────────────────────────────┬──────────────────────────┬───────────┐
    │ Department  ┆ Description                     ┆ URL                      ┆ Headcount │
    │ ---         ┆ ---                             ┆ ---                      ┆ ---       │
    │ str         ┆ str                             ┆ str                      ┆ i64       │
    ╞═════════════╪═════════════════════════════════╪══════════════════════════╪═══════════╡
    │ Engineering ┆ Builds and maintains our softw… ┆ /departments/engineering ┆ 8         │
    │ Marketing   ┆ Drives brand awareness and cus… ┆ /departments/marketing   ┆ 6         │
    │ Finance     ┆ Manages budgets, forecasting, … ┆ /departments/finance     ┆ 5         │
    │ Operations  ┆ Coordinates logistics and inte… ┆ /departments/operations  ┆ 6         │
    └─────────────┴─────────────────────────────────┴──────────────────────────┴───────────┘

    Raw scraped data: 25 rows, 6 columns
    Cleaned DataFrame: (25, 7)
    Columns: ['Name', 'Title', 'Salary', 'Years', 'Department', 'Dept_Lead_Email', 'Seniority']
    shape: (4, 4)
    ┌────────────────┬────────┬───────┬─────────────────┐
    │ Name           ┆ Salary ┆ Years ┆ Seniority       │
    │ ---            ┆ ---    ┆ ---   ┆ ---             │
    │ str            ┆ i64    ┆ i64   ┆ str             │
    ╞════════════════╪════════╪═══════╪═════════════════╡
    │ Raj Patel      ┆ 185000 ┆ 12    ┆ Senior (10+ yr) │
    │ Lina Zhang     ┆ 155000 ┆ 8     ┆ Mid (5-9 yr)    │
    │ Marcus Johnson ┆ 150000 ┆ 7     ┆ Mid (5-9 yr)    │
    │ Sofia Rivera   ┆ 140000 ┆ 5     ┆ Mid (5-9 yr)    │
    └────────────────┴────────┴───────┴─────────────────┘
    ```

    **Interpretation:** The scrape gathers three different kinds of data at once: card metadata (including a headcount parsed out of text like `Headcount: 8`), table rows, and an email address pulled from a `mailto:` link's `href`. Cleaning then does double duty — casting Salary and Years to integers *and* deriving a brand-new `Seniority` column with `pl.when/then/otherwise`. The result is a 25-row, 7-column analysis-ready dataset that never existed as a table anywhere on the "website."

    *Source: `computations/module14_examples.py` — `demo_capstone_scrape_and_clean()`*

!!! example "Worked Example: Capstone — Compensation Analysis"

    ```python
    import plotly.express as px

    # --- Step 4: Analyze ---
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

    # --- Step 5: Visualize (bar chart of the department averages) ---
    salary_fig = px.bar(
        dept_summary.to_pandas(),
        x="Department",
        y="Avg_Salary",
        color="Department",
        title="Average Salary by Department",
        labels={"Avg_Salary": "Average Salary ($)"},
        text="Avg_Salary",
    )
    # A box plot of Salary by Department and a Salary-vs-Years scatter
    # follow the same px pattern to complete the dashboard.

    print(
        f"\nSummary: {capstone_df.shape[0]} employees across "
        f"{capstone_df['Department'].n_unique()} departments | "
        f"Salary range: ${capstone_df['Salary'].min():,} – "
        f"${capstone_df['Salary'].max():,} | "
        f"Average: ${capstone_df['Salary'].mean():,.0f}"
    )
    ```

    **Output:**

    ```
    Department Compensation Summary:
    shape: (4, 7)
    ┌─────────────┬───────────┬────────────┬───────────────┬────────────┬────────────┬───────────┐
    │ Department  ┆ Headcount ┆ Avg_Salary ┆ Median_Salary ┆ Min_Salary ┆ Max_Salary ┆ Avg_Years │
    │ ---         ┆ ---       ┆ ---        ┆ ---           ┆ ---        ┆ ---        ┆ ---       │
    │ str         ┆ u32       ┆ i64        ┆ f64           ┆ i64        ┆ i64        ┆ f64       │
    ╞═════════════╪═══════════╪════════════╪═══════════════╪════════════╪════════════╪═══════════╡
    │ Engineering ┆ 8         ┆ 135625     ┆ 137500.0      ┆ 85000      ┆ 185000     ┆ 5.2       │
    │ Finance     ┆ 5         ┆ 124000     ┆ 110000.0      ┆ 95000      ┆ 195000     ┆ 6.6       │
    │ Marketing   ┆ 6         ┆ 109500     ┆ 100000.0      ┆ 72000      ┆ 175000     ┆ 4.3       │
    │ Operations  ┆ 6         ┆ 104167     ┆ 94000.0       ┆ 70000      ┆ 170000     ┆ 5.2       │
    └─────────────┴───────────┴────────────┴───────────────┴────────────┴────────────┴───────────┘

    Compensation by Seniority Level:
    shape: (4, 5)
    ┌─────────────────┬───────┬────────────┬────────────┬────────────┐
    │ Seniority       ┆ Count ┆ Avg_Salary ┆ Min_Salary ┆ Max_Salary │
    │ ---             ┆ ---   ┆ ---        ┆ ---        ┆ ---        │
    │ str             ┆ u32   ┆ i64        ┆ i64        ┆ i64        │
    ╞═════════════════╪═══════╪════════════╪════════════╪════════════╡
    │ Senior (10+ yr) ┆ 4     ┆ 181250     ┆ 170000     ┆ 195000     │
    │ Mid (5-9 yr)    ┆ 8     ┆ 123125     ┆ 90000      ┆ 155000     │
    │ Junior (2-4 yr) ┆ 10    ┆ 105000     ┆ 82000      ┆ 135000     │
    │ Entry (<2 yr)   ┆ 3     ┆ 75667      ┆ 70000      ┆ 85000      │
    └─────────────────┴───────┴────────────┴────────────┴────────────┘

    Summary: 25 employees across 4 departments | Salary range: $70,000 – $195,000 | Average: $119,480
    ```

    **Interpretation:** The business question gets its answer: Engineering leads on average pay at $135,625, while Operations trails at $104,167 — and the seniority view shows the steeper driver, with the Senior tier averaging $181,250 against $75,667 for the Entry tier. These summary tables are exactly what feed the Plotly Express dashboard (bar, box, and scatter), whose headline reads 25 employees, 4 departments, average salary $119,480 — an analysis that began as raw HTML tags.

    *Source: `computations/module14_examples.py` — `demo_capstone_analysis()`*

!!! question "Try It Yourself: Capstone Challenge — Salary Ranges"

    Extend the analysis: Which department has the widest salary gap between its highest- and lowest-paid employees? Create a bar chart showing the salary range (max - min) for each department.

    Hint: You already have `capstone_df`. Use `.group_by()` and `.agg()` to compute the range, then plot with Plotly Express.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "My browser's inspector shows `<tbody>`, so I can rely on `select('tbody > tr')`." | Browsers insert `<tbody>` automatically; the actual source may omit it, and `html.parser` will not add it. Loop over `find_all("tr")` and skip header rows instead. |
| "Delays between requests are optional politeness." | Hammering a server gets you rate-limited or blocked outright — and can degrade the site for everyone. `time.sleep()` between requests is part of a correct scraper. |
| "Once my scraper works, it will keep working." | Scrapers depend on page structure. A site redesign silently breaks selectors, which is why robust code checks for `None`, validates row lengths, and warns instead of crashing. |
| "Anonymous requests are fine — nobody needs to know it's me." | Many sites block unidentified clients. A descriptive `User-Agent` with contact information is both more effective and more honest. |

---

## Reflection Questions

1. A dataset you need exists on a public website and also through the site's REST API. What factors — technical, legal, and ethical — should push you toward the API, and is there any scenario where scraping the pages would still be reasonable?
2. `find()`/`find_all()` and `select()`/`select_one()` can locate the same elements. When would you prefer one style over the other, and how does the structure of the page influence that choice?
3. Every value scraped from HTML arrives as a string. Describe what would go wrong, step by step, if you skipped the cleaning stage and tried to compute an average salary directly from the scraped table.
4. You run `requests.get()` on a page, and BeautifulSoup finds none of the product data you can plainly see in your browser. What is the most likely explanation, and how would you confirm it?
5. Your scraper works today, but the target site redesigns its pages next quarter. Which parts of a scraping pipeline are most fragile to redesign, and what defensive habits from this module limit the damage?
6. The multi-page workflow in this module knew all four department URLs up front. How would the pattern change for a site with a "next page" button, and where would rate limiting fit into that loop?

---

## Your Assignment

The Module 14 assignment is worth **100 points plus a 10-point bonus**. You complete it in a **marimo notebook (`.py` file)** and submit the file to **Brightspace**. A final reflection section is not graded separately — it counts toward participation.

One design note: every task provides its web page **inline as an HTML string** in a setup cell (do not modify those cells), so you practice the full parsing toolkit without needing a network connection. In a real pipeline, `requests.get(url).text` would hand you the same strings. Parse with `BeautifulSoup(html_string, "html.parser")` throughout, and remember the underscore-prefix convention for cell-scoped variables.

**Task 1 — Basic Parsing: Extract Text from Tags (10 points).** A local restaurant's page carries its name, cuisine type, and description. You parse the HTML, extract the name from the `<h1>`, the cuisine from a classed `<span>`, and the description from a classed `<p>` using `.get_text(strip=True)`, print them in a specified format, and store the name in a named variable. Concepts: §14.2 (Creating a BeautifulSoup Object, Finding Elements, Extracting Text).

**Task 2 — Extract Attributes: Links and Their URLs (15 points).** A public library page lists recommended reading lists as links, each with an `href` and a `data-category` attribute. You find all `<a>` tags inside a specific `<div>`, extract each link's text, URL, and category, build a list of dictionaries, and convert it to a Polars DataFrame. Concepts: §14.2 (Extracting Attributes) and §14.4 (Building a DataFrame from Scraped Data).

**Task 3 — Parse an HTML Table into a Polars DataFrame (15 points).** A real estate agency lists properties in a table you locate by its `id`. You extract the column headers from the `<th>` tags, loop over the `<tbody>` rows, zip headers with cell values into dictionaries, and load the result into a Polars DataFrame. Concepts: §14.3 (Working with Tables) and §14.4.

**Task 4 — CSS Selectors and Class-Based Selection (15 points).** A university course catalog presents each course as a classed card `<div>` carrying a `data-department` attribute and classed `<span>` elements for the code, title, credits, and instructor. Using `select()` rather than `find_all()`, you extract all five fields per card into a Polars DataFrame. Concepts: §14.3 (CSS Selectors) with the attribute techniques of §14.2.

**Task 5 — Multi-Page Scraping: Combine Data from Multiple HTML Pages (20 points).** A sports league publishes each week's game results on a separate page, provided as a dictionary mapping week labels to HTML strings. You loop over the pages, parse each results table, add a `Week` column identifying the source page, and combine all rows into one Polars DataFrame. Concepts: §14.4 (Scraping Multiple Pages).

**Task 6 — Full Pipeline: Parse, Clean, Analyze, Visualize (25 points).** A movie review site presents reviews as classed cards with a genre attribute, a reviewer, and a numeric rating. Step one: parse every card, convert ratings to integers, and build the DataFrame. Step two: aggregate the average rating per movie (grouped by title and genre, rounded and sorted), then present the result as a Plotly Express bar chart, converting with `.to_pandas()` first. Concepts: §14.4 end to end plus the capstone pattern of §14.5; charting from Module 11.

**Task 7 — Creative Scraping Analysis, Bonus (10 points).** A product catalog page lists products with categories, prices, and customer ratings. You design your own analysis: parse everything into a Polars DataFrame, clean the price and rating strings into floats, perform at least one aggregation, build at least one Plotly Express chart, and explain your question and findings in a `mo.md()` cell. Concepts: §14.4–§14.5.

Before submitting, confirm the notebook runs top to bottom without errors and that cell-scoped variables carry the underscore prefix the instructions describe.

---

## Chapter Summary

Web scraping extracts data from web pages programmatically — the right tool when the data you need is public, no API exists, and copying by hand would not scale. The mechanics mirror what a browser does: `requests.get(url)` sends an HTTP GET request, the response's `.text` holds the raw HTML, and a status code (200 for success) reports how the conversation went. Scraping is also a practice with rules: check `robots.txt`, respect rate limits with deliberate delays, read the Terms of Service, identify yourself with a User-Agent header, and reach for an API whenever one is available.

BeautifulSoup turns an HTML string into a searchable tree. `find()` and `find_all()` locate elements by tag, class (`class_=`), or id; `select()` and `select_one()` do the same with compact CSS selectors; and tree relationships (`.parent`, `find_next()`, `find_parent()`) reach elements that are hard to search for directly. Extraction then splits into two operations — `.get_text(" ", strip=True)` for readable text and `tag["attr"]` / `tag.get("attr")` for attributes like `href` — with a handful of traps worth remembering: `.string` goes `None` on nested tags, `strip=True` can glue words together, and `<tbody>` may exist only in your browser's rendering.

The destination is always a DataFrame. The table pattern — find the table, read `<th>` headers, loop `<tr>` rows, zip into dictionaries, call `pl.DataFrame()` — generalizes from one page to many: harvest links from an index page, apply the same parse to each linked page, tag rows with their source, and concatenate. Because scraped values are strings, a cleaning stage (`str.replace_all` plus `cast`) converts formatted text like a salary with dollar signs and commas into integers ready for `group_by` summaries and Plotly Express charts. The capstone ran that entire arc — scrape, clean, analyze, visualize — and turned a fictional company's web pages into a compensation analysis no single page ever contained.

---

## What's Next

Module 15 covers **REST APIs & Data Acquisition** — the structured, reliable way to request data from web services. APIs return clean JSON instead of HTML, so `.json()` replaces the entire BeautifulSoup parsing step, and the provider explicitly permits programmatic access. When an API is available, it is always preferable to scraping — and after this module you will appreciate exactly why. The `requests` skills, status-code checks, rate-limiting habits, and fetch-to-DataFrame pipeline you built here carry over directly.
