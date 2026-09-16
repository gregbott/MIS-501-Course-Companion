"""Module 3 worked-example computations for the MIS501 Course Companion.

Every demo_*() function below reproduces exactly one Worked Example in
docs/modules/03-control-flow.md. Run this script directly to print each
example's output under a separator header, in the same order the examples
appear in the chapter.

References in Course Companion:
    demo_simple_if()              -> Module 3, Section 3.1 (Conditional Statements: if, elif, else)
    demo_if_else()                -> Module 3, Section 3.1 (Conditional Statements: if, elif, else)
    demo_elif_chain()             -> Module 3, Section 3.1 (Conditional Statements: if, elif, else)
    demo_loan_approval()          -> Module 3, Section 3.2 (Logical Operators: and, or, not)
    demo_promo_or()               -> Module 3, Section 3.2 (Logical Operators: and, or, not)
    demo_transaction_check()      -> Module 3, Section 3.2 (Logical Operators: and, or, not)
    demo_countdown()              -> Module 3, Section 3.3 (for Loops and range())
    demo_revenue_projection()     -> Module 3, Section 3.3 (for Loops and range())
    demo_batch_shipping()         -> Module 3, Section 3.3 (for Loops and range())
    demo_savings_goal()           -> Module 3, Section 3.4 (while Loops and Loop Control)
    demo_break_capacity()         -> Module 3, Section 3.4 (while Loops and Loop Control)
    demo_continue_invalid()       -> Module 3, Section 3.4 (while Loops and Loop Control)
    demo_nested_classification()  -> Module 3, Section 3.5 (Nested Logic and Common Loop Patterns)
    demo_order_processing()       -> Module 3, Section 3.5 (Nested Logic and Common Loop Patterns)

Last updated: 2026-07-23
"""


def demo_simple_if():
    """A single if — the indented block runs only when the condition is True."""
    order_total = 75.00
    free_shipping_threshold = 50.00

    # Simple if statement — checking an order total for free shipping
    if order_total >= free_shipping_threshold:
        print(f"Order total: ${order_total:.2f} — Free shipping!")


def demo_if_else():
    """if/else — one of two branches always runs."""
    order_total = 55.00
    free_shipping_threshold = 50.00
    shipping_fee = 7.99

    # if/else — apply shipping fee or free shipping
    if order_total >= free_shipping_threshold:
        final_total = order_total
        print(f"Order: ${order_total:.2f} + FREE shipping = ${final_total:.2f}")
    else:
        final_total = order_total + shipping_fee
        print(f"Order: ${order_total:.2f} + ${shipping_fee:.2f} = ${final_total:.2f}")


def demo_elif_chain():
    """elif chain — the first True condition wins; the rest are skipped."""
    annual_spending = 2800

    # Customer tier classification based on annual spending
    if annual_spending >= 5000:
        tier = "Platinum"
        discount = 0.20
    elif annual_spending >= 2000:
        tier = "Gold"
        discount = 0.15
    elif annual_spending >= 500:
        tier = "Silver"
        discount = 0.10
    else:
        tier = "Bronze"
        discount = 0.05

    print(f"Annual spending: ${annual_spending:,.2f}")
    print(f"Customer tier: {tier}")
    print(f"Discount: {discount:.0%}")


def demo_loan_approval():
    """and/not — every criterion must pass for approval."""
    age = 28
    annual_income = 55000
    has_bankruptcy = False

    # Loan approval: age >= 21 AND income >= 40000 AND no bankruptcies
    approved = age >= 21 and annual_income >= 40000 and not has_bankruptcy

    print(f"Age: {age} (min: 21)")
    print(f"Income: ${annual_income:,} (min: $40,000)")
    print(f"Bankruptcy on record: {has_bankruptcy}")
    print(f"Loan approved? {approved}")


def demo_promo_or():
    """or — one passing condition is enough."""
    is_member = False
    order_total = 125.00

    # Promotional discount: member OR order over $100
    gets_promo = is_member or order_total > 100

    print(f"Member? {is_member}")
    print(f"Order total: ${order_total:.2f}")
    print(f"Gets promotional discount? {gets_promo}")


def demo_transaction_check():
    """A combined boolean expression used directly as an if condition."""
    account_balance = 1500
    is_overdue = False
    credit_limit = 5000

    print(f"Balance: ${account_balance:,}  Credit limit: ${credit_limit:,}  Overdue: {is_overdue}")

    # Combining logical operators in an if statement
    if account_balance < credit_limit and not is_overdue:
        print("Transaction approved")
    else:
        print("Transaction declined")


def demo_countdown():
    """for loop over range() with a negative step — counting down."""
    print("Product launch countdown:")

    # Print a simple countdown for a product launch
    for day in range(5, 0, -1):
        print(f"  {day} days remaining...")
    print("  Launch day!")


def demo_revenue_projection():
    """Accumulating compound growth across loop iterations."""
    revenue = 100000
    growth_rate = 0.08

    print(f"Starting revenue: ${revenue:,} — projected growth: {growth_rate:.0%} per year")
    print()

    # <6 and >12 set left and right alignment for the column headers
    print(f"{'Year':<6} {'Revenue':>12}")
    print("-" * 20)  # "-" * 20 repeats the dash 20 times to draw a divider line

    # Project revenue growth at 8% per year for 5 years
    for year in range(1, 6):
        revenue = revenue * (1 + growth_rate)
        print(f"{year:<6} ${revenue:>11,.2f}")


def demo_batch_shipping():
    """Looping over a list, with an if/else applied to each item."""
    orders = [45.00, 120.50, 89.99, 210.00, 33.75]
    free_shipping_threshold = 50.00

    print(f"{'Order':>8}  {'Shipping':>10}")
    print("-" * 22)

    # Process a batch of order amounts
    for amount in orders:
        if amount >= free_shipping_threshold:
            print(f"${amount:>7.2f}  {'Free':>10}")
        else:
            print(f"${amount:>7.2f}  {'$7.99':>10}")


def demo_savings_goal():
    """while loop — repeat until the balance reaches the goal."""
    balance = 0
    monthly_deposit = 850
    goal = 10000
    months = 0

    # Savings goal: how many months to save $10,000?
    while balance < goal:
        balance = balance + monthly_deposit
        months = months + 1

    print(f"Monthly deposit: ${monthly_deposit:,}")
    print(f"Goal: ${goal:,}")
    print(f"Months to reach goal: {months}")
    print(f"Final balance: ${balance:,}")


def demo_break_capacity():
    """break — exit the loop as soon as adding an order would exceed capacity."""
    orders = [150, 200, 175, 300, 125, 250, 180]
    daily_capacity = 800
    total_processed = 0
    orders_processed = 0

    print(f"Daily processing capacity: ${daily_capacity}")
    print()

    # break — stop processing orders once we hit our daily capacity
    for order in orders:
        if total_processed + order > daily_capacity:
            print(f"Capacity reached — cannot add ${order} order")
            break
        total_processed = total_processed + order
        orders_processed = orders_processed + 1
        print(f"Processed order ${order} — running total: ${total_processed}")

    # len(orders) gives the number of items in the list
    print(f"\nOrders processed: {orders_processed} of {len(orders)}")
    print(f"Total value: ${total_processed}")


def demo_continue_invalid():
    """continue — skip invalid entries and keep processing the rest."""
    transactions = [250.00, -15.00, 89.50, 0, 175.25, -42.00, 310.00]
    valid_total = 0
    skipped = 0

    # continue — skip invalid entries when processing data
    for amount in transactions:
        if amount <= 0:
            skipped = skipped + 1
            continue  # skip to the next transaction
        valid_total = valid_total + amount

    print(f"Valid transaction total: ${valid_total:,.2f}")
    print(f"Skipped {skipped} invalid entries")


def demo_nested_classification():
    """An if/else nested inside a for loop, with two counters."""
    # Each item is a tuple: (customer name, order amount)
    orders = [
        ("Alice", 320.00),
        ("Bob", 45.00),
        ("Carol", 150.00),
        ("Dave", 520.00),
        ("Eve", 88.00),
    ]
    premium_threshold = 200.00
    premium_count = 0
    standard_count = 0

    print(f"Premium threshold: ${premium_threshold:.2f}")
    print()
    print(f"{'Customer':<10} {'Amount':>8}  {'Category':<10}")
    print("-" * 32)

    for name, amount in orders:
        if amount >= premium_threshold:
            category = "Premium"
            premium_count = premium_count + 1
        else:
            category = "Standard"
            standard_count = standard_count + 1
        print(f"{name:<10} ${amount:>7.2f}  {category:<10}")

    print(f"\nPremium orders: {premium_count}")
    print(f"Standard orders: {standard_count}")


def demo_order_processing():
    """Capstone: loops, conditionals, accumulators, and counters together."""
    # Order data: (product, quantity, unit_price)
    orders = [
        ("Laptop Stand", 25, 34.99),
        ("USB Hub", 100, 12.50),
        ("Monitor Cable", 60, 8.75),
        ("Desk Lamp", 10, 45.00),
        ("Keyboard", 75, 29.99),
    ]

    grand_total = 0
    flagged_count = 0

    print("=== Order Processing Report ===\n")

    for product, qty, price in orders:
        gross = qty * price
        subtotal = gross

        # Bulk discount for 50+ units
        if qty >= 50:
            subtotal = gross * 0.90
            note = f" (10% bulk discount → ${subtotal:,.2f})"
        else:
            note = ""

        # Flag large orders
        if subtotal > 1000:
            note = note + " *** MANAGER APPROVAL ***"
            flagged_count = flagged_count + 1

        grand_total = grand_total + subtotal
        print(f"  {product}: {qty} x ${price:.2f} = ${gross:,.2f}{note}")

    print(f"\nGrand total: ${grand_total:,.2f}")
    print(f"Orders flagged for approval: {flagged_count}")


if __name__ == "__main__":
    demos = [
        ("Section 3.1", demo_simple_if),
        ("Section 3.1", demo_if_else),
        ("Section 3.1", demo_elif_chain),
        ("Section 3.2", demo_loan_approval),
        ("Section 3.2", demo_promo_or),
        ("Section 3.2", demo_transaction_check),
        ("Section 3.3", demo_countdown),
        ("Section 3.3", demo_revenue_projection),
        ("Section 3.3", demo_batch_shipping),
        ("Section 3.4", demo_savings_goal),
        ("Section 3.4", demo_break_capacity),
        ("Section 3.4", demo_continue_invalid),
        ("Section 3.5", demo_nested_classification),
        ("Section 3.5", demo_order_processing),
    ]
    for section, demo in demos:
        print("=" * 72)
        print(f"{demo.__name__} — Module 3, {section}")
        print("=" * 72)
        demo()
        print()
