"""Module 1 worked-example computations for the MIS501 Course Companion.

Every demo_*() function below reproduces exactly one Worked Example in
docs/modules/01-why-python-and-setup.md. Run this script directly to print
each example's output under a separator header, in the same order the
examples appear in the chapter.

Module 1 is primarily a tooling module (why Python, Pixi, marimo), so its
runnable-Python surface is small: arithmetic sanity checks, print(),
variables, and comments — mirroring the teaching notebook's code cells.

References in Course Companion:
    demo_python_as_calculator()  -> Module 1, Section 1.4 (Your First Python Code)
    demo_profit_margin()         -> Module 1, Section 1.4 (Your First Python Code)
    demo_print_basics()          -> Module 1, Section 1.5 (print(), Variables, and Comments)
    demo_variables_first_look()  -> Module 1, Section 1.5 (print(), Variables, and Comments)
    demo_roi_with_comments()     -> Module 1, Section 1.5 (print(), Variables, and Comments)

Last updated: 2026-07-23
"""


def demo_python_as_calculator():
    """Python evaluates arithmetic expressions like a calculator."""
    # Your first Python expression — just like using a calculator
    print("2 + 2 =", 2 + 2)

    # The standard arithmetic operators
    print("10 + 5 =", 10 + 5)    # addition
    print("10 - 5 =", 10 - 5)    # subtraction
    print("10 * 5 =", 10 * 5)    # multiplication
    print("10 / 5 =", 10 / 5)    # division
    print("10 ** 2 =", 10 ** 2)  # exponent (power)
    print("10 // 3 =", 10 // 3)  # integer division
    print("10 % 3 =", 10 % 3)    # remainder (modulo)


def demo_profit_margin():
    """The module's first business calculation: quarterly profit margin."""
    # Calculate profit margin
    revenue = 450000
    costs = 320000
    profit = revenue - costs
    margin = (profit / revenue) * 100

    print("Revenue:", revenue)
    print("Costs:", costs)
    print("Profit:", profit)
    print("Profit margin:", margin)


def demo_print_basics():
    """print() displays text and as many labeled values as you want."""
    # print() lets you display text and values
    print("Hello, MIS501!")

    # You can print as many values as you want, each on its own line
    revenue = 450000
    costs = 320000
    profit = revenue - costs

    print("Revenue:", revenue)
    print("Costs:", costs)
    print("Profit:", profit)


def demo_variables_first_look():
    """Variables store values under descriptive names for later use."""
    # Variables store values for later use
    items_sold = 1200
    price_per_item = 29.99

    total_revenue = items_sold * price_per_item
    print("Items sold:", items_sold)
    print("Price per item:", price_per_item)
    print("Total revenue:", total_revenue)


def demo_roi_with_comments():
    """Comments document the why behind a return-on-investment calculation."""
    # Calculate return on investment (ROI)
    # ROI = (gain from investment - cost of investment) / cost of investment

    investment_cost = 50000    # Marketing campaign budget
    revenue_gained = 73000     # Revenue attributed to the campaign

    roi = (revenue_gained - investment_cost) / investment_cost
    print("Investment cost:", investment_cost)
    print("Revenue gained:", revenue_gained)
    print("ROI:", roi)
    print("ROI as percentage:", roi * 100, "%")


if __name__ == "__main__":
    demos = [
        ("Section 1.4", demo_python_as_calculator),
        ("Section 1.4", demo_profit_margin),
        ("Section 1.5", demo_print_basics),
        ("Section 1.5", demo_variables_first_look),
        ("Section 1.5", demo_roi_with_comments),
    ]
    for section, demo in demos:
        print("=" * 72)
        print(f"{demo.__name__} — Module 1, {section}")
        print("=" * 72)
        demo()
        print()
