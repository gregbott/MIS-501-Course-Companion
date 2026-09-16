# Module 4: Functions & Modular Thinking

## Introduction

By now you have written programs that calculate, decide, and repeat — but the logic lives wherever you happened to type it. Real business code cannot work that way. A sales-tax rule, an overtime formula, or a discount policy gets used in the shopping cart, the invoice, the payroll run, and the quarterly report, and copying the calculation into each place guarantees that someday one copy gets fixed while the others silently keep producing wrong numbers. **Functions** solve this: you write the logic once, give it a name, and call that name wherever the logic is needed. This module covers how to define and call functions, how data flows in through parameters and out through `return`, how keyword arguments and default values make calls readable, what variable scope means, and how docstrings document your work. It ends where professional code begins — with **modular thinking**: breaking a business problem into small, named, reusable pieces.

---

## Learning Objectives

By the end of this module, you should be able to:

1. **Define** and call functions using `def`, parameters, and return values
2. **Distinguish** between `return` and `print()`, and between parameters and arguments
3. **Use** keyword arguments and default parameter values to write self-documenting function calls
4. **Explain** variable scope — why variables created inside a function stay inside it
5. **Write** docstrings that document a function's purpose, inputs, and return value
6. **Use** lambda functions for simple one-line operations such as custom sort keys

---

## 4.1 From Repetition to Reuse: The DRY Principle

In Module 3 you wrote loops to repeat the same logic multiple times *in a row*. But what happens when you need the same logic in **different places** in your program? Copying and pasting code creates a maintenance problem: if you find a bug or the business rule changes, you have to find and fix every copy — and hope you did not miss one.

A **function** is a named, reusable block of code. You write the logic once, give it a name, and then **call** that name whenever you need it. This is the **DRY principle** in action: **Don't Repeat Yourself.**

Imagine you run an online store and need to calculate sales tax in three different places: the shopping cart, the invoice, and the annual report. Compare the copy-paste approach with the function approach:

!!! example "Worked Example: The Same Tax Logic — Three Copies vs. One Function"

    Without a function, the calculation is copied wherever it is needed:

    ```python
    # WITHOUT functions — the same tax calculation repeated three times

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
    ```

    With a function, the logic lives in exactly one place:

    ```python
    # WITH a function — write the logic once, use it anywhere
    def calculate_total(subtotal):
        tax = subtotal * 0.0825
        return subtotal + tax

    print(f"Cart total: ${calculate_total(150.00):.2f}")
    print(f"Invoice total: ${calculate_total(150.00):.2f}")
    print(f"Report total: ${calculate_total(150.00):.2f}")
    ```

    **Output:**

    ```
    --- Without a function: the same logic three times ---
    Cart total: $162.38
    Invoice total: $162.38
    Report total: $162.38

    --- With a function: write the logic once, use it anywhere ---
    Cart total: $162.38
    Invoice total: $162.38
    Report total: $162.38
    ```

    **Interpretation:** Both versions print identical totals of `$162.38` — the behavior did not change. What changed is maintainability: the first version has three copies of the tax logic, while the second has one. When the tax rate changes, the function version is updated in a single line and every caller is automatically correct.

    *Source: `computations/module04_examples.py` — `demo_dry_before_and_after()`*

The copy-paste version *works*, but consider what happens when the tax rate changes from 8.25% to 8.5%: you must locate and edit three separate places, and a missed copy produces totals that are quietly wrong. With the function, there is one tax rate and one place to change it. That is the power of functions — and the more places a rule is used, the bigger the payoff.

---

## 4.2 Function Fundamentals: Defining, Calling, and Returning

### Anatomy of a Function Definition

Here is the general shape of a function definition:

```python
def function_name(parameter1, parameter2):
    # body — the code that runs when you call the function
    result = parameter1 + parameter2
    return result
```

The pieces:

| Part | Purpose |
|------|---------|
| `def` | Keyword that tells Python "I'm defining a function" |
| `function_name` | The name you choose — use lowercase with underscores |
| `(parameter1, parameter2)` | Inputs the function expects (can be zero or more) |
| `:` | Marks the start of the indented body |
| Body (indented) | The code that runs each time you call the function |
| `return` | Sends a value back to the caller (optional) |

**Naming conventions:** Function names should describe what the function *does*. Use verbs: `calculate_tax`, `format_currency`, `validate_email`. Avoid vague names like `do_stuff` or `process`. Like variable names, function names use `snake_case`.

!!! example "Worked Example: Defining and Calling greet()"

    ```python
    # A simple function that greets someone by name
    def greet(name):
        return f"Hello, {name}! Welcome to MIS501."

    # Nothing happens until we CALL the function
    message = greet("Alice")
    print(message)
    ```

    **Output:**

    ```
    Hello, Alice! Welcome to MIS501.
    ```

    **Interpretation:** Two distinct things happen here. **Defining** the function registers it for later use but runs nothing — the body sits and waits. **Calling** it with an argument is what actually runs the body, builds the greeting, and returns it to the caller, where it is stored in `message` and printed.

    *Source: `computations/module04_examples.py` — `demo_define_and_call()`*

### Calling a Function

To call a function, write its name followed by **parentheses**. If the function expects inputs, put them inside the parentheses:

```python
greet("Bob")        # with an argument
greet()             # error — this function requires a name
```

Parentheses are required even when a function takes no arguments. If you write the function's bare name without parentheses, Python does not run it — it hands you the function *object* itself, which prints as something like `<function print_separator at 0x...>`. Forgetting the parentheses is one of the most common beginner mistakes, and it produces no error message — just a result you did not expect.

!!! example "Worked Example: Parentheses Make the Call"

    ```python
    # A function with no parameters
    def print_separator():
        print("=" * 40)

    print_separator()              # correct — runs the function body
    print(type(print_separator))   # no parentheses — the function object itself
    ```

    **Output:**

    ```
    ========================================
    <class 'function'>
    ```

    **Interpretation:** The first call, with parentheses, runs the body and prints the separator bar. The second line omits the parentheses, so `print_separator` refers to the function object itself — asking for its type confirms Python sees a function, not the result of running one. Always include the parentheses when you want the function to execute.

    *Source: `computations/module04_examples.py` — `demo_calling_requires_parentheses()`*

### Parameters and Arguments

Two words that sound interchangeable but are not:

- **Parameters** are the variable names listed in the function *definition*.
- **Arguments** are the actual values you pass when you *call* the function.

```python
def calculate_tax(amount, rate):   # amount and rate are parameters
    return amount * rate

calculate_tax(100, 0.0825)         # 100 and 0.0825 are arguments
```

Think of parameters as labeled slots and arguments as the values you plug into those slots. Each time you call the function, the arguments fill the slots, the body runs with those values, and the result comes back.

!!! example "Worked Example: Parameters as Slots, Arguments as Values"

    ```python
    # Business example: calculate sales tax
    def calculate_tax(amount, rate):
        return amount * rate

    purchase = 249.99
    tax = calculate_tax(purchase, 0.0825)
    print(f"Purchase: ${purchase:.2f}")
    print(f"Tax (8.25%): ${tax:.2f}")
    print(f"Total: ${purchase + tax:.2f}")
    ```

    **Output:**

    ```
    Purchase: $249.99
    Tax (8.25%): $20.62
    Total: $270.61
    ```

    **Interpretation:** The call plugs the `$249.99` purchase into the `amount` slot and the 8.25% rate into the `rate` slot; the body multiplies them and returns `$20.62` of tax. Because the function *returned* the tax rather than printing it, the caller can keep computing with it — here, adding it back to the purchase for a `$270.61` total.

    *Source: `computations/module04_examples.py` — `demo_parameters_and_arguments()`*

### Return Values: Getting Data Back

The `return` statement sends a value back to the code that called the function. Without `return`, a function returns `None` — Python's way of saying "nothing."

A common mistake is using `print()` inside a function instead of `return`. Printing displays text on screen, but it does not give the caller a value to work with. The difference matters the moment you need the result for a further calculation:

!!! example "Worked Example: return vs. print"

    ```python
    # print vs. return — a critical distinction
    def bad_add(a, b):
        print(a + b)   # displays the result but returns None

    def good_add(a, b):
        return a + b   # returns the result so you can use it

    result_bad = bad_add(3, 4)     # prints 7, but result_bad is None
    result_good = good_add(3, 4)   # returns 7, stored in result_good

    print(f"bad_add returned: {result_bad}")
    print(f"good_add returned: {result_good}")
    print(f"good_add result * 2 = {result_good * 2}")  # we can do math with it
    ```

    **Output:**

    ```
    7
    bad_add returned: None
    good_add returned: 7
    good_add result * 2 = 14
    ```

    **Interpretation:** `bad_add` displayed 7 on screen but handed back `None` — the number flashed by and is gone, so no further calculation can use it. `good_add` returned 7, which the caller stored and then doubled to 14. Only the `return` version produces a value your program can build on.

    *Source: `computations/module04_examples.py` — `demo_return_vs_print()`*

**Rule of thumb:** use `return` when you need the result for further calculations — which is almost always. Use `print()` only when the goal is to display something to the user.

### Multiple Parameters: Order Matters

When a function has multiple parameters and you pass arguments by position, the order of the arguments must match the order of the parameters. Get it backwards and Python will not complain — it will happily compute the wrong answer:

!!! example "Worked Example: Swapped Arguments, Silently Wrong"

    ```python
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
    ```

    **Output:**

    ```
    Correct (10 lbs, 200 mi): $14.00
    Swapped (200 lbs, 10 mi): $105.20
    ```

    **Interpretation:** The same two numbers, 10 and 200, produce either `$14.00` or `$105.20` depending purely on the order they are passed in. The swapped call treats the shipment as a 200-pound package traveling 10 miles, and Python raises no error — the mistake surfaces only when someone questions the bill. This fragility is exactly what keyword arguments fix.

    *Source: `computations/module04_examples.py` — `demo_positional_order_matters()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Writing `def` runs the code inside the function. | Defining only *registers* the function. The body runs when — and only when — the function is called. |
| A function name without parentheses still calls it. | The bare name refers to the function object itself. Only `name(...)` with parentheses executes the body. |
| A function that prints its result is as good as one that returns it. | The printing version hands back `None`, so the caller cannot store the result or compute with it. `return` is what makes a function's output usable. |
| Python checks that positional arguments went to the right parameters. | Python matches positional arguments purely by position. Swapped arguments produce a wrong answer with no error message. |

---

## 4.3 Keyword Arguments and Default Values

### Keyword Arguments: Explicit Is Better

Instead of relying on position, you can name each argument when you call a function. These **keyword arguments** make your code self-documenting and prevent ordering mistakes:

!!! example "Worked Example: Keyword Arguments Read Like Documentation"

    ```python
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
    ```

    **Output:**

    ```
    Shipping cost: $14.00
    Same result: $14.00
    ```

    **Interpretation:** Both calls produce `$14.00` even though the arguments appear in opposite orders — each value is routed to its parameter by *name*, not by position. Anyone reading the call can see at a glance which number is the weight and which is the distance, which is exactly what a reviewer (or your future self) needs.

    *Source: `computations/module04_examples.py` — `demo_keyword_arguments()`*

In this course — and in professional Python code — **keyword arguments are preferred** whenever a function has more than one parameter. They make code easier to read, review, and debug.

!!! note "A marimo naming note"

    In marimo, each name can be defined in only *one* cell of a notebook. The teaching notebook therefore names its improved versions `calculate_shipping2` and `calculate_total3` to avoid colliding with earlier cells. In your own scripts — and in this chapter — the clean names are used. The logic is identical.

### Default Parameter Values

You can give a parameter a **default value** so callers can omit it when the default is appropriate:

```python
def calculate_total(price, tax_rate=0.0825, discount=0):
    discounted = price * (1 - discount)
    return discounted * (1 + tax_rate)
```

- `tax_rate` defaults to 8.25% if not provided
- `discount` defaults to 0 (no discount) if not provided

This is an upgraded version of §4.1's `calculate_total`: the tax rate is no longer buried in the body as a hard-coded number, and an optional discount joins it. Callers specify only what differs from the norm:

!!! example "Worked Example: Default Values in Action"

    ```python
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
    ```

    **Output:**

    ```
    $100, default tax, no discount: $108.25
    $100, default tax, 10% discount: $97.42
    $100, 6% tax, 15% discount: $90.10
    ```

    **Interpretation:** The same `$100` price yields `$108.25` with all defaults, `$97.42` once a 10% discount is supplied, and `$90.10` when both a 6% tax rate and a 15% discount override the defaults. Default values make a function flexible without making every call verbose — the common case stays short, and unusual cases spell out only what is unusual.

    *Source: `computations/module04_examples.py` — `demo_default_parameters()`*

!!! question "Try It Yourself: Tip Calculator"

    Write a function called `calculate_tip` that takes a `bill_amount` and a `tip_rate`
    with a default of 18% (0.18). The function should **return** the tip amount.

    Then call it with an $85 bill using the default rate, and again with a 20% rate.
    Print both results formatted as dollar amounts.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Keyword arguments change what the function computes. | They change only how arguments are *routed* to parameters. The math is identical — the call is just readable and order-proof. |
| The keyword names are labels you invent at the call site. | Each keyword must exactly match a parameter name in the definition. A misspelled keyword raises a `TypeError`. |
| A parameter with a default value can no longer be changed. | The default applies only when the caller omits the argument. Passing a value overrides the default for that call. |
| Every parameter needs a default. | Required inputs should have *no* default, so forgetting them is an immediate error instead of a silent wrong answer. Reserve defaults for genuinely optional settings. |

---

## 4.4 Variable Scope and Docstrings

### Variable Scope: Local vs. Global

**Scope** determines where a variable can be seen and used. This is one of the most common sources of confusion for new programmers, so let's be precise.

**Analogy:** think of a function as a private office. Variables created inside the function are like notes on a sticky pad — they exist only while you are in that office. When you leave (the function finishes), those notes are thrown away.

- **Local variables** are created inside a function. They exist only while the function is running and cannot be accessed from outside.
- **Global variables** are created outside any function and can be *read* from inside a function. But an *assignment* inside a function creates a new local variable by default — modifying the actual global requires the `global` keyword, which you should generally avoid.

!!! example "Worked Example: Reading and Modifying a Global"

    ```python
    # Start with a global variable
    count = 0

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
    ```

    **Output:**

    ```
    Global count = 0
    Modified count = 20
    Global count is now 20

    Local count = 30
    Global count is still 20
    ```

    **Interpretation:** Reading the global works without ceremony — the first function sees 0. Changing it requires the `global` declaration, after which the value really is 20 everywhere. The third function skips the declaration, so its assignment quietly creates a brand-new *local* variable holding 30 while the global stays at 20. That last case is the trap: the code looks like it updated the global, but it did not.

    *Source: `computations/module04_examples.py` — `demo_global_vs_local()`*

The next example shows the other side of the boundary — locals are invisible from outside, and a local can even reuse an outer variable's name without touching it (called **shadowing**):

!!! example "Worked Example: Locals Stay Local (and Shadowing)"

    ```python
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
    ```

    **Output:**

    ```
    Alice works at Acme Corp
    Error: name 'employee' is not defined
    Inside function: 200
    Outside function: 100
    ```

    **Interpretation:** Inside the function, both the local `employee` and the outer `company` are visible — reading outward is allowed. But once the function finishes, its local is gone, and reaching for it raises a `NameError`. In the second half, the function's own `value` holds 200 while the outer `value` still holds 100: the local *shadows* the outer name inside the function without changing it.

    *Source: `computations/module04_examples.py` — `demo_local_scope_and_shadowing()`*

**Best practice:** avoid using the same variable name inside and outside functions — shadowing invites confusion. And rather than reaching for `global`, pass data *in* through parameters and get data *out* through `return`. Functions that communicate only through their parameters and return values are easier to test, reuse, and reason about.

### Docstrings: Documenting Your Functions

A **docstring** is a string placed on the first line of a function body that describes what the function does. Python's convention uses triple quotes:

```python
def function_name(param1, param2):
    """One-line summary of what this function does.

    Args:
        param1: Description of first parameter.
        param2: Description of second parameter.

    Returns:
        Description of what the function returns.
    """
    # function body
```

Docstrings are not just comments — Python's built-in `help()` function reads them, and most editors display them when you hover over a function call.

!!! example "Worked Example: A Docstring and help()"

    ```python
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
    ```

    **Output:**

    ```
    Original: $79.99
    After 25% discount: $59.99
    Help on function apply_discount in module __main__:

    apply_discount(price, percentage)
        Calculate the discounted price.

        Args:
            price: Original price in dollars.
            percentage: Discount as a decimal (e.g., 0.10 for 10%).

        Returns:
            The price after applying the discount.
    ```

    **Interpretation:** The function itself works as expected — a 25% discount brings the `$79.99` item down to `$59.99`. The second half of the output is `help()` reproducing the docstring: signature, summary, arguments, and return value, formatted automatically. A few extra seconds writing the docstring buys built-in documentation that every editor and every colleague can pull up on demand.

    *Source: `computations/module04_examples.py` — `demo_docstrings()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Assigning to a variable inside a function updates the outer variable of the same name. | Assignment inside a function creates a *local* variable by default. The outer variable is untouched — this is the shadowing trap. |
| The `global` keyword is the normal way to get data out of a function. | `global` is a last resort. The standard pattern is data in through parameters, data out through `return`. |
| A variable used inside a function must be defined inside it. | Functions can *read* variables from the enclosing scope. Only assignment triggers the creation of a local. |
| A docstring is just a comment with fancier quotes. | Comments are invisible to Python; docstrings are attached to the function object, surfaced by `help()`, and displayed by editors on hover. |

---

## 4.5 Modular Thinking: Refactoring, Lambdas, and the Payroll Report

### Refactoring: Before and After

**Refactoring** means restructuring existing code without changing its behavior. It is the practical payoff of everything in this module: repeated, error-prone blocks become small named functions, and the main program shrinks to a readable summary. Here is a realistic example — calculating payroll, with overtime and tax, for a small team:

!!! example "Worked Example: Refactoring the Payroll Calculation"

    Before — the same gross/tax/net logic pasted once per employee:

    ```python
    # BEFORE refactoring — repeated payroll calculations
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

    # Employee 2 — same eight lines again with hours2/rate2 ...
    # Employee 3 — same eight lines again with hours3/rate3 ...
    ```

    After — each piece of logic becomes one function, and the employees become data:

    ```python
    # AFTER refactoring — clean, reusable functions
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
    ```

    **Output:**

    ```
    --- Before: the same payroll logic copied three times ---
    Employee 1: gross=$1662.50, tax=$365.75, net=$1296.75
    Employee 2: gross=$1064.00, tax=$234.08, net=$829.92
    Employee 3: gross=$2310.00, tax=$508.20, net=$1801.80

    --- After: clean, reusable functions ---
    Alice: gross=$1662.50, tax=$365.75, net=$1296.75
    Bob: gross=$1064.00, tax=$234.08, net=$829.92
    Carol: gross=$2310.00, tax=$508.20, net=$1801.80
    ```

    **Interpretation:** The numbers are identical line for line — Alice's overtime week grosses `$1662.50` and nets `$1296.75` in both versions — which is the definition of a successful refactor: behavior preserved, structure improved. Adding a fourth employee is now one more tuple in the list; changing the overtime multiplier or tax rate means editing one default value instead of hunting through three copies.

    *Source: `computations/module04_examples.py` — `demo_refactoring_before_and_after()`*

### Lambda Functions: Quick One-Liners

Sometimes you need a tiny function for a single, simple operation — like sorting a list by a specific attribute. Python offers **lambda functions** for these cases:

```python
lambda parameters: expression
```

A lambda is an anonymous (unnamed) function consisting of a single expression. It automatically returns the result of that expression — no `return` keyword, no body, no name.

!!! example "Worked Example: A Regular Function vs. a Lambda"

    ```python
    # Regular function vs. lambda — same result
    def double(x):
        return x * 2

    double_lambda = lambda x: x * 2

    print(f"Function: {double(5)}")
    print(f"Lambda: {double_lambda(5)}")
    ```

    **Output:**

    ```
    Function: 10
    Lambda: 10
    ```

    **Interpretation:** Both forms compute exactly the same thing — each call produces 10. The lambda is not faster or more powerful; it is simply a compact notation for a function whose entire logic is one expression.

    *Source: `computations/module04_examples.py` — `demo_lambda_basics()`*

Lambdas are most useful when passed directly to another function. The flagship case is sorting a list by a custom rule — `sorted()` accepts a `key` function that tells it what to sort *by*:

!!! example "Worked Example: Sorting Products by Price with a Lambda Key"

    ```python
    # Sorting products by price using a lambda
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
    ```

    **Output:**

    ```
    Products sorted by price:
      Monitor Cable: $8.75
      USB Hub: $12.50
      Keyboard: $29.99
      Laptop Stand: $34.99
      Desk Lamp: $45.00
    ```

    **Interpretation:** The lambda tells `sorted()` to rank each product by its price rather than by its name, and the catalog comes back ordered from the `$8.75` cable up to the `$45.00` lamp. Writing a full named function for this one-time, one-expression rule would be more ceremony than the job deserves — this is exactly the situation lambdas exist for.

    *Source: `computations/module04_examples.py` — `demo_lambda_sort()`*

**When to use lambdas vs. regular functions:**

| Use a lambda when... | Use `def` when... |
|----------------------|-------------------|
| The logic is a single expression | The logic needs multiple lines |
| You need it only once (e.g., as a sort key) | You will call it in multiple places |
| It is simple enough to understand at a glance | It needs a docstring or a name for clarity |

When in doubt, use `def`. Readable code is more valuable than compact code.

!!! question "Try It Yourself: Sorting with Lambda"

    The list below contains employee names and their years of experience. Sort the list
    by years of experience (highest first) using `sorted()` with a lambda.

    ```python
    employees = [
        ("Alice", 5),
        ("Bob", 12),
        ("Carol", 3),
        ("Dave", 8),
        ("Eve", 1),
    ]
    ```

    *Hint:* Use `reverse=True` in `sorted()` to sort descending.

### Putting It All Together: The Payroll Report

The closing example combines everything from this module — function definitions, parameters, default values, return values, keyword arguments, and docstrings — in one business scenario. You manage payroll for a small department: for each employee, calculate gross pay (with overtime), apply tax, and format the results into a readable report.

!!! example "Worked Example: The Weekly Payroll Report"

    ```python
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
    ```

    **Output:**

    ```
    ==============================================================
      WEEKLY PAYROLL REPORT
    ==============================================================
      Alice      Gross:  $2,470.00 | Tax:   $543.40 | Net:  $1,926.60
      Bob        Gross:  $1,520.00 | Tax:   $334.40 | Net:  $1,185.60
      Carol      Gross:  $2,475.00 | Tax:   $544.50 | Net:  $1,930.50
      Dave       Gross:  $1,050.00 | Tax:   $231.00 | Net:    $819.00
    --------------------------------------------------------------
      Total net payroll: $5,861.70
    ==============================================================
    ```

    **Interpretation:** The main loop reads almost like plain English because every messy detail lives in a named, documented function. Alice's overtime week grosses `$2,470.00` and nets `$1,926.60`; the department's total net payroll comes to `$5,861.70`. If the tax rate changes, one default value changes. If the overtime rule changes, one function changes. The rest of the program stays untouched.

    *Source: `computations/module04_examples.py` — `demo_payroll_report()`*

Look at the division of labor in that example — each function has exactly one job:

- `calculate_gross_pay` handles the overtime math
- `apply_tax` handles the tax calculation
- `format_currency` handles number formatting
- `format_report_line` handles the display layout

This is **modular thinking**: breaking a problem into small, self-contained pieces that are easy to understand, test, and maintain. It is the same discipline you will apply to data pipelines later in the course — and it is the skill your assignment's refactoring task grades directly.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Refactoring means changing what the program does. | A correct refactor changes *structure only* — same inputs, same outputs, cleaner code. Matching before/after output is the proof. |
| Lambdas are a faster or more powerful kind of function. | They compute identically to `def` functions. Their only advantage is compactness for one-expression, single-use logic. |
| `sorted()` rearranges the original list. | `sorted()` returns a *new* sorted list and leaves the original untouched. |
| More functions always means better code. | Functions earn their keep by removing repetition or naming a meaningful step. Splitting trivial one-liners into dozens of functions hurts readability instead of helping it. |

---

## Reflection Questions

1. A tax rule changes and an analyst must update the same formula in fourteen places across several scripts. Explain how this situation arises, what risks it creates, and how the DRY principle prevents it.
2. A colleague's function prints its result instead of returning it. The output looks correct on screen, yet you cannot use the function in your own calculation. Explain what is happening and how you would describe the fix to the colleague.
3. Compare `calculate_delivery(12, 150, True, False)` with a call that names every argument. What does the keyword version communicate to a reviewer that the positional version hides, and what class of bug does it eliminate?
4. Python makes every assignment inside a function local by default. What problems would arise in a large program if functions could freely overwrite outside variables? When, if ever, is the `global` keyword justified?
5. Docstrings and comments both explain code. What makes docstrings more than comments, and what would you include in the `Args:` and `Returns:` sections of a function a teammate will use without reading its body?
6. A lambda and a `def` function can express the same logic. For a sort key used once, which do you choose, and why? For a tax calculation used in five reports, which do you choose, and why?

---

## Your Assignment

The Module 4 assignment, **Functions and Modular Thinking**, is worth **100 points plus a 10-point bonus**. You complete it in the provided marimo notebook and submit the `.py` file to Blackboard. The closing reflection section is not graded separately — it counts toward participation. Throughout the assignment, remember the notebook's conventions: define functions with `def`, use `return` (not `print()`) to hand back values, prefix cell-scoped variables with an underscore, and use keyword arguments whenever a call has multiple parameters.

### Task 1: Your First Function (10 points)

A retail store needs the final price of items after sales tax. Write a function named `calculate_price_with_tax` that takes a price and a tax rate as parameters and returns the total including tax, then call it for three given items — two taxed at the standard rate and one tax-exempt — printing each result with keyword arguments in every call. Defining and returning come from §4.2; the keyword-argument calling style from §4.3.

### Task 2: Default Parameters (15 points)

A consulting firm bills by the hour. Write `calculate_invoice` with a required hours parameter plus an hourly rate and a discount that both have default values; the function computes the subtotal, applies the discount, and returns the final amount. Call it three ways — all defaults, a higher custom rate, and a discounted long engagement — and print each labeled result. Default parameter values are covered in §4.3 and the return pattern in §4.2.

### Task 3: Keyword Arguments for Clarity (15 points)

You are given a delivery-cost function to copy exactly as provided — it combines weight, distance, and optional fragile and express flags. Your job is purely on the calling side: invoke it for four described shipping scenarios using keyword arguments for every non-default parameter, and print each scenario's cost. This task exercises the keyword-argument discipline of §4.3 and the argument-routing concepts of §4.2.

### Task 4: Return vs. Print (15 points)

A colleague's bonus-calculation function uses `print()` where it should use `return`, so its result cannot feed further calculations. Fix the function so it returns the bonus, call it with the given revenue and bonus rate, then use the returned value to compute total compensation on top of a base salary and print both figures. The print-versus-return distinction is the core of §4.2.

### Task 5: Refactoring Challenge (30 points)

The largest task: a block of repetitive shipping-cost code — the same weight-fee and zone-surcharge logic pasted once per package — must be refactored. Write `calculate_weight_fee`, `get_zone_fee`, and a `calculate_shipping` function that calls the other two, then process the provided package list with a `for` loop and keyword arguments, tracking the total cost and package count. This is the before-and-after refactoring pattern of §4.5, built on the function fundamentals of §4.2 and the calling style of §4.3, with the loop technique from Module 3.

### Task 6: Docstrings (15 points)

A compound-interest function arrives undocumented. Add a proper docstring — one-line summary, an `Args:` section for each parameter, and a `Returns:` section — then confirm it displays through `help()` and call the function for two investment scenarios, printing formatted results. Docstring structure and the `help()` check come from §4.4; the default-valued years parameter echoes §4.3.

### Task 7: Creative Exercise — Bonus (10 points)

Design your own business scenario demonstrating modular thinking — a restaurant bill splitter, a GPA calculator, and a fleet fuel-cost estimator are suggested directions. Your solution must include at least three functions with docstrings, at least one default parameter value, at least one function that calls another function, a loop that processes a collection of data, keyword arguments in your calls, and formatted output. Every section of this module contributes: §4.2 fundamentals, §4.3 defaults and keywords, §4.4 docstrings, and §4.5 modular structure.

### Reflection (participation credit)

Answer the notebook's four reflection prompts in your own words: what the DRY principle is and how functions support it, the difference between `print()` and `return` and when each belongs, a repetitive task from your own work or life that a function could simplify (including its parameters and return value), and what you found most challenging. There is no wrong answer — honest reflection helps your instructor see where support is needed.

---

## Chapter Summary

Functions let you write logic once and reuse it anywhere — the DRY principle made concrete. A definition starts with `def`, names the function with a descriptive verb phrase, lists its **parameters** as labeled slots, and runs its indented body only when called with **arguments** filling those slots. The single most consequential habit from this module is preferring `return` over `print()` inside functions: printing shows a value and discards it, while returning hands the value back so the rest of the program can build on it.

How you *call* functions matters as much as how you define them. Positional arguments are fragile — swapping two of them produces a wrong answer with no error — so this course prefers **keyword arguments** whenever a function takes multiple parameters, making every call self-documenting. **Default parameter values** keep the common case short while leaving every setting overridable. Inside a function, **scope** rules apply: assignments create local variables that vanish when the function returns, outer variables can be read but not casually overwritten, and the disciplined pattern is data in through parameters, data out through `return`. **Docstrings** — triple-quoted descriptions surfaced by `help()` and by editors — turn each function into a documented tool rather than a mystery box.

The module closed with modular thinking in practice. **Refactoring** turned three pasted copies of payroll logic into three small named functions plus a data list, with identical output proving the behavior survived. **Lambda functions** handled the opposite extreme — logic so small it fits in one expression, like a sort key. And the weekly payroll report assembled everything — definitions, defaults, keyword calls, docstrings, and a loop — into a program whose main body reads like a description of the business process itself. That is the standard your assignment asks you to meet.

---

## What's Next

Module 5 turns to **strings and regular expressions** — searching, slicing, formatting, and transforming text. Business data is full of text: customer names to standardize, product codes to parse, addresses to validate, survey responses to clean. The functions you learned to write here are exactly how that string logic gets packaged — a `clean_phone_number()` or `extract_order_id()` function written once and applied to thousands of records — so the modular habits from this module carry directly into the text-processing toolkit ahead.
