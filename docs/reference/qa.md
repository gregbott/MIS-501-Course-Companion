# MIS 501 Course Companion — Q&A Reference

This page collects the questions students most often ask while working through MIS 501, organized by module. Each answer summarizes what the corresponding chapter teaches, in plain language — use it as a quick reference alongside the full module pages.

---

## Module 1: Why Python & Environment Setup

### Q: Do I have to give up Excel now that I'm learning Python?

No. The tools coexist, and the course never asks you to abandon a spreadsheet. Think of Excel as the pocket knife you already own — great for quick, small tasks — and Python as the Swiss Army knife you are adding for the jobs Excel handles poorly. Python earns its place when the data grows large, when the steps must be reproducible, or when the same analysis has to run again next quarter without manual rework.

In practice, many analysts move between the two: Python does the heavy processing and produces a clean CSV, and Excel remains a perfectly good place to eyeball the result. The comparison table in the chapter is about where each tool fits, not about declaring a winner.

---

### Q: What does it mean that Python is an "interpreted" language, and why does that help me as a beginner?

A compiled language is like writing a book and sending it to a publisher — you have to finish the whole thing before anyone can read it. An interpreted language is like having a simultaneous translator: you say one sentence, it is understood immediately, and you can say the next one. Python works the second way. You write one line, run it, and see what happens right away.

That instant feedback loop is what makes learning by experiment practical. You never have to build a complete program before finding out whether your idea works — you can try a calculation, look at the result, adjust, and try again. Most of your learning this semester will happen through exactly that cycle.

---

### Q: Why do I need Pixi — can't I just install Python once and be done?

Different projects need different packages and different versions of those packages, and installing everything into one shared Python eventually creates conflicts. Pixi works like an app store for Python: it installs Python itself, installs the libraries your project needs, keeps each project's tools separate from every other project's, and records the whole setup in a `pixi.toml` file.

That file is the real payoff. It is a recipe card, not a program — it lists what the project needs, and anyone who has it can recreate your exact environment on their own machine. In business terms, that is what makes an analysis reproducible: a colleague, a grader, or future you can rerun your code and get the same results without borrowing your computer.

---

### Q: How is a marimo notebook different from the traditional notebooks I've heard about?

Marimo is reactive, the way a spreadsheet is: when you change a cell, every cell that depends on it reruns automatically. That has two practical consequences. First, you can never be looking at stale output left over from an earlier run — displayed results always match the current code. Second, you never have to remember to "run all cells from the top," because marimo works out the correct execution order from the dependencies between cells.

One more practical detail: a marimo notebook is stored as a plain Python `.py` file. That is the file you edit, the file you save, and the file you submit to Brightspace for assignments — you can open it in any text editor.

---

### Q: Why does `10 / 5` print as `2.0` instead of `2`, and what are `//` and `%` for?

Python has a family of division operators, and they answer different questions. The regular `/` always performs true division and keeps the decimal part, so the result is a float even when it comes out even — that is why you see `2.0`. The `//` operator does integer division and keeps only the whole number of times the divisor fits, and `%` (modulo) reports what is left over.

The last two are a natural pair for business questions like "how many full cases can we ship, and how many leftover units remain?" — `//` gives the cases, `%` gives the leftovers.

---

### Q: Why does my calculation print with a long tail of digits like a margin of 28.888888888888886?

Python is showing you the division at full precision — nothing is wrong with the stored value. Computers represent decimal numbers this way, and raw output simply displays everything. It looks alarming next to a tidy spreadsheet cell, but it is a display issue, not a calculation error.

The fix is formatting, not rounding the underlying number. Module 2 introduces f-strings and format specifiers, which let you display the same value as a clean, report-ready figure with exactly the decimal places you want, while the full-precision value stays available for further math.

---

### Q: The teaching notebook writes `_revenue` with a leading underscore, but the companion writes `revenue` — which is right?

Both, in their own context. Because marimo runs cells reactively, an ordinary variable name may only be defined in one cell of a notebook. Prefixing a name with `_` marks it as belonging to that cell only, which is how the notebooks reuse convenient names like `_revenue` or `_total` in cell after cell without collisions.

The underscore is a marimo convention, not part of Python's rules. In a plain Python script — like the examples in the companion — you simply write `revenue`. In your own assignment notebooks, follow the convention: underscore for cell-scoped temporaries, no underscore for variables other cells need to read.

---

## Module 2: Variables, Data Types & Expressions

### Q: Why store an employee ID like "EMP-2847" as a string when it's mostly digits?

Because it is a label, not a quantity. The test is whether arithmetic on the value would ever make sense: you would never add two employee IDs, average ZIP codes, or multiply phone numbers. Values like that belong in strings, where the quotes make Python treat them as text.

You give up mathematical operations by storing them this way, but that is exactly the point — losing the ability to do math on an ID is a feature, because any math on it would be a bug. The same reasoning applies to ZIP codes, phone numbers, and product codes throughout the course.

---

### Q: What's the difference between `=` and `==`?

One equals stores; two equals compares. Writing `x = 5` is an assignment — it puts the value 5 into the variable `x`. Writing `x == 5` asks a question — "is x equal to 5?" — and produces a boolean answer, `True` or `False`.

This trips up almost everyone at first, because in math class `=` meant equality. In Python, comparisons always use `==`, and the boolean they produce is ordinary data you can store in a variable, print, or use in later logic — which becomes the foundation of the `if` statements in Module 3.

---

### Q: I imported data from a spreadsheet and my calculations misbehave. Why does adding two of the values glue them together instead of adding them?

Data exported from spreadsheets and CSV files often arrives with every value as a string, even the ones that look like numbers. For strings, the `+` operator means concatenation — joining text end to end — so "adding" two numeric-looking strings produces one long string rather than a sum, and subtraction fails outright because `-` has no meaning for text.

The fix is to convert before calculating: `int()` for whole numbers and `float()` for decimals turn the text into real numbers. When a calculation misbehaves, `type()` is your first diagnostic tool — checking what type a value actually is usually reveals the problem immediately. This convert-before-calculating step is one of the most common data-cleaning moves you will make all semester.

---

### Q: Are `42` and `42.0` interchangeable?

They are two different types: `42` is an `int` (integer) and `42.0` is a `float` (a number with a decimal point). The course convention is to use integers for things you count — employees, units sold, years — and floats for things you measure — prices, percentages, weights.

Python usually handles the distinction gracefully. Mixing them in arithmetic promotes the result to a float so no precision is lost, and division with `/` always produces a float even when the answer is a whole number. The distinction matters most when you are reading a table's output and reasoning about what kind of value each column holds.

---

### Q: Why is `bool("0")` True? I thought zero was falsy.

The number `0` is falsy, but `"0"` with quotes is not a number — it is a string containing one character. Python's rule for strings is simple: only the *empty* string converts to `False`; any non-empty string, including `"0"` and even `"False"`, converts to `True`.

The full falsy list is short: `0`, `0.0`, the empty string `""`, and `None`. Everything else is truthy. This matters in practice for questions like "did the customer leave the comment field blank?" — converting the field to a boolean answers it directly, but only if you remember the rule applies to emptiness, not to what the text says.

---

### Q: My f-string printed `{name}` literally instead of the value — what went wrong?

You almost certainly left off the `f` before the opening quote. Without it, `"{name}"` is an ordinary string and the braces are just characters, so they print as-is. With the `f` prefix, the braces become windows: Python looks through them, evaluates whatever is inside, and inserts the result into the text.

It is an easy mistake to make and an easy one to spot once you know the symptom — literal curly braces in your output are the giveaway.

---

### Q: For percentages, do I multiply by 100 before using the `:.1%` format? And does formatting change my stored value?

No on both counts. The `%` specifier does the multiplication and adds the percent sign itself, so you pass the raw decimal fraction — a margin stored as a fraction displays correctly on its own, while pre-multiplying it produces an absurdly inflated percentage. Hand the specifier the decimal and let it do the work.

More generally, format specifiers like `:,.2f` and `:.1%` control only the *display*. The variable still holds its full-precision value for later calculations, which is exactly what you want: clean numbers in the report, exact numbers in the math.

---

## Module 3: Control Flow

### Q: Does every `if` need an `else`?

No — `else` is optional. An `if` on its own simply does nothing when its condition is `False`, and often that is exactly the behavior you want: print a warning only when stock is low, apply a discount only when the order qualifies, and otherwise carry on.

Add `else` when there genuinely are two paths — when something different should happen in the `False` case. And when there are more than two possibilities, that is what `elif` chains are for.

---

### Q: Why does the order of my `elif` conditions matter?

Because Python checks the conditions from top to bottom and runs the *first* one that is `True`, skipping everything after it. Only one branch of an `if`/`elif`/`else` chain ever executes.

That makes the ordering part of the logic itself. In the customer-tier example, the thresholds run from highest to lowest so a big spender hits the top tier first. If the conditions were listed lowest-first, every large value would satisfy the small threshold and stop there — labeling your best customers with the bottom tier, with no error message to warn you.

---

### Q: Is indentation just a style preference in Python?

No — indentation *defines* the structure of your code. The indented block under an `if` is what runs conditionally; the indented block under a `for` is what repeats. Change the indentation and you change what the program does, or you get an `IndentationError`.

A classic symptom: a summary line indented inside a loop prints on every iteration, while the same line un-indented prints once after the loop finishes. When output repeats unexpectedly or a line seems to be skipped, check the indentation before anything else.

---

### Q: Why doesn't `range(5)` include 5?

`range()` starts at 0 by default and always stops *before* the stop value, so `range(5)` produces 0 through 4 — five numbers, but not the number 5 itself. The same rule holds with explicit start and stop values, and it even holds counting down: a negative step counts backward but still excludes the stop value.

It feels arbitrary at first, but it is consistent with how Python counts everywhere (indexing also starts at zero, as you will see with strings and lists). If you need a count that starts at 1 for human readers, generate the range you need or add one in the display.

---

### Q: How do I choose between a `for` loop and a `while` loop?

Use `for` when you know what you are looping *over* — each item in a list, each number in a range, each row in a batch. Use `while` when you do not know in advance how many repetitions you need, only the condition that ends them: keep depositing until the balance reaches the goal, keep processing until capacity is hit.

Choosing wrong usually shows up as awkward code. A `for` loop forced into a "run until" problem needs artificial exit logic, and a `while` loop forced into an "each item" problem needs manual position tracking that `for` would have handled automatically.

---

### Q: My `while` loop has been running forever — what did I do wrong?

Nothing inside the loop body is changing the condition, so it never becomes `False`. This is the infinite loop, and it is a logic problem rather than a Python malfunction: the loop is doing exactly what you told it, indefinitely.

The fix is to make sure some statement in the body moves the loop toward its end — a deposit that grows the balance, a counter that increments, stock that decreases. When a loop runs suspiciously long, read the body and ask: which line here changes the variable my condition tests? If the answer is "none," you have found the bug.

---

### Q: What's the difference between `break` and `continue`?

`break` is the emergency exit: it ends the innermost loop immediately, skipping all remaining iterations, and the program continues after the loop. `continue` is the "skip this one" button: it abandons only the rest of the *current* iteration and moves on to the next item, keeping the loop alive.

The chapter's examples show the natural use of each — `break` stops processing orders the moment daily capacity would be exceeded, while `continue` skips invalid transactions in a data feed but keeps processing the valid ones. Note that `break` exits only the loop, not the whole program, and `continue` does not restart anything — totals and counters accumulated so far are untouched.

---

### Q: My running total keeps resetting — where does the accumulator variable belong?

Before the loop, always. The accumulator pattern is: initialize `total = 0` (or an empty collection) *above* the loop, then add to it inside the body. If the initialization sits inside the loop, it reruns on every pass and wipes out everything accumulated so far — the total you print at the end reflects only the final item.

The same placement logic applies to counters. And the mirror-image mistake is worth knowing too: the final `print` of the total belongs *after* the loop, un-indented, or it will print once per iteration instead of once at the end.

---

## Module 4: Functions & Modular Thinking

### Q: I wrote my function with `def` and ran the cell, but nothing happened. Why?

Because defining a function and calling it are two separate things. `def` only *registers* the function — the body sits and waits. Nothing inside it runs until you call the function by writing its name followed by parentheses, with any required arguments inside.

This is by design: a function is a tool you build once and use many times, so building it should not also run it. If you defined a function and saw no output, the definition worked — you just have not called it yet.

---

### Q: My function prints the right answer, but when I try to use the result in another calculation I get `None`. What's going on?

Your function uses `print()` where it should use `return`. Printing displays a value on screen and then discards it — the function hands back `None`, Python's word for "nothing," so there is no value for the caller to store or compute with. Returning, by contrast, sends the value back to the code that called the function, where it can be saved in a variable, added to something else, or passed along.

The rule of thumb: use `return` whenever the result might feed a further calculation, which is almost always. Reserve `print()` for the moments when displaying something to a human is the actual goal.

---

### Q: What's the difference between a parameter and an argument?

Parameters are the variable names listed in the function *definition* — think of them as labeled slots. Arguments are the actual values you supply when you *call* the function — the values that get plugged into those slots for that particular call.

So in a tax function defined with `amount` and `rate`, those two names are parameters; the specific purchase price and tax rate you pass in a call are arguments. The distinction matters when reading error messages and documentation, both of which use the terms precisely.

---

### Q: I passed my arguments in the wrong order and got no error — just a wrong answer. How do I protect against that?

Python matches positional arguments purely by position, so swapping two of them silently sends each value to the wrong slot. A shipping calculator fed weight-and-distance in reverse computes a confident, plausible-looking, wrong cost — the mistake only surfaces when someone questions the number.

The protection is keyword arguments: name each argument at the call site (`weight=10, distance=200`). Values are routed by name rather than position, so order no longer matters, and the call documents itself — a reviewer can see at a glance which number is which. This course prefers keyword arguments whenever a function takes more than one parameter, for exactly this reason.

---

### Q: I typed my function's name without parentheses and got something like `<function calculate_tax at 0x...>`. What is that?

That is the function *object* itself, not the result of running it. In Python, a function's bare name refers to the function as a thing — which is occasionally useful, for example when passing a function to `sorted()` — but it does not execute the body. Only the parentheses trigger a call, even for functions that take no arguments.

Forgetting the parentheses is one of the most common beginner mistakes precisely because it produces no error message — just an unexpected value where you wanted a result. If you ever see `<function ...>` in your output, add the parentheses.

---

### Q: I changed a variable inside my function, but outside the function it still has the old value. Why?

Because of scope. An assignment inside a function creates a *local* variable by default — a new variable that exists only while the function runs, even if it happens to share a name with a variable outside. The outer variable is untouched; the local one simply shadows it inside the function and vanishes when the function returns.

Functions can *read* outer variables freely, but overwriting them requires the `global` keyword — which the course treats as a last resort. The disciplined pattern is: data goes in through parameters, results come out through `return`. Functions that communicate only that way are easier to test, reuse, and reason about, and they never surprise you by silently modifying something elsewhere in the program.

---

### Q: How is a docstring different from a comment?

A comment (anything after `#`) is invisible to Python — it exists purely for human readers of the source code. A docstring — the triple-quoted string on the first line of a function body — is attached to the function object itself. Python's built-in `help()` prints it on demand, and most editors display it when you hover over a call to the function.

That attachment is what makes docstrings worth the extra structure: a summary line, an `Args:` section describing each parameter, and a `Returns:` section describing the output turn your function into a documented tool that colleagues can use without reading its body.

---

### Q: When should I use a lambda instead of a regular function?

Use a lambda when the logic is a single expression, you need it only once, and it is simple enough to understand at a glance — the flagship case is a sort key, where `sorted()` needs a small rule like "rank each item by its price." Writing a full named `def` for one-time, one-expression logic is more ceremony than the job deserves.

Use `def` for everything else: logic that needs multiple lines, anything you will call from several places, and anything that benefits from a name and a docstring. Lambdas are not faster or more powerful — they compute identically — so when in doubt, choose the readable option, which is usually `def`.

---

## Module 5: Strings & Regular Expressions

### Q: Why does `text[1]` give me the second character instead of the first?

Because indexing starts at 0: the first character lives at position 0, the second at position 1, and so on. This off-by-one surprise catches every beginner once, and it is worth internalizing early because it produces wrong extractions rather than error messages — slicing an invoice ID from the wrong position quietly returns the wrong piece of text.

Negative indexes count from the end, so `text[-1]` is the last character regardless of the string's length — handy when you do not know how long the value is. The same zero-based rules apply to lists in Module 6, so this investment pays off twice.

---

### Q: I called `name.strip()` but my variable still has the extra spaces. Why?

Strings are immutable — they cannot be changed in place. Methods like `.strip()`, `.upper()`, and `.replace()` do not edit your string; they *return a new one* with the transformation applied. If you call the method without capturing the result, the cleaned version is created and immediately discarded.

The fix is an assignment: `name = name.strip()` replaces the old value with the cleaned copy. This same return-a-new-string behavior is what makes method chaining work — each method hands a fresh string to the next one in the chain.

---

### Q: When should I use plain string methods, and when do I need regular expressions?

Use the simplest tool that works. String methods handle fixed, predictable transformations: stripping whitespace, changing case, replacing one exact substring with another, splitting on a known delimiter and joining the pieces back together. Regular expressions take over when the text's *shape* varies — "find every date in this document," "extract anything that looks like a dollar amount" — because a regex describes a pattern rather than exact characters.

Real cleaning code mixes both freely: the chapter's customer-directory pipeline uses `.strip()` and `.title()` for names but a regex to pull ZIP codes out of free-form addresses. Reaching for regex when a method would do makes code harder to read; the reverse leaves you writing fragile position-based hacks.

---

### Q: What does the `r` in `r"\d{2}"` mean, and do I really need it?

The `r` makes the string a *raw string*, which tells Python not to interpret backslash sequences as escape characters before the `re` module ever sees the pattern. Regex patterns are full of backslashes — `\d`, `\s`, `\w` — and without the `r`, Python may transform some of them first, leaving `re` with a subtly different pattern than the one you wrote.

The failure mode is what makes this dangerous: a mangled pattern often does not raise an error, it just matches the wrong things or nothing at all. The course rule is simple — write every regex pattern as a raw string, no exceptions.

---

### Q: What's the difference between `re.search`, `re.match`, and `re.findall`?

`re.search` scans the whole text and stops at the first match. `re.match` succeeds only if the pattern matches at the very *beginning* of the string — which makes it a natural validator ("does this code start with the invoice prefix?") but means it will never find a pattern sitting in the middle of the text. `re.findall` keeps scanning and returns every match as a list of plain strings.

Choose by the question you are asking: "is it there / where is the first one?" is `search`, "does this value have the right format from the start?" is `match`, and "give me all of them" is `findall`. There is also `re.sub`, the fourth workhorse, which replaces every match — either with a fixed string or with a function that transforms each match individually.

---

### Q: My code crashed calling `.group()` with an error about `None`. What happened?

`re.search` and `re.match` return a match object when they find something — and `None` when they do not. Calling `.group()` on `None` raises an error, so the crash means your pattern found no match in that particular text.

The defensive habit is to test before extracting: `if match:` guards the `.group()` call, and the `else` branch decides what a missing match means for your program — skip the record, use a default, log a warning. Real documents always contain lines that do not fit the expected format, so a parser that assumes every search succeeds is a parser that crashes on real data.

---

### Q: I added parentheses to my pattern and now `findall` returns something different. Why?

Parentheses create *capturing groups*, and groups change what `re.findall` gives back. With no groups, it returns the full matched text. With exactly one group, it returns only that group's captured piece. With two or more groups, it returns tuples of the captured pieces — which is often exactly what you want, since extracting an invoice ID and its amount as paired tuples keeps them correctly matched up.

When you only need parentheses for grouping — say, to make part of the pattern optional — and do not want them to affect the output, use a non-capturing group, written `(?:...)`. The chapter's pattern reference table uses that form so `findall` keeps returning whole matches.

---

### Q: Why does `float("1,250.00")` fail on my dollar amounts?

Python's `float()` does not understand thousands separators — the comma makes the string unparseable as a number, even though a human reads it instantly. Currency symbols cause the same failure.

The fix is to strip the formatting before converting: remove the commas (and any dollar sign) with `.replace()`, then call `float()` on what remains. The chapter's sales-report parser does exactly this, and the same clean-then-convert move reappears when you scrape formatted numbers off web pages later in the course.

---

## Module 6: Data Structures: Lists & Tuples

### Q: I wrote `prices = prices.sort()` and now my list is gone. What happened?

`.sort()` sorts the list *in place* and returns `None` — so your assignment replaced the list variable with `None`, discarding the data. The sorting actually happened, but you overwrote the reference to it.

There are two correct patterns, and the choice depends on whether you want to keep the original order. Call `prices.sort()` on its own line to reorder the list itself, or use the built-in `sorted(prices)` to get an ordered *copy* while the original stays untouched. The copy matters more often than beginners expect: if your list is in chronological order, an in-place sort destroys that ordering permanently — a classic reporting bug.

---

### Q: What's the difference between `.append()` and `.extend()`?

`.append()` adds its argument as *one* item — so appending a list puts the whole list inside your list as a single nested element. `.extend()` adds each element of its argument individually, merging the items in.

The rule of thumb: one new item, `.append()`; a batch of new items from another collection, `.extend()`. If you ever see a list-inside-a-list where you expected a longer flat list, an `.append()` that should have been `.extend()` is the usual culprit.

---

### Q: Does `.remove()` delete every copy of an item?

No — it removes only the *first* occurrence and leaves any duplicates later in the list untouched. If your inventory list contains an item twice and you `.remove()` it once, one copy survives.

Its sibling `.pop()` behaves differently in another way worth knowing: it removes an item by position (the last one by default) and *returns* it, so your code can act on what was taken off — fulfill it, log it, refund it. `.remove()` searches by value and returns nothing.

---

### Q: When should I use a tuple instead of a list?

Use a list when the collection will change — items added, removed, sorted — and when the items are all the same kind of thing, like a list of monthly sales figures. Use a tuple when the data is a fixed record whose fields play different roles, like a name-department-salary record, and when nothing should be able to modify it after creation.

Tuples cannot be changed — assigning to an index raises an error — and that immutability is a feature, not a limitation: it guarantees a record cannot be altered accidentally, and it signals your intent to other programmers. Tuples are also the standard vehicle for functions that return several values at once.

---

### Q: I made a backup with `backup = my_list`, but changing the original changed the backup too. Why?

Because plain assignment does not copy anything — it creates a second *name* for the same list object in memory. Both names point at one list, so a change made through either name is visible through both. The supposed backup never existed.

To make an independent copy, use `my_list.copy()` (or the full slice `my_list[:]`). After that, modifying the original leaves the copy untouched. The business translation: never "back up" a dataset with plain assignment before modifying it. Tuples sidestep the whole problem — since they cannot be modified, sharing one is always safe.

---

### Q: How can a function return more than one value?

By returning a tuple — and Python makes the syntax almost invisible. Writing `return minimum, maximum, average` packs the three values into a tuple automatically, and the caller unpacks them in one assignment: `low, high, avg = analyze_scores(...)`. Each returned value lands in its own named variable.

Technically the function still returns exactly one thing — a tuple — but the pack-and-unpack pattern makes it feel like a genuine multi-value return. One rule to respect: the number of variables on the left must match the number of values returned, or Python raises an error. Count the fields before unpacking.

---

### Q: Why use `enumerate()` instead of keeping my own counter or looping over `range(len(...))`?

`enumerate()` hands you the position and the item together on each pass, which is cleaner than maintaining a counter variable by hand and less error-prone than indexing into the list from a range. It counts from 0 — matching list indexing — so display-friendly numbering is just a matter of adding one in the print statement.

The position it gives you is also the key to parallel lists: the index for the months list is the same position to read from the sales list, which is how the chapter's report pairs each month with its figure and how the best/worst-month search remembers *where* the extremes occurred, not just what they were. If you do not need the position at all, skip both tools and iterate directly: `for item in my_list:`.

---

### Q: When is a list comprehension better than a regular loop?

A comprehension shines for one-line transform-or-filter jobs: apply a discount to every price, keep only the orders above a threshold, clean every name in a column. It compresses the create-empty-list, loop, append pattern into a single readable line that often mirrors the business sentence it implements — and it always builds a *new* list, leaving the source untouched.

Stick with a regular loop when the logic takes multiple steps, needs `if`/`elif`/`else` chains, or has side effects like printing or updating several collections at once. The goal is readability, not compactness for its own sake — a comprehension nobody can parse at a glance is worse than the three-line loop it replaced.

---

## Module 7: Data Structures: Dictionaries & Sets

### Q: When should I use a dictionary instead of two parallel lists?

Whenever the data is really a set of labeled lookups rather than a sequence. Parallel lists — one of product names, one of prices — link items only by position, and that link is fragile: sort one list, insert into one but not the other, or delete a single element, and every pairing after that point is silently wrong.

A dictionary makes the link explicit: the product name is the key, the price is the value, and `prices["Laptop"]` reads exactly like the business question it answers. The rule of thumb from the chapter: if you find yourself looking things up by name rather than by position, you want a dictionary.

---

### Q: What's the difference between `d["key"]` and `d.get("key")`?

They behave identically when the key exists. The difference is the missing-key case: square brackets raise a `KeyError` and stop your program, while `.get()` quietly returns `None` — or a fallback of your choosing if you pass one as the second argument.

Which behavior is better depends on the situation. Use brackets when the key is guaranteed and a missing one would indicate a real bug worth crashing on. Use `.get()` when the field is genuinely optional — one employee has a title on file, another does not — and your code should carry on with a sensible default. Real business records are incomplete often enough that `.get()` earns constant use.

---

### Q: Why did `counts[item] += 1` crash the first time an item appeared?

Because incrementing requires an existing value to add to, and the first time a category shows up there is nothing under that key yet — so the lookup raises a `KeyError`. Counting with a dictionary always has to handle the "first sighting" case.

Two patterns solve it. The explicit version checks membership first: if the item is already a key, increment; otherwise set it to 1. The compact version collapses that into one line with `counts.get(item, 0) + 1` — `.get()` supplies zero for a never-seen item, so the increment works from the first occurrence. Both produce identical results; the shortcut is simply less code, and this counting pattern reappears throughout the course's reporting work.

---

### Q: Does `"Laptop" in inventory` search the keys or the values?

The keys. The `in` operator on a dictionary answers "is this a key?" — which is usually what you want, since guarded access (`if name in prices:` before `prices[name]`) is the bracket-safe alternative to `.get()`.

To search the values instead, be explicit: `value in inventory.values()`. Mixing these up produces logic that looks right and quietly answers the wrong question, so it is worth pausing on every dictionary membership test to confirm which side of the key-value pair you mean.

---

### Q: I wrote `{}` to make an empty set and got a dictionary instead. Why?

Because the two structures share curly braces, and Python had to give the empty braces to one of them — the dictionary won. `{}` is always an empty dictionary; the only way to write an empty set is `set()`.

Non-empty literals are unambiguous — `{"a": 1}` has a colon so it is a dictionary, `{"a", "b"}` has bare values so it is a set — which is why the trap only exists for the empty case. It is a small rule, but it appears in the chapter and the assignment because everyone hits it once.

---

### Q: Why can't I write `my_set[0]`, and why does my set print in a different order than I typed it?

Sets are unordered collections — they have no positions, so there is nothing for an index to refer to, and the iteration order you observe is arbitrary rather than the insertion order. That is the trade sets make: they give up ordering and duplicates in exchange for guaranteed uniqueness and fast membership tests.

When you need a stable, readable display, sort the set at the moment of output — `sorted(my_set)` returns an ordered list — which is exactly what the chapter's examples do. If your problem genuinely needs positions or duplicates, the right structure is a list, not a set.

---

### Q: What are set operations actually good for in a business setting?

They answer comparison questions between two groups directly, in one line each. Union is "everything either group covers" — the full skill inventory across two teams. Intersection is "what both share" — the customers who ordered in both quarters. Difference is "in one but not the other" — and note that it is directional: this-quarter-minus-last-quarter gives your new customers, while the reverse gives the customers you lost. Symmetric difference is "in one side only," which surfaces everything not shared.

The chapter's customer-retention example is the template: three set operations turn two quarterly customer lists into repeat, new, and lost customers — churn analysis in three lines. Any paired-group comparison in your own work (this month vs. last month, plan A vs. plan B) fits the same mold.

---

### Q: How do I read nested dictionaries without crashing on missing keys?

Chain `.get()` calls, one per level, and give the intermediate levels an empty dictionary as their default. In `d.get("employee", {}).get("skills", "Unknown")`, the `{}` is the trick: if the outer key is missing, the first `.get()` returns an empty dictionary instead of `None`, so the second `.get()` still has something to call itself on and returns your final default instead of raising an error.

This chained pattern becomes second nature once you work with JSON in Module 8, because real-world JSON is nested dictionaries and lists all the way down, and fields you expected are routinely absent.

---

## Module 8: File I/O & Working with JSON

### Q: Why does everyone insist on `with open(...)` instead of just calling `close()` myself?

Because the `with` statement guarantees the file is closed no matter how the block ends — including when an error occurs partway through. A manual `close()` call is exactly the line a crash skips: the exception jumps out of your code before reaching it, potentially leaving the file locked or leaving written data stuck in a buffer that never reaches the disk.

The intuition to keep is that `with` matters *most* when something goes wrong, which is precisely when you cannot rely on your own cleanup code running. Every example in the module and every task in the assignment uses the context-manager pattern, and it is worth making a permanent habit.

---

### Q: I opened a file with mode `"w"` and my existing data vanished. What happened?

Mode `"w"` means write-and-overwrite: it erases the file's contents the instant the file is opened, before you have written anything. That is the intended behavior for producing a fresh report, and a destructive surprise for anything you meant to keep.

If the goal is to add to an existing file — a daily log, an append-only record — the mode you want is `"a"`, which starts writing at the end and preserves what is there. The three modes form a simple contract: `"r"` reads (and errors if the file is missing), `"w"` creates or replaces, `"a"` creates or extends. Choosing between `"w"` and `"a"` deliberately, every time, is the habit that prevents the loss.

---

### Q: Why do numbers read from a file refuse to do math?

Because everything read from a text file is a string — including values that look exactly like numbers. A file does not store types; it stores characters, and Python hands them to you as text. Arithmetic on those strings either fails or misbehaves (the `+` operator concatenates).

The pattern from the chapter is read, strip, split, *convert*: after splitting a line into fields, apply `int()` or `float()` to each numeric field before storing it. Once converted, all the usual math and aggregation work. This is also a preview of one of Polars' conveniences in the next module — `pl.read_csv()` performs the type conversion for you.

---

### Q: Why does printing lines from a file produce a blank line after each one?

Every line you read keeps its trailing newline character — the invisible `"\n"` that ended the line in the file. When you then `print()` the line, print adds its own newline on top, producing the double spacing.

The standard fix is `.strip()` on each line as you read it, which removes leading and trailing whitespace including that newline. Stripping before comparing, splitting, or printing is part of the routine line-processing pattern, and forgetting it also breaks equality checks — a line that looks like `"Widget A"` but still carries its newline will not equal the string `"Widget A"`.

---

### Q: When does it matter whether I read a file all at once or line by line?

For the small files in this course, it barely matters — `.read()` swallowing the whole file into one string is convenient and fine. The difference appears with large files: `.read()` must fit the entire file in memory at once, while iterating with `for line in f:` streams it, holding just one line at a time. For a server log measured in gigabytes, streaming is the difference between a working script and an out-of-memory failure.

One trap worth flagging: `.readlines()` *looks* like the streaming option but is not — it loads every line into a list at once, the same memory cost as `.read()`. The genuinely memory-safe approach is direct iteration over the file object.

---

### Q: What's the difference between `json.load()` and `json.loads()`?

The trailing `s` means *string*. `json.load()` reads from an open file; `json.loads()` parses a JSON string you already have in memory — most commonly the body of a web API response. The same naming pattern covers the writing direction: `json.dump()` writes to a file, `json.dumps()` produces a JSON string.

Whichever entry point you use, the result is the same: plain Python dictionaries, lists, strings, and numbers. There is no special "JSON object" needing special methods — every dictionary and list skill from Modules 6 and 7 applies unchanged the moment the data is loaded.

---

### Q: Do I write `true`, `false`, and `null` in my Python code when working with JSON?

No — those are JSON's spellings, and they exist only inside JSON text. In Python they are `True`, `False`, and `None`, and the `json` module translates automatically in both directions at the boundary: your `False` becomes `false` in the file, and a `null` in the file becomes `None` in your program.

The practical consequence: test parsed values the Python way (`is None`, `if flag:`), never by comparing against the strings `"null"` or `"true"`. If you find yourself typing a lowercase `true` in Python code, something has gone sideways.

---

### Q: Why use `pathlib` instead of building file paths by joining strings?

Because string-glued paths hard-code one operating system's separator, and they break the moment the code runs somewhere else — Windows and Mac/Linux disagree about slashes. The `/` operator on `Path` objects inserts the correct separator for whatever system the code is running on, so the same script works everywhere.

`Path` objects also know how to take themselves apart (`.name`, `.stem`, `.suffix`, `.parent`), can check the disk before you commit (`.exists()`), and offer one-call shortcuts for small whole-file reads and writes (`.read_text()`, `.write_text()`). One related portability tip from the chapter: for a temporary folder that exists on every operating system, ask `tempfile.gettempdir()` rather than hard-coding a location.

---

## Module 9: Introduction to Polars

### Q: We just learned to parse CSV files by hand in Module 8 — why did we bother if `pl.read_csv()` does it in one line?

Because now you know what that one line is doing for you — opening the file, splitting the lines, converting every field's type — and you can debug it when something looks wrong. The hand-rolled version was the lesson; the library call is the practice.

The broader trade the course makes at this point: hand the mechanical work to the library and spend your attention on the analysis. Manual loops over rows are slow to run and slower to write once datasets reach thousands of rows; Polars does the same work on whole columns at once. What does not change is your responsibility to verify the import — check the shape, the column names, and the inferred types before trusting any of it.

---

### Q: Why does this course use Polars instead of pandas?

Polars is the newer of the two libraries and was chosen for speed and clarity. Its engine is written in Rust, it uses memory efficiently, and — most relevant for learners — its API is built around one consistent idea: expressions that describe what to do with whole columns. Pandas, the older and widely used alternative, offers many ways to do the same thing, which is flexible for experts and confusing for beginners, and its missing-value handling is messier.

Knowing one makes the other learnable. The concepts you practice here — DataFrames, selecting, filtering, grouping, joining — exist in pandas too, so the skills transfer if a future employer's codebase uses it.

---

### Q: Does `shape: (5, 4)` mean five columns and four rows?

The other way around: shape always reads **(rows, columns)**, rows first. A shape of `(5, 4)` is five rows and four columns.

It is a small convention with outsized consequences, because misreading it inverts your understanding of the data's size. Checking `.shape` right after loading — and reading it rows-first — is part of the inspection habit the module builds, alongside `.columns`, `.schema`, `head()`, and `describe()`.

---

### Q: What are the `str`, `f64`, and `i64` labels printed under the column names?

Type codes — one per column, showing what Polars inferred when it read the data. `str` is text, `i64` is a 64-bit integer (whole numbers), and `f64` is a 64-bit float (decimals). They are not variable names or data; they are metadata about each column.

Reading that dtype row is a habit that catches import problems early. A salary column that came in as `str` means something in the file prevented numeric inference; a date column showing `str` means date arithmetic will not work until you cast it (a Module 10 topic). The printout tells you all of this before you run a single calculation.

---

### Q: What does `pl.col()` do that a plain column-name string can't?

A plain string can only *keep* a column. Wrapping the name in `pl.col()` creates an expression — a recipe describing the column and, optionally, what to do with it — which you can then compute with: multiply it, divide it by another column, round it, and name the result with `.alias()`. That is how one `select()` or `with_columns()` call turns an annual salary into monthly and weekly breakdowns without writing a loop.

Two things to know about expressions: they do not fetch data when you write them (the recipe runs when handed to `select()` or `filter()`), and a computed column keeps the source column's name unless you `.alias()` it — so alias anything you compute, both for clarity and to avoid accidental collisions.

---

### Q: Why can't I write `and`/`or` between my filter conditions, and why does every condition need parentheses?

Python's `and`/`or` keywords do not work on column expressions — Polars needs the symbols `&` (and), `|` (or), and `~` (not) to combine conditions across whole columns. Writing the keywords produces an error rather than a wrong answer, so at least the failure is loud.

The parentheses are not optional style: without them, Python's operator precedence groups the expression incorrectly, and you get an error or, worse, a filter that tests something different from what you meant. The safe pattern is mechanical — wrap every individual condition in its own parentheses before joining them with `&` or `|`. And when the condition is "this column matches any value in a list," skip the chained `|` entirely and use `is_in()`.

---

### Q: Did `filter()` delete rows from my DataFrame?

No — and neither does `select()`, `sort()`, or any other Polars method. Each one returns a *new* DataFrame and leaves the original untouched. Your source data is still intact under its original variable name; the filtered result exists only in the value the method returned.

This immutability is why you must assign results to keep them: `high_earners = employees.filter(...)`. It is also what makes chaining possible — each step feeds a fresh DataFrame to the next — and it prevents a whole category of bugs where an exploratory filter quietly corrupts the dataset every later cell depends on.

---

### Q: I sorted and took the first five rows for a "top five" list, but got the smallest values. What did I miss?

`sort()` is ascending by default — smallest first — so `head()` after a bare sort trims the *bottom* of the ranking. For a biggest-first list, pass `descending=True` to the sort, then take `head()`.

The sort-then-head recipe is the standard answer to every "top N" business question — top customers by revenue, top products by margin — but it only works if the sort direction matches the question. It is also worth remembering that `head()` returns the first rows *in the current order*, not a representative sample; without a deliberate sort in front of it, it just shows whatever happens to be first.

---

## Module 10: Polars: Transformations & Aggregations

### Q: I called `with_columns()` to add a column, but my DataFrame doesn't have it. Why?

Because Polars DataFrames are immutable: `with_columns()` computed your new column and returned a *new* DataFrame containing it — and if you did not assign that result to a variable, it was discarded. The original DataFrame was never going to change.

The fix is the assignment: `df = df.with_columns(...)` (or a new name, if you want to keep the raw version around — often a good idea). This same rule explains most "my change disappeared" moments in Polars: every method returns a new frame, and only what you assign survives.

---

### Q: My date column sorts in a strange order and date arithmetic doesn't work. Why does Polars treat my dates as text?

Because a date in a CSV file is just characters, and unless told otherwise Polars loads it as a `String`. A string column full of date-shaped text *looks* right in the printout, but it sorts alphabetically and supports no date math. Appearances are not evidence — check `.schema` to see what the column actually is.

The repair is a cast: `pl.col("order_date").str.to_date("%Y-%m-%d")`, where the format string describes how the text is laid out. Reusing the same column name in `.alias()` replaces the string column with the typed one — a deliberate use of the rule that aliasing onto an existing name overwrites that column rather than erroring. After the cast, the printed values look identical; the difference is the dtype, and everything date-related starts working.

---

### Q: What's the difference between `pl.len()` and `.count()` in an aggregation?

`pl.len()` counts the rows in each group, blanks included. `.count()` looks at one specific column and counts only the cells that actually hold a value, skipping nulls. On a clean table they agree exactly, which is why the distinction is easy to miss — the difference appears precisely when your data has gaps.

The chapter's guidance: when the business question is "how many orders came from this region?", you want a row count, so reach for `pl.len()`. The `.count()` variant earns its place after left joins, where unmatched rows are padded with nulls and counting the join key is how a customer with no orders correctly reports zero instead of one.

---

### Q: Why does my grouped report come back in a different order each time I run it?

Because Polars makes no guarantee about the order of groups in a `group_by` result — the rows come back in whatever order the engine produced them, which can vary run to run. Nothing is wrong with the numbers; only the arrangement is unstable.

The habit that fixes it: end every report with an explicit `.sort()` on the column that should govern the display — revenue descending for a ranking, the category name ascending for a reference table. This makes the report readable, and it makes reruns reproducible line for line, which matters as soon as anyone compares two versions of your output.

---

### Q: After joining a lookup table, my row count dropped. What's the difference between a left join and an inner join?

An inner join keeps only the rows that match in *both* tables — any row in your main table whose key has no partner in the lookup table is silently dropped. A left join keeps *every* row from the left table and fills the columns from the right table with `null` where no match exists.

The choice is a business decision as much as a technical one. A revenue dashboard built with an inner join quietly erases the customers who placed no orders — often exactly the dormant customers management most needs to see. The workhorse in business reporting is the left join: keep every transaction or every customer, and attach context where it exists. When the two joins give the same result, it just means every key happened to match; when the counts differ, the missing rows are the story.

---

### Q: Is `null` the same as zero, and what should I fill missing values with?

No — `null` means *absent*, not zero, and treating the two as interchangeable corrupts your statistics. Filling a missing price with zero tells every later calculation the item is free, which drags down averages and totals in ways nobody will flag as an error. Meanwhile, aggregations like `.mean()` silently *skip* nulls rather than failing, so the code runs and the answer describes fewer rows than you think — which is why diagnosis with `null_count()` comes before any aggregation.

The right fill is a business judgment about what the gap means. Sometimes zero genuinely is correct; sometimes a computed value like the column's mean is a reasonable default; sometimes the honest move is removing the incomplete rows or leaving the nulls and saying so. The tools — `fill_null()`, `is_not_null()`, `drop_nulls()` — are simple; choosing among them is the analytical work.

---

### Q: `drop_nulls()` deleted most of my table. Why?

Because by default it removes any row containing a null in *any* column — one blank cell anywhere disqualifies the whole row. On a wide table where different columns have scattered gaps, that compounds quickly and can quietly discard the bulk of your data.

Two safer alternatives: filter on the specific column that matters (`filter(pl.col("price").is_not_null())`) keeps rows complete in that column while tolerating gaps elsewhere, and counting rows before and after any removal — as the chapter's example does — makes the cost of the operation visible instead of silent.

---

### Q: Should I chain everything into one long pipeline, or use intermediate variables?

The results are identical either way, so this is about readability and debugging, not correctness. A chain — each method on its own line inside parentheses — reads top-to-bottom like a recipe and avoids the clutter of stale intermediate variables that invite mistakes. Intermediate variables make each step's output inspectable, which is exactly what you want while debugging a pipeline that produces a wrong number somewhere in the middle.

Many analysts do both in sequence: build and debug with intermediate variables, then consolidate into a chain once each step is verified. One clarification about the syntax — the surrounding parentheses are ordinary Python line-continuation, not special Polars machinery. They exist only so each `.method()` can sit on its own line.

---

## Module 11: Visualization: Matplotlib & Plotly Express

### Q: Do I need `plt.show()` to see my chart in marimo?

No. Marimo displays a figure automatically when it is the last expression in a cell — so you end the cell with the figure object and it renders. `plt.show()` belongs to plain Python scripts run from a terminal, and the course's examples never use it.

This is the same last-expression display rule you have relied on since Module 1; figures are just one more kind of value marimo knows how to render.

---

### Q: What's the difference between the figure and the axes in matplotlib?

The figure is the overall canvas — the blank page — and the axes is one plot area drawn on it where data actually appears. You add data and labels through the axes (`ax.bar()`, `ax.set_title()`, `ax.set_xlabel()`), while canvas-level jobs like saving to a file or titling a multi-panel exhibit belong to the figure (`fig.savefig()`, `fig.suptitle()`).

The standard starting point for every chart is `fig, ax = plt.subplots()` — despite the plural name, called with no arguments it creates one figure containing one axes, and it is the recommended opening line for single-panel charts too. With a grid layout it instead returns an array of axes, one per panel.

---

### Q: My months plot in the order Apr, Feb, Jan... How do I get calendar order?

Month names are strings, and strings sort alphabetically — which scrambles any time axis built from them. The fix is to tell Polars the order you mean: cast the column to `pl.Enum` with an explicit list of the months in calendar order, and from then on `.sort()` follows the calendar instead of the alphabet.

The same trick applies to any column with a meaningful non-alphabetical order: weekday names, size labels like S/M/L, quarter labels. Whenever a chart's x-axis looks shuffled, an alphabetical sort of category names is the first suspect.

---

### Q: Aren't histograms just bar charts?

They look similar but answer different questions. A bar chart compares *categories you chose* — revenue by product, visitors by park — with one bar per category. A histogram takes a single numeric column and shows its *distribution*: matplotlib divides the value range into equal-width bins and draws one bar per bin showing how many values fall inside.

Two consequences follow. First, you do not pick a histogram's categories — the bins are computed from the data, and changing the bin count reshapes the chart. Second, overlaying two histograms for comparison requires one *shared* set of bin edges passed to both; letting each compute its own edges from its own range produces two misaligned grids whose bars cannot be compared.

---

### Q: When should I use matplotlib and when Plotly Express?

Matplotlib produces static, publication-quality images — the right choice for printed reports, PDFs, and slide decks, where interactivity would die anyway and fine-grained control over every element pays off. Plotly Express produces interactive charts you can hover, zoom, and pan — the right choice for exploring data yourself and for dashboards others will click around in, and its one-function-call API is quicker to write.

The chapter's rule of thumb: polished static figure for a deliverable, Plotly for exploration and interaction. Exporting follows the same split — `savefig()` for images, `write_html()` to keep a Plotly chart interactive in a browser (a static image export freezes it).

---

### Q: Why does matplotlib want `.to_list()` while Plotly Express wants `.to_pandas()`?

The two libraries operate at different levels. Matplotlib works with plain sequences — you extract each column you need as a Python list and pass the lists to `ax.bar()` or `ax.plot()`. Plotly Express works with a whole DataFrame at once — you convert with `.to_pandas()` and then *name* the columns you want on each axis, and arguments like `color=` do the grouping, coloring, and legend-building that matplotlib would require a loop for.

Mixing the two conventions up is the most common error in this module, so it is worth committing to memory: matplotlib gets lists, Plotly Express gets a pandas DataFrame.

---

### Q: Why shouldn't I just plot all my raw rows?

Because a plotting library given a million raw transaction rows produces an unreadable smear and a slow notebook — and even the module's modest dataset would clutter a chart if plotted row by row. The workflow the course teaches is aggregate first, then visualize: use Polars `group_by().agg()` to reduce the data to the small summary table a chart actually wants — one row per bar, one point per period — and hand that to the plotting library.

This also keeps the analysis honest: the summary table *is* the chart's data, so you can read the exact numbers behind every visual element, and the chart becomes the final step of the same pipeline rather than a separate computation that might disagree with it.

---

### Q: How do I decide which chart type to use?

Start from the question, not the chart menu. The four core types each answer one kind of question: how do categories compare — bar chart; how does a value change over time — line chart; is there a relationship between two variables — scatter plot; how is a single variable distributed — histogram. The chapter's selection table adds composition (pie or stacked bar) and comparing two distributions (overlaid histograms or box plot).

When in doubt, a bar chart for categories or a line chart for time series covers most business reporting. And whatever you choose, the chart is not finished until it carries a title, labeled axes, and — in a report — a sentence saying what the reader should take from it.

---

## Module 12: Marimo Interactive Features

### Q: Why do I have to create a widget in one cell and read its `.value` in a different cell?

Because marimo's reactivity works through the dependency graph between cells. When Cell B reads `dropdown.value`, marimo records that B depends on the dropdown — so every time the user changes the selection, B reruns automatically with the new value. If you create the widget and read its value in the same cell, there is no cross-cell dependency to trigger: you get the value as of creation time, and nothing reacts when the user interacts.

The two-cell pattern is therefore the entire mechanism: create and display the widget in one cell, read `.value` in another. Any cell that references the widget becomes, in effect, its handler.

---

### Q: I assigned my dropdown to a variable, but it never appeared on screen. Why?

Marimo renders a cell's *last expression* — and an assignment displays nothing. Creating the widget stores it in a variable, but to show it you must also put the widget's name on its own line at the end of the cell (or include it in a layout call like `mo.hstack()`).

This is the same display rule you have used all course for DataFrames and figures, applied to widgets. If a control is mysteriously invisible, check whether the cell ends with the widget or with an assignment.

---

### Q: Where do I register the callback or event handler for my slider?

Nowhere — marimo has no callback wiring. In frameworks you may have seen elsewhere, you attach a handler function to each control; in marimo, the dependency graph plays that role. Any cell that reads the slider's `.value` reruns automatically whenever the slider moves. There is no refresh button, no event registration, and no "on change" function to write.

This is why the module's design patterns focus on structure instead: data flows one direction — widgets, then filters, then aggregation, then visualization — and marimo refuses to run circular dependencies outright.

---

### Q: How do I give my dropdown an "All" option?

You add it yourself — dropdowns have no built-in "everything" choice. The pattern from the chapter builds the options list as `["All"]` plus the sorted unique values from the data, and then the *filter code* must cooperate: when the selection equals `"All"`, skip filtering on that dimension entirely rather than looking for a literal category named All.

Deriving the real options from the data itself (rather than typing them) is worth copying too — the widget can never drift out of sync with the DataFrame when a new category appears.

---

### Q: My search box filters out everything before the user even types. Why?

Because a text widget's value starts as the empty string, and a containment filter against `""` — or worse, logic that treats empty as a search term — can match nothing. Your filter cell has to decide explicitly what an empty box means, and the sensible convention is "no filter": if the query is non-empty, apply the containment test; otherwise show all rows.

Two refinements from the chapter's example: strip and lowercase the query, and lowercase the column being searched, so users can type in whatever case they think in. Sensible behavior at the empty state is part of the broader design rule that every widget should carry a reasonable default, so the notebook shows meaningful content the moment it opens.

---

### Q: What does `mo.ui.table()` add over just ending the cell with the DataFrame?

Both display a table, but the widget version is also an *input*. `mo.ui.table()` renders the DataFrame with sorting and pagination, and — with selection enabled — lets the user click rows; those selected rows come back as `table.value`, a DataFrame containing only what was clicked, which downstream cells can chart or summarize. The user hand-picks items for comparison and the chart follows.

One thing to plan for: `table.value` can hold zero rows, because nothing is selected until the user clicks. Handle the empty case with a friendly message rather than letting a chart cell fail on an empty selection.

---

### Q: Why should all my filters live in one cell?

Because duplicated filter logic drifts. If each chart cell re-applies its own copy of the region and threshold filters, then one day one chart gets updated and another does not — and the dashboard quietly contradicts itself, with two panels disagreeing about what "the filtered data" means.

The pattern the module teaches: one cell reads every filtering widget's `.value`, applies all the conditions in sequence, and exports a single filtered DataFrame. Every downstream chart, table, and summary consumes that one DataFrame, so all of them always agree — and when the filter logic needs to change, there is exactly one place to change it.

---

### Q: What kind of value does each widget actually give me back?

The natural Python value for what the control represents, ready to use without conversion. A dropdown's `.value` is the selected option itself — the string you would filter on — not the option's position. A slider's value is numeric, in the units set by its start, stop, and step, so it compares directly against a column. A checkbox returns a plain boolean, which drops straight into an `if` statement. A text box returns a string, which starts out empty.

Knowing this saves you from defensive conversions and from bugs like testing a checkbox against the string "checked" — the widget already speaks your program's language.

---

## Module 13: DuckDB: SQL-Based Data Analysis

### Q: Why learn SQL when Polars already does all of this?

Because SQL is the shared language of corporate data — order databases, cloud warehouses, BI tools, and Excel's Power Query all speak it — and analysts who read and write it can pull answers from nearly any system they encounter. Your colleagues on data teams likely think in SQL, which makes a query the easiest artifact to share. And some questions, particularly multi-table joins and ad-hoc exploration, are simply more natural to express as a query than as a method chain.

The goal is not to replace Polars but to carry both. The module's integration section makes the pairing concrete: DuckDB can query a Polars DataFrame by name, and any result converts back to Polars with `.pl()` — so you use SQL where SQL reads best and Polars where it does, often in the same analysis.

---

### Q: Don't databases need a server? What makes DuckDB different?

DuckDB is an *embedded* database: it runs entirely inside your Python process. There is no server to install, start, or connect to, no administrator to call — `import duckdb` is the whole installation-and-connection story. It is also *analytical*, meaning it is optimized for the filtering, grouping, joining, and aggregating that analysts do all day, rather than for the record-at-a-time updates of a transactional system.

The chapter's shorthand: think of it as SQLite's data-analysis cousin — the database that lives where your code lives.

---

### Q: Can I really query a CSV file without loading it first?

Yes — put the file's path where a table name would go, as in `SELECT * FROM 'orders.csv'`, and DuckDB reads the file, infers each column's type (dates become real dates, numbers become numbers), and runs the query in one step. For one-off questions this is the simplest possible workflow.

Creating tables first (`CREATE TABLE ... AS SELECT`) is an optimization, not a requirement: it copies the data into the database once so repeated queries stop paying the file-parsing cost. In-memory tables vanish when your Python session ends, so use them for working sessions, and remember that querying the file directly is just as correct for a single question.

---

### Q: My condition `status == "Completed"` failed in SQL. What are the syntax differences that trip up Python programmers?

SQL comparison uses a single `=`, not `==` — the double-equals is a Python habit SQL rejects. String literals take single quotes (`'Completed'`), not double. And naming a computed column uses `AS`, which — like everything in a query — affects only the result, never the source file.

One more type-related trap from the chapter: `LIKE` pattern-matching works on *text*, and DuckDB's type inference may have made your date column a real `DATE`. Pattern-matching a date requires converting it first with `CAST(order_date AS VARCHAR)`; without the cast, DuckDB reports that no matching function exists.

---

### Q: What's the difference between WHERE and HAVING?

WHERE filters *rows* before any grouping happens; HAVING filters *groups* after the aggregation has run. The chapter's image: WHERE is the bouncer at the door, HAVING is the bouncer at the VIP section. A condition on an aggregate — "customers whose total spending exceeds a threshold" — can only live in HAVING, because when WHERE runs, no totals exist yet to test.

Many queries use both, filtering at two stages: WHERE keeps only completed orders, the GROUP BY totals them per customer, and HAVING keeps only the customers whose totals qualify. One portability note: referring to a SELECT alias inside HAVING is a DuckDB convenience; the form that works in every database repeats the aggregate expression itself.

---

### Q: When do `COUNT(*)` and `COUNT(column)` give different answers?

Whenever the counted column contains NULLs. `COUNT(*)` counts rows; `COUNT(column)` counts only the rows where that column holds a value. On a clean table they agree, which hides the distinction until the exact moment it matters: after a LEFT JOIN, where unmatched rows are padded with NULLs.

The chapter's example is the one to remember. A customer with no orders survives a LEFT JOIN as one NULL-padded row — `COUNT(*)` counts that row and wrongly reports one order, while counting the join key (`COUNT(o.order_id)`) skips the NULL and correctly reports zero. When counting per group after a left join, count the key.

---

### Q: My LEFT JOIN started acting like an INNER JOIN — customers with no orders disappeared. What happened?

Almost certainly a right-table condition placed in the WHERE clause. A LEFT JOIN pads unmatched left-table rows with NULLs in the right table's columns — and a WHERE condition on one of those columns (say, filtering on order status) evaluates against NULL, fails, and discards exactly the padded rows the LEFT JOIN existed to keep. The query silently degrades to an inner join.

The fix is to move right-table conditions into the join's `ON` clause, where they restrict *which rows can match* without discarding left-table rows that match nothing. Conditions on the left table are fine in WHERE. This is one of SQL's subtler traps, and it is why the chapter's every-customer report filters status inside the `ON`.

---

### Q: How do DuckDB and Polars actually work together in one notebook?

In both directions, with almost no ceremony. Going in, DuckDB can query a Polars DataFrame by its Python variable name — write `FROM orders` in the SQL and DuckDB finds the DataFrame, reading its memory directly without copying (both tools build on the same Arrow format). Coming out, every DuckDB result converts to a Polars DataFrame with a single `.pl()` call, ready for further transformation or a Plotly chart.

That round trip is the modern-analyst pipeline in miniature: SQL for the relational heavy lifting, Polars for data work, Plotly for charts. One marimo-specific caution: a DataFrame name inside a SQL *string* is invisible to marimo's dependency graph, so those cells do not rerun automatically when the data changes — rerun them yourself.

---

## Module 14: Web Scraping

### Q: If data is publicly visible on a website, am I allowed to scrape it?

Visibility is not permission. Before scraping any real site, the chapter's ground rules apply: check the site's `robots.txt` file, which states what automated tools may access; read the Terms of Service, since some sites prohibit scraping outright; respect rate limits by pausing between requests; never scrape personal data without a lawful basis; and prefer an API whenever one exists, because it is faster, more reliable, and explicitly permitted.

This module practices on HTML strings created in Python precisely so you can learn the techniques with no ethical exposure. When you take the skills to real sites — including for your capstone — the checklist above is part of doing the job correctly, not an optional courtesy.

---

### Q: I can see the data in my browser, but my scrape comes back empty. Why?

This is the number-one reason a beginner's first real scrape fails: the site builds its content with JavaScript *after* the page loads. `requests.get()` receives only the initial HTML the server sends — it does not run JavaScript — so anything the page assembles afterward simply is not in `response.text`, no matter how plainly you can see it in the browser.

You can confirm the diagnosis by viewing the page's raw source (not the browser's inspector, which shows the post-JavaScript result) and searching for the data you expected. If it is absent, tools that render pages (Selenium, Playwright) exist but are beyond this module — and it is also a good moment to check whether the site offers an API instead.

---

### Q: Why does BeautifulSoup use `class_` with a trailing underscore?

Because `class` is a reserved word in Python — it introduces class definitions — so it cannot be used as a keyword argument. BeautifulSoup's workaround is `class_`: writing `soup.find("div", class_="dept-card")` searches by CSS class, and the underscore is just the price of coexisting with Python's grammar.

Forgetting the underscore produces a syntax error rather than a silent bug, so at least the mistake announces itself. The alternative spelling `attrs={"class": "dept-card"}` avoids the issue entirely, as do CSS selectors (`select("div.dept-card")`), where the class is part of the selector string.

---

### Q: What's the difference between `find()`/`find_all()` and `select()`/`select_one()`?

They locate the same elements by different syntax. `find()` and `find_all()` take a tag name plus keyword filters and return the first match or all matches, respectively. `select_one()` and `select()` do the same jobs using CSS selector strings — the compact notation web developers use — where `.class`, `#id`, and combinations like `"div.dept-card a"` (links anywhere inside dept-cards) replace nested searching with one expression.

Choose whichever reads more clearly for the page at hand: deeply scoped extractions are often one tidy selector, while simple tag-plus-class lookups are perfectly clear as `find_all()`. Just keep the return shapes straight — `select_one()` mirrors `find()` (one tag or `None`), `select()` mirrors `find_all()` (a list).

---

### Q: Why did `.string` return `None` on a tag I can see has text, and why did `get_text(strip=True)` glue two words together?

Both are text-extraction traps the chapter demonstrates. `.string` returns the text only when a tag has exactly one child; the moment a tag contains nested markup — a `<strong>` inside a `<span>` — it has multiple children and `.string` returns `None`. Use `.get_text()` when nesting is possible, which on real pages is always.

The gluing comes from how `strip=True` works: it strips each text node separately and joins the pieces with *nothing*, so text split across nested tags loses the space between words. The fix is to supply a separator: `.get_text(" ", strip=True)` joins the pieces with a space, preserving word boundaries. That form is the chapter's recommended default.

---

### Q: Why are my scraped salaries and quantities useless for math?

Because everything extracted from HTML arrives as a string — a salary comes out as text complete with its dollar sign and commas, and a count comes out as digits-in-a-string. The DataFrame builds fine, but every column is text, and no arithmetic works until you clean it.

The two-step habit from the chapter is scrape, then clean: use a regex replacement (`str.replace_all`) to strip the currency formatting, then `.cast()` the column to an integer or float type. Checking the dtype row of the DataFrame after a scrape tells you instantly which columns still need the treatment.

---

### Q: My browser's inspector shows a `<tbody>` in the table, but my `tbody`-based selector finds nothing. What gives?

Browsers insert a `<tbody>` into every table automatically when they render the page — so the inspector *always* shows one — but the tag is optional in the actual HTML source, and Python's parser does not add it for you. A selector that requires `tbody` silently returns nothing on any table whose source omits it, and you get an empty result instead of an error.

The defensive pattern from the chapter's reusable table scraper: loop over all `<tr>` elements instead of selecting through `tbody`, and skip the header row by checking that a row actually produced data cells. More broadly, remember that the inspector shows the browser's *repaired* version of the page; your scraper sees the raw source.

---

### Q: Why should my scraper wait between requests and identify itself?

The delay is rate limiting — a `time.sleep()` between requests keeps you from overwhelming someone else's server. It is not optional politeness: hammering a site gets you rate-limited or blocked outright, and can degrade the site for everyone else. The chapter's robust fetch function puts the delay in a `finally` block so it happens after every request, success or failure.

Identification is the User-Agent header. Many sites block anonymous clients, and a descriptive user-agent with contact information is both more effective and more honest than pretending to be a browser. Together with checking status codes before parsing and returning `None` on failure instead of crashing, these habits are what separate a responsible scraper from a nuisance.

---

## Module 15: REST APIs & Data Acquisition

### Q: When should I use an API instead of scraping the website?

Whenever an API exists — the chapter's rule of thumb is that scraping is the last resort. An API returns structured JSON instead of raw HTML, so the entire BeautifulSoup parsing step collapses into one `.json()` call; its endpoints are stable and versioned instead of breaking when the site redesigns; the responses carry only data rather than full pages, so they are faster; and programmatic access is explicitly permitted rather than a Terms-of-Service gray area.

The trade-offs on the API side are authentication (most production APIs require a key) and rate limits — both manageable with the practices this module teaches. Reach for scraping only when the data you need is public and no API offers it.

---

### Q: What does it mean that REST is "stateless," and why do I care?

Stateless means the server remembers nothing between requests — each request is a complete, independent transaction. The practical consequence for your code: every request must carry everything the server needs, every time — the query parameters, the authentication headers, all of it. There is no "I logged in earlier" or "continue where we left off"; if page three of a paginated dataset needs your key and your filters, they go on that request too.

The design pays off in reliability and scale — any server can answer any request because no conversation history matters — but the mental model for you is simple: build each request as if it were the first.

---

### Q: Why didn't my `try`/`except` catch the 404?

Because a 404 is not an exception — it is a *completed* request whose answer happens to be "not found." The server responded; the conversation succeeded; the status code carries the bad news. `requests` raises exceptions only for network-level failures (timeouts, unreachable hosts), so error handling has two separate layers: `try`/`except` for network problems, and a status-code check for HTTP errors.

The bridge between the layers is `response.raise_for_status()`, which converts a 4xx or 5xx status into an exception so one `try`/`except` block can handle both kinds of failure. The chapter's `fetch_json()` pattern — raise for status, catch each exception type, return `None` with a readable message — is the shape that keeps a nightly pipeline logging problems instead of crashing on them.

---

### Q: Should I build the query string myself by concatenating text onto the URL?

No — pass a dictionary to the `params=` argument and let `requests` build the URL. Manual concatenation breaks on spaces and special characters, which must be URL-encoded; the library encodes them correctly, keeps the call readable, and you can confirm the final URL it constructed by printing `response.url`.

Query parameters are also worth using aggressively for their own sake: they filter, sort, and limit *on the server*, so you download only the records you need instead of the whole dataset. On production APIs that charge per record or per megabyte, server-side filtering saves both time and money.

---

### Q: I got a 429 status code — have I been banned?

No — 429 means "too many requests": you exceeded the provider's request budget for the current time window, and the condition is temporary. The correct response is to wait and retry, ideally with exponential backoff — doubling the wait after each rate-limited attempt so a congested server gets progressively more breathing room. What actually gets API keys banned is ignoring 429s and hammering the server with instant retries.

Prevention is cheaper than retrying: a polite `time.sleep()` between requests keeps you under most limits, and many APIs report your remaining budget in rate-limit response headers you can check as you go.

---

### Q: The API gave me only the first batch of records, but there should be thousands. Where's the rest?

Behind pagination. Many APIs cap each response at a page of records, and collecting the full dataset means requesting page after page — via page-number parameters, offsets, or a server-provided cursor, depending on the API. A script without a pagination loop silently analyzes page one and nothing else, with no error to warn you.

The loop pattern from the chapter: request a page, stop when an empty page (or the response's own page-count metadata) says you are done, add a polite delay between requests, and guard the whole thing with a maximum-pages safety limit so a misbehaving API cannot keep your script looping — and billing — forever. Wrapped in a reusable function, any paginated endpoint becomes one call.

---

### Q: My request hung forever. Why didn't it just time out on its own?

Because `requests` has no default timeout — left unspecified, a hung server can hang your program indefinitely. The fix is to pass `timeout=` on every request, no exceptions; every example in this module does, and a timeout expiring raises an exception your error handling can catch and report.

Timeouts are one piece of the broader robustness kit for acquisition code that must run unattended: layered error handling, backoff on rate limits, pagination safety limits — and caching, where each successful response is saved to a local file so a later network failure degrades to using yesterday's data with a warning instead of crashing the whole pipeline.

---

### Q: Why does `pl.DataFrame()` produce weird columns (or errors) from my API data?

Because real API responses are nested — a user record with an address dictionary inside it, and a geo dictionary inside that — while `pl.DataFrame()` expects a list of *flat* dictionaries: one level, plain values. Fed nested structures, it produces awkward struct columns or fails outright.

The missing step is flattening: loop over the records and build a simple dictionary per record, pulling nested values up to top-level keys of your choosing (city from inside the address, company name from inside the company). It is also the natural moment for light cleaning — converting numeric strings to numbers, for instance. Fetch, flatten, load, clean, analyze is the module's pipeline pattern, and flattening is the step that trips people up most.

---

## Module 16: Capstone: Proposal & Data Acquisition

### Q: How can I tell whether my research question is specific enough?

Two tests from the chapter. First, name the variables: a real research question identifies a dependent variable — the outcome being measured — and one or more independent variables — the factors thought to influence it. If you cannot say what the outcome column of your dataset would be, you do not yet have a question. Second, the chart test: can you picture a chart or table that *answers* the question? If you can imagine the axes, the question is probably sharp enough; if no chart could answer it, it is still a topic.

Passing both tests early is the highest-leverage work in the whole capstone, because the question determines the data you need, the analysis you run, and the charts you build.

---

### Q: Isn't a more ambitious project a better project?

No — appropriate scope is one of the five criteria of a good capstone, and it works in reverse of ambition. The project must be completable in roughly two weeks with the tools you know, and a focused answer to a modest question beats an unfinished attempt at a grand one. "Can we predict the stock market?" fails where "how do weather and time of day affect ridership?" succeeds.

The framing the chapter offers: the capstone is a proof-of-concept analysis, not a dissertation. What it demonstrates — framing a question, acquiring data, exploring it, presenting findings — is the core workflow of applied analytics, and executing that workflow cleanly is what a grader, a portfolio reviewer, or a hiring manager is looking for.

---

### Q: I have a topic — say, "airline delays." Is that a research question?

Not yet, but it is a repairable start. A topic names an area; a question names an outcome and the factors that might drive it — "which routes and times of day have the worst average delays?" turns the topic into something a dataset can answer. The chapter's weak-question gallery ("analyze sales data," "what is business?") all fail the same way, and the fix is almost always the same: narrow it by asking *what about* the topic you want to know.

So keep your topic — genuine interest matters, since a joyless project shows — and sharpen it until it names measurable variables and passes the chart test.

---

### Q: Should I get my capstone data from a file, an API, or by scraping?

For most projects, a downloadable CSV is the pragmatic choice: sources like Kaggle and data.gov are well documented, and `pl.read_csv()` has you analyzing within minutes. Reach for an API when the question demands fresh or specialized data that only lives behind one, and for scraping only when the data exists nowhere else — and budget extra time for either route, because the error handling, pagination, and politeness practices from Modules 14 and 15 become part of your acquisition code.

The decision framework in the chapter weighs each route's trade-offs: files are easy but may be stale, APIs are fresh but rate-limited and often authenticated, scraping gets exactly what you need but is fragile and carries ethical obligations.

---

### Q: How do I vet a dataset before committing my project to it?

Run it through the six-point quality checklist: size (at least a hundred rows, more is better), completeness (how many missing values, and can you handle them?), relevance (does it contain the columns your question needs?), recency (is it current enough for the question?), accessibility (can you actually download or fetch it without barriers?), and license (are you allowed to use it for a class project?).

Relevance is the check beginners most often skip — a dataset can be large, fresh, and free and still lack the one column your dependent variable requires, so open the data or its documentation and confirm the columns exist before committing. The chapter's estimate is that thirty minutes of vetting up front saves hours of frustration later, and your assignment formalizes the habit by having you run two candidate sources through this exact checklist.

---

### Q: What if my research question changes once I start exploring the data?

That is normal analytics practice, not a failure of planning. The proposal is explicitly a starting point, not a contract — questions routinely evolve on contact with the data, and week-one exploration sometimes reveals that the data cannot answer the original question but can answer a neighboring one. Refining and proceeding is the professional move.

The proposal still earns its keep as a planning device: filling in the seven-section template forces vague intentions to become concrete commitments about data, methodology, and timeline. Just hold the plan loosely enough to follow what the data actually supports.

---

### Q: The walkthrough generates its own fake data — doesn't that defeat the purpose?

Only the acquisition step differs. Everything after it — inspecting shape and schema, checking nulls, running `describe()`, grouping by each independent variable, charting, and interpreting — is identical whether the data was downloaded, fetched from an API, scraped, or generated. The walkthrough uses synthetic data so the whole pipeline is reproducible for every student.

Synthetic data also has one teaching advantage real data cannot offer: the ground truth is known, because the generator deliberately built in the commute-hour, weather, and weekend effects. That lets you verify the analysis *recovers* what was planted. What it cannot teach is the messiness of real data — which is why the chapter warns that your own dataset will likely need the Module 10 cleaning steps this example got to skip.

---

### Q: Why do the exploration tables show the number of records next to each average?

Because an average without its sample size is a classic way to fool yourself. A group mean resting on three rows and one resting on thirty look identical in a summary table, but they deserve different levels of trust — a handful of extreme rows can drag a small group's average anywhere. Including a record count per group (and, where it helps, a second statistic like the median) lets the reader judge whether each figure is solid or a fluke.

The chapter's walkthrough models the habit in every grouped table, and it carries into Module 17's warning about group-by results generally: check the supporting evidence before treating a table as proof of an effect.

---

## Module 17: Capstone: Analysis & Presentation

### Q: Why does the chapter analyze a coffee-shop chain when my assignment is about a library system?

The separation is deliberate: the chapter teaches the *method* on one business so your assignment produces the *answers* on another. Every technique — cleaning and feature engineering, the five-way group-by analysis, the SQL cross-tabulation and window function, the chart set, the executive summary — is demonstrated end to end on the coffee data, and the library assignment asks you to transfer the workflow, not copy results.

That transfer is the point. The analytical workflow is the same regardless of subject matter, and being able to move it from one domain to another is precisely the skill a capstone certifies.

---

### Q: Why can't I just sum the customer-count column to get total store traffic?

Because of the data's grain. Each row in the coffee dataset is one *product* at one store on one day, but `customer_count` is *store-level* daily foot traffic — so the same number repeats on all five product rows of a store-day. Summing it across raw rows counts every visitor five times, silently inflating traffic by the number of product categories.

The correct moves are to aggregate to the right grain first (group to store-days and take `.first()` or `.mean()` of the repeated value) or to deduplicate before summing. The chapter flags this trap twice because your library assignment contains the same structure — branch-level checkout totals repeated across program rows — and the deduplication adjustment is graded.

---

### Q: The busiest store earned the least per visitor. Which number is the "right" one?

Neither, until you name the decision. "Best-performing store" is ambiguous — best *at what?* Total revenue ranks stores by volume; revenue per customer ranks them by efficiency, and in the chapter's data the two rankings run in nearly opposite directions. A high-traffic location can win on sheer footfall while extracting the least from each visitor, and a quiet location can be the most efficient in the chain.

The analytical lesson is to compute both and let the business question choose: a decision about where to invest capacity cares about volume, while a decision about pricing or store-format economics cares about efficiency. A recommendation built on only one of the two metrics can point in exactly the wrong direction — and the chapter's broader refrain is that traffic and revenue are separate levers that do not always move together.

---

### Q: What's a window function, and how is it different from GROUP BY?

`GROUP BY` collapses rows: many input rows become one output row per group, and the detail is gone. A window function computes across a "window" of related rows — the previous seven days, everything so far this year — while *keeping every row*, adding the computed value as a new column alongside the originals. If your result must show daily rows *and* a weekly average on each one, you need a window, because a group-by cannot keep both.

The chapter's example is the seven-day rolling average: a CTE first aggregates to one row per store per day, then `AVG(...) OVER (PARTITION BY store ORDER BY date ...)` smooths each day against the six before it, turning noisy daily revenue into a visible trend. Your assignment uses the same CTE-plus-window shape with a running total — a different frame, same pattern.

---

### Q: If I compute the same summary in Polars and in DuckDB, will the numbers match?

Yes — on the same data with the same logic, they agree to the cent, and the chapter proves it by computing the store summary both ways side by side. The engines do not "flavor" arithmetic; any differences you observe trace to differing logic (filters, null handling, rounding), never to the tool.

So the choice between them is style, not correctness: SQL tends to read best for cross-tabulations and window functions, Polars for chained transformations and conditional logic. One small caveat on the round trip — dtypes can shift cosmetically (DuckDB promotes integer sums to a wide decimal type), so check dtypes after an engine hand-off even though the values are exact. A capstone that uses each tool where it is strongest reads as fluency.

---

### Q: What goes in an executive summary, and who is it for?

It is findings-first prose for a non-technical decision-maker who may read nothing else — often the only part that gets read. The form the chapter models: answer the research question directly, lead with findings rather than methods, attach a number to every claim, bold one claim per paragraph, and end with a recommendation that names *actions*, not virtues. Methods live in the notebook underneath it.

The working discipline behind it: gather the headline numbers from the data itself — pulled fresh, not retyped from memory — before writing a word, so the summary can never contradict its own appendix. Every sentence should trace back to a figure your analysis produced; that is what "grounded in the data" means in practice, and it is the standard your assignment's narrative task grades.

---

### Q: Doesn't admitting limitations weaken my report?

The opposite — stating limitations is how you control the interpretation of your work. Readers will find the boundaries eventually; naming them first tells the reader exactly how much weight your conclusions can bear, shows analytical maturity, and preserves your credibility when the boundaries surface. The chapter's model example acknowledges what its data cannot support — no cost data means a revenue lift cannot prove promotions are *profitable* — and says so plainly.

What earns no credit is vague humility ("the data could be better"). Good limitation writing has a specific shape: what we cannot conclude, why, and what data or method would fix it — with each limitation suggesting its own piece of future work. Your assignment grades three distinct limitations and three concrete next steps on exactly that standard.

---

### Q: How many charts should my capstone include?

Four to six, each earning its place — chosen because it answers a facet of the research question, not because it was possible to make. Dozens of charts are always possible; a reader's attention is the scarce resource, and choosing the few that best carry the argument is an editorial decision the chapter treats as part of the analysis itself.

Every chart also needs a title, labeled axes, and a written interpretation underneath — a chart without a sentence is a puzzle, not a finding. The chart shows the pattern; the sentence says what it means for the business and what to do about it. Where you are tempted to build five near-duplicate charts (one per store, say), the chapter's alternative is one chart driven by a marimo widget — same information, and the reader explores it themselves.
