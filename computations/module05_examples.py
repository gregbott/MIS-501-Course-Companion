"""Module 5 worked-example computations for the MIS 501 Course Companion.

Every demo_*() function below reproduces exactly one Worked Example in
docs/modules/05-strings-and-regex.md. Run this script directly to print
each example's output under a separator header, in the same order the
examples appear in the chapter.

References in Course Companion:
    demo_string_indexing()          -> Module 5, Section 5.1 (String Indexing and Slicing)
    demo_string_slicing()           -> Module 5, Section 5.1 (String Indexing and Slicing)
    demo_string_methods_tour()      -> Module 5, Section 5.2 (Essential String Methods)
    demo_split_and_join()           -> Module 5, Section 5.2 (Essential String Methods)
    demo_method_chaining()          -> Module 5, Section 5.2 (Essential String Methods)
    demo_phone_cleaning_functions() -> Module 5, Section 5.2 (Essential String Methods)
    demo_search_and_findall()       -> Module 5, Section 5.3 (Regular Expressions and the re Module)
    demo_re_sub()                   -> Module 5, Section 5.3 (Regular Expressions and the re Module)
    demo_re_match()                 -> Module 5, Section 5.3 (Regular Expressions and the re Module)
    demo_character_classes()        -> Module 5, Section 5.4 (Building Patterns: Character Classes, Quantifiers, and Groups)
    demo_quantifiers()              -> Module 5, Section 5.4 (Building Patterns: Character Classes, Quantifiers, and Groups)
    demo_regex_groups()             -> Module 5, Section 5.4 (Building Patterns: Character Classes, Quantifiers, and Groups)
    demo_customer_data_cleaning()   -> Module 5, Section 5.5 (Cleaning and Parsing Business Text)
    demo_invoice_parsing()          -> Module 5, Section 5.5 (Cleaning and Parsing Business Text)
    demo_standardize_dates()        -> Module 5, Section 5.5 (Cleaning and Parsing Business Text)
    demo_sales_report_parsing()     -> Module 5, Section 5.5 (Cleaning and Parsing Business Text)

Last updated: 2026-07-23
"""

import re


# ---------------------------------------------------------------------------
# Section 5.1 — String Indexing and Slicing
# ---------------------------------------------------------------------------

def demo_string_indexing():
    """Access individual characters of an invoice ID by index."""
    invoice_id = "INV-2024-001"

    print(f"Full string: {invoice_id}")
    print(f"First character: {invoice_id[0]}")
    print(f"Fourth character: {invoice_id[3]}")
    print(f"Last character: {invoice_id[-1]}")
    print(f"Length: {len(invoice_id)} characters")


def demo_string_slicing():
    """Extract substrings from an invoice ID and a phone number with slices."""
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


# ---------------------------------------------------------------------------
# Section 5.2 — Essential String Methods
# ---------------------------------------------------------------------------

def demo_string_methods_tour():
    """strip/title cleaning, replace/upper standardizing, and find locating."""
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


def demo_split_and_join():
    """Reformat a US date to ISO format with split and join."""
    date_us = "02/14/2026"

    parts = date_us.split("/")
    print(f"Split into parts: {parts}")

    date_iso = "-".join([parts[2], parts[0], parts[1]])
    print(f"US format:  {date_us}")
    print(f"ISO format: {date_iso}")


def demo_method_chaining():
    """Chain strip, lower, and replace to standardize a department name."""
    raw_dept = "  Marketing & Sales  "

    clean_dept = raw_dept.strip().lower().replace(" & ", "_and_")
    print(f"Raw:   '{raw_dept}'")
    print(f"Clean: '{clean_dept}'")


def demo_phone_cleaning_functions():
    """Pair of small functions that clean and format messy phone numbers."""
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


# ---------------------------------------------------------------------------
# Section 5.3 — Regular Expressions and the re Module
# ---------------------------------------------------------------------------

def demo_search_and_findall():
    """re.search finds the first date; re.findall finds every date."""
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


def demo_re_sub():
    """Redact phone numbers by replacing every pattern match."""
    text = "Contact us at 512-555-1234 or 512-555-5678"

    redacted = re.sub(r"\d{3}-\d{3}-\d{4}", "[REDACTED]", text)
    print(f"Original: {text}")
    print(f"Redacted: {redacted}")


def demo_re_match():
    """re.match keeps only the codes that START with the invoice pattern."""
    codes = ["INV-2024-001", "PO-2024-015", "INV-2024-042", "RET-2024-003"]

    print("Invoice codes (starting with INV-):")
    for code in codes:
        m = re.match(r"INV-\d{4}-\d{3}", code)
        if m:
            print(f"  {code}")


# ---------------------------------------------------------------------------
# Section 5.4 — Building Patterns: Character Classes, Quantifiers, and Groups
# ---------------------------------------------------------------------------

def demo_character_classes():
    """Extract state abbreviation + ZIP pairs with character classes."""
    addresses = [
        "123 Main St, Austin, TX 78701",
        "456 Oak Ave, Denver, CO 80202",
        "789 Pine Rd, Seattle, WA 98101",
    ]

    for addr in addresses:
        match = re.search(r"[A-Z]{2}\s\d{5}", addr)
        if match:
            print(f"State + ZIP: {match.group()}")


def demo_quantifiers():
    """Match dollar amounts of varying lengths with the + quantifier."""
    text = "Revenue was $1,234,567 in Q1 and costs were $845,000"

    # \$[\d,]+ matches a $ followed by one or more digits or commas
    amounts = re.findall(r"\$[\d,]+", text)
    print(f"Dollar amounts: {amounts}")


def demo_regex_groups():
    """Capture parts of a match with groups, singly and with findall."""
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


# ---------------------------------------------------------------------------
# Section 5.5 — Cleaning and Parsing Business Text
# ---------------------------------------------------------------------------

def demo_customer_data_cleaning():
    """Four small functions clean a batch of messy customer records."""
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


def demo_invoice_parsing():
    """Pull invoice number, date, line items, and total out of message text."""
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


def demo_standardize_dates():
    """re.sub with a function replacement converts US dates to ISO format."""
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


def demo_sales_report_parsing():
    """Capstone: regex + functions + a loop parse a sales report into data."""
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


if __name__ == "__main__":
    demos = [
        ("Section 5.1", demo_string_indexing),
        ("Section 5.1", demo_string_slicing),
        ("Section 5.2", demo_string_methods_tour),
        ("Section 5.2", demo_split_and_join),
        ("Section 5.2", demo_method_chaining),
        ("Section 5.2", demo_phone_cleaning_functions),
        ("Section 5.3", demo_search_and_findall),
        ("Section 5.3", demo_re_sub),
        ("Section 5.3", demo_re_match),
        ("Section 5.4", demo_character_classes),
        ("Section 5.4", demo_quantifiers),
        ("Section 5.4", demo_regex_groups),
        ("Section 5.5", demo_customer_data_cleaning),
        ("Section 5.5", demo_invoice_parsing),
        ("Section 5.5", demo_standardize_dates),
        ("Section 5.5", demo_sales_report_parsing),
    ]
    for section, demo in demos:
        print("=" * 72)
        print(f"{demo.__name__} — Module 5, {section}")
        print("=" * 72)
        demo()
        print()
