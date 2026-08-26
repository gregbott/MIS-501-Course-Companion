# Module 3: Control Flow

## Introduction

Up to now, your code has run straight through from top to bottom — every line executes once, in order. That is fine for simple calculations, but real business logic needs two additional capabilities: **making decisions** ("If the customer is a premium member, apply a 15% discount. Otherwise, apply 5%.") and **repeating tasks** ("For each invoice in the batch, calculate the total and flag any that are overdue."). These capabilities are called **control flow** because they control *which* lines of code run and *how many* times they run. This module gives you the full toolkit: `if`/`elif`/`else` for decisions, `and`/`or`/`not` for combining conditions, `for` and `while` loops for repetition, and `break`/`continue` for fine-grained loop control. By the end you will process a batch of purchase orders — applying discounts, flagging exceptions, and totaling results — in code that reads like a set of business rules written in English. This is where programming starts to feel genuinely powerful.

---

## Learning Objectives

By the end of this module, you should be able to:

1. **Write** conditional statements using `if`, `elif`, and `else`
2. **Combine** multiple conditions using the logical operators `and`, `or`, and `not`
3. **Use** `for` loops with `range()` and `while` loops to repeat actions
4. **Control** loop execution with `break` and `continue`
5. **Build** nested control structures for multi-step business logic
6. **Recognize** the accumulator, counter, and search patterns that cover most loops you will write

---

## 3.1 Conditional Statements: `if`, `elif`, `else`

An `if` statement lets your code make a decision. The structure is:

```python
if condition:
    # code that runs when condition is True
```

The condition is any expression that produces a boolean — usually a comparison like the ones you wrote in Module 2. When the condition is `True`, the indented block runs; when it is `False`, Python skips the block entirely.

**Indentation matters.** The indented block below the `if` is the code that runs conditionally. Python uses indentation (4 spaces) instead of braces or keywords to define blocks. This is different from most other languages, but it forces your code to be visually organized.

**Analogy:** think of an `if` statement like a doorway with a bouncer. The condition is the rule ("Are you on the list?"). If you meet the condition, you get through. If not, the bouncer sends you away.

!!! example "Worked Example: Free Shipping Check"

    ```python
    order_total = 75.00
    free_shipping_threshold = 50.00

    # Simple if statement — checking an order total for free shipping
    if order_total >= free_shipping_threshold:
        print(f"Order total: ${order_total:.2f} — Free shipping!")
    ```

    **Output:**

    ```
    Order total: $75.00 — Free shipping!
    ```

    **Interpretation:** The comparison `order_total >= free_shipping_threshold` evaluates to `True` because the $75.00 order clears the threshold, so the indented block runs and the message prints. When the condition is `False`, an `if` with no `else` simply does nothing — no message, and no error.

    *Source: `computations/module03_examples.py` — `demo_simple_if()`*

### Adding `else`

What if you want to do something different when the condition is `False`? That is what `else` is for:

```python
if condition:
    # runs when True
else:
    # runs when False
```

Exactly one of the two branches always executes — never both, never neither.

!!! example "Worked Example: Shipping Fee Decision"

    ```python
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
    ```

    **Output:**

    ```
    Order: $55.00 + FREE shipping = $55.00
    ```

    **Interpretation:** The $55.00 order qualifies for free shipping, so the `if` branch runs and the final total equals the order amount. Had the order fallen below the threshold, the `else` branch would have added the shipping fee instead — one of the two branches always runs.

    *Source: `computations/module03_examples.py` — `demo_if_else()`*

### Multiple Conditions with `elif`

When you have more than two possibilities, use `elif` (short for "else if"). Python checks each condition from top to bottom and runs the **first** one that is `True`:

```python
if condition_1:
    # runs if condition_1 is True
elif condition_2:
    # runs if condition_1 is False AND condition_2 is True
elif condition_3:
    # runs if the above are False AND condition_3 is True
else:
    # runs if none of the above are True
```

You can have as many `elif` blocks as you need. The `else` at the end is optional but is a good safety net to catch anything you did not anticipate.

!!! example "Worked Example: Customer Tier Classification"

    ```python
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
    ```

    **Output:**

    ```
    Annual spending: $2,800.00
    Customer tier: Gold
    Discount: 15%
    ```

    **Interpretation:** Python tests the conditions top to bottom: $2,800.00 fails the Platinum test but passes the Gold test, so the customer earns the 15% discount and the chain stops there — the Silver and Bronze conditions are never checked. The first `True` condition wins, which is why the thresholds are ordered from highest to lowest.

    *Source: `computations/module03_examples.py` — `demo_elif_chain()`*

!!! question "Try It Yourself: Grade Calculator"

    Write an `if`/`elif`/`else` block that assigns a letter grade based on a numeric
    score:

    - 90 and above: `"A"`
    - 80–89: `"B"`
    - 70–79: `"C"`
    - 60–69: `"D"`
    - Below 60: `"F"`

    Change the score value and re-run to test different cases.

    ```python
    score = 85

    # Write your if/elif/else block here
    # grade = ???

    # print(f"Score: {score} — Grade: {grade}")
    ```

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Every `if` needs an `else`. | `else` is optional. An `if` on its own simply does nothing when the condition is `False` — often exactly what you want. |
| Python checks every condition in an `if`/`elif` chain. | Python stops at the **first** `True` condition and skips the rest. Only one branch of the chain ever runs. |
| The order of `elif` conditions does not matter. | Because the first `True` wins, ordering is part of the logic. Testing `>= 500` before `>= 5000` would label every big spender "Silver". |
| Indentation is just cosmetic style. | Indentation *defines* which lines belong to the block. Wrong indentation changes what the code does — or raises an `IndentationError`. |

---

## 3.2 Logical Operators: `and`, `or`, `not`

Sometimes a single condition is not enough. Logical operators let you combine multiple conditions into one expression:

| Operator | Meaning | Example |
|----------|---------|---------|
| `and` | Both must be True | `age >= 18 and has_id` |
| `or` | At least one must be True | `is_member or has_coupon` |
| `not` | Reverses True/False | `not is_expired` |

**Analogy:**

- `and` is like needing *both* a ticket *and* an ID to enter a venue
- `or` is like a store accepting cash *or* credit card — either one works
- `not` flips the answer: "not expired" means "still valid"

### Requiring Every Condition: `and` and `not`

A loan approval is a classic all-or-nothing decision: every criterion must pass.

!!! example "Worked Example: Loan Approval with `and` and `not`"

    ```python
    age = 28
    annual_income = 55000
    has_bankruptcy = False

    # Loan approval: age >= 21 AND income >= 40000 AND no bankruptcies
    approved = age >= 21 and annual_income >= 40000 and not has_bankruptcy

    print(f"Age: {age} (min: 21)")
    print(f"Income: ${annual_income:,} (min: $40,000)")
    print(f"Bankruptcy on record: {has_bankruptcy}")
    print(f"Loan approved? {approved}")
    ```

    **Output:**

    ```
    Age: 28 (min: 21)
    Income: $55,000 (min: $40,000)
    Bankruptcy on record: False
    Loan approved? True
    ```

    **Interpretation:** All three criteria pass — the applicant is 28 (minimum 21), earns $55,000 (minimum $40,000), and `not has_bankruptcy` flips `False` to `True` — so the chained `and` expression is `True`. With `and`, a single failing criterion anywhere in the chain would make the whole expression `False`.

    *Source: `computations/module03_examples.py` — `demo_loan_approval()`*

### Accepting Any Condition: `or`

With `or`, one passing condition is enough — useful for promotions where customers can qualify in more than one way.

!!! example "Worked Example: Promotional Discount with `or`"

    ```python
    is_member = False
    order_total = 125.00

    # Promotional discount: member OR order over $100
    gets_promo = is_member or order_total > 100

    print(f"Member? {is_member}")
    print(f"Order total: ${order_total:.2f}")
    print(f"Gets promotional discount? {gets_promo}")
    ```

    **Output:**

    ```
    Member? False
    Order total: $125.00
    Gets promotional discount? True
    ```

    **Interpretation:** The membership test fails, but the $125.00 order clears the qualifying amount, and `or` needs only one side to be `True`. Notice that the decision lives in a boolean variable (`gets_promo`) — you can compute a decision in one place and act on it later.

    *Source: `computations/module03_examples.py` — `demo_promo_or()`*

### Using Combined Conditions in an `if`

The boolean expressions above were stored in variables. Just as often, a combined condition sits directly inside an `if` statement:

!!! example "Worked Example: Transaction Check Inside an `if`"

    ```python
    account_balance = 1500
    is_overdue = False
    credit_limit = 5000

    print(f"Balance: ${account_balance:,}  Credit limit: ${credit_limit:,}  Overdue: {is_overdue}")

    # Combining logical operators in an if statement
    if account_balance < credit_limit and not is_overdue:
        print("Transaction approved")
    else:
        print("Transaction declined")
    ```

    **Output:**

    ```
    Balance: $1,500  Credit limit: $5,000  Overdue: False
    Transaction approved
    ```

    **Interpretation:** The $1,500 balance is under the $5,000 limit and the account is not overdue, so the combined condition is `True` and the transaction goes through. This is the standard shape of a business rule in code: build one boolean expression from several checks, then branch on it.

    *Source: `computations/module03_examples.py` — `demo_transaction_check()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| `and` succeeds when either side is `True`. | That is `or`. With `and`, *both* sides must be `True` — one failing condition sinks the whole expression. |
| Python's `or` means "one or the other, but not both." | Python's `or` is inclusive: it is `True` when either side **or both** are `True`. |
| `if is_member == True:` is required to test a boolean. | The boolean *is* the condition — write `if is_member:` and `if not is_expired:`. Comparing to `True` is redundant. |
| Each side of `and`/`or` can lean on the other, as in `age and income >= 40000`. | Each side must be a complete condition on its own: `age >= 21 and annual_income >= 40000`. Incomplete sides run, but test the wrong thing. |

---

## 3.3 `for` Loops and `range()`

A `for` loop repeats a block of code once for each item in a sequence. The most common way to create a sequence of numbers is with `range()`:

```python
for variable in range(n):
    # this block runs n times
```

**Analogy:** a `for` loop is like going down a checklist. You start at the top, do the task for item 1, then item 2, and so on until you reach the end.

`range()` generates numbers starting from 0 by default:

| Call | Produces |
|------|----------|
| `range(5)` | 0, 1, 2, 3, 4 |
| `range(1, 6)` | 1, 2, 3, 4, 5 |
| `range(0, 10, 2)` | 0, 2, 4, 6, 8 |
| `range(5, 0, -1)` | 5, 4, 3, 2, 1 |

The third number is the **step**. A negative step counts *down* — and just like counting up, the stop value is not included, so `range(5, 0, -1)` ends at 1, not 0.

!!! example "Worked Example: Product Launch Countdown"

    ```python
    print("Product launch countdown:")

    # Print a simple countdown for a product launch
    for day in range(5, 0, -1):
        print(f"  {day} days remaining...")
    print("  Launch day!")
    ```

    **Output:**

    ```
    Product launch countdown:
      5 days remaining...
      4 days remaining...
      3 days remaining...
      2 days remaining...
      1 days remaining...
      Launch day!
    ```

    **Interpretation:** The negative step counts down from 5, and because the stop value is excluded, the last day printed is 1. The final print statement is *not* indented, so it sits outside the loop body and runs once after the loop finishes — indentation controls loop membership just as it controls `if` blocks.

    *Source: `computations/module03_examples.py` — `demo_countdown()`*

### Business Example: Compound Growth

A `for` loop can project revenue growth over several years, replacing the tedious process of copying formulas down a spreadsheet column. Each year's revenue is last year's revenue multiplied by $(1 + r)$, where $r$ is the growth rate.

Two formatting details appear in the code: `<6` and `>12` inside the f-strings set left and right column alignment (a Module 2 idea extended), and `"-" * 20` repeats the dash character to draw a divider line — multiplying a string repeats it.

!!! example "Worked Example: Five-Year Revenue Projection"

    ```python
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
    ```

    **Output:**

    ```
    Starting revenue: $100,000 — projected growth: 8% per year

    Year        Revenue
    --------------------
    1      $ 108,000.00
    2      $ 116,640.00
    3      $ 125,971.20
    4      $ 136,048.90
    5      $ 146,932.81
    ```

    **Interpretation:** Reassigning `revenue` inside the loop makes each year's calculation start from the previous year's result — $100,000 compounding at 8% reaches $146,932.81 by year 5. In a handful of lines you built a projection that would take a spreadsheet formula plus repeated copy-paste operations, and extending the horizon means changing one number in `range()`.

    *Source: `computations/module03_examples.py` — `demo_revenue_projection()`*

### Looping Over Collections

`for` loops also work with lists and other collections. We cover lists in depth in Module 6, but here is a preview so you can see the pattern — the loop variable takes on each list item in turn:

!!! example "Worked Example: Batch Shipping Decisions"

    ```python
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
    ```

    **Output:**

    ```
       Order    Shipping
    ----------------------
    $  45.00       $7.99
    $ 120.50        Free
    $  89.99        Free
    $ 210.00        Free
    $  33.75       $7.99
    ```

    **Interpretation:** The loop applies the same if/else decision to every amount in the list: three orders ship free, while the $45.00 and $33.75 orders each pay the $7.99 fee. Making an item-by-item decision across a collection is the core pattern of batch data processing — the same shape you will later apply to thousands of rows.

    *Source: `computations/module03_examples.py` — `demo_batch_shipping()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| `range(5)` produces 1 through 5. | It produces 0, 1, 2, 3, 4 — starting at 0, and stopping *before* the stop value. |
| `range(1, 6)` includes 6. | The stop value is never included, counting up or down. `range(1, 6)` ends at 5; `range(5, 0, -1)` ends at 1. |
| The loop variable must be named `i`. | Any valid name works, and descriptive names (`day`, `year`, `amount`) make the loop self-explanatory. |
| You must increment the loop variable yourself in a `for` loop. | The `for` loop advances through the sequence automatically. Manual updating is only needed in `while` loops — mixing this up is a common source of bugs. |

---

## 3.4 `while` Loops and Loop Control

### `while`: Repeating Until a Condition Changes

A `while` loop keeps running as long as its condition is `True`. Use it when you do not know in advance how many times you need to repeat.

```python
while condition:
    # this block repeats as long as condition is True
```

**Analogy:** a `while` loop is like stirring a pot "until it boils." You do not know exactly how many stirs that will take — you just keep going until the condition is met.

**Warning:** if the condition never becomes `False`, the loop runs forever (an "infinite loop"). Always make sure something inside the loop changes the condition.

!!! example "Worked Example: Savings Goal with a `while` Loop"

    ```python
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
    ```

    **Output:**

    ```
    Monthly deposit: $850
    Goal: $10,000
    Months to reach goal: 12
    Final balance: $10,200
    ```

    **Interpretation:** Depositing $850 per month reaches the $10,000 goal in 12 months, finishing at $10,200 — the loop ran exactly as many times as needed without knowing that count in advance, which is what distinguishes `while` from `for`. The deposit line inside the body is what eventually makes the condition `False`; remove it and the loop would never end.

    *Source: `computations/module03_examples.py` — `demo_savings_goal()`*

### `break`: The Emergency Exit

Sometimes you need finer control over a loop:

- **`break`** — immediately exits the loop, skipping any remaining iterations
- **`continue`** — skips the rest of the current iteration and moves to the next one

Think of `break` as an emergency exit and `continue` as a "skip this one" button.

!!! example "Worked Example: Stopping at Daily Capacity with `break`"

    ```python
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
    ```

    **Output:**

    ```
    Daily processing capacity: $800

    Processed order $150 — running total: $150
    Processed order $200 — running total: $350
    Processed order $175 — running total: $525
    Capacity reached — cannot add $300 order

    Orders processed: 3 of 7
    Total value: $525
    ```

    **Interpretation:** The first three orders fit, bringing the running total to $525; adding the $300 order would exceed the $800 capacity, so `break` ends the loop immediately and the remaining orders are never examined. The summary confirms 3 of 7 orders were processed — `len()` reports how many items the list holds.

    *Source: `computations/module03_examples.py` — `demo_break_capacity()`*

### `continue`: Skip This One

Where `break` abandons the loop entirely, `continue` abandons only the current item — a natural fit for skipping bad records in a data feed.

!!! example "Worked Example: Skipping Invalid Transactions with `continue`"

    ```python
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
    ```

    **Output:**

    ```
    Valid transaction total: $824.75
    Skipped 3 invalid entries
    ```

    **Interpretation:** When `continue` fires on a negative or zero amount, the accumulator line below it is skipped for that iteration, so only valid transactions reach the $824.75 total; the counter reports 3 skipped entries. Unlike `break`, the loop keeps going — it just abandons the rest of the current iteration.

    *Source: `computations/module03_examples.py` — `demo_continue_invalid()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| A `while` loop stops the instant its condition becomes `False`, even mid-block. | The condition is checked only at the *top* of each iteration. The body always finishes the current pass first. |
| An infinite loop means something is broken in Python. | It means nothing in the body changes the condition. The fix is in your logic: ensure some statement moves the loop toward `False`. |
| `break` exits the program. | `break` exits only the innermost enclosing loop; the program continues with the first statement after that loop. |
| `continue` restarts the loop from the first item. | `continue` skips ahead to the *next* iteration. Progress made so far — totals, counters, position in the sequence — is untouched. |

---

## 3.5 Nested Logic and Common Loop Patterns

### Nested Control Structures

You can put `if` statements inside loops, loops inside `if` statements, or even loops inside loops. This is called **nesting**, and it lets you handle more complex logic. The key is to keep track of **indentation levels** — each nested block is indented one more level (4 more spaces) than its parent.

**A quick note on the data below.** Each item in the list is written as `("Alice", 320.00)` — two values grouped together in parentheses. This grouping is called a **tuple** (we cover tuples in depth in Module 6). When you loop with `for name, amount in orders:`, Python **unpacks** each tuple, putting the first value into `name` and the second into `amount` — a convenient shortcut for stepping through paired data.

!!! example "Worked Example: Classifying a Batch of Orders"

    ```python
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
    ```

    **Output:**

    ```
    Premium threshold: $200.00

    Customer     Amount  Category
    --------------------------------
    Alice      $ 320.00  Premium
    Bob        $  45.00  Standard
    Carol      $ 150.00  Standard
    Dave       $ 520.00  Premium
    Eve        $  88.00  Standard

    Premium orders: 2
    Standard orders: 3
    ```

    **Interpretation:** Every order flows through the if/else nested inside the loop: amounts at or above the $200.00 threshold are labeled Premium and the rest Standard, with the counters tallying 2 Premium and 3 Standard orders. The classification line and both counter updates are indented under the `if`/`else`, while the table row prints for every order — the indentation level tells you exactly which statements run when.

    *Source: `computations/module03_examples.py` — `demo_nested_classification()`*

!!! question "Try It Yourself: Inventory Alert System"

    You have a list of products with their stock levels. Write a loop that checks each
    product and prints an alert based on the stock level:

    - 0 units: `"OUT OF STOCK"`
    - 1–10 units: `"LOW STOCK — reorder soon"`
    - 11 or more: `"In stock"`

    The data is provided below. Fill in the logic.

    ```python
    inventory = [
        ("Wireless Mouse", 3),
        ("USB-C Hub", 0),
        ("Laptop Stand", 25),
        ("Webcam", 8),
        ("Keyboard", 0),
        ("Monitor Arm", 14),
    ]

    # for product, stock in inventory:
    #     if ???:
    #         status = "OUT OF STOCK"
    #     elif ???:
    #         status = "LOW STOCK — reorder soon"
    #     else:
    #         status = "In stock"
    #     print(f"{product}: {stock} units — {status}")
    ```

### Putting It All Together: Order Processing

The closing example combines conditionals, loops, accumulators, and counters in a realistic scenario.

**Scenario:** you have a batch of product orders. For each order you need to:

1. Calculate the subtotal (quantity times unit price)
2. Apply a 10% bulk discount for orders of 50+ units
3. Flag any order over $1,000 for manager approval
4. Compute the grand total across all orders

!!! example "Worked Example: Order Processing Report"

    ```python
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
    ```

    **Output:**

    ```
    === Order Processing Report ===

      Laptop Stand: 25 x $34.99 = $874.75
      USB Hub: 100 x $12.50 = $1,250.00 (10% bulk discount → $1,125.00) *** MANAGER APPROVAL ***
      Monitor Cable: 60 x $8.75 = $525.00 (10% bulk discount → $472.50)
      Desk Lamp: 10 x $45.00 = $450.00
      Keyboard: 75 x $29.99 = $2,249.25 (10% bulk discount → $2,024.33) *** MANAGER APPROVAL ***

    Grand total: $4,946.57
    Orders flagged for approval: 2
    ```

    **Interpretation:** For each order the loop computes the gross amount, the first `if` applies the 10% bulk discount where the quantity qualifies, and the second `if` flags discounted subtotals that still exceed the approval limit — 2 orders here. Meanwhile the accumulator builds the $4,946.57 grand total and the counter tracks the flags. This accumulate–decide–report structure is the template for the assignment's payroll task.

    *Source: `computations/module03_examples.py` — `demo_order_processing()`*

That block of code reads almost like a set of business rules written in English. Every decision and calculation is explicit, and anyone reading the code can follow the logic step by step. This is the kind of automation that saves hours of manual spreadsheet work.

### Common Loop Patterns

Three patterns cover a large portion of the loops you will ever write. If you can recognize which pattern applies, writing the loop becomes straightforward.

**1. Accumulator — running total**

```python
total = 0
for item in items:
    total = total + item
```

**2. Counter — counting things that match a condition**

```python
count = 0
for item in items:
    if some_condition:
        count = count + 1
```

**3. Search — find the first match and stop**

```python
for item in items:
    if item meets criteria:
        print("Found it!")
        break
```

The order-processing report above used an accumulator (`grand_total`) and a counter (`flagged_count`) side by side; the daily-capacity example in §3.4 was a search-like loop that stopped with `break`.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| An accumulator can be initialized inside the loop. | `total = 0` inside the body resets the total on every iteration. Initialize accumulators and counters *before* the loop. |
| A summary line indented inside the loop prints once. | Indented inside the body, it prints on *every* iteration. Un-indent it to run once after the loop ends. |
| Tuple unpacking (`for name, amount in ...`) only works for pairs. | It matches however many values each tuple holds — the order-processing loop unpacked three (`product, qty, price`). The count of names must match the tuple size. |
| More nesting shows more skill. | Deep nesting is hard to read and debug. Keep it shallow (2–3 levels); if logic gets deeper, restructure it — Module 4's functions are the main tool for that. |

---

## Reflection Questions

1. What is the difference between a `for` loop and a `while` loop? Describe one business task that clearly calls for each, and explain what would go wrong if you swapped them.
2. Think of a real-world business process that involves both a decision (conditional) and repetition (loop) — approving expense reports, restocking shelves, screening applications. How would you translate it into Python logic, and which loop pattern (accumulator, counter, search) does it use?
3. The customer-tier example orders its `elif` thresholds from highest to lowest. What specific misclassification would occur if the conditions were listed from lowest to highest instead, given that Python runs the first `True` branch?
4. A colleague's `while` loop has been running for ten minutes on data that should take seconds. What is the most likely cause, and what would you look for in the loop body to confirm and fix it?
5. In the transaction-cleaning example, `continue` skips invalid entries but keeps processing. When would `break` be the safer choice for bad data, and what business risk does each choice carry (processing too little vs. including bad records)?
6. The revenue projection replaced a spreadsheet column of copied formulas with a loop. As the projection horizon grows or the growth rule changes, what maintenance advantages does the loop version have — and what does the spreadsheet version still do better?

---

## Your Assignment

The Module 3 assignment, **Decision Logic and Loops**, is worth **100 points plus a 10-point bonus**. You complete it in the provided marimo notebook and submit the `.py` file to Blackboard. The closing reflection section is not graded separately — it counts toward participation. Read each task carefully before writing code, pay close attention to indentation (it defines your code blocks), and use the underscore prefix (`_`) for variable names inside marimo cells. If you get stuck, return to the sections referenced below.

### Task 1: Grade Classification (10 points)

A university registrar needs to convert numeric scores into letter grades. Write an `if`/`elif`/`else` chain that assigns the standard five letter grades across the score bands given in the notebook, then print the score and the resulting grade. This is the `elif`-chain skill from §3.1 — and the same problem posed in that section's Try It Yourself prompt.

### Task 2: Loan Eligibility Check (15 points)

A bank approves an application only when all three criteria hold: a minimum credit score, a minimum annual income, and no prior defaults on record. Combine the three checks into a single boolean expression using `and` and `not`, then use an `if`/`else` to print the decision alongside the applicant's numbers. The operators come from §3.2 and the branching from §3.1.

### Task 3: Monthly Expense Summary (15 points)

A department manager tracks six months of operating expenses in a list. Loop through the list with a `for` loop, add each value to a running total, then compute the average using `len()` and print both figures with dollar formatting. This is the accumulator pattern from §3.5 applied with the collection-looping skills of §3.3.

### Task 4: Inventory Depletion (15 points)

A warehouse ships a fixed number of units each week, and the manager needs to know how many full weeks the current stock covers. Use a `while` loop that subtracts the weekly demand from stock and counts each week, stopping when the remaining stock can no longer cover a full week; report the weeks and the leftover units. The `while` mechanics — including making sure the loop terminates — are in §3.4.

### Task 5: Order Processing with Tiered Discounts (20 points)

A purchasing department processes a batch of orders given as (product, quantity, unit price) tuples. Apply a *two-tier* quantity discount (a larger discount at a high quantity threshold, a smaller one at a middle threshold, none below that), flag any discounted subtotal that exceeds the approval limit, and track both the grand total and the number of flagged orders. This extends §3.5's order-processing example — which used a single discount tier — using the `elif` chain from §3.1 and loops from §3.3.

### Task 6: Weekly Payroll Calculator (25 points)

For each employee tuple (name, hours worked, hourly rate), compute gross pay where hours beyond the standard week earn time-and-a-half, select a tax rate from three gross-pay brackets, and derive net pay. Accumulate the total payroll and count how many employees earned overtime, then print a formatted report. This task combines every section: conditionals (§3.1), the bracket logic (§3.1), loops and unpacking (§3.3, §3.5), and the accumulator/counter patterns (§3.5).

### Task 7: Creative Exercise — Bonus (10 points)

Design your own business scenario that uses at least four Module 3 concepts from the notebook's list — conditional logic, logical operators, a `for` loop, a `while` loop, an accumulator or counter, or nested structures. Suggested directions include a shipping cost calculator, a sales commission system, or an inventory reorder system. Include at least three comments explaining your logic and print formatted output that clearly shows the results.

### Reflection (participation credit)

Answer the notebook's three prompts in your own words: the difference between `for` and `while` loops and when you would choose each; a real-world business process involving both a decision and repetition, translated into Python logic; and what you found most challenging. There is no wrong answer — honest reflection helps you learn and shows your instructor where to provide support.

---

## Chapter Summary

Conditional statements let code make decisions. An `if` runs its indented block only when the condition is `True`; `else` supplies the alternative path, and `elif` chains handle multiple possibilities, with Python running the *first* `True` branch and skipping the rest — which makes the ordering of conditions part of the logic. Indentation is not decoration in Python: it defines which statements belong to which block. Logical operators extend single conditions into real business rules: `and` requires every criterion (loan approvals), `or` accepts any one qualifying path (promotions), and `not` inverts a flag. A combined boolean expression can be stored in a variable or placed directly in an `if`.

Loops handle repetition. A `for` loop runs once per item in a sequence — numbers from `range()` (start included, stop excluded, with an optional step that can count down) or items in a list — which is how the module projected compound revenue growth and applied a shipping rule across a batch of orders. A `while` loop repeats until its condition turns `False`, fitting problems where the number of iterations is unknown in advance, such as months needed to reach a savings goal; something in the body must move the condition toward `False`, or the loop never ends. `break` exits a loop early (stopping at daily capacity), and `continue` skips just the current iteration (passing over invalid transactions).

Nesting an `if` inside a loop is the workhorse structure of batch processing: classify each item, update an accumulator or counter, and report after the loop. The order-processing example combined all of it — tuple unpacking, a discount condition, an approval flag, a running grand total — into code that reads like written business rules. Most loops you will ever write reduce to three recognizable patterns: the accumulator (running total), the counter (matches of a condition), and the search (find the first hit and `break`). Recognize the pattern and the code follows.

---

## What's Next

Module 4 covers **functions and modular thinking** — reusable blocks of code that you call by name. The order-processing logic you built here works, but if three different reports need the same discount rule, copying the loop three times invites inconsistency. Functions let you write the logic once, give it a name, hand it inputs, and get back outputs — turning scripts into organized, maintainable tools. The conditionals and loops from this module become the *bodies* of those functions, and the misconception table's advice about deep nesting gets its real solution: when logic gets complicated, break it into functions.
