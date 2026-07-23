"""Module 4 worked-example computations for the MIS 501 Course Companion.

Every demo_*() function below reproduces exactly one Worked Example in
docs/modules/04-functions.md. Run this script directly to print each
example's output under a separator header, in the same order the examples
appear in the chapter.

References in Course Companion:
    demo_dry_before_and_after()         -> Module 4, Section 4.1 (From Repetition to Reuse: The DRY Principle)
    demo_define_and_call()              -> Module 4, Section 4.2 (Function Fundamentals: Defining, Calling, and Returning)
    demo_calling_requires_parentheses() -> Module 4, Section 4.2 (Function Fundamentals: Defining, Calling, and Returning)
    demo_parameters_and_arguments()     -> Module 4, Section 4.2 (Function Fundamentals: Defining, Calling, and Returning)
    demo_return_vs_print()              -> Module 4, Section 4.2 (Function Fundamentals: Defining, Calling, and Returning)
    demo_positional_order_matters()     -> Module 4, Section 4.2 (Function Fundamentals: Defining, Calling, and Returning)
    demo_keyword_arguments()            -> Module 4, Section 4.3 (Keyword Arguments and Default Values)
    demo_default_parameters()           -> Module 4, Section 4.3 (Keyword Arguments and Default Values)
    demo_global_vs_local()              -> Module 4, Section 4.4 (Variable Scope and Docstrings)
    demo_local_scope_and_shadowing()    -> Module 4, Section 4.4 (Variable Scope and Docstrings)
    demo_docstrings()                   -> Module 4, Section 4.4 (Variable Scope and Docstrings)
    demo_refactoring_before_and_after() -> Module 4, Section 4.5 (Modular Thinking: Refactoring, Lambdas, and the Payroll Report)
    demo_lambda_basics()                -> Module 4, Section 4.5 (Modular Thinking: Refactoring, Lambdas, and the Payroll Report)
    demo_lambda_sort()                  -> Module 4, Section 4.5 (Modular Thinking: Refactoring, Lambdas, and the Payroll Report)
    demo_payroll_report()               -> Module 4, Section 4.5 (Modular Thinking: Refactoring, Lambdas, and the Payroll Report)

Last updated: 2026-07-23
"""

# Module-level global used by demo_global_vs_local(). The demo resets it to 0
# at the start of every call so its output is deterministic on every run.
count = 0


def demo_dry_before_and_after():
    """The same tax calculation copied three times vs. written once as a function."""
    print("--- Without a function: the same logic three times ---")

    # Shopping cart
    cart_subtotal = 150.00
    cart_tax = cart_subtotal * 0.0825
    cart_total = cart_subtotal + cart_tax
    print(f"Cart total: ${cart_total:.2f}")

    # Invoice
    invoice_subtotal = 150.00
    invoice_tax = invoice_subtotal * 0.0825
    invoice_total = invoice_subtotal + invoice_tax
    print(f"Invoice total: ${invoice_total:.2f}")

    # Annual report line item
    report_subtotal = 150.00
    report_tax = report_subtotal * 0.0825
    report_total = report_subtotal + report_tax
    print(f"Report total: ${report_total:.2f}")

    print()
    print("--- With a function: write the logic once, use it anywhere ---")

    def calculate_total(subtotal):
        tax = subtotal * 0.0825
        return subtotal + tax

    print(f"Cart total: ${calculate_total(150.00):.2f}")
    print(f"Invoice total: ${calculate_total(150.00):.2f}")
    print(f"Report total: ${calculate_total(150.00):.2f}")


def demo_define_and_call():
    """Defining a function registers it; calling it runs the body."""
    # A simple function that greets someone by name
    def greet(name):
        return f"Hello, {name}! Welcome to MIS 501."

    # Nothing happens until we CALL the function
    message = greet("Alice")
    print(message)


def demo_calling_requires_parentheses():
    """Parentheses run the function; the bare name is just the function object."""
    # A function with no parameters
    def print_separator():
        print("=" * 40)

    print_separator()              # correct — runs the function body
    print(type(print_separator))   # no parentheses — the function object itself


def demo_parameters_and_arguments():
    """Parameters are labeled slots; arguments are the values you plug in."""
    # Business example: calculate sales tax
    def calculate_tax(amount, rate):
        return amount * rate

    purchase = 249.99
    tax = calculate_tax(purchase, 0.0825)
    print(f"Purchase: ${purchase:.2f}")
    print(f"Tax (8.25%): ${tax:.2f}")
    print(f"Total: ${purchase + tax:.2f}")


def demo_return_vs_print():
    """print() displays a value but returns None; return hands the value back."""
    def bad_add(a, b):
        print(a + b)   # displays the result but returns None

    def good_add(a, b):
        return a + b   # returns the result so you can use it

    result_bad = bad_add(3, 4)     # prints 7, but result_bad is None
    result_good = good_add(3, 4)   # returns 7, stored in result_good

    print(f"bad_add returned: {result_bad}")
    print(f"good_add returned: {result_good}")
    print(f"good_add result * 2 = {result_good * 2}")  # we can do math with it


def demo_positional_order_matters():
    """Swapping positional arguments silently produces a wrong answer."""
    # Shipping cost calculator — order of arguments matters
    def calculate_shipping(weight, distance):
        base_rate = 5.00
        per_pound = 0.50
        per_mile = 0.02
        return base_rate + (weight * per_pound) + (distance * per_mile)

    # Correct order: weight=10, distance=200
    cost_correct = calculate_shipping(10, 200)
    print(f"Correct (10 lbs, 200 mi): ${cost_correct:.2f}")

    # Swapped order: weight=200, distance=10 — wrong result!
    cost_swapped = calculate_shipping(200, 10)
    print(f"Swapped (200 lbs, 10 mi): ${cost_swapped:.2f}")


def demo_keyword_arguments():
    """Keyword arguments name every value, so order no longer matters."""
    def calculate_shipping(weight, distance):
        base_rate = 5.00
        per_pound = 0.50
        per_mile = 0.02
        return base_rate + (weight * per_pound) + (distance * per_mile)

    # With keyword arguments — the call documents itself
    cost = calculate_shipping(
        weight=10,
        distance=200,
    )
    print(f"Shipping cost: ${cost:.2f}")

    # You can even reverse the order — same result
    cost_reversed = calculate_shipping(
        distance=200,
        weight=10,
    )
    print(f"Same result: ${cost_reversed:.2f}")


def demo_default_parameters():
    """Default values make parameters optional; callers override only what differs."""
    def calculate_total(price, tax_rate=0.0825, discount=0):
        discounted = price * (1 - discount)
        return discounted * (1 + tax_rate)

    # Use all defaults
    total_default = calculate_total(price=100)
    print(f"$100, default tax, no discount: ${total_default:.2f}")

    # Override just the discount
    total_discounted = calculate_total(
        price=100,
        discount=0.10,
    )
    print(f"$100, default tax, 10% discount: ${total_discounted:.2f}")

    # Override both
    total_custom = calculate_total(
        price=100,
        tax_rate=0.06,
        discount=0.15,
    )
    print(f"$100, 6% tax, 15% discount: ${total_custom:.2f}")


def demo_global_vs_local():
    """Reading a global, modifying it with `global`, and creating a local instead."""
    global count
    count = 0  # reset the module-level global so every run prints the same output

    # Example 1: Reading a global variable
    def read_global():
        print(f"Global count = {count}")

    read_global()

    # Example 2: Modifying a global variable (requires the 'global' keyword)
    def modify_global():
        global count
        count = 20
        print(f"Modified count = {count}")

    modify_global()
    print(f"Global count is now {count}\n")

    # Example 3: Assignment creates a LOCAL variable (does not affect the global)
    def create_local():
        count = 30  # this is a NEW local variable, not the global one
        print(f"Local count = {count}")

    create_local()
    print(f"Global count is still {count}")


def demo_local_scope_and_shadowing():
    """Locals vanish when the function ends; same-named locals shadow outer values."""
    company = "Acme Corp"  # defined outside the function

    def show_employee():
        employee = "Alice"  # local — only exists inside this function
        print(f"{employee} works at {company}")

    show_employee()

    # employee does not exist out here
    try:
        print(employee)
    except NameError as e:
        print(f"Error: {e}")

    # A local with the same name as an outer variable — they are different
    value = 100

    def double_value():
        value = 200  # this is a NEW local variable, not the outer one
        print(f"Inside function: {value}")

    double_value()
    print(f"Outside function: {value}")  # still 100


def demo_docstrings():
    """A triple-quoted docstring documents the function and feeds help()."""
    def apply_discount(price, percentage):
        """Calculate the discounted price.

        Args:
            price: Original price in dollars.
            percentage: Discount as a decimal (e.g., 0.10 for 10%).

        Returns:
            The price after applying the discount.
        """
        return price * (1 - percentage)

    # Call the function
    sale_price = apply_discount(
        price=79.99,
        percentage=0.25,
    )
    print("Original: $79.99")
    print(f"After 25% discount: ${sale_price:.2f}")

    # The docstring is accessible via help()
    help(apply_discount)


def demo_refactoring_before_and_after():
    """Repeated payroll logic refactored into three small functions plus a loop."""
    print("--- Before: the same payroll logic copied three times ---")

    # Employee 1
    hours1 = 45
    rate1 = 35.00
    if hours1 > 40:
        gross1 = (40 * rate1) + ((hours1 - 40) * rate1 * 1.5)
    else:
        gross1 = hours1 * rate1
    tax1 = gross1 * 0.22
    net1 = gross1 - tax1
    print(f"Employee 1: gross=${gross1:.2f}, tax=${tax1:.2f}, net=${net1:.2f}")

    # Employee 2
    hours2 = 38
    rate2 = 28.00
    if hours2 > 40:
        gross2 = (40 * rate2) + ((hours2 - 40) * rate2 * 1.5)
    else:
        gross2 = hours2 * rate2
    tax2 = gross2 * 0.22
    net2 = gross2 - tax2
    print(f"Employee 2: gross=${gross2:.2f}, tax=${tax2:.2f}, net=${net2:.2f}")

    # Employee 3
    hours3 = 50
    rate3 = 42.00
    if hours3 > 40:
        gross3 = (40 * rate3) + ((hours3 - 40) * rate3 * 1.5)
    else:
        gross3 = hours3 * rate3
    tax3 = gross3 * 0.22
    net3 = gross3 - tax3
    print(f"Employee 3: gross=${gross3:.2f}, tax=${tax3:.2f}, net=${net3:.2f}")

    print()
    print("--- After: clean, reusable functions ---")

    def calculate_gross(hours, rate, overtime_multiplier=1.5):
        """Calculate gross pay with overtime for hours over 40."""
        if hours > 40:
            regular = 40 * rate
            overtime = (hours - 40) * rate * overtime_multiplier
            return regular + overtime
        return hours * rate

    def calculate_tax(gross, tax_rate=0.22):
        """Calculate tax amount from gross pay."""
        return gross * tax_rate

    def calculate_net(gross, tax):
        """Calculate net pay (gross minus tax)."""
        return gross - tax

    # Now processing any employee is three clean lines
    employees = [
        ("Alice", 45, 35.00),
        ("Bob", 38, 28.00),
        ("Carol", 50, 42.00),
    ]

    for name, hours, rate in employees:
        gross = calculate_gross(hours=hours, rate=rate)
        tax = calculate_tax(gross=gross)
        net = calculate_net(gross=gross, tax=tax)
        print(f"{name}: gross=${gross:.2f}, tax=${tax:.2f}, net=${net:.2f}")


def demo_lambda_basics():
    """A lambda is an anonymous one-expression function."""
    # Regular function vs. lambda — same result
    def double(x):
        return x * 2

    double_lambda = lambda x: x * 2

    print(f"Function: {double(5)}")
    print(f"Lambda: {double_lambda(5)}")


def demo_lambda_sort():
    """Lambdas shine as sort keys — order products by price."""
    products = [
        ("Laptop Stand", 34.99),
        ("USB Hub", 12.50),
        ("Monitor Cable", 8.75),
        ("Desk Lamp", 45.00),
        ("Keyboard", 29.99),
    ]

    # Sort by price (the second element of each tuple)
    sorted_products = sorted(
        products,
        key=lambda item: item[1],
    )

    print("Products sorted by price:")
    for name, price in sorted_products:
        print(f"  {name}: ${price:.2f}")


def demo_payroll_report():
    """Capstone example: parameters, defaults, keyword args, and docstrings together."""
    def calculate_gross_pay(hours, hourly_rate, overtime_multiplier=1.5):
        """Calculate gross pay with overtime for hours exceeding 40.

        Args:
            hours: Total hours worked.
            hourly_rate: Base pay rate per hour.
            overtime_multiplier: Multiplier for overtime hours (default 1.5x).

        Returns:
            Total gross pay as a float.
        """
        if hours > 40:
            regular = 40 * hourly_rate
            overtime = (hours - 40) * hourly_rate * overtime_multiplier
            return regular + overtime
        return hours * hourly_rate

    def apply_tax(amount, rate=0.22):
        """Calculate the tax on an amount.

        Args:
            amount: The taxable amount.
            rate: Tax rate as a decimal (default 0.22 for 22%).

        Returns:
            The tax amount.
        """
        return amount * rate

    def format_currency(value):
        """Format a number as a dollar string with commas and two decimals."""
        return f"${value:,.2f}"

    def format_report_line(name, gross, tax, net):
        """Format one line of the payroll report."""
        return (
            f"  {name:<10}"
            f" Gross: {format_currency(gross):>10}"
            f" | Tax: {format_currency(tax):>9}"
            f" | Net: {format_currency(net):>10}"
        )

    # Employee data: (name, hours, rate)
    employees = [
        ("Alice", 45, 52.00),
        ("Bob", 40, 38.00),
        ("Carol", 50, 45.00),
        ("Dave", 35, 30.00),
    ]

    total_payroll = 0

    print("=" * 62)
    print("  WEEKLY PAYROLL REPORT")
    print("=" * 62)

    for name, hours, rate in employees:
        gross = calculate_gross_pay(
            hours=hours,
            hourly_rate=rate,
        )
        tax = apply_tax(amount=gross)
        net = gross - tax
        total_payroll = total_payroll + net
        print(format_report_line(
            name=name,
            gross=gross,
            tax=tax,
            net=net,
        ))

    print("-" * 62)
    print(f"  Total net payroll: {format_currency(total_payroll)}")
    print("=" * 62)


if __name__ == "__main__":
    demos = [
        ("Section 4.1", demo_dry_before_and_after),
        ("Section 4.2", demo_define_and_call),
        ("Section 4.2", demo_calling_requires_parentheses),
        ("Section 4.2", demo_parameters_and_arguments),
        ("Section 4.2", demo_return_vs_print),
        ("Section 4.2", demo_positional_order_matters),
        ("Section 4.3", demo_keyword_arguments),
        ("Section 4.3", demo_default_parameters),
        ("Section 4.4", demo_global_vs_local),
        ("Section 4.4", demo_local_scope_and_shadowing),
        ("Section 4.4", demo_docstrings),
        ("Section 4.5", demo_refactoring_before_and_after),
        ("Section 4.5", demo_lambda_basics),
        ("Section 4.5", demo_lambda_sort),
        ("Section 4.5", demo_payroll_report),
    ]
    for section, demo in demos:
        print("=" * 72)
        print(f"{demo.__name__} — Module 4, {section}")
        print("=" * 72)
        demo()
        print()
