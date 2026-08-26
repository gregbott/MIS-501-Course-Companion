# Module 5: Strings & Regular Expressions

## Introduction

Business data is full of text: customer names, addresses, product descriptions, invoice numbers, email addresses, phone numbers, dates in a half-dozen formats. Before any of it can be analyzed, it usually needs to be cleaned, split apart, or transformed into a consistent shape — the name typed as `"   alice JOHNSON  "` and the phone stored as `"512.555.5678"` have to become presentable before they reach a report or a database. This module covers Python's two toolkits for that work. String indexing, slicing, and methods handle predictable transformations, and the `re` module's regular expressions describe *patterns* — "two digits, a slash, two digits, a slash, four digits" — so you can find, validate, extract, and replace text whose exact content varies. Combined with the functions you wrote in Module 4, these tools turn messy exports and free-form documents into structured data you can compute with.

---

## Learning Objectives

By the end of this module, you should be able to:

1. **Use** string indexing and slicing to extract parts of text
2. **Apply** common string methods (`split`, `join`, `strip`, `replace`, `find`, `upper`, `lower`)
3. **Explain** what regular expressions are and when to use them
4. **Use** the `re` module to search, match, find, and replace text patterns
5. **Build** patterns with character classes, quantifiers, and groups
6. **Write** functions that clean and transform messy text data

---

## 5.1 String Indexing and Slicing

A string is a **sequence** of characters. Each character occupies a numbered position called an **index**, and the numbering starts at 0, not 1:

```
String:  I  N  V  -  2  0  2  4  -  0  0  1
Index:   0  1  2  3  4  5  6  7  8  9  10 11
```

### Indexing Individual Characters

You access a single character with square brackets: `text[index]`. **Negative indexing** counts from the end: `text[-1]` is the last character, `text[-2]` is second to last, and so on — handy when you do not know how long the string is.

!!! example "Worked Example: Indexing an Invoice ID"

    ```python
    invoice_id = "INV-2024-001"

    print(f"Full string: {invoice_id}")
    print(f"First character: {invoice_id[0]}")
    print(f"Fourth character: {invoice_id[3]}")
    print(f"Last character: {invoice_id[-1]}")
    print(f"Length: {len(invoice_id)} characters")
    ```

    **Output:**

    ```
    Full string: INV-2024-001
    First character: I
    Fourth character: -
    Last character: 1
    Length: 12 characters
    ```

    **Interpretation:** Position numbers start at zero, which is why the fourth character — the first hyphen — lives at index three. A negative index counts backward from the end, so the final character comes back without knowing the length in advance, and `len()` confirms the ID is 12 characters long.

    *Source: `computations/module05_examples.py` — `demo_string_indexing()`*

### Slicing Substrings

**Slicing** extracts a portion of a string with the syntax `text[start:stop]`. The slice includes the character at `start` but stops *before* `stop`:

```python
text[start:stop]     # characters from start up to (not including) stop
text[start:]         # from start to the end
text[:stop]          # from the beginning up to stop
```

Think of it like cutting a ribbon: you mark where to start cutting and where to stop, and you keep the piece in between.

!!! example "Worked Example: Slicing an Invoice ID and a Phone Number"

    ```python
    invoice_id = "INV-2024-001"

    # Extract the prefix, year, and sequence number
    prefix = invoice_id[:3]       # "INV"
    year = invoice_id[4:8]        # "2024"
    sequence = invoice_id[9:]     # "001"

    print(f"Invoice: {invoice_id}")
    print(f"Prefix: {prefix}")
    print(f"Year: {year}")
    print(f"Sequence: {sequence}")

    # Practical example: extract the area code from a phone number
    phone = "(512) 555-1234"

    area_code = phone[1:4]
    local_number = phone[6:]

    print()
    print(f"Phone: {phone}")
    print(f"Area code: {area_code}")
    print(f"Local number: {local_number}")
    ```

    **Output:**

    ```
    Invoice: INV-2024-001
    Prefix: INV
    Year: 2024
    Sequence: 001

    Phone: (512) 555-1234
    Area code: 512
    Local number: 555-1234
    ```

    **Interpretation:** Three slices split the invoice ID into its business meaning — the prefix, the year 2024, and the sequence number. The same technique pulls the 512 area code out of a formatted phone number. Position-based extraction like this works whenever the format is fixed; when the format varies, the regex tools later in this module take over.

    *Source: `computations/module05_examples.py` — `demo_string_slicing()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| The first character is at position 1. | Indexing starts at 0. `text[1]` is the *second* character — an off-by-one error that produces wrong extractions, not error messages. |
| `text[start:stop]` includes the character at `stop`. | The stop position is excluded. `text[4:8]` returns exactly the characters at positions 4, 5, 6, and 7. |
| Indexing and slicing behave the same past the end of the string. | Single-character indexing past the end raises an `IndexError`; slicing is forgiving and simply returns whatever exists in the range. |
| You can fix one character with `text[0] = "X"`. | Strings are **immutable** — they cannot be changed in place. You build a new string instead, using slices or the methods in the next section. |

---

## 5.2 Essential String Methods

Python strings come with dozens of built-in methods. These are the ones you will use most often for cleaning and transforming business data:

| Method | What it does | Example |
|--------|-------------|---------|
| `.upper()` | Convert to uppercase | `"hello".upper()` → `"HELLO"` |
| `.lower()` | Convert to lowercase | `"HELLO".lower()` → `"hello"` |
| `.title()` | Capitalize the first letter of every word | `"alice johnson".title()` → `"Alice Johnson"` |
| `.strip()` | Remove leading/trailing whitespace | `" hi ".strip()` → `"hi"` |
| `.replace(old, new)` | Replace all occurrences | `"a-b-c".replace("-", "/")` → `"a/b/c"` |
| `.find(sub)` | Find position of substring (-1 if not found) | `"hello".find("ll")` → `2` |
| `.split(sep)` | Split into a list on separator | `"a,b,c".split(",")` → `["a","b","c"]` |
| `.join(list)` | Join a list into a string | `", ".join(["a","b"])` → `"a, b"` |
| `.startswith(prefix)` | Check if string starts with prefix | `"INV-001".startswith("INV")` → `True` |
| `.endswith(suffix)` | Check if string ends with suffix | `"report.pdf".endswith(".pdf")` → `True` |

Strings are **immutable** — they cannot be changed in place. So the methods that transform text (`.upper()`, `.lower()`, `.title()`, `.strip()`, `.replace()`) hand back a **new** string and leave the original untouched. The rest answer a question *about* the string instead: `.find()` gives you a number (the position, or `-1` when the substring is absent), `.split()` gives you a list, and `.startswith()` / `.endswith()` give you `True` or `False`.

### Cleaning, Standardizing, and Locating

The next example shows three everyday moves in one place: stripping and re-casing a messy name, standardizing a product code, and locating a keyword so you can slice from it.

!!! example "Worked Example: Strip, Replace, and Find in Action"

    ```python
    # Cleaning messy customer data with .strip() and .title()
    raw_name = "   alice JOHNSON  "

    cleaned = raw_name.strip().title()
    print(f"Raw:     '{raw_name}'")
    print(f"Cleaned: '{cleaned}'")

    # Standardizing product codes with .replace() and .upper()
    raw_code = "PROD 2024 A-100"

    clean_code = raw_code.replace(" ", "-").upper()
    print()
    print(f"Raw:   {raw_code}")
    print(f"Clean: {clean_code}")

    # Locating a keyword with .find()
    report_line = "Total revenue for Q3: $245,000"

    pos = report_line.find("$")
    print()
    if pos != -1:
        amount_text = report_line[pos:]
        print(f"Found dollar amount at position {pos}: {amount_text}")
    else:
        print("No dollar amount found")
    ```

    **Output:**

    ```
    Raw:     '   alice JOHNSON  '
    Cleaned: 'Alice Johnson'

    Raw:   PROD 2024 A-100
    Clean: PROD-2024-A-100

    Found dollar amount at position 22: $245,000
    ```

    **Interpretation:** Each transforming method returns a new string, so the cleaned name and standardized code are fresh values — the raw inputs are unchanged. `.find()` answers a question instead: it reports the dollar sign at position 22, and slicing from that position onward extracts `$245,000`. Checking the result before slicing matters, because a missing substring produces a sentinel of negative one rather than an error.

    *Source: `computations/module05_examples.py` — `demo_string_methods_tour()`*

### Splitting and Joining

`.split()` and `.join()` are natural partners: one breaks a string into a list of parts, the other reassembles a list into a string. Together they handle most delimited-text reformatting.

!!! example "Worked Example: Reformatting a Date with Split and Join"

    ```python
    date_us = "02/14/2026"

    parts = date_us.split("/")
    print(f"Split into parts: {parts}")

    date_iso = "-".join([parts[2], parts[0], parts[1]])
    print(f"US format:  {date_us}")
    print(f"ISO format: {date_iso}")
    ```

    **Output:**

    ```
    Split into parts: ['02', '14', '2026']
    US format:  02/14/2026
    ISO format: 2026-02-14
    ```

    **Interpretation:** Splitting on the slash yields a list holding month, day, and year as separate strings. `.join()` — called on the *separator* — reassembles them in year-month-day order, producing the ISO form `2026-02-14` that databases and sorting prefer. This split–reorder–join pattern converts between delimited formats without any regex at all.

    *Source: `computations/module05_examples.py` — `demo_split_and_join()`*

### Method Chaining

Because each transforming method returns a new string, you can **chain** several together in one line. Python reads them left to right:

```python
cleaned = raw_input.strip().lower().replace(" ", "_")
```

This is equivalent to:

```python
step1 = raw_input.strip()
step2 = step1.lower()
cleaned = step2.replace(" ", "_")
```

Chaining keeps your code concise, but do not chain more than three or four methods or readability suffers.

!!! example "Worked Example: Chaining Methods to Standardize a Department Name"

    ```python
    raw_dept = "  Marketing & Sales  "

    clean_dept = raw_dept.strip().lower().replace(" & ", "_and_")
    print(f"Raw:   '{raw_dept}'")
    print(f"Clean: '{clean_dept}'")
    ```

    **Output:**

    ```
    Raw:   '  Marketing & Sales  '
    Clean: 'marketing_and_sales'
    ```

    **Interpretation:** Python applies the methods left to right: the padding disappears, the letters drop to lowercase, and the ampersand phrase becomes an underscore token. One line performs three transformations and yields a value clean enough to serve as a column name or file name. Order matters — replacing before stripping would have turned the outer padding into stray underscores.

    *Source: `computations/module05_examples.py` — `demo_method_chaining()`*

!!! question "Try It Yourself: Cleaning Customer Records"

    The list below contains messy customer email addresses. Write a loop that
    cleans each one by stripping whitespace and converting to lowercase, then
    prints the cleaned result.

    ```python
    emails = [
        "  Alice.Johnson@EXAMPLE.com ",
        "BOB.SMITH@example.COM",
        " carol.WILLIAMS@Example.Com  ",
    ]

    # for email in emails:
    #     clean = ???
    #     print(clean)
    ```

### Building Cleaning Functions

In Module 4 you learned to write reusable functions, and string cleaning is a perfect use case — the same steps apply to many records. The example below pairs two single-purpose functions: one strips a phone number down to its digits, the other formats those digits consistently.

!!! example "Worked Example: Reusable Phone-Cleaning Functions"

    ```python
    def clean_phone(raw_phone):
        """Remove non-digit characters from a phone number string.

        Args:
            raw_phone: A phone number in any format (e.g., "(512) 555-1234").

        Returns:
            A string containing only the digits (e.g., "5125551234").
        """
        cleaned = ""
        for char in raw_phone:
            if char.isdigit():
                cleaned = cleaned + char
        return cleaned

    def format_phone(digits):
        """Format a 10-digit string as (XXX) XXX-XXXX.

        Args:
            digits: A string of exactly 10 digits.

        Returns:
            Formatted phone number string.
        """
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"

    # Process messy phone numbers
    phones = [
        "(512) 555-1234",
        "512.555.5678",
        "512-555-9012",
        "  5125553456  ",
    ]

    for raw in phones:
        digits = clean_phone(raw_phone=raw)
        formatted = format_phone(digits=digits)
        print(f"{raw:>20s}  →  {formatted}")
    ```

    **Output:**

    ```
          (512) 555-1234  →  (512) 555-1234
            512.555.5678  →  (512) 555-5678
            512-555-9012  →  (512) 555-9012
            5125553456    →  (512) 555-3456
    ```

    **Interpretation:** Four differently formatted inputs converge on one standard format. `clean_phone` keeps only the digit characters, and `format_phone` reassembles them with the slicing technique from earlier in this module — each function does exactly one job, so either can be reused or changed without touching the other. This is the design habit the rest of the module builds on.

    *Source: `computations/module05_examples.py` — `demo_phone_cleaning_functions()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| `name.strip()` on its own cleans the variable. | Strings are immutable — the method *returns* a cleaned copy. Without an assignment like `name = name.strip()`, the result is discarded. |
| `.find()` raises an error when the substring is missing. | It returns `-1`. Code that slices with the result must check for that sentinel first, or it will slice from the wrong end of the string. |
| `.split(",")` and `.split()` do the same thing. | With an argument, the string splits on that exact separator. With no argument, it splits on any run of whitespace — a different behavior that is often exactly what you want for free-form text. |
| `.join()` is called on the list. | It is called on the *separator*: `", ".join(items)`. The list is the argument. |
| The order of chained methods never matters. | Methods apply left to right, and reordering can change the result — replacing spaces before stripping turns the surrounding padding into replacement characters. |

---

## 5.3 Regular Expressions and the `re` Module

String methods are great for simple, predictable operations. But consider these requests:

- "Find all dates in the format MM/DD/YYYY in this document"
- "Extract every email address from a customer feedback file"
- "Check if a product code matches the pattern ABC-1234"

**Regular expressions** (often shortened to **regex**) are a special language for describing text patterns. Python provides them through the `re` module. Think of a regex as a "search template" — instead of searching for an exact string like `"2024"`, you describe a *pattern* like "four digits in a row."

The `re` module provides four functions you will use most often:

| Function | What it does | Returns |
|----------|-------------|---------|
| `re.search(pattern, text)` | Find first match anywhere in text | Match object or `None` |
| `re.match(pattern, text)` | Match only at the start of text | Match object or `None` |
| `re.findall(pattern, text)` | Find all non-overlapping matches | List of strings |
| `re.sub(pattern, replacement, text)` | Replace all matches | New string |

The examples in the rest of this module assume `import re` has been run once at the top of the notebook.

### Searching and Finding All Matches

`re.search` scans the text and stops at the *first* match, returning a **match object** that knows both the matched text (`.group()`) and where it sits (`.start()`, `.end()`). `re.findall` keeps scanning and returns every match as a plain list of strings.

!!! example "Worked Example: First Match vs. All Matches"

    ```python
    import re

    text = "Order placed on 03/15/2025 and shipped on 03/18/2025"

    # re.search — find the FIRST occurrence of the pattern
    match = re.search(r"\d{2}/\d{2}/\d{4}", text)
    if match:
        print(f"First date found: {match.group()}")
        print(f"Position: {match.start()} to {match.end()}")

    # re.findall — find ALL matches, not just the first
    dates = re.findall(r"\d{2}/\d{2}/\d{4}", text)
    print(f"All dates found: {dates}")
    print(f"Number of dates: {len(dates)}")
    ```

    **Output:**

    ```
    First date found: 03/15/2025
    Position: 16 to 26
    All dates found: ['03/15/2025', '03/18/2025']
    Number of dates: 2
    ```

    **Interpretation:** `re.search` returns a match object — not the text itself — and that object reports both the matched date and its location, characters 16 to 26. `re.findall` returns plain strings instead: the order-status line contains 2 dates, and both come back in one call. When a pattern is absent, `re.search` returns `None`, which is why the `if match:` guard comes before any call to `.group()`.

    *Source: `computations/module05_examples.py` — `demo_search_and_findall()`*

Let's break down the pattern `\d{2}/\d{2}/\d{4}`:

| Part | Meaning |
|------|---------|
| `\d` | Any digit (0-9) |
| `{2}` | Exactly 2 of the previous element |
| `/` | A literal forward slash |
| `{4}` | Exactly 4 of the previous element |

So the full pattern means: "two digits, a slash, two digits, a slash, four digits" — which is exactly the MM/DD/YYYY date format.

The `r` before the string (`r"\d{2}/..."`) is a **raw string** — it tells Python not to interpret backslashes as escape characters. Always use raw strings for regex patterns.

### Replacing with `re.sub`

`re.sub()` is the regex counterpart of `.replace()`: instead of replacing one exact substring, it replaces *every match of a pattern*.

!!! example "Worked Example: Redacting Phone Numbers"

    ```python
    text = "Contact us at 512-555-1234 or 512-555-5678"

    redacted = re.sub(r"\d{3}-\d{3}-\d{4}", "[REDACTED]", text)
    print(f"Original: {text}")
    print(f"Redacted: {redacted}")
    ```

    **Output:**

    ```
    Original: Contact us at 512-555-1234 or 512-555-5678
    Redacted: Contact us at [REDACTED] or [REDACTED]
    ```

    **Interpretation:** Both phone numbers disappear in a single call — no loop, and no need to know the numbers in advance, because the pattern describes their shape. Masking sensitive values before sharing a document is a routine compliance task, and `re.sub` is the standard tool for it.

    *Source: `computations/module05_examples.py` — `demo_re_sub()`*

### Anchored Matching with `re.match`

`re.match` succeeds only when the pattern matches at the *beginning* of the string. That makes it a natural validator: does this value start with the format I expect?

!!! example "Worked Example: Filtering Invoice Codes"

    ```python
    codes = ["INV-2024-001", "PO-2024-015", "INV-2024-042", "RET-2024-003"]

    print("Invoice codes (starting with INV-):")
    for code in codes:
        m = re.match(r"INV-\d{4}-\d{3}", code)
        if m:
            print(f"  {code}")
    ```

    **Output:**

    ```
    Invoice codes (starting with INV-):
      INV-2024-001
      INV-2024-042
    ```

    **Interpretation:** Only the two codes that begin with the invoice prefix survive the filter — the purchase-order and return codes fail at the very first character, so `re.match` returns `None` for them. When the pattern might sit anywhere inside the string rather than at the start, use `re.search` instead.

    *Source: `computations/module05_examples.py` — `demo_re_match()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| `re.match` looks for the pattern anywhere in the string. | It is anchored to the *start*. A pattern in the middle of the text is found by `re.search`, never by `re.match`. |
| The `r` prefix is optional decoration. | Without it, Python may interpret backslash sequences in the pattern as escape characters before `re` ever sees them. Always write patterns as raw strings. |
| `re.search` returns the matching text. | It returns a match *object* (or `None`). You call `.group()` on the object to get the text, and `.start()` / `.end()` to get its position. |
| Calling `.group()` is always safe. | If nothing matched, `re.search` and `re.match` return `None`, and `.group()` on `None` raises an error. Test the result (`if match:`) first. |
| `re.findall` returns match objects. | It returns plain strings — or tuples of strings once the pattern contains multiple groups, as §5.4 shows. |

---

## 5.4 Building Patterns: Character Classes, Quantifiers, and Groups

The date pattern above used two building blocks — `\d` for "any digit" and `{n}` for "exactly n of them." This section fills out the toolkit: character classes say *what* can match at a position, quantifiers say *how many* times, and groups capture the pieces you care about.

### Character Classes: What to Match

A **character class** defines a set of characters that can match at one position.

| Pattern | Matches | Example |
|---------|---------|---------|
| `\d` | Any digit | `\d\d` matches `"42"` |
| `\D` | Any non-digit | `\D` matches `"A"`, `" "`, `"!"` |
| `\w` | Any word character (letter, digit, underscore) | `\w+` matches `"hello_123"` |
| `\W` | Any non-word character | `\W` matches `" "`, `"-"`, `"."` |
| `\s` | Any whitespace (space, tab, newline) | `\s+` matches `"  "` |
| `\S` | Any non-whitespace | `\S+` matches `"word"` |
| `[abc]` | Any one of a, b, or c | `[aeiou]` matches a vowel |
| `[A-Z]` | Any uppercase letter | `[A-Z]{2}` matches `"TX"` |
| `[0-9]` | Any ASCII digit 0-9 | `[0-9]{5}` matches `"78701"` |
| `.` | Any character except newline | `...` matches any 3 characters |

`[0-9]` and `\d` are interchangeable for everyday US business data. The one difference: `\d` also matches digits from other writing systems (for example the Arabic-script `٣`), while `[0-9]` is strictly the ASCII digits 0 through 9.

!!! example "Worked Example: Extracting State and ZIP with Character Classes"

    ```python
    addresses = [
        "123 Main St, Austin, TX 78701",
        "456 Oak Ave, Denver, CO 80202",
        "789 Pine Rd, Seattle, WA 98101",
    ]

    for addr in addresses:
        match = re.search(r"[A-Z]{2}\s\d{5}", addr)
        if match:
            print(f"State + ZIP: {match.group()}")
    ```

    **Output:**

    ```
    State + ZIP: TX 78701
    State + ZIP: CO 80202
    State + ZIP: WA 98101
    ```

    **Interpretation:** The pattern reads as "two uppercase letters, one whitespace character, five digits." Street names, cities, and building numbers all vary, yet the state–ZIP pair is located in every address — the pattern describes the *shape* of the target rather than its exact text, which is precisely what string methods cannot do.

    *Source: `computations/module05_examples.py` — `demo_character_classes()`*

### Quantifiers: How Many to Match

Quantifiers specify how many times a pattern element should repeat:

| Quantifier | Meaning | Example |
|-----------|---------|---------|
| `{n}` | Exactly n times | `\d{3}` matches `"512"` |
| `{n,m}` | Between n and m times | `\d{2,4}` matches `"42"` or `"2024"` |
| `*` | Zero or more times | `\d*` matches nothing or `"123"` |
| `+` | One or more times | `\d+` matches `"1"` or `"12345"` |
| `?` | Zero or one time (optional) | `\d?` matches nothing or `"5"` |

The most commonly used are `+` (one or more) and `{n}` (exact count).

!!! example "Worked Example: Dollar Amounts of Varying Lengths"

    ```python
    text = "Revenue was $1,234,567 in Q1 and costs were $845,000"

    # \$[\d,]+ matches a $ followed by one or more digits or commas
    amounts = re.findall(r"\$[\d,]+", text)
    print(f"Dollar amounts: {amounts}")
    ```

    **Output:**

    ```
    Dollar amounts: ['$1,234,567', '$845,000']
    ```

    **Interpretation:** The plus quantifier means "one or more of the preceding class," so the same pattern captures both the seven-figure revenue and the six-figure `$845,000` cost without knowing either length in advance. The dollar sign is escaped in the pattern because a bare one carries a special meaning in regex.

    *Source: `computations/module05_examples.py` — `demo_quantifiers()`*

### Groups: Capturing Parts of a Match

Parentheses `()` in a regex create a **group** — a sub-pattern whose match you can extract separately. This is how you pull specific pieces out of a larger pattern: the whole pattern still has to match, but each parenthesized piece is retrievable on its own.

!!! example "Worked Example: Capturing the Parts of a Date and an Invoice"

    ```python
    # Groups — extract the parts of a date separately
    text = "Invoice date: 03/15/2025"

    match = re.search(r"(\d{2})/(\d{2})/(\d{4})", text)
    if match:
        print(f"Full match: {match.group()}")
        print(f"Month: {match.group(1)}")
        print(f"Day: {match.group(2)}")
        print(f"Year: {match.group(3)}")

    # findall with groups — returns tuples of the captured groups
    invoice_text = """
    INV-2024-001: $1,250.00
    INV-2024-002: $340.50
    INV-2024-003: $8,900.75
    """

    invoices = re.findall(r"(INV-\d{4}-\d{3}): \$([\d,.]+)", invoice_text)
    print()
    for inv_id, amount in invoices:
        print(f"  {inv_id}  →  ${amount}")
    ```

    **Output:**

    ```
    Full match: 03/15/2025
    Month: 03
    Day: 15
    Year: 2025

      INV-2024-001  →  $1,250.00
      INV-2024-002  →  $340.50
      INV-2024-003  →  $8,900.75
    ```

    **Interpretation:** `.group()` with no argument returns the full match, while each numbered group returns one captured piece — the month, day, and year arrive pre-separated, ready for the split-and-join reordering trick from earlier in the module. In the second half, the pattern contains two groups, so `re.findall` returns a list of *tuples*, and tuple unpacking in the loop assigns the invoice ID and its amount in one step.

    *Source: `computations/module05_examples.py` — `demo_regex_groups()`*

When `findall` is used with **two or more** groups, it returns a list of tuples — each tuple holds the captured groups, as above. With exactly one group it returns a list of strings containing just that group's text, and with no groups a list of the full matches.

### Common Business Patterns

Here are regex patterns for data you will encounter regularly. These are worth keeping as a reference.

| Data | Pattern | Example Match |
|------|---------|---------------|
| US phone | `\d{3}-\d{3}-\d{4}` | `512-555-1234` |
| Email (simple) | `\S+@\S+\.\S+` | `alice@example.com` |
| US date | `\d{2}/\d{2}/\d{4}` | `03/15/2025` |
| ISO date | `\d{4}-\d{2}-\d{2}` | `2025-03-15` |
| US ZIP code | `\d{5}(?:-\d{4})?` | `78701` or `78701-1234` |
| Dollar amount | `\$[\d,]+(?:\.\d{2})?` | `$1,234.56` |
| Product code | `[A-Z]{2,4}-\d{3,5}` | `INV-2024` |

The `?` after the parentheses means that part is optional. These use `(?:...)` — a **non-capturing** group — so `re.findall` returns the whole match (`"78701-1234"`) rather than just the group inside. Plain `(...)` capturing groups would make `findall` return only the captured piece (`"-1234"`), which is rarely what you want here.

!!! question "Try It Yourself: Extract Email Addresses"

    Use `re.findall()` to extract all email addresses from the text below.

    ```python
    feedback = """
    Customer feedback received:
    - "Great product!" — alice.j@example.com
    - "Needs improvement" — bob_smith@company.org
    - "Will buy again" — carol.w@shop.net
    """

    # Extract emails using re.findall
    # emails = re.findall(r"???", feedback)
    # for email in emails:
    #     print(email)
    ```

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| `.` in a pattern matches a literal period. | `.` matches *any* character except a newline. Write `\.` to match an actual dot — email and version-number patterns get this wrong constantly. |
| `+` and `*` are interchangeable. | `+` requires at least one occurrence; `*` also matches zero occurrences, which can make a pattern match empty text where you did not expect it. |
| A quantifier repeats the whole pattern. | It applies only to the element immediately before it — `ab+` matches one `a` followed by repeated `b`s. Wrap a sub-pattern in parentheses to repeat all of it. |
| Adding parentheses never changes what `findall` returns. | Capturing groups change the return value to just the captured pieces (tuples when there are two or more). Use a non-capturing `(?:...)` group when you only need the grouping. |
| `\d` and `[0-9]` behave differently in everyday work. | For US business data they are interchangeable; the only difference is that `\d` also accepts digits from other writing systems. |

---

## 5.5 Cleaning and Parsing Business Text

Real-world data is messy. This section combines everything so far — string methods, regex, and the function design from Module 4 — into the workflows you will actually run: cleaning a batch of records, parsing semi-structured documents, and standardizing formats across a whole text.

### A Reusable Cleaning Pipeline

When importing data from a spreadsheet or form submissions, each field needs its own cleaning rule. The pattern: one small function per field, then a loop that applies all of them to every record.

!!! example "Worked Example: Cleaning a Batch of Customer Records"

    ```python
    def clean_name(raw_name):
        """Strip whitespace and convert to title case."""
        return raw_name.strip().title()

    def clean_email(raw_email):
        """Strip whitespace and convert to lowercase."""
        return raw_email.strip().lower()

    def extract_zip(address):
        """Extract a 5-digit ZIP code from an address string.

        Args:
            address: A string containing a US address.

        Returns:
            The ZIP code as a string, or "N/A" if not found.
        """
        match = re.search(r"\d{5}", address)
        if match:
            return match.group()
        return "N/A"

    def format_phone_number(raw_phone):
        """Extract digits from a phone string and format as (XXX) XXX-XXXX.

        Args:
            raw_phone: Phone number in any format.

        Returns:
            Formatted phone string, or the original if not 10 digits.
        """
        digits = re.sub(r"\D", "", raw_phone)
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        return raw_phone

    # Messy customer records
    customers = [
        ("  alice JOHNSON ", "Alice.J@EXAMPLE.COM", "123 Main St, Austin TX 78701", "512.555.1234"),
        ("BOB smith  ", " Bob@Company.ORG ", "456 Oak Ave Denver CO 80202", "(303) 555-5678"),
        (" Carol Williams", "CAROL@shop.NET  ", "789 Pine Rd, Seattle WA 98101", "206-555-9012"),
    ]

    print(f"{'Name':<20} {'Email':<28} {'ZIP':<6} {'Phone'}")
    print("-" * 80)

    for raw_name, raw_email, raw_addr, raw_phone in customers:
        name = clean_name(raw_name=raw_name)
        email = clean_email(raw_email=raw_email)
        zip_code = extract_zip(address=raw_addr)
        phone = format_phone_number(raw_phone=raw_phone)
        print(f"{name:<20} {email:<28} {zip_code:<6} {phone}")
    ```

    **Output:**

    ```
    Name                 Email                        ZIP    Phone
    --------------------------------------------------------------------------------
    Alice Johnson        alice.j@example.com          78701  (512) 555-1234
    Bob Smith            bob@company.org              80202  (303) 555-5678
    Carol Williams       carol@shop.net               98101  (206) 555-9012
    ```

    **Interpretation:** Four single-purpose functions turn inconsistent records into a uniform directory — names in title case, emails lowercased, ZIP codes extracted by pattern, phones stripped to digits and reformatted. The main loop stays clean and readable, and if the phone format ever changes, you update exactly one function and every record picks up the change. Note the regex replacement inside `format_phone_number`: substituting every *non*-digit with nothing is a one-line version of the character-by-character loop that `clean_phone` used earlier.

    *Source: `computations/module05_examples.py` — `demo_customer_data_cleaning()`*

### Parsing Semi-Structured Text

Sometimes business data arrives as semi-structured text rather than neat columns — an emailed invoice, a pasted report. Regex lets you extract the structured data from the noise.

!!! example "Worked Example: Parsing an Invoice Text Block"

    ```python
    invoice_text = """
    INVOICE #INV-2025-047
    Date: 02/14/2026
    Customer: Acme Corporation

    Items:
      Widget A x 50 @ $12.99
      Widget B x 120 @ $8.50
      Widget C x 25 @ $34.00

    Subtotal: $2,519.50
    Tax (8.25%): $207.86
    Total: $2,727.36
    """

    # Extract the invoice number
    inv_match = re.search(r"INV-\d{4}-\d{3}", invoice_text)
    print(f"Invoice: {inv_match.group()}")

    # Extract the date
    date_match = re.search(r"\d{2}/\d{2}/\d{4}", invoice_text)
    print(f"Date: {date_match.group()}")

    # Extract all line items: product, quantity, unit price
    items = re.findall(r"(\w[\w ]+\w)\s+x\s+(\d+)\s+@\s+\$([\d.]+)", invoice_text)
    print("\nLine items:")
    for product, qty, price in items:
        print(f"  {product}: {qty} units at ${price}")

    # Extract the total
    total_match = re.search(r"Total:\s+\$([\d,.]+)", invoice_text)
    print(f"\nTotal: ${total_match.group(1)}")
    ```

    **Output:**

    ```
    Invoice: INV-2025-047
    Date: 02/14/2026

    Line items:
      Widget A: 50 units at $12.99
      Widget B: 120 units at $8.50
      Widget C: 25 units at $34.00

    Total: $2,727.36
    ```

    **Interpretation:** Three targeted patterns pull out the invoice number, the date, and every line item — product name, quantity, and unit price captured as separate groups — while the surrounding prose is simply never matched. The final search captures the `$2,727.36` total *without* its label, because `.group()` with a group number returns only the parenthesized part.

    *Source: `computations/module05_examples.py` — `demo_invoice_parsing()`*

### `re.sub` with a Function Replacement

`re.sub()` can accept a **function** as the replacement instead of a string. The function receives each match object and returns the replacement text — full control over how every match is transformed. This is how you standardize a format across an entire document in one call.

!!! example "Worked Example: Standardizing Date Formats"

    ```python
    def standardize_date(text):
        """Convert dates from MM/DD/YYYY to YYYY-MM-DD format in a text string.

        Args:
            text: A string potentially containing dates in MM/DD/YYYY format.

        Returns:
            The text with all dates converted to ISO format.
        """
        def reformat(match):
            month = match.group(1)
            day = match.group(2)
            year = match.group(3)
            return f"{year}-{month}-{day}"

        return re.sub(
            r"(\d{2})/(\d{2})/(\d{4})",
            reformat,
            text,
        )

    report = "Meeting on 02/14/2026, follow-up by 03/01/2026, deadline 04/15/2026."
    standardized = standardize_date(text=report)

    print(f"Original:     {report}")
    print(f"Standardized: {standardized}")
    ```

    **Output:**

    ```
    Original:     Meeting on 02/14/2026, follow-up by 03/01/2026, deadline 04/15/2026.
    Standardized: Meeting on 2026-02-14, follow-up by 2026-03-01, deadline 2026-04-15.
    ```

    **Interpretation:** The inner `reformat` function receives each match object, reorders its three captured groups, and returns the ISO form. All three dates convert in one `re.sub` call while every other character of the sentence is left untouched — a string-replacement approach would need to know each date in advance.

    *Source: `computations/module05_examples.py` — `demo_standardize_dates()`*

### Capstone: Parsing a Sales Report

The closing example uses everything from this module — string methods, regex groups, and functions — to turn a block of report text into structured records with a computed total.

**A quick preview:** the parsing function below packages each row into a **dictionary** — a labeled container written with `{}` where you look values up by name, like `entry["name"]`, instead of by position. Dictionaries are the main topic of Module 7, so don't worry about the syntax yet; for now just read `entry["name"]` as "the name field of this entry."

!!! example "Worked Example: Sales Report Text to Structured Data"

    ```python
    def parse_sales_entry(line):
        """Parse a sales report line into a dictionary.

        Expected format: "REP-NNN  Name  $amount  region"

        Args:
            line: A single line from the sales report.

        Returns:
            A dictionary with keys: rep_id, name, amount, region.
            Returns None if the line does not match the expected format.
        """
        pattern = r"(REP-\d{3})\s+([\w ]+?)\s+\$([\d,]+\.\d{2})\s+(\w+)"
        match = re.search(pattern, line)
        if match:
            return {
                "rep_id": match.group(1),
                "name": match.group(2).strip(),
                "amount": float(match.group(3).replace(",", "")),
                "region": match.group(4),
            }
        return None

    def format_currency(value):
        """Format a number as $X,XXX.XX."""
        return f"${value:,.2f}"

    report_text = """
    Q4 Sales Report — All Regions
    ==============================
    REP-101  Alice Chen       $42,350.00  West
    REP-102  Bob Martinez     $38,900.50  South
    REP-103  Carol Davis      $51,200.75  East
    REP-104  Dave Kim         $29,450.00  West
    REP-105  Eve Johnson      $44,800.25  South
    ==============================
    """

    entries = []
    for line in report_text.strip().split("\n"):
        entry = parse_sales_entry(line=line)
        if entry:
            entries.append(entry)

    # Display parsed results
    print(f"{'ID':<10} {'Name':<18} {'Amount':>12} {'Region':<8}")
    print("-" * 50)

    total = 0
    for e in entries:
        print(
            f"{e['rep_id']:<10} "
            f"{e['name']:<18} "
            f"{format_currency(e['amount']):>12} "
            f"{e['region']:<8}"
        )
        total = total + e["amount"]

    print("-" * 50)
    print(f"{'Total':<29} {format_currency(total):>12}")
    print(f"\nReps parsed: {len(entries)}")
    ```

    **Output:**

    ```
    ID         Name                     Amount Region  
    --------------------------------------------------
    REP-101    Alice Chen           $42,350.00 West    
    REP-102    Bob Martinez         $38,900.50 South   
    REP-103    Carol Davis          $51,200.75 East    
    REP-104    Dave Kim             $29,450.00 West    
    REP-105    Eve Johnson          $44,800.25 South   
    --------------------------------------------------
    Total                          $206,701.50
    
    Reps parsed: 5
    ```

    **Interpretation:** `Reps parsed: 5` confirms that only the data rows matched — the title and separator lines come back as `None` and are skipped, so messy framing text never corrupts the results. The regex extracts each field, the function organizes it into a dictionary (converting the amount to a number after removing its comma), and the loop accumulates the `$206,701.50` total. This *regex to extract, function to organize, loop to process* pattern is one you will use repeatedly with real business data.

    *Source: `computations/module05_examples.py` — `demo_sales_report_parsing()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Once you know regex, string methods are obsolete. | Use the simplest tool that works: methods for fixed transformations (strip, case, exact replace), regex when the text's *shape* varies. Mixing both, as the cleaning pipeline does, is normal. |
| `re.sub` only accepts a replacement string. | It also accepts a function, which receives the match object and returns the replacement — the key to per-match transformations like date reordering. |
| `float("1,250.00")` converts a formatted amount. | Python's `float()` rejects thousands separators. Remove them first with `.replace(",", "")`, exactly as `parse_sales_entry` does. |
| A parser can assume every line contains data. | Real documents carry headers, separators, and blank lines. Returning `None` for non-matching lines — and skipping them in the loop — is what makes a parser robust. |

---

## Reflection Questions

1. A teammate uses a regex to uppercase department names and another to trim whitespace. Both work. What is the case for using plain string methods for those tasks and reserving regex for pattern-shaped problems, and where would you draw the line?
2. Strings are immutable, so every cleaning step produces a new string. How does this property make a chained pipeline like `raw.strip().lower().replace(" ", "_")` predictable — and what bug does it prevent when two variables refer to the same original text?
3. The module insists on raw strings (`r"..."`) for every pattern. What kind of failure could a non-raw pattern produce, and why might that failure be harder to notice than an ordinary error message?
4. `re.match` validated invoice codes by anchoring at the start of the string. Describe a business validation where `re.search` would silently accept bad input that `re.match` would correctly reject.
5. Capturing groups changed what `re.findall` returned — from full matches to tuples of pieces. When extracting invoice IDs *and* amounts together, why is getting them as paired tuples safer than running two separate `findall` calls and lining up the two lists?
6. The customer-cleaning example used one small function per field instead of one large cleaning function. If the company later adds a "clean job title" rule and changes the phone format, how does the one-function-per-task design reduce the risk of those changes?

---

## Your Assignment

The Module 5 assignment, **Strings & Regular Expressions**, is worth **100 points plus a 10-point bonus**. You complete it in the provided marimo notebook and submit the `.py` file to Blackboard. The closing reflection section is not graded separately — it counts toward participation. Throughout the assignment: use raw strings (`r"..."`) for every regex pattern, use keyword arguments when calling functions with multiple parameters, and remember that string methods return new strings rather than modifying the original.

### Task 1: String Slicing and Indexing (10 points)

A hospital system stores patient record IDs in a fixed `DEPT-YYYY-NNNNN` layout — a department code, an admission year, and a patient sequence number at known positions. Using slicing (not `split`) plus indexing, extract and print the department, year, sequence number, and the record's final digit. The positional extraction techniques are all in §5.1.

### Task 2: String Methods — Cleaning Product Data (15 points)

An e-commerce company imported product names that arrive with stray whitespace, inconsistent capitalization, and underscores where spaces belong. Write a loop that cleans each name — strip the padding, replace the underscores with spaces, convert to title case — and prints the raw and cleaned versions side by side. The methods and the chaining style come from §5.2.

### Task 3: Split, Join, and Reformat (15 points)

A logistics company receives shipment entries as single pipe-delimited strings holding a tracking number, origin city, destination city, and weight. Write a `parse_shipment` function that splits each entry, strips the whitespace from every part, and returns a formatted one-line summary; then call it in a loop over the shipment list. Splitting and joining are covered in §5.2, and the function structure follows Module 4.

### Task 4: Regex — Finding Patterns with `findall` (15 points)

A compliance officer needs to scan a company memo for sensitive information. Use `re.findall` three times to extract every date, every dollar amount, and every employee ID from the memo text, printing each labeled result list. The `findall` workflow is in §5.3, and the character classes and quantifiers you need — along with a reference table of these exact business patterns — are in §5.4.

### Task 5: Regex Groups — Extracting Structured Data (20 points)

A property management company logs maintenance requests as semi-structured text lines. Write a `parse_maintenance_request` function — docstring required — that uses `re.search` with capturing groups to pull the request ID, unit, category, and cost from one line, returning them in a dictionary or `None` when a line does not match. Then loop through the log, print a formatted summary, and track the total cost of all requests. Groups are introduced in §5.4, and the parse-into-a-dictionary pattern is demonstrated in §5.5.

### Task 6: Combined Challenge — Clean and Parse a Business Document (25 points)

A vendor contact list copied from an old system has inconsistent formatting in every entry. Split the text into entries on blank lines, then extract and clean each vendor's company name and contact person with string methods, reformat the phone by stripping it to digits with `re.sub` and rebuilding the standard layout, and pull the email out with `re.search` before lowercasing it. Print the result as a formatted contact directory. This task combines §5.2 methods, §5.3 regex functions, and the §5.5 pipeline design.

### Task 7: Creative Exercise — Bonus (10 points)

Design your own text-parsing scenario. Suggested directions include parsing job postings, validating URLs, pricing out a restaurant-menu order, or processing server logs — but any realistic scenario qualifies. Requirements: at least two functions with docstrings, at least one string method, at least one regex operation (`search`, `findall`, or `sub`), a loop that processes multiple records, and clear formatted output.

### Reflection (participation credit)

Answer the notebook's four reflection prompts in your own words: when you would choose string methods versus regular expressions (with an example of each), what the `r` prefix does and why patterns need it, what regex groups are and why they are useful (with an example from the assignment), and what you found most challenging. There is no wrong answer — honest reflection helps your instructor see where support is needed.

---

## Chapter Summary

Strings are sequences, so the position tools come first: indexing retrieves a single character (counting from zero, with negative indexes counting from the end), and slicing extracts a substring from a start position up to — but not including — a stop position. Because strings are immutable, nothing edits text in place. The transforming methods (`.strip()`, `.upper()`, `.lower()`, `.title()`, `.replace()`) return new strings, which is exactly what makes method chaining work, while the reporting methods answer questions instead: `.find()` returns a position, `.split()` a list, `.startswith()` a boolean. `.split()` and `.join()` together handle most delimited-text reformatting, as the US-to-ISO date conversion showed.

Regular expressions take over when the text's shape varies. A pattern is a search template built from character classes (`\d`, `\w`, `\s`, `[A-Z]`) that say *what* can match, quantifiers (`+`, `*`, `?`, `{n}`) that say *how many*, and groups (`(...)`) that capture the pieces you want back. The `re` module applies patterns four ways: `re.search` finds the first match anywhere, `re.match` tests only the start of the string, `re.findall` returns every match — as tuples of captured pieces once a pattern has multiple groups — and `re.sub` replaces every match, accepting either a string or a per-match function as the replacement. Always write patterns as raw strings, and always check that `search`/`match` did not return `None` before calling `.group()`.

The module closed with the workflow that makes both toolkits pay off: one small function per cleaning task, regex to extract structure from semi-structured text, and a loop to process the batch — skipping the lines that return `None`. The customer directory, invoice parser, and sales-report capstone all followed that *extract, organize, process* shape, and the assignment asks you to build the same machinery against new business documents.

---

## What's Next

Module 6 covers **lists and tuples** — Python's built-in structures for holding collections of values. You have been using lists all module without examining them: `.split()` returned one, `re.findall` returned one, and every cleaning loop walked through one. Module 6 makes them the main subject: creating and modifying lists, list methods, and list comprehensions — and the indexing and slicing syntax you just learned for strings carries over to lists unchanged, so `items[0]` and `items[2:5]` will already feel familiar.
