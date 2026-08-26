# Module 12: Marimo Interactive Features

## Introduction

Every module so far has treated a notebook as a one-way street: you write code, run it, and read the output. This module changes the direction of travel. Because marimo tracks the dependencies between cells, it can re-run cells automatically whenever an input changes — and when that input is a dropdown, slider, search box, or checkbox, your notebook becomes an interactive application. That distinction matters in business more than almost anywhere else: the person who needs the answer (a product manager choosing which region to expand, a director checking whether accessories are growing) is usually not the person who wrote the code. A notebook with well-designed widgets lets a manager who has never written a line of Python filter data, adjust thresholds, and explore charts on their own. By the end of this module you will build exactly that: a tabbed sales dashboard driven by five coordinated controls.

---

## Learning Objectives

By the end of this module, you should be able to:

1. **Create** interactive UI elements using `mo.ui.dropdown`, `mo.ui.slider`, `mo.ui.text`, and `mo.ui.checkbox`
2. **Build** reactive data filters that update downstream results automatically
3. **Display** and filter DataFrames interactively with `mo.ui.table`
4. **Compose** dashboard layouts using `mo.hstack`, `mo.vstack`, and `mo.ui.tabs`
5. **Combine** Plotly Express charts with marimo UI elements for interactive exploration
6. **Design** an interactive data exploration workflow that a non-programmer can use

---

## 12.1 From Static Notebooks to Interactive Tools

Marimo's reactive execution model was introduced back in Module 1: cells form a dependency graph, and when a variable changes, every cell that uses it re-runs. Until now that mostly meant you never had stale results. This module pairs the same mechanism with **UI widgets** — on-screen controls whose current setting is a Python value. Move a slider, and every cell that reads the slider re-runs. No callbacks, no event handlers, no "refresh" button: the dependency graph does the work.

!!! note "How This Chapter's Examples Are Verified"

    Widgets only exist inside a running marimo session — a plain Python script
    cannot render a dropdown or wait for a click. The Worked Examples in this
    chapter therefore come from a companion script in which an ordinary
    variable stands in for each widget's `.value` (for example,
    `selected_region = "North"` plays the role of `region_dropdown.value`).
    The downstream filtering and aggregation logic is exactly the teaching
    notebook's, and each Output block states which widget settings it
    simulates. To experience the live behavior — drag, click, type — open
    `m12_teaching.py` with marimo and interact with the real widgets.

### The Dataset

The whole module works on one product-sales dataset: monthly sales records across regions, product categories, and individual products — the kind of data a product manager or analyst explores with filters and charts. A setup cell in the teaching notebook writes the CSV to `/tmp/m12_sales.csv` and reads it back with Polars.

!!! example "Worked Example: Loading the Product-Sales Dataset"

    ```python
    import polars as pl

    # A setup cell has written the module's sales CSV to /tmp
    sales = pl.read_csv("/tmp/m12_sales.csv")

    print(f"Loaded sales data: {sales.shape[0]} rows, {sales.shape[1]} columns")
    print(f"Regions: {sales['region'].unique().sort().to_list()}")
    print(f"Categories: {sales['category'].unique().sort().to_list()}")
    print(f"Products: {sales['product'].unique().sort().to_list()}")

    sales.head(5)   # bare last expression — marimo renders it as a table
    ```

    **Output:**

    ```
    Loaded sales data: 54 rows, 7 columns
    Regions: ['East', 'North', 'South', 'West']
    Categories: ['Accessories', 'Electronics']
    Products: ['Keyboard', 'Laptop', 'Monitor', 'Mouse']

    First 5 rows:
    shape: (5, 7)
    ┌───────┬────────┬─────────────┬─────────┬───────┬─────────┬────────┐
    │ month ┆ region ┆ category    ┆ product ┆ units ┆ revenue ┆ cost   │
    │ ---   ┆ ---    ┆ ---         ┆ ---     ┆ ---   ┆ ---     ┆ ---    │
    │ str   ┆ str    ┆ str         ┆ str     ┆ i64   ┆ i64     ┆ i64    │
    ╞═══════╪════════╪═════════════╪═════════╪═══════╪═════════╪════════╡
    │ Jan   ┆ North  ┆ Electronics ┆ Laptop  ┆ 120   ┆ 143880  ┆ 95400  │
    │ Feb   ┆ North  ┆ Electronics ┆ Laptop  ┆ 135   ┆ 161865  ┆ 101250 │
    │ Mar   ┆ North  ┆ Electronics ┆ Laptop  ┆ 150   ┆ 179850  ┆ 112500 │
    │ Apr   ┆ North  ┆ Electronics ┆ Laptop  ┆ 110   ┆ 131890  ┆ 82500  │
    │ May   ┆ North  ┆ Electronics ┆ Laptop  ┆ 165   ┆ 197835  ┆ 123750 │
    └───────┴────────┴─────────────┴─────────┴───────┴─────────┴────────┘
    ```

    **Interpretation:** Each of the 54 rows is one product's performance in one region for one month: units sold, revenue earned, and cost incurred. Four regions, two categories, and four products give the filters in this module something meaningful to slice — and the dataset is small enough that you can verify any widget-driven result by hand.

    *Source: `computations/module12_examples.py` — `demo_sales_dataset()`*

### How Marimo Reactivity Works

Before touching any widget, it helps to see the mechanism that makes them useful:

1. **You create a UI element** in one cell and return it (for example, a dropdown).
2. **Marimo displays it**, and the user interacts with it.
3. **Every cell that references that element re-runs automatically** when its value changes.

The key rule: **create and display** the widget in one cell, **read its `.value`** in a *different* cell. This separation is what triggers the reactive update.

```
Cell A:  dropdown = mo.ui.dropdown(...)    # create
         dropdown                          # display (bare last line renders it)

Cell B:  selected = dropdown.value         # read the value
         ... filter data using selected ...
```

Note the bare `dropdown` line in Cell A. Marimo shows a cell's **last expression**; an assignment alone displays nothing, so the widget only appears if you put its name on its own line after creating it. When the user picks a new option in Cell A, marimo sees that Cell B depends on `dropdown` and re-runs Cell B with the new value.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "I can create a widget and read its `.value` in the same cell." | Reading `.value` in the cell that creates the widget does not react — you get the value as of creation time, and nothing re-runs on interaction. Create and display in one cell; read `.value` in another. |
| "Assigning the widget to a variable is enough to display it." | An assignment displays nothing. Marimo renders a cell's *last expression*, so the widget's name must appear on its own line (or inside a layout call) at the end of the cell. |
| "I need to register a callback or event handler to respond to a click." | Marimo has no callback wiring. Any cell that references the widget is automatically a "handler" — it re-runs whenever the widget's value changes. |

---

## 12.2 The Core Widgets: Dropdown, Slider, Text, and Checkbox

Four widgets cover most business filtering needs: a **dropdown** for categorical choices, a **slider** for numeric thresholds, a **text box** for free-text search, and a **checkbox** for on/off toggles. Each follows the same two-cell pattern from the previous section.

### `mo.ui.dropdown()` — Selecting Categories

A dropdown presents a list of options and lets the user pick one. It is the most common widget for categorical filters — region, product type, department, status.

```python
dropdown = mo.ui.dropdown(
    options=["North", "South", "East", "West"],
    value="North",       # default selection
    label="Region",
)
```

In the teaching notebook, the dropdown's options come from the data itself, so the widget never drifts out of sync with the DataFrame:

!!! example "Worked Example: Filtering with a Dropdown Selection"

    ```python
    # Cell 1 — create and display the dropdown
    _regions = sales["region"].unique().sort().to_list()
    region_dropdown = mo.ui.dropdown(
        options=_regions,
        value=_regions[0],
        label="Select Region",
    )
    region_dropdown

    # Cell 2 — re-runs whenever region_dropdown changes
    # (the companion script simulates region_dropdown.value == "North")
    _selected = region_dropdown.value
    _filtered = sales.filter(pl.col("region") == _selected)

    _summary = (
        _filtered
        .group_by("product")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
        .sort("total_revenue", descending=True)
    )

    _fig = px.bar(
        _summary.to_pandas(),
        x="product",
        y="total_revenue",
        title=f"Revenue by Product — {_selected} Region",
        labels={"total_revenue": "Revenue ($)", "product": "Product"},
        color="product",
    )
    _fig
    ```

    **Output:**

    ```
    Simulating dropdown selection: North

    Rows for the North region: 18

    Revenue by product (the data behind the bar chart):
    shape: (3, 2)
    ┌──────────┬───────────────┐
    │ product  ┆ total_revenue │
    │ ---      ┆ ---           │
    │ str      ┆ i64           │
    ╞══════════╪═══════════════╡
    │ Laptop   ┆ 1031140       │
    │ Monitor  ┆ 461340        │
    │ Keyboard ┆ 213333        │
    └──────────┴───────────────┘
    ```

    **Interpretation:** Selecting North keeps 18 of the sales rows, and the bar chart built from them shows Laptop leading the region at $1,031,140 — more than Monitor ($461,340) and Keyboard ($213,333) combined. When the user picks a different region, the filter, the aggregation, and the chart all recompute without anyone touching the code.

    *Source: `computations/module12_examples.py` — `demo_dropdown_region_filter()`*

### `mo.ui.slider()` — Setting Numeric Thresholds

Sliders let users set a numeric value by dragging a handle. Common uses: a minimum revenue threshold, a date range, or the number of items to display.

```python
slider = mo.ui.slider(
    start=0,
    stop=100000,
    step=5000,
    value=20000,
    label="Minimum Revenue",
)
```

The teaching notebook points the slider at a revenue floor and lets *two* cells react to it — a summary message and a scatter plot:

!!! example "Worked Example: A Revenue Threshold Slider"

    ```python
    # Cell 1 — create and display the slider
    revenue_slider = mo.ui.slider(
        start=0,
        stop=200000,
        step=5000,
        value=50000,
        label="Minimum Revenue",
    )
    revenue_slider

    # Cell 2 — summary text that re-runs when the slider moves
    # (the companion script simulates revenue_slider.value == 50000)
    _threshold = revenue_slider.value
    _filtered = sales.filter(pl.col("revenue") >= _threshold)

    mo.md(
        f"""
    **Threshold:** ${_threshold:,}

    **Rows matching:** {_filtered.shape[0]} of {sales.shape[0]}
    ({_filtered.shape[0] / sales.shape[0] * 100:.0f}%)
    """
    )

    # Cell 3 — a scatter plot of only the rows above the threshold
    _fig = px.scatter(
        _filtered.to_pandas(),
        x="units",
        y="revenue",
        color="product",
        hover_data=["month", "region"],
        title=f"Products with Revenue >= ${_threshold:,}",
        labels={"units": "Units Sold", "revenue": "Revenue ($)"},
    )
    _fig
    ```

    **Output:**

    ```
    Simulating slider value: 50000 (Minimum Revenue)

    Threshold: $50,000
    Rows matching: 30 of 54 (56%)

    Rows above the threshold by product (the points on the scatter plot):
    shape: (2, 2)
    ┌─────────┬──────────────────────┐
    │ product ┆ rows_above_threshold │
    │ ---     ┆ ---                  │
    │ str     ┆ u32                  │
    ╞═════════╪══════════════════════╡
    │ Laptop  ┆ 18                   │
    │ Monitor ┆ 12                   │
    └─────────┴──────────────────────┘
    ```

    **Interpretation:** At a $50,000 floor, 30 of 54 rows (56%) qualify — and every survivor is a Laptop or Monitor record (18 and 12 scatter points respectively). Keyboards and mice never clear the bar in any month, so a manager dragging this slider watches the accessories disappear from the chart well before the electronics do.

    *Source: `computations/module12_examples.py` — `demo_slider_revenue_threshold()`*

!!! question "Try It Yourself: One Slider, Two Reactions"

    In the teaching notebook, drag the revenue slider and watch both the
    summary text and the scatter plot update. Notice that two separate cells
    react to the same slider — any cell that references `revenue_slider`
    re-runs.

### `mo.ui.text()` — Free-Text Search

A text input lets users type a search string. Use it to filter rows where a column contains the typed text — a simple product search, for example.

```python
search_box = mo.ui.text(
    placeholder="Type a product name...",
    label="Search",
)
```

One detail deserves care: before the user types anything, `search_box.value` is an empty string. The filter cell should treat "empty" as "show everything" rather than matching nothing:

!!! example "Worked Example: Searching Products by Substring"

    ```python
    # Cell 1 — create and display the search box
    search_box = mo.ui.text(
        placeholder="Type a product name...",
        label="Product Search",
    )
    search_box

    # Cell 2 — filter on the typed text, case-insensitively
    # (the companion script simulates search_box.value == "key")
    _query = search_box.value.strip().lower()

    if _query:
        _filtered = sales.filter(
            pl.col("product").str.to_lowercase().str.contains(_query, literal=True)
        )
    else:
        _filtered = sales    # empty search shows all rows

    print(f"Search: '{search_box.value}' — {_filtered.shape[0]} rows found")
    _filtered.head(10)
    ```

    **Output:**

    ```
    Simulating text input: 'key'

    Search: 'key' — 18 rows found

    First 10 matching rows:
    shape: (10, 7)
    ┌───────┬────────┬─────────────┬──────────┬───────┬─────────┬───────┐
    │ month ┆ region ┆ category    ┆ product  ┆ units ┆ revenue ┆ cost  │
    │ ---   ┆ ---    ┆ ---         ┆ ---      ┆ ---   ┆ ---     ┆ ---   │
    │ str   ┆ str    ┆ str         ┆ str      ┆ i64   ┆ i64     ┆ i64   │
    ╞═══════╪════════╪═════════════╪══════════╪═══════╪═════════╪═══════╡
    │ Jan   ┆ North  ┆ Accessories ┆ Keyboard ┆ 400   ┆ 31960   ┆ 16000 │
    │ Feb   ┆ North  ┆ Accessories ┆ Keyboard ┆ 450   ┆ 35955   ┆ 18000 │
    │ Mar   ┆ North  ┆ Accessories ┆ Keyboard ┆ 420   ┆ 33558   ┆ 16800 │
    │ Apr   ┆ North  ┆ Accessories ┆ Keyboard ┆ 380   ┆ 30362   ┆ 15200 │
    │ May   ┆ North  ┆ Accessories ┆ Keyboard ┆ 500   ┆ 39950   ┆ 20000 │
    │ Jun   ┆ North  ┆ Accessories ┆ Keyboard ┆ 520   ┆ 41548   ┆ 20800 │
    │ Jan   ┆ South  ┆ Accessories ┆ Keyboard ┆ 300   ┆ 23970   ┆ 12000 │
    │ Feb   ┆ South  ┆ Accessories ┆ Keyboard ┆ 320   ┆ 25568   ┆ 12800 │
    │ Mar   ┆ South  ┆ Accessories ┆ Keyboard ┆ 350   ┆ 27965   ┆ 14000 │
    │ Apr   ┆ South  ┆ Accessories ┆ Keyboard ┆ 310   ┆ 24769   ┆ 12400 │
    └───────┴────────┴─────────────┴──────────┴───────┴─────────┴───────┘
    ```

    **Interpretation:** Typing the partial string `key` matches every Keyboard row — 18 in total — because the filter lowercases both sides before checking containment. Users search the way they think ("key", "Key", "KEYBOARD"), and the case-insensitive substring match meets them there.

    *Source: `computations/module12_examples.py` — `demo_text_search()`*

### `mo.ui.checkbox()` — Toggling Options

Checkboxes are on/off switches. They are useful for toggling features: show or hide a data series, enable a filter, switch between chart types.

```python
show_trend = mo.ui.checkbox(value=True, label="Show trend line")
```

The teaching notebook creates one checkbox per region and rebuilds a line chart from whichever boxes are ticked:

!!! example "Worked Example: Region Checkboxes Driving a Line Chart"

    ```python
    # Cell 1 — four checkboxes displayed in a row
    show_north = mo.ui.checkbox(value=True, label="Show North")
    show_south = mo.ui.checkbox(value=True, label="Show South")
    show_east = mo.ui.checkbox(value=True, label="Show East")
    show_west = mo.ui.checkbox(value=True, label="Show West")

    mo.hstack([show_north, show_south, show_east, show_west])

    # Cell 2 — build the region list from the checkbox states
    # (the companion script simulates North=True, South=False,
    #  East=False, West=True)
    _regions = []
    if show_north.value:
        _regions.append("North")
    if show_south.value:
        _regions.append("South")
    if show_east.value:
        _regions.append("East")
    if show_west.value:
        _regions.append("West")

    _month_map = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6}
    _summary = (
        sales.filter(pl.col("region").is_in(_regions))
        .group_by("month", "region")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
        .with_columns(pl.col("month").replace_strict(_month_map).alias("month_num"))
        .sort("month_num", "region")
        .select("month", "region", "total_revenue")
    )

    _fig = px.line(
        _summary.to_pandas(),
        x="month",
        y="total_revenue",
        color="region",
        markers=True,
        title="Monthly Revenue by Region (toggle regions above)",
        labels={"total_revenue": "Revenue ($)", "month": "Month"},
    )
    _fig
    ```

    **Output:**

    ```
    Simulating checkbox states: North=True, South=False, East=False, West=True
    Regions included: ['North', 'West']

    Monthly revenue for the selected regions (the data behind the line chart):
    shape: (12, 3)
    ┌───────┬────────┬───────────────┐
    │ month ┆ region ┆ total_revenue │
    │ ---   ┆ ---    ┆ ---           │
    │ str   ┆ str    ┆ i64           │
    ╞═══════╪════════╪═══════════════╡
    │ Jan   ┆ North  ┆ 245740        │
    │ Jan   ┆ West   ┆ 17940         │
    │ Feb   ┆ North  ┆ 274710        │
    │ Feb   ┆ West   ┆ 19435         │
    │ Mar   ┆ North  ┆ 279813        │
    │ …     ┆ …      ┆ …             │
    │ Apr   ┆ West   ┆ 17342         │
    │ May   ┆ North  ┆ 321665        │
    │ May   ┆ West   ┆ 20930         │
    │ Jun   ┆ North  ┆ 348238        │
    │ Jun   ┆ West   ┆ 21528         │
    └───────┴────────┴───────────────┘
    ```

    **Interpretation:** With South and East unticked, the line chart draws two series instead of four. The contrast is stark: North climbs to $348,238 by June, while West — which only sells the Mouse — stays around $21,528. Checkbox combinations like this let a viewer isolate any subset of regions without ever editing the filter code. Note also that the teaching notebook displays a friendly message instead of a chart when *no* box is ticked — always plan for the empty case.

    *Source: `computations/module12_examples.py` — `demo_checkbox_region_toggle()`*

!!! question "Try It Yourself: Toggling Regions"

    Toggle the checkboxes in the teaching notebook. Each combination produces
    a different view of the same data. Notice how the chart updates without
    you writing any new code — that is the power of reactive UI.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "`dropdown.value` returns the position of the chosen option." | It returns the selected option itself (for example, the string `"North"`), ready to use directly in a filter expression. |
| "A slider's value comes back as text that must be converted." | The value is numeric, in the units defined by `start`, `stop`, and `step` — compare it to a column directly. |
| "An empty search box means no rows match." | Before any typing, `text.value` is `""`. Your filter cell must decide what that means — the notebook's pattern (`if _query: ... else: show all`) treats an empty box as "no filter". |
| "A checkbox reports `\"checked\"` or `\"unchecked\"`." | `checkbox.value` is a Python boolean (`True`/`False`), so it drops straight into an `if` statement. |

---

## 12.3 Combining Widgets and Interactive Tables

Real dashboards use several widgets together. Each widget controls a different dimension of the data — region, product category, revenue threshold — and the output reflects all of them simultaneously. The pattern stays the same: create the widgets (grouped in one cell is fine), then read all their `.value` properties in the analysis cell.

### Combining Multiple Widgets

The teaching notebook builds a three-widget control panel. Two details are worth copying into your own work. First, each dropdown gets a manual `"All"` option, and the filter code *skips* that dimension when `"All"` is selected. Second, all filters are applied in one cell that exports a single `filtered_data` DataFrame, so every downstream cell shares the same definition of "the current data."

!!! example "Worked Example: Three Coordinated Filters"

    ```python
    # Cell 1 — the control panel, displayed in a row
    _regions = ["All"] + sales["region"].unique().sort().to_list()
    _categories = ["All"] + sales["category"].unique().sort().to_list()

    filter_region = mo.ui.dropdown(options=_regions, value="All", label="Region")
    filter_category = mo.ui.dropdown(options=_categories, value="All", label="Category")
    filter_min_rev = mo.ui.slider(
        start=0, stop=200000, step=10000, value=0, label="Min Revenue"
    )

    mo.hstack([filter_region, filter_category, filter_min_rev], justify="start", gap=1)

    # Cell 2 — apply all filters at once and export filtered_data
    # (the companion script simulates Region="North",
    #  Category="Electronics", Min Revenue=100000)
    _df = sales

    if filter_region.value != "All":
        _df = _df.filter(pl.col("region") == filter_region.value)

    if filter_category.value != "All":
        _df = _df.filter(pl.col("category") == filter_category.value)

    _df = _df.filter(pl.col("revenue") >= filter_min_rev.value)

    filtered_data = _df
    print(
        f"Filters: region={filter_region.value}, "
        f"category={filter_category.value}, "
        f"min_revenue=${filter_min_rev.value:,}"
    )
    print(f"Rows after filtering: {filtered_data.shape[0]}")

    # Cell 3 — a bar chart that reflects every active filter
    _summary = (
        filtered_data
        .group_by("product")
        .agg(
            pl.col("revenue").sum().alias("total_revenue"),
            pl.col("units").sum().alias("total_units"),
        )
        .sort("total_revenue", descending=True)
    )

    _fig = px.bar(
        _summary.to_pandas(),
        x="product",
        y="total_revenue",
        color="product",
        title="Filtered Revenue by Product",
        labels={"total_revenue": "Revenue ($)", "product": "Product"},
        text="total_revenue",
    )
    _fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    _fig
    ```

    **Output:**

    ```
    Simulating control panel: Region=North, Category=Electronics, Min Revenue=$100,000

    Filters: region=North, category=Electronics, min_revenue=$100,000
    Rows after filtering: 6

    Filtered revenue by product (the data behind the bar chart):
    shape: (1, 3)
    ┌─────────┬───────────────┬─────────────┐
    │ product ┆ total_revenue ┆ total_units │
    │ ---     ┆ ---           ┆ ---         │
    │ str     ┆ i64           ┆ i64         │
    ╞═════════╪═══════════════╪═════════════╡
    │ Laptop  ┆ 1031140       ┆ 860         │
    └─────────┴───────────────┴─────────────┘
    ```

    **Interpretation:** The three filters act together: North narrows the regions, Electronics narrows the categories, and the $100,000 floor eliminates every Monitor month — leaving 6 rows, all of them Laptop sales. The chart collapses to a single bar: $1,031,140 of revenue on 860 units. Reading each widget's `.value` in one central cell keeps the combined logic in one place.

    *Source: `computations/module12_examples.py` — `demo_combined_filters()`*

### `mo.ui.table()` — Interactive DataFrame Display

`mo.ui.table()` renders a Polars (or pandas) DataFrame as an interactive table with sorting, pagination, and row selection. Users can click column headers to sort, and click rows to pass them downstream.

```python
table = mo.ui.table(
    data=df,
    selection="multi",   # allow selecting multiple rows
    label="Sales Data",
)
```

The selected rows come back as `table.value` — a DataFrame containing only the rows the user clicked. That turns a display element into an *input* element: the user hand-picks items, and your code charts whatever they picked.

!!! example "Worked Example: Charting Rows Selected in a Table"

    ```python
    # Cell 1 — a product-by-region summary the user can sort and select from
    _summary = (
        sales
        .group_by("product", "region")
        .agg(
            pl.col("revenue").sum().alias("total_revenue"),
            pl.col("units").sum().alias("total_units"),
            pl.col("cost").sum().alias("total_cost"),
        )
        .with_columns(
            (pl.col("total_revenue") - pl.col("total_cost")).alias("profit"),
        )
        .sort("total_revenue", descending=True)
    )

    product_table = mo.ui.table(
        data=_summary,
        selection="multi",
        label="Click rows to select them for charting",
    )
    product_table

    # Cell 2 — chart only the selected rows
    # (the companion script simulates selecting the Laptop rows)
    _selected = product_table.value

    if len(_selected) > 0:
        _fig = px.bar(
            _selected.to_pandas(),
            x="product",
            y="total_revenue",
            color="region",
            barmode="group",
            title=f"Selected Products ({len(_selected)} rows)",
            labels={"total_revenue": "Revenue ($)", "product": "Product"},
        )
        _display = mo.vstack([
            mo.md(f"**{len(_selected)} rows selected** — chart below shows only selected data."),
            _fig,
        ])
    else:
        _display = mo.md("*Select one or more rows in the table above to generate a chart.*")
    _display
    ```

    **Output:**

    ```
    The summary shown in mo.ui.table (sortable, selectable):
    shape: (9, 6)
    ┌──────────┬────────┬───────────────┬─────────────┬────────────┬────────┐
    │ product  ┆ region ┆ total_revenue ┆ total_units ┆ total_cost ┆ profit │
    │ ---      ┆ ---    ┆ ---           ┆ ---         ┆ ---        ┆ ---    │
    │ str      ┆ str    ┆ i64           ┆ i64         ┆ i64        ┆ i64    │
    ╞══════════╪════════╪═══════════════╪═════════════╪════════════╪════════╡
    │ Laptop   ┆ North  ┆ 1031140       ┆ 860         ┆ 650400     ┆ 380740 │
    │ Laptop   ┆ East   ┆ 875270        ┆ 730         ┆ 547500     ┆ 327770 │
    │ Laptop   ┆ South  ┆ 809325        ┆ 675         ┆ 506250     ┆ 303075 │
    │ Monitor  ┆ North  ┆ 461340        ┆ 1320        ┆ 277200     ┆ 184140 │
    │ Monitor  ┆ South  ┆ 373965        ┆ 1070        ┆ 224700     ┆ 149265 │
    │ Keyboard ┆ North  ┆ 213333        ┆ 2670        ┆ 106800     ┆ 106533 │
    │ Keyboard ┆ South  ┆ 163000        ┆ 2040        ┆ 81600      ┆ 81400  │
    │ Keyboard ┆ East   ┆ 155006        ┆ 1940        ┆ 77600      ┆ 77406  │
    │ Mouse    ┆ West   ┆ 115713        ┆ 3870        ┆ 38700      ┆ 77013  │
    └──────────┴────────┴───────────────┴─────────────┴────────────┴────────┘

    Simulating table selection: the Laptop rows
    3 rows selected — chart below shows only selected data.

    Selected rows (the data behind the grouped bar chart):
    shape: (3, 3)
    ┌─────────┬────────┬───────────────┐
    │ product ┆ region ┆ total_revenue │
    │ ---     ┆ ---    ┆ ---           │
    │ str     ┆ str    ┆ i64           │
    ╞═════════╪════════╪═══════════════╡
    │ Laptop  ┆ North  ┆ 1031140       │
    │ Laptop  ┆ East   ┆ 875270        │
    │ Laptop  ┆ South  ┆ 809325        │
    └─────────┴────────┴───────────────┘
    ```

    **Interpretation:** The table shows the full product-by-region summary; clicking the Laptop rows hands exactly 3 rows to the chart cell, which compares North ($1,031,140), East ($875,270), and South ($809,325). The summary also rewards a sort by the profit column: Mouse earns the least revenue ($115,713) yet its profit ($77,013) nearly matches Keyboard East's ($77,406) — margins matter, not just top-line revenue.

    *Source: `computations/module12_examples.py` — `demo_table_selection()`*

!!! question "Try It Yourself: Hand-Picking Rows"

    Click on rows in the teaching notebook's table. The chart below it
    updates to show only the products and regions you selected. This pattern
    is useful when you want users to hand-pick items for comparison.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "Dropdowns come with a built-in 'All' choice." | You add `"All"` to the options list yourself, and your filter code must explicitly skip that dimension when `"All"` is selected. |
| "`table.value` is the whole DataFrame I displayed." | It holds only the rows the user has selected — possibly zero rows. Always handle the empty-selection case with a helpful message. |
| "If several widgets are created in one cell, returning one of them is enough." | Every widget another cell reads must be returned from its creating cell. Group them visually with `mo.hstack`, but return them all. |

---

## 12.4 Layout Composition and Live Charts

Analysis cells produce charts, tables, and markdown. Layout helpers arrange those pieces side-by-side or into tabbed panels — essential for dashboard-like views.

| Function | Layout |
|----------|--------|
| `mo.hstack([a, b, c])` | Horizontal row |
| `mo.vstack([a, b, c])` | Vertical stack |
| `mo.ui.tabs({...})` | Tabbed panels |

### `mo.hstack()` and `mo.vstack()`

```python
mo.hstack([chart_1, chart_2])          # side by side
mo.vstack([title_md, chart, table])    # stacked vertically
```

The teaching notebook pairs two bar charts — revenue by region and revenue by category — in a single horizontal row:

!!! example "Worked Example: Two Charts Side by Side"

    ```python
    _by_region = (
        sales.group_by("region")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
        .sort("total_revenue", descending=True)
    )

    _by_category = (
        sales.group_by("category")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
        .sort("total_revenue", descending=True)
    )

    _fig1 = px.bar(
        _by_region.to_pandas(),
        x="region", y="total_revenue",
        title="Revenue by Region", color="region",
    )
    _fig2 = px.bar(
        _by_category.to_pandas(),
        x="category", y="total_revenue",
        title="Revenue by Category", color="category",
    )

    mo.hstack([_fig1, _fig2])   # the two charts render in one row
    ```

    **Output:**

    ```
    Left chart — Revenue by Region:
    shape: (4, 2)
    ┌────────┬───────────────┐
    │ region ┆ total_revenue │
    │ ---    ┆ ---           │
    │ str    ┆ i64           │
    ╞════════╪═══════════════╡
    │ North  ┆ 1705813       │
    │ South  ┆ 1346290       │
    │ East   ┆ 1030276       │
    │ West   ┆ 115713        │
    └────────┴───────────────┘

    Right chart — Revenue by Category:
    shape: (2, 2)
    ┌─────────────┬───────────────┐
    │ category    ┆ total_revenue │
    │ ---         ┆ ---           │
    │ str         ┆ i64           │
    ╞═════════════╪═══════════════╡
    │ Electronics ┆ 3551040       │
    │ Accessories ┆ 647052        │
    └─────────────┴───────────────┘
    ```

    **Interpretation:** Placed side by side, the two views answer different questions at a glance: geographically, North leads at $1,705,813 while West trails at $115,713; by category, Electronics out-earns Accessories $3,551,040 to $647,052. `mo.hstack` costs one line and saves the reader a scroll.

    *Source: `computations/module12_examples.py` — `demo_side_by_side_summaries()`*

### `mo.ui.tabs()`

Tabs keep a notebook compact — instead of scrolling through many charts, users choose which view they want:

```python
layout_tabs = mo.ui.tabs({
    "Trend": _trend_fig,        # a line chart of monthly revenue
    "Products": _product_fig,   # a bar chart of revenue by product
    "Raw Data": mo.ui.table(data=sales.head(20), label="First 20 rows"),
})
layout_tabs
```

Each tab's content is any displayable object — a Plotly figure, a `mo.ui.table`, a `mo.vstack` of several pieces, or plain markdown. The dictionary keys become the tab labels. The aggregations feeding each panel are the same `group_by` patterns you have used all module; the capstone at the end of this chapter assembles a full tabbed dashboard and verifies its numbers.

### Choosing the Chart's Metric with a Dropdown

The real power of this module comes from connecting Plotly's charts to marimo's widgets. Here a dropdown chooses which *column* the chart visualizes — same chart structure, different data, controlled entirely by the user:

!!! example "Worked Example: A Metric-Selector Dropdown"

    ```python
    # Cell 1 — dropdown to select the y-axis metric
    metric_dropdown = mo.ui.dropdown(
        options=["revenue", "units", "cost"],
        value="revenue",
        label="Metric",
    )
    metric_dropdown

    # Cell 2 — the chart re-aggregates on the chosen column
    # (the companion script simulates metric_dropdown.value == "units")
    _metric = metric_dropdown.value

    _summary = (
        sales
        .group_by("product", "region")
        .agg(pl.col(_metric).sum().alias("total"))
        .sort("total", descending=True)
    )

    _fig = px.bar(
        _summary.to_pandas(),
        x="product",
        y="total",
        color="region",
        barmode="group",
        title=f"Total {_metric.title()} by Product and Region",
        labels={"total": _metric.title(), "product": "Product"},
    )
    _fig
    ```

    **Output:**

    ```
    Simulating metric selection: units

    Total units by product and region (the data behind the grouped bar chart):
    shape: (9, 3)
    ┌──────────┬────────┬───────┐
    │ product  ┆ region ┆ total │
    │ ---      ┆ ---    ┆ ---   │
    │ str      ┆ str    ┆ i64   │
    ╞══════════╪════════╪═══════╡
    │ Mouse    ┆ West   ┆ 3870  │
    │ Keyboard ┆ North  ┆ 2670  │
    │ Keyboard ┆ South  ┆ 2040  │
    │ Keyboard ┆ East   ┆ 1940  │
    │ Monitor  ┆ North  ┆ 1320  │
    │ Monitor  ┆ South  ┆ 1070  │
    │ Laptop   ┆ North  ┆ 860   │
    │ Laptop   ┆ East   ┆ 730   │
    │ Laptop   ┆ South  ┆ 675   │
    └──────────┴────────┴───────┘
    ```

    **Interpretation:** Switching the metric to units inverts the story the revenue view told: Mouse leads at 3,870 units while the Laptop — the revenue champion — sells the fewest (860, 730, and 675 across its three regions). Cheap items move in volume; expensive items earn in dollars. Letting the viewer flip between metrics with one dropdown surfaces that contrast without a second chart.

    *Source: `computations/module12_examples.py` — `demo_metric_dropdown()`*

!!! question "Try It Yourself: Switching Metrics"

    Switch the metric dropdown in the teaching notebook between "revenue",
    "units", and "cost". The chart axes and title update to match — same
    chart structure, different data, controlled entirely by the user.

### Building a Data Explorer

Combining a metric dropdown, a group-by dropdown, and a filtering slider produces a general-purpose explorer — the pattern behind real business dashboards:

!!! example "Worked Example: A Three-Control Data Explorer"

    ```python
    # Cell 1 — explorer controls in a row
    explore_column = mo.ui.dropdown(
        options=["revenue", "units", "cost"], value="revenue",
        label="Column to Explore",
    )
    explore_min = mo.ui.slider(
        start=0, stop=500, step=10, value=0,
        label="Minimum Units",
    )
    explore_group = mo.ui.dropdown(
        options=["product", "region", "category"], value="product",
        label="Group By",
    )

    mo.hstack([explore_column, explore_group, explore_min], justify="start", gap=1)

    # Cell 2 — filter, aggregate, and chart
    # (the companion script simulates Column="revenue",
    #  Group By="region", Minimum Units=200)
    _col = explore_column.value
    _group = explore_group.value
    _min_units = explore_min.value

    _df = sales.filter(pl.col("units") >= _min_units)

    _agg = (
        _df
        .group_by(_group)
        .agg(pl.col(_col).sum().alias("total"))
        .sort("total", descending=True)
    )

    _fig = px.bar(
        _agg.to_pandas(),
        x=_group,
        y="total",
        color=_group,
        title=f"Total {_col.title()} by {_group.title()} (units >= {_min_units})",
        labels={"total": _col.title(), _group: _group.title()},
    )

    mo.vstack([
        mo.md(f"**{_df.shape[0]}** rows after filtering (min units = {_min_units})"),
        _fig,
    ])
    ```

    **Output:**

    ```
    Simulating explorer controls: Column=revenue, Group By=region, Minimum Units=200

    31 rows after filtering (min units = 200)

    Total revenue by region (units >= 200):
    shape: (4, 2)
    ┌────────┬────────┐
    │ region ┆ total  │
    │ ---    ┆ ---    │
    │ str    ┆ i64    │
    ╞════════╪════════╡
    │ North  ┆ 608268 │
    │ South  ┆ 306295 │
    │ East   ┆ 155006 │
    │ West   ┆ 115713 │
    └────────┴────────┘
    ```

    **Interpretation:** A 200-unit floor keeps 31 rows — and silently removes every Laptop record, since no Laptop month reaches that volume. The remaining revenue ranking (North at $608,268 down to West at $115,713) therefore describes high-volume products only. That is the explorer's lesson for dashboard builders: a filter on one column reshapes what every chart appears to say, so label the active filters clearly, as the title and summary line do here.

    *Source: `computations/module12_examples.py` — `demo_data_explorer()`*

---

## 12.5 Design Patterns and the Capstone Dashboard

### Design Patterns for Interactive Workflows

As your interactive notebooks grow, five patterns keep them maintainable:

**1. One widget per cell, or group related widgets in one cell.** Each UI element another cell reads must be returned from its creating cell. If you group widgets with `mo.hstack`, return them all:

```python
return slider_a, slider_b, dropdown_c
```

**2. Separate creation from consumption.** The cell that creates a widget should not also do heavy computation with its value. Create and display in one cell, compute in another.

**3. Avoid circular dependencies.** If Cell A depends on Cell B and Cell B depends on Cell A, marimo raises an error. Data should flow in one direction:

```
Widgets --> Filters --> Aggregation --> Visualization
```

**4. Keep filter logic centralized.** Apply all filters in one cell and export the filtered DataFrame. Multiple downstream cells can then use `filtered_data` without duplicating filter logic — and without the risk of two charts silently disagreeing about what "filtered" means.

**5. Provide sensible defaults.** Always set a `value=` on widgets so the notebook displays meaningful content when first opened, before the user interacts.

### Capstone: Interactive Sales Data Explorer

The teaching notebook closes by combining everything in the module — dropdowns for region and category, a slider for minimum revenue, a text input for product search, a checkbox toggling trend lines, and a tabbed layout with overview charts, trend views, a scatter plot, and a data table. This is the kind of tool you could hand to a manager and say: *"Explore the data yourself."*

The control panel groups all five widgets with nested layout calls:

```python
# --- Capstone: Control Panel (one cell, returns all five widgets) ---
cap_region = mo.ui.dropdown(options=_regions, value="All", label="Region")
cap_category = mo.ui.dropdown(options=_categories, value="All", label="Category")
cap_min_revenue = mo.ui.slider(
    start=0, stop=200000, step=5000, value=0, label="Min Revenue ($)"
)
cap_search = mo.ui.text(placeholder="Search products...", label="Product Search")
cap_show_trend = mo.ui.checkbox(value=True, label="Show trend lines")

mo.vstack([
    mo.md("### Control Panel"),
    mo.hstack([cap_region, cap_category, cap_min_revenue], justify="start", gap=1),
    mo.hstack([cap_search, cap_show_trend], justify="start", gap=1),
])
```

A single filter cell then reads all four filtering widgets (pattern 4 above) and exports `cap_filtered` for the dashboard to consume:

!!! example "Worked Example: The Capstone Filter Cell"

    ```python
    # --- Capstone: apply all filters in one cell ---
    # (the companion script simulates Region="North", Category="All",
    #  Min Revenue=50000, Search="")
    cap_filtered = sales.with_columns(
        (pl.col("revenue") - pl.col("cost")).alias("profit"),
    )

    if cap_region.value != "All":
        cap_filtered = cap_filtered.filter(pl.col("region") == cap_region.value)

    if cap_category.value != "All":
        cap_filtered = cap_filtered.filter(pl.col("category") == cap_category.value)

    cap_filtered = cap_filtered.filter(pl.col("revenue") >= cap_min_revenue.value)

    _query = cap_search.value.strip().lower()
    if _query:
        cap_filtered = cap_filtered.filter(
            pl.col("product").str.to_lowercase().str.contains(_query, literal=True)
        )

    print(
        f"Showing {cap_filtered.shape[0]} of {sales.shape[0]} rows | "
        f"Region: {cap_region.value} | Category: {cap_category.value} | "
        f"Min Revenue: ${cap_min_revenue.value:,} | Search: '{cap_search.value}'"
    )
    ```

    **Output:**

    ```
    Simulating control panel: Region=North, Category=All, Min Revenue=$50,000, Search=''

    Showing 12 of 54 rows | Region: North | Category: All | Min Revenue: $50,000 | Search: ''

    First 5 filtered rows (with the computed profit column):
    shape: (5, 6)
    ┌───────┬─────────┬───────┬─────────┬────────┬────────┐
    │ month ┆ product ┆ units ┆ revenue ┆ cost   ┆ profit │
    │ ---   ┆ ---     ┆ ---   ┆ ---     ┆ ---    ┆ ---    │
    │ str   ┆ str     ┆ i64   ┆ i64     ┆ i64    ┆ i64    │
    ╞═══════╪═════════╪═══════╪═════════╪════════╪════════╡
    │ Jan   ┆ Laptop  ┆ 120   ┆ 143880  ┆ 95400  ┆ 48480  │
    │ Feb   ┆ Laptop  ┆ 135   ┆ 161865  ┆ 101250 ┆ 60615  │
    │ Mar   ┆ Laptop  ┆ 150   ┆ 179850  ┆ 112500 ┆ 67350  │
    │ Apr   ┆ Laptop  ┆ 110   ┆ 131890  ┆ 82500  ┆ 49390  │
    │ May   ┆ Laptop  ┆ 165   ┆ 197835  ┆ 123750 ┆ 74085  │
    └───────┴─────────┴───────┴─────────┴────────┴────────┘
    ```

    **Interpretation:** Four widget values funnel through one cell: the region dropdown keeps North, the category dropdown ("All") is skipped, the $50,000 slider removes every Keyboard month (none reaches the floor), and the empty search box is skipped — leaving 12 of 54 rows. The cell also pre-computes a per-row profit column so the dashboard's Data Table tab can be sorted by profitability.

    *Source: `computations/module12_examples.py` — `demo_capstone_filters()`*

The dashboard cell turns `cap_filtered` into four tabs — Overview (revenue and profit bars plus a totals line), Trends (monthly lines whose mode obeys the checkbox), Scatter (units vs. revenue), and Data Table (a selectable `mo.ui.table`):

```python
# --- Capstone: tabbed dashboard (abridged) ---
_by_product = (
    cap_filtered.group_by("product")
    .agg(
        pl.col("revenue").sum().alias("total_revenue"),
        pl.col("units").sum().alias("total_units"),
        pl.col("cost").sum().alias("total_cost"),
    )
    .with_columns((pl.col("total_revenue") - pl.col("total_cost")).alias("profit"))
    .sort("total_revenue", descending=True)
)
# ... px.bar revenue + profit charts, stacked over a totals line ...

_monthly = (
    cap_filtered.group_by("month")
    .agg(
        pl.col("revenue").sum().alias("total_revenue"),
        pl.col("units").sum().alias("total_units"),
    )
    .with_columns(pl.col("month").replace_strict(_month_map).alias("month_num"))
    .sort("month_num")
)
# ... px.line charts; mode="lines+markers" if cap_show_trend.value else "markers" ...

_dashboard = mo.ui.tabs({
    "Overview": _overview,
    "Trends": _trend_tab,
    "Scatter": _scatter_fig,
    "Data Table": mo.ui.table(data=cap_filtered, selection="multi"),
})
_dashboard
```

!!! example "Worked Example: The Overview and Trends Tabs"

    ```python
    # The aggregations behind the Overview and Trends tabs, computed on
    # the filtered data from the capstone filter cell.
    # (the companion script keeps simulating Region="North",
    #  Category="All", Min Revenue=50000, Search="")
    print(_by_product)         # Overview tab bar-chart data

    print(
        f"Total Revenue: ${cap_filtered['revenue'].sum():,} | "
        f"Total Units: {cap_filtered['units'].sum():,} | "
        f"Total Profit: ${(cap_filtered['revenue'].sum() - cap_filtered['cost'].sum()):,}"
    )

    print(_monthly)            # Trends tab line-chart data
    ```

    **Output:**

    ```
    Capstone filters still applied: Region=North, Category=All, Min Revenue=$50,000, Search=''

    Overview tab — revenue and profit by product:
    shape: (2, 5)
    ┌─────────┬───────────────┬─────────────┬────────────┬────────┐
    │ product ┆ total_revenue ┆ total_units ┆ total_cost ┆ profit │
    │ ---     ┆ ---           ┆ ---         ┆ ---        ┆ ---    │
    │ str     ┆ i64           ┆ i64         ┆ i64        ┆ i64    │
    ╞═════════╪═══════════════╪═════════════╪════════════╪════════╡
    │ Laptop  ┆ 1031140       ┆ 860         ┆ 650400     ┆ 380740 │
    │ Monitor ┆ 461340        ┆ 1320        ┆ 277200     ┆ 184140 │
    └─────────┴───────────────┴─────────────┴────────────┴────────┘

    Total Revenue: $1,492,480 | Total Units: 2,180 | Total Profit: $564,880

    Trends tab — monthly totals (the data behind the line charts):
    shape: (6, 3)
    ┌───────┬───────────────┬─────────────┐
    │ month ┆ total_revenue ┆ total_units │
    │ ---   ┆ ---           ┆ ---         │
    │ str   ┆ i64           ┆ i64         │
    ╞═══════╪═══════════════╪═════════════╡
    │ Jan   ┆ 213780        ┆ 320         │
    │ Feb   ┆ 238755        ┆ 355         │
    │ Mar   ┆ 246255        ┆ 340         │
    │ Apr   ┆ 205285        ┆ 320         │
    │ May   ┆ 281715        ┆ 405         │
    │ Jun   ┆ 306690        ┆ 440         │
    └───────┴───────────────┴─────────────┘
    ```

    **Interpretation:** With the capstone filters active, the Overview tab reports $1,492,480 in revenue and $564,880 in profit, with Laptop supplying $380,740 of that profit on far fewer units than Monitor. The Trends tab shows a dip to $205,285 in April followed by a climb to $306,690 in June — the kind of pattern a manager spots in seconds on a line chart. Every number updates the moment any control changes.

    *Source: `computations/module12_examples.py` — `demo_capstone_overview()`*

!!! question "Try It Yourself: Capstone Challenge"

    Using the capstone control panel in the teaching notebook, answer these
    business questions:

    1. **Which region has the highest laptop revenue?** Set Category to
       "Electronics", search for "Laptop", and compare regions.
    2. **Which products exceed $100,000 total revenue in the North?**
       Set Region to "North" and check the Overview tab.
    3. **Is there a growth trend for accessories?** Set Category to
       "Accessories" and look at the Trends tab.
    4. **Which individual product sales are the most profitable?** Go to the
       Data Table tab and click the **profit** column header to sort. Each
       row shows one product's revenue, cost, and profit for a single region
       and month.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "Two cells can read each other's variables if I am careful about order." | Marimo rejects circular dependencies outright — the notebook will not run. Design data to flow one way: widgets, then filters, then aggregation, then visualization. |
| "Each chart cell should re-apply the filters it needs." | Duplicated filter logic drifts: one chart gets updated, another does not, and the dashboard quietly contradicts itself. Centralize filtering in one cell and export a single filtered DataFrame. |
| "Defaults do not matter because users will adjust the widgets anyway." | The first render uses each widget's `value=`. Without sensible defaults, the notebook opens on an empty or misleading view — the worst possible first impression for a tool meant for non-programmers. |

---

## Reflection Questions

1. Explain, in terms of marimo's dependency graph, why a widget must be created and displayed in one cell while its `.value` is read in a different cell. What specifically fails to happen if both occur in the same cell?
2. For each of the following filters, pick the most suitable widget — dropdown, slider, text box, or checkbox — and justify the choice: choosing one of twelve sales districts, hiding discontinued products, setting a maximum shipping cost, and finding customers whose company name contains a word.
3. `mo.ui.table()` displays a DataFrame, but so does simply ending a cell with the DataFrame's name. What does the widget version add, and describe an analysis where row selection genuinely changes what a downstream cell computes.
4. The combined-filters pattern reads every widget's `.value` in a single cell that exports one filtered DataFrame. What can go wrong in a dashboard where each chart applies its own copy of the filter logic instead?
5. You are handing your capstone-style dashboard to a manager who has never used a notebook. Which default widget values would you choose, what would you name the widget labels, and which of the five design patterns protects the manager most from confusing behavior?

---

## Your Assignment

The Module 12 assignment is worth **100 points plus a 10-point bonus**. You complete it in a **marimo notebook (`.py` file)** and submit the file to **Blackboard**. The final reflection section is not graded separately — it counts toward participation. Setup cells in the notebook create every CSV file the tasks read (under `/tmp/`), so you only write the widget and analysis code. Two rules from the notebook's tips deserve repeating before you start: create and display each widget in one cell and read its `.value` in a separate cell, and keep the underscore prefix on cell-scoped temporary variables while widgets and DataFrames returned from a cell go unprefixed.

**Task 1: Dropdown Selection (10 points).** A city library system tracks book checkouts by branch and genre. You build a dropdown of the sorted branch names (defaulting to the first), then in a second cell read its `.value`, filter to the selected branch, total its checkouts, and present the result with `mo.md()`. This is the two-cell dropdown pattern from the dropdown part of §12.2.

**Task 2: Slider Filtering (15 points).** A hospital emergency department logs patient wait times by day and severity. You create a slider that sets a maximum wait-time threshold, filter to visits at or under it, then group the survivors by severity with a count and an average wait, displaying the threshold and matching-row counts. The slider mechanics are §12.2; the grouped summary reuses Module 10's `group_by().agg()`.

**Task 3: Text Search and Checkbox Toggle (15 points).** A real estate agency wants its listings searchable by neighborhood (case-insensitive) with a checkbox that restricts results to properties with a pool. You display both widgets in a row with `mo.hstack()`, apply the two filters in sequence, report the match count, and draw a Plotly Express bar chart of the matching listings. The text and checkbox widgets are §12.2, the two-filter combination follows §12.3, and the chart techniques come from Module 11.

**Task 4: Interactive Table with Chart (15 points).** University enrollment records get aggregated by department, displayed in a multi-select `mo.ui.table()`, and whatever departments the user selects are charted as a grouped bar chart with their average GPA shown via `mo.md()` — including a friendly message when nothing is selected, stacked with `mo.vstack()`. The table-selection pattern is §12.3; the vertical stacking is §12.4.

**Task 5: Combined Filters with Plotly Chart (20 points).** A restaurant chain's orders flow through a three-widget control panel — two dropdowns with an `"All"` option and a minimum-order slider arranged with `mo.hstack()`. One cell applies all three filters and exports the filtered DataFrame; a third cell aggregates by meal type and draws a bar chart with dollar-formatted labels. This is the centralized-filter pattern of §12.3 combined with the chart-plus-widget techniques of §12.4.

**Task 6: Full Interactive Dashboard (25 points).** Weather-station readings for several cities meet a four-widget control panel (city dropdown, metric dropdown, minimum-temperature slider, trend-line checkbox) arranged with `mo.vstack()` and `mo.hstack()`. A filter cell exports the filtered data, and a `mo.ui.tabs()` dashboard presents an Overview bar chart of the selected metric by city, a Trend line chart in month order whose mode obeys the checkbox, and a Data Table tab. This task is the capstone pattern of §12.5 built on the layout tools of §12.4.

**Task 7: Creative Interactive App — Bonus (10 points).** Design your own interactive exploration app: a dataset of at least 10 rows and 4 columns, at least three different widget types, at least one Plotly Express chart that reacts to the widgets, a layout element (`mo.hstack()`, `mo.vstack()`, or `mo.ui.tabs()`), and a `mo.md()` summary that updates with the filter state. The prompt suggests scenarios — a pet adoption tracker, a coffee-shop menu explorer, a playlist analyzer, a travel expense tracker — but any business-flavored idea that exercises every part of this module qualifies.

---

## Chapter Summary

This module turned marimo from a place where you write analyses into a place where others *use* them. The four core widgets each map to a kind of business question: `mo.ui.dropdown()` for categorical choices like region or product line, `mo.ui.slider()` for numeric thresholds like a revenue floor, `mo.ui.text()` for free-text search, and `mo.ui.checkbox()` for on/off toggles. All of them work through one mechanism — create and display the widget in one cell, read its `.value` in another — because marimo's dependency graph re-runs every cell that references a widget the moment its value changes. No callbacks, no manual refreshing.

From there the module scaled up: multiple widgets feeding one centralized filter cell that exports a single filtered DataFrame; `mo.ui.table()` turning a displayed summary into an input, with `table.value` carrying the user's selected rows to downstream charts; and layout helpers — `mo.hstack()`, `mo.vstack()`, `mo.ui.tabs()` — arranging charts, tables, and markdown into dashboard views. Connecting Plotly Express to widget values completed the loop: a dropdown can choose the chart's metric or grouping column, so one chart cell serves many questions.

The capstone tied everything together into a five-widget, four-tab sales explorer, and the design patterns behind it are the durable lesson: data flows one direction (widgets to filters to aggregation to visualization), filter logic lives in exactly one cell, every widget carries a sensible default, and circular dependencies are a design error marimo refuses to run. Those patterns are what separate a notebook that works for you from a tool that works for your organization.

---

## What's Next

You can now build interactive tools over DataFrames you shape with Polars. Module 13 adds a different lever: **DuckDB, SQL-based data analysis**. You will run SQL queries directly against DataFrames and files inside your notebook — combining SQL's declarative "say what you want" style with everything Python offers around it. If you have colleagues who think in SQL (most data teams do), Module 13 is where your Python work and their world meet; and a SQL query feeding a widget-driven marimo dashboard is a natural pairing of the two modules.
