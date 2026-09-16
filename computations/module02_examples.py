"""Module 2 worked-example computations for the MIS501 Course Companion.

Every demo_*() function below reproduces exactly one Worked Example in
docs/modules/02-variables-and-types.md. Run this script directly to print
each example's output under a separator header, in the same order the
examples appear in the chapter.

References in Course Companion:
    demo_descriptive_variables()      -> Module 2, Section 2.1 (Variables and Assignment)
    demo_reassignment()               -> Module 2, Section 2.1 (Variables and Assignment)
    demo_ints_and_floats()            -> Module 2, Section 2.2 (Core Data Types)
    demo_strings_and_concatenation()  -> Module 2, Section 2.2 (Core Data Types)
    demo_booleans()                   -> Module 2, Section 2.2 (Core Data Types)
    demo_compound_interest()          -> Module 2, Section 2.3 (Arithmetic and Comparison Operators)
    demo_comparison_operators()       -> Module 2, Section 2.3 (Arithmetic and Comparison Operators)
    demo_dynamic_typing()             -> Module 2, Section 2.4 (Dynamic Typing and Type Conversion)
    demo_type_conversion()            -> Module 2, Section 2.4 (Dynamic Typing and Type Conversion)
    demo_truthy_falsy()               -> Module 2, Section 2.4 (Dynamic Typing and Type Conversion)
    demo_fstring_basics()             -> Module 2, Section 2.5 (F-Strings: Clean Output Formatting)
    demo_fstring_number_formats()     -> Module 2, Section 2.5 (F-Strings: Clean Output Formatting)
    demo_sales_report()               -> Module 2, Section 2.5 (F-Strings: Clean Output Formatting)

Last updated: 2026-07-23
"""


def demo_descriptive_variables():
    """Descriptive snake_case variable names in a revenue calculation."""
    # Good variable names — descriptive and snake_case
    quarterly_revenue = 128500
    customer_count = 342
    average_order_value = quarterly_revenue / customer_count

    print("Quarterly revenue:", quarterly_revenue)
    print("Customer count:", customer_count)
    print("Average order value:", average_order_value)


def demo_reassignment():
    """Assigning a new value to an existing variable replaces the old one."""
    price = 19.99
    print("Original price:", price)

    price = 24.99
    print("Updated price:", price)


def demo_ints_and_floats():
    """Integers for counts, floats for prices; int * float produces a float."""
    units_sold = 500          # int — a count
    unit_price = 12.50        # float — a price
    total = units_sold * unit_price  # int * float = float

    print("Units sold:", units_sold, "  type:", type(units_sold))
    print("Unit price:", unit_price, "  type:", type(unit_price))
    print("Total:", total, "  type:", type(total))


def demo_strings_and_concatenation():
    """Strings hold text — including 'numbers' that are labels — and join with +."""
    company = "Northwind Traders"
    department = "Marketing"
    employee_id = "EMP-2847"

    print("Company:", company)
    print("Department:", department)
    print("Employee ID:", employee_id)

    first_name = "Sarah"
    last_name = "Chen"

    # Concatenation joins strings together
    full_name = first_name + " " + last_name
    print("Full name:", full_name)


def demo_booleans():
    """Booleans answer yes/no questions with True or False."""
    is_active_customer = True
    has_overdue_invoice = False

    print("Active customer?", is_active_customer)
    print("Overdue invoice?", has_overdue_invoice)


def demo_compound_interest():
    """Operator precedence in the compound interest formula A = P * (1 + r) ** n."""
    # Compound interest: A = P * (1 + r) ** n
    # How much is $10,000 worth after 5 years at 7% annual return?
    principal = 10000
    rate = 0.07
    years = 5

    future_value = principal * (1 + rate) ** years
    print("Future value:", future_value)


def demo_comparison_operators():
    """Comparison operators return booleans — revenue vs. target."""
    monthly_revenue = 45000
    monthly_target = 50000

    on_target = monthly_revenue >= monthly_target
    gap = monthly_target - monthly_revenue

    print("Revenue:", monthly_revenue)
    print("Target:", monthly_target)
    print("Met target?", on_target)
    print("Gap to target:", gap)


def demo_dynamic_typing():
    """One variable can hold values of different types over its lifetime."""
    value = 42
    print(value, "is", type(value))

    value = 42.0
    print(value, "is", type(value))

    value = "forty-two"
    print(value, "is", type(value))

    value = True
    print(value, "is", type(value))


def demo_type_conversion():
    """Convert CSV-style text to numbers before doing math."""
    # Simulating data that arrived as text from a CSV
    revenue_text = "52300"
    expenses_text = "41800"

    # This would fail: revenue_text - expenses_text (can't subtract strings)

    # Convert to numbers first
    revenue = float(revenue_text)
    expenses = float(expenses_text)
    profit = revenue - expenses

    print("Revenue (as number):", revenue)
    print("Expenses (as number):", expenses)
    print("Profit:", profit)


def demo_truthy_falsy():
    """How Python converts other types to booleans."""
    print("bool(0):", bool(0))
    print("bool(42):", bool(42))
    print('bool(""):', bool(""))
    print('bool("hello"):', bool("hello"))


def demo_fstring_basics():
    """F-strings insert variable values into text through curly braces."""
    product = "Premium Widget"
    quantity = 250
    unit_price = 34.99
    total = quantity * unit_price

    print(f"Product: {product}")
    print(f"Quantity: {quantity} units")
    print(f"Unit price: ${unit_price}")
    print(f"Total: ${total}")


def demo_fstring_number_formats():
    """Format specifiers produce report-ready numbers."""
    annual_revenue = 2847563.50
    annual_expenses = 1923841.75
    profit = annual_revenue - annual_expenses
    margin = profit / annual_revenue

    print(f"Annual Revenue:  ${annual_revenue:,.2f}")
    print(f"Annual Expenses: ${annual_expenses:,.2f}")
    print(f"Profit:          ${profit:,.2f}")
    print(f"Profit Margin:   {margin:.1%}")


def demo_sales_report():
    """Capstone example: variables, arithmetic, comparison, and f-strings together."""
    # Sales report for Q3
    product_name = "CloudSync Pro"
    units_q1 = 1340
    units_q2 = 1580
    units_q3 = 1875
    price_per_unit = 49.99

    # Calculate totals
    total_units = units_q1 + units_q2 + units_q3
    total_revenue = total_units * price_per_unit
    avg_units_per_quarter = total_units / 3

    # Growth from Q1 to Q3
    growth_rate = (units_q3 - units_q1) / units_q1

    # Check if we hit the annual target of 5,000 units
    annual_target = 5000
    on_track = total_units >= annual_target

    print(f"=== Sales Report: {product_name} ===")
    print(f"Units Sold — Q1: {units_q1:,}  Q2: {units_q2:,}  Q3: {units_q3:,}")
    print(f"Total units (3 quarters): {total_units:,}")
    print(f"Total revenue: ${total_revenue:,.2f}")
    print(f"Avg units/quarter: {avg_units_per_quarter:,.0f}")
    print(f"Growth (Q1 to Q3): {growth_rate:.1%}")
    print(f"Annual target: {annual_target:,} units")
    print(f"Target reached? {on_track}")


if __name__ == "__main__":
    demos = [
        ("Section 2.1", demo_descriptive_variables),
        ("Section 2.1", demo_reassignment),
        ("Section 2.2", demo_ints_and_floats),
        ("Section 2.2", demo_strings_and_concatenation),
        ("Section 2.2", demo_booleans),
        ("Section 2.3", demo_compound_interest),
        ("Section 2.3", demo_comparison_operators),
        ("Section 2.4", demo_dynamic_typing),
        ("Section 2.4", demo_type_conversion),
        ("Section 2.4", demo_truthy_falsy),
        ("Section 2.5", demo_fstring_basics),
        ("Section 2.5", demo_fstring_number_formats),
        ("Section 2.5", demo_sales_report),
    ]
    for section, demo in demos:
        print("=" * 72)
        print(f"{demo.__name__} — Module 2, {section}")
        print("=" * 72)
        demo()
        print()
