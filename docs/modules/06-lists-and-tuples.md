# Module 6: Data Structures: Lists & Tuples

## Introduction

In Modules 1–5 you worked with individual values — a single price, one customer name, a lone invoice number. Real business data almost never arrives that way: it comes in **collections** — a list of products, a batch of monthly sales figures, a roster of employees. This module introduces **lists**, Python's most versatile tool for storing ordered collections, and shows how to access, modify, loop over, and transform them. You will also meet **tuples**, which look like lists but cannot be changed after creation — a property that makes them the natural container for fixed records like `(name, department, salary)` and for functions that return several results at once. Once you can work with lists and tuples, you can process entire datasets instead of one value at a time, which is the step that turns the calculations from earlier modules into genuine data analysis.

---

## Learning Objectives

By the end of this module, you should be able to:

1. **Create** lists and access elements using indexing and slicing
2. **Use** common list methods to add, remove, and organize data
3. **Iterate** over lists using `for` loops and `enumerate()`
4. **Write** list comprehensions to transform and filter data
5. **Explain** the difference between mutable lists and immutable tuples
6. **Use** tuple unpacking to assign multiple values simultaneously

---

## 6.1 Lists: Creating, Indexing, and Slicing

A **list** is an ordered collection of items enclosed in **square brackets** `[]`, with items separated by commas:

```python
products = ["Laptop", "Monitor", "Keyboard"]
prices   = [999.99, 349.50, 79.95]
```

Lists can hold any type of data — strings, numbers, booleans, or even a mix. In practice you will often keep **parallel lists**: one list of product names and a matching list of prices, where position links them together.

### Creating Lists

!!! example "Worked Example: Creating Lists of Business Data"

    ```python
    products = ["Laptop", "Monitor", "Keyboard", "Mouse", "Webcam"]
    prices = [999.99, 349.50, 79.95, 24.99, 64.50]
    in_stock = [True, True, False, True, True]

    print(f"Products: {products}")
    print(f"Prices: {prices}")
    print(f"In stock: {in_stock}")
    print(f"Number of products: {len(products)}")
    ```

    **Output:**

    ```
    Products: ['Laptop', 'Monitor', 'Keyboard', 'Mouse', 'Webcam']
    Prices: [999.99, 349.5, 79.95, 24.99, 64.5]
    In stock: [True, True, False, True, True]
    Number of products: 5
    ```

    **Interpretation:** One list holds strings, another floats, a third booleans — each list keeps its items in the order you wrote them, and `len()` reports the count of 5. Notice that the price entered as `349.50` displays as `349.5`: Python drops a float's trailing zero when printing a raw list, just as it did with single values in earlier modules.

    *Source: `computations/module06_examples.py` — `demo_creating_lists()`*

You can also create an empty list and add items later:

```python
orders = []    # start with an empty list
```

The `len()` function tells you how many items are in a list, just as it counts characters in a string. Empty lists plus `len()` set up the accumulator patterns coming in §6.3.

### Indexing: Accessing Individual Items

Like strings, lists use **zero-based indexing**. The first item is at index 0, the second at index 1, and so on. Negative indexes count from the end:

```
Products:  "Laptop"  "Monitor"  "Keyboard"  "Mouse"  "Webcam"
Index:        0          1          2          3         4
Negative:    -5         -4         -3         -2        -1
```

Unlike strings, lists are **mutable** — you can change an individual item by assigning to its index. With a string, `text[0] = "X"` raises an error; with a list, the same move simply replaces the old value.

!!! example "Worked Example: Indexing and Updating a Price"

    ```python
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
    ```

    **Output:**

    ```
    products[0]  (first):          Laptop
    products[2]  (third):          Keyboard
    products[-1] (last):           Webcam
    products[-2] (second to last): Mouse
    Before: [999.99, 349.5, 79.95, 24.99, 64.5]
    After:  [999.99, 349.5, 69.95, 24.99, 64.5]
    ```

    **Interpretation:** Index 0 is the first item and index 2 is the *third* — the off-by-one surprise every beginner hits once. Index -1 reaches the last item without you needing to know the list's length. The assignment then replaces the keyboard's 79.95 price with 69.95 in place: the list itself changed, which is the mutability that strings lack.

    *Source: `computations/module06_examples.py` — `demo_indexing_and_updating()`*

### Slicing: Extracting Sublists

Slicing works the same way as with strings: `list[start:stop]` returns a new list containing items from `start` up to (but not including) `stop`. Omitting `start` begins at the front; omitting `stop` runs to the end; negative positions count from the back.

!!! example "Worked Example: Slicing Monthly Sales Data"

    ```python
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
    ```

    **Output:**

    ```
    All months:      [42000, 38500, 51200, 47800, 39900, 55100, 44300, 49000]
    Q1 months:       [42000, 38500, 51200]
    Middle months:   [51200, 47800, 39900, 55100]
    Last two months: [44300, 49000]
    Original intact: [42000, 38500, 51200, 47800, 39900, 55100, 44300, 49000]
    ```

    **Interpretation:** Each slice is a **new list**; the final line shows the source data untouched. The last-two-months slice picks out 44300 and 49000 with a negative start, so the same code keeps working as new months are appended. Slicing is how you analyze a subset — one quarter, a recent window — without risking the full dataset.

    *Source: `computations/module06_examples.py` — `demo_slicing()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| `products[1]` returns the first product. | Indexing is zero-based: `[0]` is the first item, `[1]` is the second. Negative indexes count from the end (`[-1]` is the last). |
| `list[start:stop]` includes the item at `stop`. | The stop position is excluded — `[:3]` returns the items at positions 0, 1, and 2. |
| Slicing removes the extracted items from the original list. | Slicing copies items into a new list; the original is unchanged. Removal requires the methods in §6.2. |
| Lists must hold items of a single type. | A list can mix strings, numbers, and booleans. Same-type lists are still the norm for numeric work, since operations like summing require numbers. |

---

## 6.2 List Methods: Adding, Removing, and Organizing

Lists come with built-in methods for adding, removing, and reorganizing items. Because lists are mutable, the methods that add, remove, or reorder items modify the list **in place** rather than returning a new one. The last two, `.index()` and `.count()`, do not change the list at all — they just report information about it (a position and a tally). `.pop()` does both: it removes an item *and* hands it back to you.

| Method | What it does | Example |
|--------|-------------|---------|
| `.append(item)` | Add one item to the end | `products.append("Tablet")` |
| `.extend(list)` | Add all items from another list | `products.extend(["Cable", "Case"])` |
| `.insert(i, item)` | Insert item at position i | `products.insert(0, "Server")` |
| `.remove(item)` | Remove first occurrence of item | `products.remove("Mouse")` |
| `.pop(i)` | Remove and return item at index i | `products.pop(-1)` |
| `.sort()` | Sort the list in place | `prices.sort()` |
| `.reverse()` | Reverse the list in place | `prices.reverse()` |
| `.index(item)` | Find index of first occurrence | `products.index("Monitor")` |
| `.count(item)` | Count occurrences of item | `ratings.count(5)` |

### Building and Trimming a List

The next example builds an order from nothing, then cleans up an inventory list — the two halves of day-to-day list maintenance.

!!! example "Worked Example: Building an Order, Trimming an Inventory"

    ```python
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
    ```

    **Output:**

    ```
    Empty order:  []
    After append: ['Laptop', 'Monitor']
    After insert: ['Laptop', 'Keyboard', 'Monitor']
    After extend: ['Laptop', 'Keyboard', 'Monitor', 'Mouse', 'Webcam']

    Inventory before: ['Laptop', 'Monitor', 'Keyboard', 'Mouse', 'Monitor', 'Webcam']
    After remove:     ['Laptop', 'Keyboard', 'Mouse', 'Monitor', 'Webcam']
    Popped item:      Webcam
    After pop:        ['Laptop', 'Keyboard', 'Mouse', 'Monitor']
    ```

    **Interpretation:** `.append()` grows the order one item at a time, `.insert()` slides Keyboard in between the existing items, and `.extend()` merges a whole list at once. On the removal side, `.remove()` deletes only the *first* Monitor — the duplicate later in the list survives — and `.pop()` both removes Webcam and returns it, so your code can act on what was taken off (fulfill it, log it, refund it).

    *Source: `computations/module06_examples.py` — `demo_adding_and_removing()`*

### Sorting: `.sort()` vs `sorted()`

`.sort()` rearranges a list in place and returns `None`. If you need a sorted copy without changing the original, use the built-in `sorted()` function instead.

!!! example "Worked Example: Sorting Sales In Place and by Copy"

    ```python
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
    ```

    **Output:**

    ```
    Original:           [42000, 38500, 51200, 47800, 39900]
    Sorted ascending:   [38500, 39900, 42000, 47800, 51200]
    Sorted descending:  [51200, 47800, 42000, 39900, 38500]

    sorted() copy:      [38500, 42000, 51200]
    Original unchanged: [42000, 38500, 51200]
    ```

    **Interpretation:** After `.sort()`, the original month-by-month order is gone — the same list object now runs from 38500 up to 51200, and `reverse=True` flips it. When order carries meaning (January first!), reach for `sorted()` instead: the copy is ordered while the source list still starts at 42000. Losing chronological order to an accidental in-place sort is a classic reporting bug.

    *Source: `computations/module06_examples.py` — `demo_sorting()`*

!!! question "Try It Yourself: Managing a Product List"

    Start with the product list below. Add `"Tablet"` to the end, insert
    `"Headphones"` at position 2, then remove `"Mouse"`. Print the result after
    each step.

    ```python
    products = ["Laptop", "Monitor", "Keyboard", "Mouse", "Webcam"]

    # products.append(???)
    # print(products)

    # products.insert(???, ???)
    # print(products)

    # products.remove(???)
    # print(products)
    ```

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| `prices = prices.sort()` stores the sorted list. | `.sort()` sorts in place and returns `None` — that assignment throws away your list. Call `prices.sort()` on its own line, or use `sorted(prices)` for a copy. |
| `.remove(item)` deletes every occurrence. | It removes only the *first* match. Duplicates later in the list remain. |
| `.append([a, b])` adds two items. | `.append()` adds its argument as **one** item — here, a nested list. To add each element individually, use `.extend([a, b])`. |
| `.pop()` just deletes an item. | It deletes *and returns* the item, which is why you can capture it: `last = inventory.pop()`. |

---

## 6.3 Iterating Over Lists

In Module 3 you learned `for` loops. Lists and `for` loops are natural partners — a loop visits every item in a list, one at a time, so the same five-line loop can process five rows or five million.

### Processing Every Item

The number-accumulator pattern from Module 3 pairs directly with lists: start a total at zero, add each list item as the loop visits it.

!!! example "Worked Example: Total and Average Revenue with a Loop"

    ```python
    monthly_sales = [42000, 38500, 51200, 47800, 39900]

    total = 0
    for sale in monthly_sales:
        total = total + sale

    average = total / len(monthly_sales)
    print(f"Monthly sales:   {monthly_sales}")
    print(f"Months counted:  {len(monthly_sales)}")
    print(f"Total revenue:   ${total:,.2f}")
    print(f"Average monthly: ${average:,.2f}")
    ```

    **Output:**

    ```
    Monthly sales:   [42000, 38500, 51200, 47800, 39900]
    Months counted:  5
    Total revenue:   $219,400.00
    Average monthly: $43,880.00
    ```

    **Interpretation:** The loop variable `sale` takes each list value in turn, and the accumulator grows to $219,400.00 across the 5 months; dividing by `len()` yields the $43,880.00 monthly average. Python's built-in `sum()` can replace this loop for a plain total (as shown later in this module), but writing the accumulator yourself is the skill that generalizes to logic `sum()` cannot do.

    *Source: `computations/module06_examples.py` — `demo_loop_totals()`*

### `enumerate()`: When You Need Both the Index and the Value

Sometimes you need to know *which* item you are on, not just the item itself. The `enumerate()` function gives you both:

```python
for index, item in enumerate(my_list):
    print(f"Item {index}: {item}")
```

This is cleaner than manually tracking a counter variable. The position is also the key to working with **parallel lists**: the index that `enumerate()` hands you for `months` is the same position to read from `sales`.

!!! example "Worked Example: Numbered Report and Best/Worst Months"

    ```python
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
    ```

    **Output:**

    ```
    Monthly Sales Report
    -----------------------------------
      1. January      $ 42,000.00
      2. February     $ 38,500.00
      3. March        $ 51,200.00
      4. April        $ 47,800.00
      5. May          $ 39,900.00

    Best month:  March ($51,200.00)
    Worst month: February ($38,500.00)
    ```

    **Interpretation:** `enumerate()` supplies the position, so `i + 1` numbers the report rows 1 through 5 for human readers while `sales[i]` pulls the matching amount from the parallel list. The second loop tracks the *index* of the running best and worst instead of just the amounts — that is what lets the final lines name March ($51,200.00) and February ($38,500.00) rather than reporting bare numbers.

    *Source: `computations/module06_examples.py` — `demo_enumerate_reports()`*

### Building Lists with Loops: The Accumulator Pattern

A common pattern is to start with an *empty list* and build it up inside a loop — the **list accumulator**. It is the same idea as the number accumulator, but collecting items instead of adding numbers: create an empty list, loop, conditionally `.append()`.

!!! example "Worked Example: Filtering High-Value Orders"

    ```python
    order_amounts = [150, 45, 320, 89, 510, 72, 205, 33]

    high_value = []
    for amount in order_amounts:
        if amount >= 200:
            high_value.append(amount)

    print(f"All orders: {order_amounts}")
    print(f"High-value orders (>= $200): {high_value}")
    print(f"Count: {len(high_value)} of {len(order_amounts)}")
    ```

    **Output:**

    ```
    All orders: [150, 45, 320, 89, 510, 72, 205, 33]
    High-value orders (>= $200): [320, 510, 205]
    Count: 3 of 8
    ```

    **Interpretation:** Only 3 of the 8 orders clear the $200 bar, and they land in `high_value` in their original order. This create-empty, loop, conditionally-append shape appears constantly in data processing — filtering customers, flagging late invoices, collecting error records. Python offers a more concise way to write it, which is exactly what the next section covers.

    *Source: `computations/module06_examples.py` — `demo_accumulator_filter()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| `enumerate()` starts counting at 1. | It starts at 0, matching list indexing. Display-friendly numbering is `i + 1` in the print, as the report example shows. |
| You need `range(len(list))` to loop over a list. | Iterate directly (`for item in my_list:`); reach for `enumerate()` only when you also need the position. |
| Reassigning the loop variable changes the list. | The loop variable holds the current item for that pass — reassigning it does not touch the list. Modifying the list requires index assignment or list methods. |
| The accumulator can be created inside the loop. | `total = 0` or `high_value = []` must come *before* the loop; placing it inside resets the accumulator on every pass. |

---

## 6.4 List Comprehensions

A **list comprehension** creates a new list by applying an expression to each item in an existing sequence. It is a compact alternative to the loop-and-append pattern from §6.3.

**Basic syntax:**

```python
new_list = [expression for item in iterable]
```

**With a filter:**

```python
new_list = [expression for item in iterable if condition]
```

### Loop vs. Comprehension

!!! example "Worked Example: A Discount Two Ways"

    ```python
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
    ```

    **Output:**

    ```
    Applying a 10% discount to each price
    Original:          [999.99, 349.5, 79.95, 24.99, 64.5]
    Discounted (loop): [899.99, 314.55, 71.95, 22.49, 58.05]
    Discounted (comp): [899.99, 314.55, 71.95, 22.49, 58.05]
    ```

    **Interpretation:** Both versions produce identical lists — the 10% discount takes the 999.99 laptop down to 899.99 either way. The comprehension collapses three lines (create, loop, append) into one that reads almost like the business sentence it implements: "the discounted price, for each price in prices." Neither version modifies `prices`; both build a new list.

    *Source: `computations/module06_examples.py` — `demo_comprehension_vs_loop()`*

### Filtering with `zip()` and Transforming with String Methods

The `zip()` function pairs up items from two lists so you can iterate over them together — the tool of choice for parallel lists like products and their prices. Comprehensions also combine naturally with the string methods you learned in the strings module: cleaning a whole column of messy text becomes one line.

!!! example "Worked Example: Filter, Format, and Clean in One Line Each"

    ```python
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
    ```

    **Output:**

    ```
    Products under $100: ['Keyboard', 'Mouse', 'Webcam']
    Formatted names: ['Alice Chen', 'Bob Martinez', 'Carol Davis']
    Numeric amounts: [42000.0, 38500.0, 51200.0]
    ```

    **Interpretation:** In the first comprehension, `zip()` walks the two parallel lists together, the `if` keeps only pairs priced under $100, and the expression keeps just the *name* — filter on one list, collect from the other. The other two show the transform side: `.title()` standardizes every employee name, and chained `.replace()` calls strip the currency formatting so `"$42,000"` becomes the number 42000.0, ready for math.

    *Source: `computations/module06_examples.py` — `demo_comprehension_filters()`*

**When to use comprehensions vs. loops:**

| Use a comprehension when... | Use a loop when... |
|----------------------------|-------------------|
| Transforming or filtering a list | Logic requires multiple steps |
| The expression fits on one line | You need `if`/`elif`/`else` chains |
| You want a new list as the result | You need side effects (printing, appending to multiple lists) |

!!! question "Try It Yourself: List Comprehension"

    Given the list of employee salaries below, create a new list containing only
    salaries above $60,000, and a second list with each salary increased by 5%.

    ```python
    salaries = [55000, 72000, 48000, 91000, 63000, 85000, 45000]

    # above_60k = [??? for s in salaries if ???]
    # print(f"Above $60k: {above_60k}")

    # with_raise = [??? for s in salaries]
    # print(f"With 5% raise: {with_raise}")
    ```

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| A comprehension modifies the list it reads from. | It always builds a **new** list; the source list is unchanged. |
| The `if` filter goes at the front of the comprehension. | The filter clause comes after the `for` part: `[expr for item in lst if condition]`. |
| Comprehensions are always better than loops. | For multi-step logic, `if`/`elif` chains, or side effects like printing, a regular loop is clearer. Comprehensions shine for one-line transform-or-filter jobs. |
| You need one comprehension to filter and another to transform. | One comprehension does both at once — the expression transforms while the `if` filters, as the under-$100 example shows. |

---

## 6.5 Tuples, Unpacking, and Mutability

Lists and functions work well together — a function can accept a list, process it, and hand back summary values. But what happens when a function needs to return **several** results at once? Python's answer is the **tuple**, and it is also the answer to "how do I represent a fixed record like one employee's name, department, and salary?"

### Functions That Return Several Values

When a function returns several results, it bundles them together and you pull them apart on the way in — `total, average, ... = ...`. That bundle is a tuple; for now, read the assignment line as "give each returned value its own name."

!!! example "Worked Example: Quarterly Sales Summaries from One Function"

    ```python
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
    ```

    **Output:**

    ```
    Q1 Summary:
      Total:   $131,700.00
      Average: $ 43,900.00
      Highest: $ 51,200.00
      Lowest:  $ 38,500.00
      Count:   3 months

    Q2 Summary:
      Total:   $142,800.00
      Average: $ 47,600.00
      Highest: $ 55,100.00
      Lowest:  $ 39,900.00
      Count:   3 months
    ```

    **Interpretation:** One function call yields all the statistics for a quarter — Q1's 3 months total $131,700.00 while Q2 climbs to $142,800.00 — and the built-ins `sum()`, `max()`, `min()`, and `len()` do the heavy lifting on any list of numbers. Writing the function once and calling it per quarter is the reuse principle from the functions module applied to list data.

    *Source: `computations/module06_examples.py` — `demo_summarize_sales()`*

### Tuples: Immutable Sequences

A **tuple** is like a list, but it **cannot be changed** after creation. Tuples use **parentheses** `()` instead of square brackets `[]`:

```python
coordinates = (30.2672, -97.7431)    # Austin, TX
rgb_color   = (255, 128, 0)          # orange
employee    = ("Alice Chen", "Marketing", 72000)
```

You can read items from a tuple using indexing, just like a list. But you cannot assign to an index, append, or remove items.

!!! example "Worked Example: Reading a Tuple — and Failing to Change It"

    ```python
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
    ```

    **Output:**

    ```
    Name: Alice Chen
    Department: Marketing
    Salary: $72,000
    Length: 3

    Error: 'tuple' object does not support item assignment
    Original tuple unchanged: ('Laptop', 999.99, True)
    ```

    **Interpretation:** Reading by index and calling `len()` work exactly as with lists — the record has 3 fields and the salary reads out as $72,000. Writing is where tuples differ: the attempted price change raises `TypeError`, the `try`/`except` catches it, and the product still lists at 999.99. Immutability is a feature — it guarantees a record cannot be altered accidentally.

    *Source: `computations/module06_examples.py` — `demo_tuple_basics()`*

### Why Use Tuples Instead of Lists?

If tuples are just lists you cannot change, why bother?

| Use a **list** when... | Use a **tuple** when... |
|----------------------|----------------------|
| The collection will change (add/remove items) | The data should not change (coordinates, database rows) |
| Order matters and you need to sort | You want to signal "this is fixed" to other programmers |
| You are building up results incrementally | You are returning multiple values from a function |
| The items are all the same type (list of prices) | The items have different roles (name, department, salary) |

Tuples communicate **intent**: "this data is a fixed record, not a growing collection." You have already met them — when Module 4's payroll loop wrote `for name, hours, rate in employees:`, each `(name, hours, rate)` was a tuple.

### Tuple Unpacking: Assigning Multiple Values at Once

**Unpacking** lets you assign each element of a tuple (or list) to a separate variable in a single line:

```python
name, department, salary = ("Alice Chen", "Marketing", 72000)
```

This is more readable than accessing each element by index — and it is the mechanism behind three everyday moves: reading records, looping with `enumerate()` and `zip()`, and swapping variables.

!!! example "Worked Example: Unpacking Records, Catalogs, and Swaps"

    ```python
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
    ```

    **Output:**

    ```
    Employee: Bob Martinez
    Department: Sales
    Salary: $68,000
    City: Houston

    Product Catalog:
      1. Laptop: $999.99
      2. Monitor: $349.50
      3. Keyboard: $79.95

    Before swap: first=Marketing, second=Sales
    After swap:  first=Sales, second=Marketing
    ```

    **Interpretation:** One assignment line replaces four separate index lookups, and every field of the $68,000 record gets a readable name. The catalog loop unpacks at two levels — `enumerate()` hands over a counter while `zip()` hands over a `(product, price)` pair — which is why the loop header reads `for i, (product, price) in ...`. The swap works because Python packs the right-hand side into a tuple before unpacking it on the left, so no temporary variable is needed.

    *Source: `computations/module06_examples.py` — `demo_tuple_unpacking()`*

### Functions Returning Multiple Values

Functions often use tuples to return more than one value. The `return minimum, maximum, average` line below creates a tuple automatically — Python packs the values on the way out, and unpacking assigns them to separate variables on the way in.

!!! example "Worked Example: Analyzing Customer Ratings"

    ```python
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
    ```

    **Output:**

    ```
    Customer Ratings Analysis:
      Ratings: [4.5, 3.8, 4.9, 2.1, 4.7, 3.5, 4.2]
      Lowest:  2.1
      Highest: 4.9
      Average: 4.0
    ```

    **Interpretation:** The function condenses the whole ratings list into three numbers a manager would ask for: the 2.1 outlier that deserves follow-up, the 4.9 high, and the 4.0 average. Note that no parentheses appear in the `return` line — the commas alone create the tuple.

    *Source: `computations/module06_examples.py` — `demo_analyze_scores()`*

### Mutability in Action: The Shared-Reference Gotcha

Mutability affects how Python handles your data behind the scenes. When you write `backup = departments`, you do **not** get a copy — both names point to the **same list** in memory, and changing one changes the other. To make an independent copy, use the `.copy()` method (or a full slice `[:]`). Tuples sidestep the problem entirely, because they cannot be modified in the first place.

!!! example "Worked Example: Aliasing vs. an Independent Copy"

    ```python
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
    ```

    **Output:**

    ```
    Original: ['Marketing', 'Sales', 'Engineering', 'Finance']
    Backup:   ['Marketing', 'Sales', 'Engineering', 'Finance']
    Same object? True

    Original: [10, 20, 30, 40, 50]
    Copy:     [10, 20, 30, 40]
    Same object? False
    ```

    **Interpretation:** Appending Finance through one name changed the "backup" too, and the `is` check confirms both names refer to one object — the supposed backup never existed. With `.copy()`, appending 50 leaves the copy untouched and `is` reports two separate objects. In business terms: never "back up" a dataset with plain assignment before modifying it.

    *Source: `computations/module06_examples.py` — `demo_aliasing_and_copy()`*

### Useful Built-in Functions for Lists

Python provides several built-in functions that work on any list — you have now seen most of them in action:

| Function | What it does | Example |
|----------|-------------|---------|
| `len(lst)` | Number of items | `len([1,2,3])` → `3` |
| `sum(lst)` | Sum of all items | `sum([10,20,30])` → `60` |
| `min(lst)` | Smallest item | `min([10,20,30])` → `10` |
| `max(lst)` | Largest item | `max([10,20,30])` → `30` |
| `sorted(lst)` | Return a sorted copy | `sorted([3,1,2])` → `[1,2,3]` |
| `reversed(lst)` | Return items in reverse order | `list(reversed([1,2,3]))` → `[3,2,1]` |
| `zip(a, b)` | Pair up items from two lists | `list(zip([1,2],[3,4]))` → `[(1,3),(2,4)]` |
| `enumerate(lst)` | Pair each item with its index | `list(enumerate(["a","b"]))` → `[(0,"a"),(1,"b")]` |

### Putting It All Together: Sales Performance Report

The closing example combines lists, tuples, unpacking, functions, and comprehensions in a realistic scenario: monthly sales data for a team of representatives, from which you need each person's total, a performance classification, and a formatted report.

!!! example "Worked Example: Quarterly Sales Performance Report"

    ```python
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
    ```

    **Output:**

    ```
    =================================================================
      QUARTERLY SALES PERFORMANCE REPORT
      (Target: $120,000.00 per rep)
    =================================================================
      Name               Region          Total Status
    -----------------------------------------------------------------
      Alice Chen         West      $131,700.00 Above Target
      Bob Martinez       South     $113,500.00 Below Target
      Carol Davis        East      $146,500.00 Above Target
      Dave Kim           West      $104,500.00 Below Target
      Eve Johnson        South     $156,000.00 Above Target
    -----------------------------------------------------------------
      Team Total: $652,200.00
      Team Average: $130,440.00
      Top Performers: Alice Chen, Carol Davis, Eve Johnson
    =================================================================
    ```

    **Interpretation:** Each rep is a *tuple* (a fixed record) holding a *list* (a growing series of monthly figures) — the two structures nested to match the shape of the data. The loop unpacks each record, the functions compute and classify against the $120,000.00 target, the accumulator collects result tuples, and two comprehensions produce the summary: a team total of $652,200.00, a $130,440.00 average, and the roster of reps above target. Every concept in this module appears in these lines, and this is the pattern your assignment's combined challenge asks you to reproduce.

    *Source: `computations/module06_examples.py` — `demo_sales_performance_report()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| `backup = my_list` creates a safe copy. | Both names now point to the *same* list — changes through either name affect both. Use `my_list.copy()` or `my_list[:]` for an independent copy. |
| A function returning several values performs some special multi-return. | It returns exactly one value: a tuple. `return a, b, c` packs a tuple; `x, y, z = f()` unpacks it. |
| Unpacking ignores extra elements. | The number of variables must match the number of elements exactly, or Python raises a `ValueError`. Count the fields in the record before unpacking. |
| Tuples are pointless read-only lists. | Immutability protects fixed records from accidental change, signals intent to other programmers, and is the standard vehicle for multi-value returns and mixed-role fields like `(name, department, salary)`. |

---

## Reflection Questions

1. A colleague stores each customer order as a list (`["Acme Corp", "2026-07-15", 4890.00]`) and another colleague stores the same record as a tuple. What can go wrong with the list version during a long analysis session, and what does the tuple version give up in exchange for that safety?
2. The accumulator filter in §6.3 and the comprehension filter in §6.4 produce the same kind of result. What signals in a task would lead you to write one instead of the other, and how does each choice affect a teammate reading your code later?
3. Zero-based indexing means the "first" item lives at index 0. Where in a monthly-report scenario could this off-by-one behavior silently produce a wrong-but-plausible number rather than an error, and how would you catch it?
4. The shared-reference gotcha in §6.5 made a "backup" that was not a backup. Describe a real business situation — a price list, a budget draft — where this bug could go unnoticed until it caused visible damage, and the one-line change that prevents it.
5. `summarize_sales()` returns five values as a tuple that the caller unpacks into named variables. Compare this design to a function that simply prints the five statistics itself. What can the caller do with unpacked values that printed output cannot support?
6. Parallel lists (`months` and `sales`) rely on positions staying aligned. Which everyday operations from §6.2 could break that alignment, and why might a list of tuples like `("March", 51200)` be more robust?

---

## Your Assignment

The Module 6 assignment, **Lists & Tuples**, is worth **100 points plus a 10-point bonus**. You complete it in the provided marimo notebook and submit the `.py` file to Brightspace. The closing reflection section is not graded separately — it counts toward participation. Two habits from the notebook's tips will save you grief: list methods like `.append()` and `.sort()` modify the list in place and return `None` (never write `x = x.append(item)`), and `sorted()` is the tool when you need an ordered copy without changing the original.

### Task 1: List Creation, Indexing, and Slicing (10 points)

A regional bank's branch cities are listed in the order they were opened. Using indexing and slicing only — no loops — print specific individual branches (first, most recent, third), extract the oldest and most recent groups as sublists, and report the total branch count. Everything you need is in §6.1: zero-based and negative indexing, slice notation, and `len()`.

### Task 2: List Methods (15 points)

A project manager's task board is a Python list that you modify step by step: append a new task, insert one at a given position, remove a completed task, sort alphabetically, then pop the last item and show what came off. You print the list after each operation to watch it evolve. The methods — and the in-place behavior that makes printing after each step meaningful — are covered in §6.2.

### Task 3: Iterating with Loops and `enumerate()` (15 points)

Given parallel lists of weekday names and daily revenue, use a `for` loop to compute the weekly total, a loop that tracks positions to find the highest- and lowest-revenue days (reporting both day name and amount), and `enumerate()` to print a numbered daily report. The built-ins `sum()`, `max()`, and `min()` are off-limits here — the point is writing the accumulator and best/worst logic yourself, as demonstrated in §6.3 (`len()` is allowed).

### Task 4: List Comprehensions (15 points)

From a list of retail prices, build three new lists using comprehensions rather than loops: discounted sale prices rounded to two decimals, a filtered list of premium items above a price cutoff, and formatted price-label strings. The transform, filter, and formatting comprehension patterns all appear in §6.4.

### Task 5: Tuples and Unpacking (20 points)

Employee records arrive as `(name, department, annual_salary)` tuples. Part A: write a `format_employee` function (with a docstring) that unpacks one record and returns a formatted directory line. Part B: loop through the employee list calling your function, and compute the average salary. Part C: demonstrate immutability by attempting to modify a tuple inside a `try`/`except` block and printing the error. Tuples, unpacking, and the immutability error are all in §6.5; the docstring conventions come from Module 4.

### Task 6: Combined Challenge — Inventory Analysis (25 points)

Warehouse items are `(product_name, category, quantity, unit_price)` tuples. You write two docstringed functions — one computing an item's total value, one classifying its stock level — then a loop that unpacks each record, calls both functions, prints an aligned report line, and accumulates the total inventory value. A list comprehension collects the low-stock product names for the closing summary. This task mirrors the structure of the capstone report in §6.5, drawing on iteration from §6.3 and comprehensions from §6.4.

### Task 7: Creative Exercise — Bonus (10 points)

Design your own business scenario demonstrating lists and tuples: a grade book, a flight tracker, a restaurant order system, and a real-estate analyzer are suggested directions. Whatever you choose must include a list of at least five tuple records, at least two functions with docstrings, tuple unpacking in a loop, at least one list comprehension, a summary calculation, and clearly formatted output.

### Reflection (participation credit)

Answer the notebook's four reflection prompts in your own words: when you would choose a list versus a tuple, where tuple unpacking made your code cleaner, how you decide between a loop-with-append and a comprehension, and what challenged you most. There is no wrong answer — honest reflection helps your instructor see where support is needed.

---

## Chapter Summary

Lists are ordered, mutable collections built with square brackets. Zero-based indexing reaches any single item (with negative indexes counting from the end), slicing extracts a sublist without touching the original, and assignment to an index changes an item in place — the mutability that separates lists from strings. A family of methods handles maintenance: `.append()`, `.insert()`, and `.extend()` grow a list; `.remove()` and `.pop()` shrink it; `.sort()` reorders it in place and returns `None`, while the built-in `sorted()` returns an ordered copy and leaves the source alone.

Loops turn lists into analysis. A `for` loop visits every item; an accumulator builds a total or collects matching items into a new list; and `enumerate()` supplies the position alongside the value — the key to numbered reports, best/worst tracking, and parallel lists. List comprehensions compress the create-loop-append pattern into a single readable line, with an optional `if` for filtering and `zip()` to walk two lists together; multi-step logic and side effects still belong in ordinary loops.

Tuples are the immutable counterpart: fixed records whose fields play different roles, written with parentheses and incapable of being modified after creation. They power multi-value returns — `return minimum, maximum, average` packs a tuple that the caller unpacks into named variables — and unpacking is the same mechanism that makes `enumerate()`, `zip()`, and the no-temporary-variable swap read cleanly. Mutability carries one final lesson: assigning a list to a second name shares one object rather than copying it, so an independent backup requires `.copy()`. The closing sales-performance report combined every one of these pieces, and the assignment asks you to build the same kind of pipeline yourself.

---

## What's Next

Module 7 introduces **dictionaries and sets** — data structures that look up values by *name* instead of by position. Where this module's parallel lists linked a month to its sales figure by index, a dictionary makes the link explicit: `sales["March"]`. Dictionaries are essential for structured data and will prepare you for loading JSON files and building data pipelines later in the course, while sets provide fast membership tests and duplicate removal. The tuples you mastered here return immediately — as fixed records stored inside dictionaries and as the items dictionaries hand back when you loop over them.
