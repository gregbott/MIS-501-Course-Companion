"""Module 6 worked-example computations for the MIS501 Course Companion.

Every demo_*() function below reproduces exactly one Worked Example in
docs/modules/06-lists-and-tuples.md. Run this script directly to print
each example's output under a separator header, in the same order the
examples appear in the chapter.

References in Course Companion:
    demo_creating_lists()             -> Module 6, Section 6.1 (Lists: Creating, Indexing, and Slicing)
    demo_indexing_and_updating()      -> Module 6, Section 6.1 (Lists: Creating, Indexing, and Slicing)
    demo_slicing()                    -> Module 6, Section 6.1 (Lists: Creating, Indexing, and Slicing)
    demo_adding_and_removing()        -> Module 6, Section 6.2 (List Methods: Adding, Removing, and Organizing)
    demo_sorting()                    -> Module 6, Section 6.2 (List Methods: Adding, Removing, and Organizing)
    demo_loop_totals()                -> Module 6, Section 6.3 (Iterating Over Lists)
    demo_enumerate_reports()          -> Module 6, Section 6.3 (Iterating Over Lists)
    demo_accumulator_filter()         -> Module 6, Section 6.3 (Iterating Over Lists)
    demo_comprehension_vs_loop()      -> Module 6, Section 6.4 (List Comprehensions)
    demo_comprehension_filters()      -> Module 6, Section 6.4 (List Comprehensions)
    demo_summarize_sales()            -> Module 6, Section 6.5 (Tuples, Unpacking, and Mutability)
    demo_tuple_basics()               -> Module 6, Section 6.5 (Tuples, Unpacking, and Mutability)
    demo_tuple_unpacking()            -> Module 6, Section 6.5 (Tuples, Unpacking, and Mutability)
    demo_analyze_scores()             -> Module 6, Section 6.5 (Tuples, Unpacking, and Mutability)
    demo_aliasing_and_copy()          -> Module 6, Section 6.5 (Tuples, Unpacking, and Mutability)
    demo_sales_performance_report()   -> Module 6, Section 6.5 (Tuples, Unpacking, and Mutability)

Last updated: 2026-07-23
"""


def demo_creating_lists():
    """Creating lists of business data and counting items with len()."""
    products = ["Laptop", "Monitor", "Keyboard", "Mouse", "Webcam"]
    prices = [999.99, 349.50, 79.95, 24.99, 64.50]
    in_stock = [True, True, False, True, True]

    print(f"Products: {products}")
    print(f"Prices: {prices}")
    print(f"In stock: {in_stock}")
    print(f"Number of products: {len(products)}")


def demo_indexing_and_updating():
    """Zero-based and negative indexing, plus updating an item in place."""
    products = ["Laptop", "Monitor", "Keyboard", "Mouse", "Webcam"]

    print(f"products[0]  (first):          {products[0]}")
    print(f"products[2]  (third):          {products[2]}")
    print(f"products[-1] (last):           {products[-1]}")
    print(f"products[-2] (second to last): {products[-2]}")

    # Lists are mutable — update the keyboard's price at index 2
    prices = [999.99, 349.50, 79.95, 24.99, 64.50]
    print(f"Before: {prices}")

    prices[2] = 69.95
    print(f"After:  {prices}")


def demo_slicing():
    """Slicing extracts sublists without modifying the original list."""
    quarterly_sales = [42000, 38500, 51200, 47800, 39900, 55100, 44300, 49000]
    print(f"All months:      {quarterly_sales}")

    # First quarter (indexes 0-2)
    q1 = quarterly_sales[:3]
    print(f"Q1 months:       {q1}")

    # Middle section
    middle = quarterly_sales[2:6]
    print(f"Middle months:   {middle}")

    # Last two months
    recent = quarterly_sales[-2:]
    print(f"Last two months: {recent}")

    print(f"Original intact: {quarterly_sales}")


def demo_adding_and_removing():
    """Building an order with append/insert/extend, then trimming with remove/pop."""
    # Building an order list step by step
    order = []
    print(f"Empty order:  {order}")

    order.append("Laptop")
    order.append("Monitor")
    print(f"After append: {order}")

    order.insert(1, "Keyboard")  # insert between Laptop and Monitor
    print(f"After insert: {order}")

    order.extend(["Mouse", "Webcam"])
    print(f"After extend: {order}")

    # Removing items from a list
    inventory = ["Laptop", "Monitor", "Keyboard", "Mouse", "Monitor", "Webcam"]
    print(f"\nInventory before: {inventory}")

    inventory.remove("Monitor")  # removes only the FIRST "Monitor"
    print(f"After remove:     {inventory}")

    last_item = inventory.pop()  # removes and returns the last item
    print(f"Popped item:      {last_item}")
    print(f"After pop:        {inventory}")


def demo_sorting():
    """Sorting in place with .sort() versus making a sorted copy with sorted()."""
    monthly_sales = [42000, 38500, 51200, 47800, 39900]
    print(f"Original:           {monthly_sales}")

    monthly_sales.sort()
    print(f"Sorted ascending:   {monthly_sales}")

    monthly_sales.sort(reverse=True)
    print(f"Sorted descending:  {monthly_sales}")

    # sorted() returns a new list and leaves the original alone
    original = [42000, 38500, 51200]
    sorted_copy = sorted(original)
    print(f"\nsorted() copy:      {sorted_copy}")
    print(f"Original unchanged: {original}")


def demo_loop_totals():
    """Accumulating a total and computing an average with a for loop."""
    monthly_sales = [42000, 38500, 51200, 47800, 39900]

    total = 0
    for sale in monthly_sales:
        total = total + sale

    average = total / len(monthly_sales)
    print(f"Monthly sales:   {monthly_sales}")
    print(f"Months counted:  {len(monthly_sales)}")
    print(f"Total revenue:   ${total:,.2f}")
    print(f"Average monthly: ${average:,.2f}")


def demo_enumerate_reports():
    """enumerate() for a numbered report and for tracking best/worst positions."""
    months = ["January", "February", "March", "April", "May"]
    sales = [42000, 38500, 51200, 47800, 39900]

    # Numbered monthly sales report
    print("Monthly Sales Report")
    print("-" * 35)
    for i, month in enumerate(months):
        print(f"  {i + 1}. {month:<12} ${sales[i]:>10,.2f}")

    # Find the best and worst performing months
    best_idx = 0
    worst_idx = 0

    for i, amount in enumerate(sales):
        if amount > sales[best_idx]:
            best_idx = i
        if amount < sales[worst_idx]:
            worst_idx = i

    print(f"\nBest month:  {months[best_idx]} (${sales[best_idx]:,.2f})")
    print(f"Worst month: {months[worst_idx]} (${sales[worst_idx]:,.2f})")


def demo_accumulator_filter():
    """The list accumulator pattern: create empty, loop, conditionally append."""
    order_amounts = [150, 45, 320, 89, 510, 72, 205, 33]

    high_value = []
    for amount in order_amounts:
        if amount >= 200:
            high_value.append(amount)

    print(f"All orders: {order_amounts}")
    print(f"High-value orders (>= $200): {high_value}")
    print(f"Count: {len(high_value)} of {len(order_amounts)}")


def demo_comprehension_vs_loop():
    """The same discount computed with a loop and with a list comprehension."""
    prices = [999.99, 349.50, 79.95, 24.99, 64.50]
    print("Applying a 10% discount to each price")

    # Loop approach: apply the discount to each price
    discounted_loop = []
    for p in prices:
        discounted_loop.append(p * 0.90)

    # Comprehension approach: same result, one line
    discounted_comp = [p * 0.90 for p in prices]

    print(f"Original:          {prices}")
    print(f"Discounted (loop): {[round(p, 2) for p in discounted_loop]}")
    print(f"Discounted (comp): {[round(p, 2) for p in discounted_comp]}")


def demo_comprehension_filters():
    """Comprehensions that filter with zip() and transform with string methods."""
    # Filter: only products under $100
    products = ["Laptop", "Monitor", "Keyboard", "Mouse", "Webcam"]
    prices = [999.99, 349.50, 79.95, 24.99, 64.50]

    affordable = [
        name
        for name, price in zip(products, prices)
        if price < 100
    ]
    print(f"Products under $100: {affordable}")

    # Transform: convert a list of names to title case
    employees = ["alice chen", "bob martinez", "carol davis"]
    formatted = [name.title() for name in employees]
    print(f"Formatted names: {formatted}")

    # Clean: extract dollar amounts (as floats) from formatted strings
    revenue_strings = ["$42,000", "$38,500", "$51,200"]
    amounts = [float(s.replace("$", "").replace(",", "")) for s in revenue_strings]
    print(f"Numeric amounts: {amounts}")


def demo_summarize_sales():
    """A function that returns five summary values bundled as a tuple."""

    def summarize_sales(sales):
        """Calculate summary statistics for a list of sales figures.

        Args:
            sales: A list of numeric sales values.

        Returns:
            A tuple of (total, average, highest, lowest, count).
        """
        return (
            sum(sales),
            sum(sales) / len(sales),
            max(sales),
            min(sales),
            len(sales),
        )

    q1_sales = [42000, 38500, 51200]
    q2_sales = [47800, 39900, 55100]

    # Unpack the five returned values into separate variables
    q1_total, q1_avg, q1_high, q1_low, q1_count = summarize_sales(sales=q1_sales)
    q2_total, q2_avg, q2_high, q2_low, q2_count = summarize_sales(sales=q2_sales)

    print("Q1 Summary:")
    print(f"  Total:   ${q1_total:>10,.2f}")
    print(f"  Average: ${q1_avg:>10,.2f}")
    print(f"  Highest: ${q1_high:>10,.2f}")
    print(f"  Lowest:  ${q1_low:>10,.2f}")
    print(f"  Count:   {q1_count} months")

    print("\nQ2 Summary:")
    print(f"  Total:   ${q2_total:>10,.2f}")
    print(f"  Average: ${q2_avg:>10,.2f}")
    print(f"  Highest: ${q2_high:>10,.2f}")
    print(f"  Lowest:  ${q2_low:>10,.2f}")
    print(f"  Count:   {q2_count} months")


def demo_tuple_basics():
    """Reading from a tuple by index, and the error raised by assignment."""
    # Creating and reading from tuples
    employee = ("Alice Chen", "Marketing", 72000)

    print(f"Name: {employee[0]}")
    print(f"Department: {employee[1]}")
    print(f"Salary: ${employee[2]:,}")
    print(f"Length: {len(employee)}")

    # Tuples are immutable — assigning to an index raises TypeError
    product = ("Laptop", 999.99, True)

    try:
        product[1] = 899.99  # TypeError!
    except TypeError as e:
        print(f"\nError: {e}")

    print(f"Original tuple unchanged: {product}")


def demo_tuple_unpacking():
    """Unpacking records, looping with enumerate()+zip(), and swapping values."""
    # Unpacking a tuple into named variables
    record = ("Bob Martinez", "Sales", 68000, "Houston")

    name, department, salary, city = record

    print(f"Employee: {name}")
    print(f"Department: {department}")
    print(f"Salary: ${salary:,}")
    print(f"City: {city}")

    # Unpacking is what makes enumerate() and zip() so clean
    products = ["Laptop", "Monitor", "Keyboard"]
    prices = [999.99, 349.50, 79.95]

    print("\nProduct Catalog:")
    for i, (product, price) in enumerate(zip(products, prices)):
        print(f"  {i + 1}. {product}: ${price:.2f}")

    # Swap two variables without a temporary variable
    first = "Marketing"
    second = "Sales"
    print(f"\nBefore swap: first={first}, second={second}")

    first, second = second, first
    print(f"After swap:  first={first}, second={second}")


def demo_analyze_scores():
    """A function returning (minimum, maximum, average) unpacked at the call site."""

    def analyze_scores(scores):
        """Calculate the min, max, and average of a list of scores.

        Args:
            scores: A list of numeric scores.

        Returns:
            A tuple of (minimum, maximum, average).
        """
        minimum = min(scores)
        maximum = max(scores)
        average = sum(scores) / len(scores)
        return minimum, maximum, average

    customer_ratings = [4.5, 3.8, 4.9, 2.1, 4.7, 3.5, 4.2]

    # Unpack the three returned values
    low, high, avg = analyze_scores(scores=customer_ratings)

    print("Customer Ratings Analysis:")
    print(f"  Ratings: {customer_ratings}")
    print(f"  Lowest:  {low}")
    print(f"  Highest: {high}")
    print(f"  Average: {avg:.1f}")


def demo_aliasing_and_copy():
    """Two names for one list versus an independent .copy()."""
    # Lists are mutable — changes affect the same object
    departments = ["Marketing", "Sales", "Engineering"]
    backup = departments  # this does NOT make a copy!

    departments.append("Finance")
    print(f"Original: {departments}")
    print(f"Backup:   {backup}")  # also changed!
    print(f"Same object? {departments is backup}")

    # Making a proper copy of a list
    original = [10, 20, 30, 40]
    copy = original.copy()

    original.append(50)
    print(f"\nOriginal: {original}")
    print(f"Copy:     {copy}")  # unchanged
    print(f"Same object? {original is copy}")


def demo_sales_performance_report():
    """Capstone: lists, tuples, unpacking, functions, and comprehensions together."""
    # Sales data: each tuple is (name, region, [monthly sales])
    sales_team = [
        ("Alice Chen", "West", [42000, 38500, 51200]),
        ("Bob Martinez", "South", [35000, 41000, 37500]),
        ("Carol Davis", "East", [48000, 52000, 46500]),
        ("Dave Kim", "West", [31000, 33500, 40000]),
        ("Eve Johnson", "South", [55000, 48000, 53000]),
    ]

    def calculate_rep_total(monthly_sales):
        """Calculate total sales from a list of monthly figures."""
        return sum(monthly_sales)

    def format_currency(value):
        """Format a number as $X,XXX.XX."""
        return f"${value:,.2f}"

    def classify_performance(total, threshold=120000):
        """Classify a rep as 'Above Target' or 'Below Target'."""
        if total >= threshold:
            return "Above Target"
        return "Below Target"

    # Process each rep and build a results list
    results = []
    for name, region, monthly in sales_team:
        total = calculate_rep_total(monthly_sales=monthly)
        status = classify_performance(total=total)
        results.append((name, region, total, status))

    # Display the report
    print("=" * 65)
    print("  QUARTERLY SALES PERFORMANCE REPORT")
    print(f"  (Target: {format_currency(120000)} per rep)")
    print("=" * 65)
    print(f"  {'Name':<18} {'Region':<8} {'Total':>12} {'Status'}")
    print("-" * 65)

    for name, region, total, status in results:
        print(
            f"  {name:<18} "
            f"{region:<8} "
            f"{format_currency(total):>12} "
            f"{status}"
        )

    # Summary statistics using comprehensions
    all_totals = [total for _, _, total, _ in results]
    team_total = sum(all_totals)
    team_avg = team_total / len(all_totals)
    top_performers = [
        name for name, _, _, status in results
        if status == "Above Target"
    ]

    print("-" * 65)
    print(f"  Team Total: {format_currency(team_total)}")
    print(f"  Team Average: {format_currency(team_avg)}")
    print(f"  Top Performers: {', '.join(top_performers)}")
    print("=" * 65)


if __name__ == "__main__":
    demos = [
        ("Section 6.1", demo_creating_lists),
        ("Section 6.1", demo_indexing_and_updating),
        ("Section 6.1", demo_slicing),
        ("Section 6.2", demo_adding_and_removing),
        ("Section 6.2", demo_sorting),
        ("Section 6.3", demo_loop_totals),
        ("Section 6.3", demo_enumerate_reports),
        ("Section 6.3", demo_accumulator_filter),
        ("Section 6.4", demo_comprehension_vs_loop),
        ("Section 6.4", demo_comprehension_filters),
        ("Section 6.5", demo_summarize_sales),
        ("Section 6.5", demo_tuple_basics),
        ("Section 6.5", demo_tuple_unpacking),
        ("Section 6.5", demo_analyze_scores),
        ("Section 6.5", demo_aliasing_and_copy),
        ("Section 6.5", demo_sales_performance_report),
    ]
    for section, demo in demos:
        print("=" * 72)
        print(f"{demo.__name__} — Module 6, {section}")
        print("=" * 72)
        demo()
        print()
