# Module 11: Visualization: Matplotlib & Plotly Express

## Introduction

A table of numbers can answer a question, but a chart can *reveal* one. Visualization turns rows and columns into patterns your eye recognizes instantly — trends going up, outliers standing out, categories compared side by side. In business settings a well-chosen chart often communicates more in five seconds than a spreadsheet can in five minutes. This module covers two complementary Python libraries: **matplotlib**, the foundational plotting library that produces static, publication-quality figures for reports and slide decks, and **Plotly Express**, a high-level library that creates interactive charts you can hover, zoom, and filter — ideal for exploration and dashboards. Both sit at the end of the pipeline you have been building since Module 9: read the data, transform and aggregate it with Polars, then hand a small summary table to the plotting library.

**How this chapter shows chart output.** A printed page cannot host a rendered or interactive figure, so every Worked Example pairs the chart-building code with the *numbers behind the chart*: the aggregated values each bar, line, point, or bin represents, plus a text confirmation of the figure's structure (its title, labels, and bar/line/trace counts). The cited demo script computes and prints exactly those numbers — run it to reproduce every figure in this chapter. In marimo, a figure displays automatically when it is the last expression in a cell, so you never call `plt.show()`.

---

## Learning Objectives

By the end of this module, you should be able to:

1. **Create** common chart types — bar, line, scatter, and histogram — using matplotlib
2. **Customize** charts with titles, labels, colors, legends, gridlines, and annotations
3. **Build** interactive visualizations with Plotly Express
4. **Compose** multi-panel figures using subplots
5. **Convert** Polars DataFrames into the format each plotting library expects
6. **Select** the right chart type for a given data question

---

## 11.1 Getting Started: The Sales Dataset, Figures, and Axes

### The Module Dataset

Every chart in this module draws on one business dataset: six months of sales (January through June) for two regions (North and South) and three products (Laptop, Monitor, Keyboard). Each row records the units sold, revenue earned, and cost incurred for one month-region-product combination. The teaching notebook writes this data to a CSV file and reads it back with `pl.read_csv()` — the same file workflow you practiced in Modules 8 and 9.

!!! example "Worked Example: Loading the Sales Dataset"

    ```python
    import polars as pl
    import matplotlib.pyplot as plt
    import plotly.express as px

    # The setup cell wrote six months of sales data to this CSV
    sales = pl.read_csv("/tmp/m11_sales.csv")

    print(f"Loaded sales data: {sales.shape[0]} rows, {sales.shape[1]} columns")
    print(
        f"Coverage: {sales['month'].n_unique()} months x "
        f"{sales['region'].n_unique()} regions x "
        f"{sales['product'].n_unique()} products"
    )
    sales.head(5)
    ```

    **Output:**

    ```
    Loaded sales data: 36 rows, 7 columns
    Coverage: 6 months x 2 regions x 3 products

    First five rows:
    shape: (5, 7)
    ┌───────┬────────┬─────────┬─────────────┬───────┬─────────┬────────┐
    │ month ┆ region ┆ product ┆ category    ┆ units ┆ revenue ┆ cost   │
    │ ---   ┆ ---    ┆ ---     ┆ ---         ┆ ---   ┆ ---     ┆ ---    │
    │ str   ┆ str    ┆ str     ┆ str         ┆ i64   ┆ i64     ┆ i64    │
    ╞═══════╪════════╪═════════╪═════════════╪═══════╪═════════╪════════╡
    │ Jan   ┆ North  ┆ Laptop  ┆ Electronics ┆ 120   ┆ 143880  ┆ 95400  │
    │ Feb   ┆ North  ┆ Laptop  ┆ Electronics ┆ 135   ┆ 161865  ┆ 101250 │
    │ Mar   ┆ North  ┆ Laptop  ┆ Electronics ┆ 150   ┆ 179850  ┆ 112500 │
    │ Apr   ┆ North  ┆ Laptop  ┆ Electronics ┆ 110   ┆ 131890  ┆ 82500  │
    │ May   ┆ North  ┆ Laptop  ┆ Electronics ┆ 165   ┆ 197835  ┆ 123750 │
    └───────┴────────┴─────────┴─────────────┴───────┴─────────┴────────┘
    ```

    **Interpretation:** The dataset has 36 rows — every combination of 6 months, 2 regions, and 3 products — and 7 columns. Each row is one cell of a sales cube: North sold 120 laptops in Jan for 143880 dollars of revenue against 95400 of cost. Small enough to check by hand, rich enough to answer real portfolio questions.

    *Source: `computations/module11_examples.py` — `demo_sales_dataset()`*

### Figure and Axes

Every matplotlib chart is built from two objects:

- **Figure** — the overall canvas (think of it as the blank page)
- **Axes** — the individual plot area within the figure, where data gets drawn

The recommended way to create both at once is `plt.subplots()`:

```python
fig, ax = plt.subplots()        # one figure containing one plot area
fig, axes = plt.subplots(1, 2)  # one figure containing two plot areas
```

You then call methods on `ax` to add data and formatting — `ax.bar()`, `ax.set_title()`, `ax.set_xlabel()` — while the figure handles canvas-level jobs like saving to a file. Despite the plural name, `plt.subplots()` with no arguments is the standard way to start *every* chart, including single-panel ones.

### Your First Chart

A bar chart takes two parallel sequences — the category labels and the bar heights — and three labeling calls make it presentable.

!!! example "Worked Example: A First Bar Chart — Quarterly Revenue"

    ```python
    categories = ["Q1", "Q2", "Q3", "Q4"]
    revenue = [245000, 312000, 289000, 378000]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(categories, revenue, color="steelblue")
    ax.set_title("Quarterly Revenue")
    ax.set_ylabel("Revenue ($)")
    ax.set_xlabel("Quarter")

    plt.tight_layout()
    fig   # in marimo, ending the cell with the figure displays it
    ```

    **Output:**

    ```
    Data behind the bars:
      Q1: $245,000
      Q2: $312,000
      Q3: $289,000
      Q4: $378,000

    Tallest bar: Q4 ($378,000)
    Figure structure: 4 bars | title='Quarterly Revenue' | xlabel='Quarter' | ylabel='Revenue ($)'
    ```

    **Interpretation:** Four categories become 4 bars, and the tallest — Q4 at $378,000 — is visible at a glance, which is the point of the chart. The three `set_*` calls supply the title and axis labels a reader needs to interpret the bars without asking you what they mean.

    *Source: `computations/module11_examples.py` — `demo_first_bar_chart()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "You must call `plt.show()` to see a chart in marimo." | marimo displays a figure automatically when it is the last expression in a cell. `plt.show()` belongs to plain scripts run from a terminal, not to marimo notebooks. |
| "Figure and axes are the same thing." | The figure is the canvas; the axes is one plot area drawn on it. Data and labels attach to the axes (`ax.set_title()`); canvas-level jobs belong to the figure (`fig.suptitle()`, `fig.savefig()`). |
| "`plt.subplots()` is only for multi-panel figures." | With no arguments it creates one figure with one axes — the recommended starting point for every chart, single-panel included. |

---

## 11.2 The Four Core Chart Types

Four chart types cover most business reporting. Each answers a different kind of question, and choosing among them starts with naming the question you are asking.

| Question | Chart type | Business example |
|----------|-----------|------------------|
| How do categories compare? | Bar chart | Revenue by product |
| How does a value change over time? | Line chart | Monthly sales trend |
| Is there a relationship between X and Y? | Scatter plot | Units sold vs. revenue |
| How is a variable distributed? | Histogram | Order sizes |

### Bar Charts — Comparing Categories

Bar charts answer: **"How do these categories compare?"** — revenue by region, sales by quarter, market share by competitor. Two methods cover both orientations: `ax.bar(x, height)` for vertical bars and `ax.barh(y, width)` for horizontal bars, which work well when category names are long. The workflow is the one from the previous module: aggregate with `group_by().agg()`, sort so the bars tell an ordered story, then extract each column with `.to_list()` for matplotlib. A loop over `ax.text()` adds a value label above each bar so readers get exact figures without leaving the chart.

!!! example "Worked Example: Vertical and Horizontal Bar Charts"

    ```python
    # Vertical bars: total revenue by product, largest first
    by_product = (
        sales
        .group_by("product")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
        .sort("total_revenue", descending=True)
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(
        by_product["product"].to_list(),
        by_product["total_revenue"].to_list(),
        color=["#2196F3", "#4CAF50", "#FF9800"],
    )
    ax.set_title("Total Revenue by Product")
    ax.set_ylabel("Revenue ($)")

    # Value labels on top of each bar
    for i, val in enumerate(by_product["total_revenue"].to_list()):
        ax.text(i, val + 5000, f"${val:,.0f}", ha="center", fontsize=9)

    # Horizontal bars: total revenue by region
    by_region = (
        sales
        .group_by("region")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
        .sort("total_revenue")
    )

    fig2, ax2 = plt.subplots(figsize=(7, 3.5))
    ax2.barh(
        by_region["region"].to_list(),
        by_region["total_revenue"].to_list(),
        color=["#FF7043", "#42A5F5"],
    )
    ax2.set_title("Total Revenue by Region")
    ax2.set_xlabel("Revenue ($)")
    ```

    **Output:**

    ```
    Vertical bar chart -- total revenue by product:
      Laptop     $1,840,465
      Monitor      $835,305
      Keyboard     $376,333
    Largest bar: Laptop ($1,840,465) | Smallest bar: Keyboard ($376,333)

    Horizontal bar chart -- total revenue by region:
      South      $1,346,290
      North      $1,705,813
    North leads South by $359,523
    Figure structure: 3 vertical bars, 2 horizontal bars
    ```

    **Interpretation:** Sorting before plotting makes the story immediate: Laptop revenue ($1,840,465) dwarfs Keyboard revenue ($376,333), a comparison a reader absorbs faster from bar heights than from the numbers alone. The horizontal chart shows North ahead of South by $359,523 — and because `barh` was fed the ascending sort, the longest bar lands on top.

    *Source: `computations/module11_examples.py` — `demo_bar_charts()`*

!!! question "Try It Yourself: Units Sold by Product"

    Modify the bar chart to show **total units sold** by product instead of revenue. Change the bar color to `"#9C27B0"` (purple), and update the title and y-axis label to match.

### Line Charts — Trends Over Time

Line charts answer: **"How does this value change over time?"** — monthly revenue trends, website traffic over weeks, stock price movements. Key methods:

- `ax.plot(x, y)` — basic line
- `ax.plot(x, y, marker="o")` — line with a marker at each data point
- `ax.legend()` — show the legend when plotting multiple lines

**Putting months in calendar order.** There is one catch with time-based charts: month *names* sort alphabetically by default (`Apr, Feb, Jan, Jun…`), which scrambles a time axis. The fix is to tell Polars the order you mean. Casting the column to an ordered category with `pl.Enum` — think of it as a custom sort list — makes `.sort()` follow the calendar instead of the alphabet:

```python
month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
df.with_columns(pl.col("month").cast(pl.Enum(month_order))).sort("month")
```

This module reuses the same pattern every time it charts by month, so the x-axis always reads Jan through Jun.

!!! example "Worked Example: A Monthly Trend Line in Calendar Order"

    ```python
    north = (
        sales
        .filter(pl.col("region") == "North")
        .group_by("month")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
    )

    # Cast to an ordered category so .sort() follows the calendar
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    north_sorted = (
        north
        .with_columns(pl.col("month").cast(pl.Enum(month_order)))
        .sort("month")
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(north_sorted["month"], north_sorted["total_revenue"],
            marker="o", color="#1976D2", linewidth=2)
    ax.set_title("Monthly Revenue — North Region")
    ax.set_ylabel("Revenue ($)")
    ax.set_xlabel("Month")
    ax.grid(axis="y", alpha=0.3)
    ```

    **Output:**

    ```
    Months sorted as plain strings (alphabetical -- scrambles the timeline):
      Apr -> Feb -> Jan -> Jun -> Mar -> May

    Months sorted with pl.Enum (calendar order):
      Jan -> Feb -> Mar -> Apr -> May -> Jun

    Line chart data -- monthly revenue, North region:
      Jan  $245,740
      Feb  $274,710
      Mar  $279,813
      Apr  $235,647
      May  $321,665
      Jun  $348,238
    Lowest month: Apr ($235,647) | Highest month: Jun ($348,238)
    Figure structure: 1 line with 6 points | title='Monthly Revenue — North Region'
    ```

    **Interpretation:** The first two blocks of output show why the cast matters — a plain string sort would plot Apr first and May last, turning a real trend into visual noise. In calendar order the story reads correctly: North climbs from $245,740 in Jan to $348,238 in Jun, with one dip to $235,647 in Apr that a manager would want explained.

    *Source: `computations/module11_examples.py` — `demo_line_calendar_order()`*

Plotting several lines on one axes is a loop: filter the data for each group, call `ax.plot()` with a `label`, and finish with `ax.legend()`. This is the standard pattern for comparing regions, products, or scenarios over the same time axis.

!!! example "Worked Example: Two Regions on One Time Axis"

    ```python
    by_region_month = (
        sales
        .group_by("region", "month")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
        .with_columns(pl.col("month").cast(pl.Enum(month_order)))
        .sort("month")
    )

    fig, ax = plt.subplots(figsize=(8, 4))

    for region, color in [("North", "#1976D2"), ("South", "#E53935")]:
        data = by_region_month.filter(pl.col("region") == region)
        ax.plot(
            data["month"], data["total_revenue"],
            marker="o", color=color, linewidth=2, label=region,
        )

    ax.set_title("Monthly Revenue by Region")
    ax.set_ylabel("Revenue ($)")
    ax.set_xlabel("Month")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    ```

    **Output:**

    ```
    Line chart data -- monthly revenue by region:
      Month       North     South       Gap
      Jan       245,740   184,305    61,435
      Feb       274,710   198,888    75,822
      Mar       279,813   209,780    70,033
      Apr       235,647   225,564    10,083
      May       321,665   255,337    66,328
      Jun       348,238   272,416    75,822

    Jan-to-Jun growth: North $102,498, South $88,111
    Figure structure: 2 lines | legend: North, South
    ```

    **Interpretation:** Two lines on one axes let the eye compare trajectories: both regions grow, North stays on top every month, and North adds $102,498 from Jan to Jun against South's $88,111. The gap column exposes what the chart shows visually — the lines nearly touch in Apr, when North's dip shrinks the gap to $10,083, then separate again.

    *Source: `computations/module11_examples.py` — `demo_line_by_region()`*

!!! question "Try It Yourself: One Line per Product"

    Modify the multi-line chart to compare **products** instead of regions. You should get three lines — one each for Laptop, Monitor, and Keyboard. Hint: loop over the three product names instead of the two regions, and give each its own color and label.

### Scatter Plots — Relationships Between Variables

Scatter plots answer: **"Is there a relationship between X and Y?"** — price vs. demand, marketing spend vs. sales, experience vs. salary. The basic call plots one point per row:

```python
fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(
    sales["units"].to_list(),
    sales["revenue"].to_list(),
    alpha=0.7, color="#7B1FA2", edgecolors="white", s=60,
)
```

The `alpha` (transparency), `edgecolors`, and `s` (marker size) arguments keep overlapping points readable. A single-color cloud shows *whether* a relationship exists; coloring the points by a category shows *why* — each group gets its own `ax.scatter()` call with a `label`, exactly like the multi-line loop above.

!!! example "Worked Example: Units vs. Revenue, Colored by Product"

    ```python
    colors = {"Laptop": "#1976D2", "Monitor": "#4CAF50", "Keyboard": "#FF9800"}

    fig, ax = plt.subplots(figsize=(7, 5))
    for product, color in colors.items():
        subset = sales.filter(pl.col("product") == product)
        ax.scatter(
            subset["units"].to_list(),
            subset["revenue"].to_list(),
            alpha=0.7, color=color, edgecolors="white", s=60, label=product,
        )

    ax.set_title("Units vs. Revenue by Product")
    ax.set_xlabel("Units Sold")
    ax.set_ylabel("Revenue ($)")
    ax.legend()
    ax.grid(alpha=0.3)
    ```

    **Output:**

    ```
    Scatter plot: 36 points (one per month-region-product row)
      Laptop    12 points | units 90-180 | revenue $107,910-$215,820 | price per unit $1,199.00
      Monitor   12 points | units 150-260 | revenue $52,425-$90,870 | price per unit $349.50
      Keyboard  12 points | units 300-520 | revenue $23,970-$41,548 | price per unit $79.90
    Within each product the points climb together: more units sold, more revenue.
    Figure structure: 3 color groups | title='Units vs. Revenue by Product'
    ```

    **Interpretation:** Without color, the 36 points look like one weak overall relationship. Colored by product, the chart resolves into three tight diagonal clusters — each product's points climb along their own line because each has a fixed price per unit ($1,199.00 for laptops down to $79.90 for keyboards). Keyboards sell the most units (up to 520) for the least revenue; laptops are the mirror image. Color turned one confusing cloud into three clean stories.

    *Source: `computations/module11_examples.py` — `demo_scatter_by_product()`*

### Histograms — Distribution of Values

Histograms answer: **"How is this variable distributed?"** — order sizes, salary ranges, customer ages. The key method is `ax.hist(data, bins=N)`: matplotlib divides the value range into `N` equal-width bins and draws one bar per bin showing how many values fall inside it. Unlike a bar chart, you do not choose the categories — the bins *are* computed from the data, and changing `bins` reshapes the chart.

One subtlety arises when overlaying two histograms to compare distributions: each `ax.hist()` call computes bin edges from its own data's min and max. Two calls with `bins=10` produce two *different* grids, and the bars stop lining up on the same intervals — an invalid comparison. The fix is to compute one shared list of edges and pass it to both calls.

!!! example "Worked Example: Revenue Distribution, Then Two Regions Overlaid"

    ```python
    # One histogram of all revenue values
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(sales["revenue"].to_list(), bins=12,
            color="#00897B", edgecolor="white")
    ax.set_title("Distribution of Monthly Revenue Values")
    ax.set_xlabel("Revenue ($)")
    ax.set_ylabel("Frequency")

    # Overlaid histograms need ONE shared set of bin edges
    revenue = sales.filter(pl.col("region").is_in(["North", "South"]))["revenue"]
    low, high = revenue.min(), revenue.max()
    bin_edges = [low + (high - low) * i / 10 for i in range(11)]

    fig2, ax2 = plt.subplots(figsize=(7, 4))
    for region, color in [("North", "#1976D2"), ("South", "#E53935")]:
        data = sales.filter(pl.col("region") == region)["revenue"].to_list()
        ax2.hist(data, bins=bin_edges, alpha=0.5, color=color,
                 edgecolor="white", label=region)

    ax2.set_title("Revenue Distribution by Region")
    ax2.set_xlabel("Revenue ($)")
    ax2.set_ylabel("Frequency")
    ax2.legend()
    ```

    **Output:**

    ```
    Histogram of 36 revenue values in 12 bins:
      $  23,970.0 - $  39,957.5 | 11 ###########
      $  39,957.5 - $  55,945.0 |  3 ###
      $  55,945.0 - $  71,932.5 |  5 #####
      $  71,932.5 - $  87,920.0 |  4 ####
      $  87,920.0 - $ 103,907.5 |  1 #
      $ 103,907.5 - $ 119,895.0 |  2 ##
      $ 119,895.0 - $ 135,882.5 |  2 ##
      $ 135,882.5 - $ 151,870.0 |  2 ##
      $ 151,870.0 - $ 167,857.5 |  2 ##
      $ 167,857.5 - $ 183,845.0 |  2 ##
      $ 183,845.0 - $ 199,832.5 |  1 #
      $ 199,832.5 - $ 215,820.0 |  1 #
    Tallest bin: 11 of the 36 values

    Overlaid histograms -- shared bin edges from $23,970 to $215,820:
      Bin range              North South
      $23,970-$43,155            6     6
      $43,155-$62,340            0     3
      $62,340-$81,525            4     3
      $81,525-$100,710           2     0
      $100,710-$119,895          0     2
      $119,895-$139,080          1     2
      $139,080-$158,265          1     1
      $158,265-$177,450          1     1
      $177,450-$196,635          1     0
      $196,635-$215,820          2     0
    ```

    **Interpretation:** The distribution is right-skewed: 11 of the 36 values crowd into the lowest bin (keyboard revenue), while the long tail to the right is laptop revenue. On the shared grid, the overlaid version shows the regional difference cleanly — only North reaches the top bin ($196,635 and above, with 2 values), because only North's laptop months climb that high. Had each region computed its own bins, none of these bars would be comparable.

    *Source: `computations/module11_examples.py` — `demo_histograms()`*

!!! question "Try It Yourself: Distribution of Units Sold"

    Create a histogram of the `units` column. Experiment with different numbers of bins — try 8, 15, and 20 — and watch how the shape of the distribution changes with the bin count.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "Sorting month names puts them in calendar order." | Strings sort alphabetically: Apr, Feb, Jan… Cast the column to `pl.Enum` with an explicit order list so `.sort()` follows the calendar. The same trick applies to weekday names and size labels like S/M/L. |
| "A histogram is just a bar chart." | A bar chart compares categories you chose; a histogram bins a numeric column to show its distribution. The bins are computed from the data, and changing `bins` changes the chart's shape. |
| "To overlay two histograms, give each one `bins=10`." | Each call would compute its own edges from its own min and max — two different grids whose bars do not line up. Compute one shared list of edges and pass it to both calls. |
| "More data on the chart is always better." | Aggregate with Polars first, then plot the small summary table. Plotting a million raw rows produces an unreadable smear and a slow notebook; a grouped summary produces the answer. |

---

## 11.3 Customization and Multi-Panel Figures

Professional charts need clear labels and thoughtful formatting. The customization toolbox:

| Method | Purpose |
|--------|---------|
| `ax.set_title("...")` | Chart title |
| `ax.set_xlabel("...")` / `ax.set_ylabel("...")` | Axis labels |
| `ax.legend()` | Show the legend |
| `ax.grid(alpha=0.3)` | Light gridlines |
| `ax.annotate("text", xy=(...))` | Add an annotation with an arrow |
| `ax.set_xlim(a, b)` / `ax.set_ylim(a, b)` | Set the axis range |
| `ax.tick_params(labelsize=10)` | Adjust tick label size |
| `fig.suptitle("...")` | Title above all subplots |

### A Polished Grouped Bar Chart

Grouped bars place two series side by side within each category — revenue next to profit for every product. matplotlib does not offset the bars for you: the second series is drawn shifted by the bar width, and the tick positions are then re-centered between each pair.

!!! example "Worked Example: Revenue vs. Profit, Grouped Bars"

    ```python
    by_product = (
        sales
        .group_by("product")
        .agg(
            pl.col("revenue").sum().alias("total_revenue"),
            pl.col("cost").sum().alias("total_cost"),
        )
        .sort("total_revenue", descending=True)
        .with_columns(
            (pl.col("total_revenue") - pl.col("total_cost")).alias("profit"),
        )
    )

    products = by_product["product"].to_list()
    revenue = by_product["total_revenue"].to_list()
    profit = by_product["profit"].to_list()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(products, revenue, color="#1976D2", label="Revenue", width=0.4)
    ax.bar(
        [i + 0.4 for i in range(len(products))],
        profit,
        color="#4CAF50", label="Profit", width=0.4,
    )

    # Re-center the tick labels between each pair of bars
    ax.set_xticks([i + 0.2 for i in range(len(products))])
    ax.set_xticklabels(products)

    ax.set_title("Revenue vs. Profit by Product", fontsize=14, fontweight="bold")
    ax.set_ylabel("Amount ($)", fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    ax.tick_params(labelsize=10)
    ```

    **Output:**

    ```
    Grouped bar chart data -- revenue vs. profit by product:
      Product        Revenue      Profit
      Laptop       1,840,465     683,815
      Monitor        835,305     333,405
      Keyboard       376,333     187,933

    Figure structure: 6 bars (3 products x 2 series) | legend: Revenue, Profit
    Title: 'Revenue vs. Profit by Product'
    ```

    **Interpretation:** Placing profit beside revenue reveals what a revenue-only chart hides: Laptop's bar towers at 1,840,465 in revenue but keeps 683,815 as profit, while Keyboard converts a much larger share of its 376,333 revenue into 187,933 profit. The legend and re-centered tick labels are what make the 6 bars readable as 3 labeled pairs.

    *Source: `computations/module11_examples.py` — `demo_grouped_bar_revenue_profit()`*

### Annotations — Pointing at What Matters

An annotation is text plus an arrow anchored to a data point — the chart equivalent of pointing at the screen during a presentation. `ax.annotate()` takes the text, an `xy` anchor (the data point), an `xytext` position (where the text sits), and `arrowprops` for the arrow. One practical detail: extend the y-axis with `ax.set_ylim(top=...)` before annotating a peak, or the label collides with the top of the chart.

!!! example "Worked Example: Annotating the Peak Month"

    ```python
    monthly = (
        sales
        .group_by("month")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
    )

    vals = []
    for m in month_order:
        row = monthly.filter(pl.col("month") == m)
        vals.append(row["total_revenue"][0])

    max_idx = vals.index(max(vals))

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(month_order, vals, marker="o", color="#1976D2", linewidth=2)

    # Headroom so the label sits above the peak but inside the chart
    ax.set_ylim(top=max(vals) * 1.15)

    ax.annotate(
        f"Peak: ${vals[max_idx]:,.0f}",
        xy=(max_idx, vals[max_idx]),
        xytext=(max_idx - 1.5, vals[max_idx] + 15000),
        arrowprops=dict(arrowstyle="->", color="#E53935"),
        fontsize=11, color="#E53935", fontweight="bold",
    )

    ax.set_title("Monthly Revenue with Peak Annotated")
    ax.set_ylabel("Revenue ($)")
    ax.grid(axis="y", alpha=0.3)
    ```

    **Output:**

    ```
    Monthly total revenue (all regions, all products):
      Jan  $430,045
      Feb  $473,598
      Mar  $489,593
      Apr  $461,211
      May  $577,002
      Jun  $620,654

    Peak month: Jun
    Annotation drawn on the chart: 'Peak: $620,654'
    y-axis top extended to $713,752 to make room for the label
    ```

    **Interpretation:** The code finds the peak instead of hard-coding it — `vals.index(max(vals))` locates Jun at $620,654, so the annotation stays correct if the data changes. Extending the y-axis top to $713,752 gives the label room above the peak; without that call the text would sit against the chart's upper edge.

    *Source: `computations/module11_examples.py` — `demo_annotate_peak()`*

### Subplots — Multi-Panel Figures

Subplots place multiple related charts in a single figure — the format of every business review dashboard. `plt.subplots(nrows, ncols)` returns the figure and an *array* of axes:

```python
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
axes[0].bar(...)    # left panel   (1-D indexing for a single row)
axes[1].plot(...)   # right panel

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
axes[0, 0].bar(...)     # top-left   (2-D indexing for a grid)
axes[0, 1].plot(...)    # top-right
axes[1, 0].hist(...)    # bottom-left
axes[1, 1].scatter(...) # bottom-right
```

Note the indexing difference: a single row gives a one-dimensional array (`axes[0]`), while a grid gives a two-dimensional one (`axes[0, 0]`). Each element is a full axes object supporting every method from the sections above.

!!! example "Worked Example: A 2x2 Grid — Four Views of the Same Data"

    ```python
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

    # Top-left: revenue by product (bar)
    by_prod = sales.group_by("product").agg(pl.col("revenue").sum()).sort("product")
    axes[0, 0].bar(by_prod["product"].to_list(), by_prod["revenue"].to_list(),
                   color=["#1976D2", "#4CAF50", "#FF9800"])
    axes[0, 0].set_title("Revenue by Product")

    # Top-right: monthly trend (line)
    monthly = sales.group_by("month").agg(pl.col("revenue").sum())
    vals = []
    for m in month_order:
        row = monthly.filter(pl.col("month") == m)
        vals.append(row["revenue"][0])
    axes[0, 1].plot(month_order, vals, marker="o", color="#1976D2")
    axes[0, 1].set_title("Monthly Revenue Trend")

    # Bottom-left: revenue distribution (histogram)
    axes[1, 0].hist(sales["revenue"].to_list(), bins=12,
                    color="#00897B", edgecolor="white")
    axes[1, 0].set_title("Revenue Distribution")

    # Bottom-right: units vs. revenue (scatter), one color per product
    product_colors = {"Keyboard": "#1976D2", "Laptop": "#4CAF50", "Monitor": "#FF9800"}
    for product, color in product_colors.items():
        subset = sales.filter(pl.col("product") == product)
        axes[1, 1].scatter(subset["units"].to_list(), subset["revenue"].to_list(),
                           alpha=0.7, color=color, edgecolors="white", label=product)
    axes[1, 1].set_title("Units vs. Revenue by Product")
    axes[1, 1].legend(fontsize=8)

    fig.suptitle("Sales Data — Four Perspectives", fontsize=14, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    ```

    **Output:**

    ```
    Figure: 2x2 subplot grid — 'Sales Data — Four Perspectives'
      Panel [0, 0] Revenue by Product (bar): Keyboard $376,333 | Laptop $1,840,465 | Monitor $835,305
      Panel [0, 1] Monthly Revenue Trend (line): Jan $430,045 rising to Jun $620,654
      Panel [1, 0] Revenue Distribution (histogram): 36 values in 12 bins, tallest bin 11
      Panel [1, 1] Units vs. Revenue by Product (scatter): 36 points in 3 color groups
    ```

    **Interpretation:** One figure now answers four questions at once — category comparison, time trend, distribution, and relationship — using all four chart types from the previous section. `fig.suptitle()` names the whole exhibit, and the `rect` argument to `tight_layout` reserves the top strip so panels do not collide with that title.

    *Source: `computations/module11_examples.py` — `demo_subplot_grid()`*

!!! question "Try It Yourself: A 1x3 Regional Comparison"

    Create a 1x3 subplot (three charts in a row) showing: (1) a bar chart of total revenue by region, (2) a bar chart of total units by region, and (3) a bar chart of total profit (revenue minus cost) by region. Hint: `plt.subplots(nrows=1, ncols=3, figsize=(15, 4))` — and remember that a single row means one-dimensional indexing.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "`axes[0, 0]` works for every subplot layout." | `plt.subplots(1, 2)` returns a 1-D array indexed `axes[0]`, `axes[1]`; only true grids like `(2, 2)` return a 2-D array indexed `axes[0, 0]`. Mixing them up raises an `IndexError`. |
| "matplotlib offsets grouped bars automatically." | Both series draw at the same x positions unless you shift one by the bar width yourself — and then re-center the tick labels between the pairs. |
| "`tight_layout()` is optional polish." | Without it, axis labels and titles routinely clip or overlap, especially in multi-panel figures. With a `suptitle`, pass `rect` so the top strip stays reserved for it. |
| "An annotation is just text placed on the chart." | `ax.annotate()` anchors text to a *data point* (`xy`) with separate text placement (`xytext`) and an arrow — and computing the anchor from the data keeps it correct when the data changes. |

---

## 11.4 Plotly Express and the Polars-to-Visualization Workflow

### Interactive Charts in One Function Call

Plotly Express creates charts you can **hover over**, **zoom into**, and **pan across**. The API is concise — most charts are a single function call naming a DataFrame and its columns. Plotly Express works with pandas DataFrames, so with Polars you convert using `.to_pandas()`. (Recent Plotly versions also accept Polars DataFrames directly, but `.to_pandas()` is the most reliable approach.)

Where matplotlib asks you to loop over groups and assign colors, Plotly Express does the grouping itself: `color="region"` splits the data into one trace per region, colors them, and builds the legend — one argument replacing the whole loop.

!!! example "Worked Example: An Interactive Grouped Bar Chart"

    ```python
    summary = (
        sales
        .group_by("product", "region")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
        .sort("total_revenue", descending=True)
    )

    fig = px.bar(
        summary.to_pandas(),      # Plotly Express works with pandas DataFrames
        x="product",
        y="total_revenue",
        color="region",
        barmode="group",
        title="Revenue by Product and Region",
        labels={"total_revenue": "Revenue ($)", "product": "Product"},
    )
    fig
    ```

    **Output:**

    ```
    Aggregated data handed to px.bar():
    shape: (6, 3)
    ┌──────────┬────────┬───────────────┐
    │ product  ┆ region ┆ total_revenue │
    │ ---      ┆ ---    ┆ ---           │
    │ str      ┆ str    ┆ i64           │
    ╞══════════╪════════╪═══════════════╡
    │ Laptop   ┆ North  ┆ 1031140       │
    │ Laptop   ┆ South  ┆ 809325        │
    │ Monitor  ┆ North  ┆ 461340        │
    │ Monitor  ┆ South  ┆ 373965        │
    │ Keyboard ┆ North  ┆ 213333        │
    │ Keyboard ┆ South  ┆ 163000        │
    └──────────┴────────┴───────────────┘

    Figure structure: 2 traces (one per region): North, South
    Bar mode: group | Title: 'Revenue by Product and Region'
    Tallest bar: Laptop / North ($1,031,140)
    ```

    **Interpretation:** One function call turned a 6-row summary into a grouped, colored, legended chart — `color="region"` produced the 2 traces that the matplotlib version needed a loop and manual offsets to build. In the browser, hovering any bar shows its exact value; the tallest is Laptop in the North at $1,031,140. The `labels` dictionary renames raw column names into presentation-ready axis titles.

    *Source: `computations/module11_examples.py` — `demo_plotly_bar()`*

The same one-call pattern covers the other core chart types. A line chart by region reuses the `pl.Enum` calendar-ordering pattern before the handoff, and a histogram overlays regions with `barmode="overlay"`:

```python
fig = px.line(
    monthly_sorted.to_pandas(),
    x="month", y="total_revenue", color="region", markers=True,
    title="Monthly Revenue Trend by Region",
)

fig = px.histogram(
    sales.to_pandas(),
    x="revenue", nbins=15, color="region",
    barmode="overlay", opacity=0.7,
    title="Revenue Distribution by Region",
)
```

Scatter plots are where interactivity pays off most: `size=` maps a third column to bubble area, and `hover_data=` decides which extra columns appear in the tooltip — so each point can identify itself.

!!! example "Worked Example: An Interactive Bubble Scatter"

    ```python
    fig = px.scatter(
        sales.to_pandas(),
        x="units",
        y="revenue",
        color="product",
        size="cost",
        hover_data=["month", "region"],
        title="Units vs. Revenue (bubble size = cost)",
        labels={"units": "Units Sold", "revenue": "Revenue ($)"},
    )
    fig
    ```

    **Output:**

    ```
    px.scatter() input: 36 rows -- x=units, y=revenue, color=product, size=cost
    Traces: 3 (Laptop, Monitor, Keyboard)
    Bubble size spans cost $12,000 (Keyboard, South, Jan) to $135,000 (Laptop, North, Jun)
    Hover shows: month, region (plus x, y, color, and size values)
    Title: 'Units vs. Revenue (bubble size = cost)'
    ```

    **Interpretation:** This one chart encodes four columns: position (units and revenue), color (product, as 3 traces), and bubble area (cost, spanning $12,000 to $135,000). The hover tooltip answers the follow-up question a static chart cannot — "which point is that?" — by naming the month and region of any bubble you touch.

    *Source: `computations/module11_examples.py` — `demo_plotly_scatter()`*

!!! question "Try It Yourself: An Interactive Scatter by Region"

    Create a Plotly Express scatter plot of `units` (x) vs. `revenue` (y), colored by `region`, with `product` shown in the hover data. Add a meaningful title and axis labels via the `labels` dictionary.

### Plotly vs. Matplotlib: When to Use Each

| Criteria | matplotlib | Plotly Express |
|----------|-----------|----------------|
| **Output** | Static images (PNG, PDF, SVG) | Interactive HTML |
| **Best for** | Reports, publications, slides | Exploration, dashboards |
| **Customization** | Fine-grained control | Quick, opinionated defaults |
| **Interactivity** | None (static) | Hover, zoom, pan, filter |
| **File size** | Small (image) | Larger (bundles JavaScript) |
| **Learning curve** | Steeper | Gentler |

**Rule of thumb:** use matplotlib when you need a polished static figure for a report or slide deck; use Plotly Express when you want to explore data interactively or build dashboards.

### The Polars-to-Visualization Workflow

Each library needs data in a format it understands:

- **matplotlib** works with Python lists (or NumPy arrays) — extract columns with `.to_list()`:

    ```python
    ax.bar(df["product"].to_list(), df["revenue"].to_list())
    ```

- **Plotly Express** works with pandas DataFrames — convert with `.to_pandas()`:

    ```python
    px.bar(df.to_pandas(), x="product", y="revenue")
    ```

The pattern in both cases: **aggregate with Polars first**, then hand a small summary DataFrame to the plotting library. Never plot raw data with millions of rows — summarize, then visualize.

### Chart Selection Framework

| Data question | Chart type | Example |
|---------------|-----------|---------|
| How do categories compare? | **Bar chart** | Revenue by product |
| How does a value change over time? | **Line chart** | Monthly sales trend |
| Is there a relationship between X and Y? | **Scatter plot** | Price vs. demand |
| How is a variable distributed? | **Histogram** | Salary distribution |
| What is the composition of a whole? | **Pie / stacked bar** | Market share |
| How do two distributions compare? | **Overlaid histograms / box plot** | Revenue by region |

When in doubt, start with a bar chart (for categories) or a line chart (for time series) — these cover most business reporting needs.

### Saving and Exporting Figures

matplotlib exports with `savefig()`; Plotly exports with `write_html()` (interactive) or `write_image()` (static, requires the kaleido package):

```python
fig.savefig("chart.png", dpi=150, bbox_inches="tight")  # matplotlib
fig.savefig("chart.pdf")                                # vector, for print

fig.write_html("chart.html")   # Plotly: stays interactive in a browser
fig.write_image("chart.png")   # Plotly: static snapshot
```

For business reports, export matplotlib as PDF or PNG. For dashboards or email, export Plotly as HTML so recipients keep the hover-and-zoom behavior.

!!! example "Worked Example: Saving a Chart to PNG"

    ```python
    by_product = (
        sales
        .group_by("product")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
        .sort("total_revenue", descending=True)
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(by_product["product"].to_list(),
           by_product["total_revenue"].to_list(),
           color="#1976D2")
    ax.set_title("Revenue by Product")
    ax.set_ylabel("Revenue ($)")
    plt.tight_layout()

    fig.savefig("revenue_by_product.png", dpi=150, bbox_inches="tight")
    print("Saved chart to revenue_by_product.png")
    ```

    **Output:**

    ```
    Saved chart to revenue_by_product.png (dpi=150, bbox_inches='tight')
    File exists: True
    Chart saved with 3 bars and title 'Revenue by Product'
    ```

    **Interpretation:** `dpi=150` controls resolution — higher for print, lower for screens — and `bbox_inches="tight"` trims surplus whitespace around the figure. The confirmation check shows the file landed on disk, ready to drop into a slide deck.

    *Source: `computations/module11_examples.py` — `demo_save_figure()`*

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "Both libraries take a Polars DataFrame the same way." | matplotlib wants plain lists — extract with `.to_list()`. Plotly Express wants a pandas DataFrame — convert with `.to_pandas()`. Mixing these up is the most common Module 11 error. |
| "Interactive charts are always better." | Interactivity dies in print and PDF, and HTML exports are heavier files. Static matplotlib figures remain the standard for reports and slides; Plotly wins for exploration and dashboards. |
| "Exporting a Plotly chart to PNG keeps the hover behavior." | Only `write_html()` preserves interactivity. `write_image()` produces a frozen snapshot (and needs the kaleido package installed). |
| "Plotly needs a loop to color by group like matplotlib does." | The `color=` argument does the grouping, coloring, and legend in one step — one trace per category, no loop. |

---

## 11.5 Capstone: A Multi-Chart Business Dashboard

The capstone brings everything together: a dashboard built from the sales data using both matplotlib (static panels for the meeting deck) and Plotly (interactive views for exploration). The business question: **"How is our product portfolio performing across regions, and what trends should we act on?"**

### Step 1: Prepare the Summary Tables

A dashboard is only as good as the tables behind it. Three Polars summaries feed every panel: a monthly view, a per-product view with profit margin, and a region-by-product view. This is the aggregate-first workflow — all computation happens in Polars before any chart is drawn.

!!! example "Worked Example: The Capstone Summary Tables"

    ```python
    monthly_summary = (
        sales
        .group_by("month")
        .agg(
            pl.col("revenue").sum().alias("total_revenue"),
            pl.col("cost").sum().alias("total_cost"),
            pl.col("units").sum().alias("total_units"),
        )
        .with_columns(
            (pl.col("total_revenue") - pl.col("total_cost")).alias("profit"),
        )
    )

    product_summary = (
        sales
        .group_by("product")
        .agg(
            pl.col("revenue").sum().alias("total_revenue"),
            pl.col("cost").sum().alias("total_cost"),
            pl.col("units").sum().alias("total_units"),
        )
        .with_columns(
            (pl.col("total_revenue") - pl.col("total_cost")).alias("profit"),
            ((pl.col("total_revenue") - pl.col("total_cost"))
             / pl.col("total_revenue") * 100).round(1).alias("margin_pct"),
        )
        .sort("total_revenue", descending=True)
    )

    region_product = (
        sales
        .group_by("region", "product")
        .agg(
            pl.col("revenue").sum().alias("total_revenue"),
            pl.col("units").sum().alias("total_units"),
        )
    )

    print("Capstone data prepared:")
    print(f"  monthly_summary:  {monthly_summary.shape}")
    print(f"  product_summary:  {product_summary.shape}")
    print(f"  region_product:   {region_product.shape}")
    print(product_summary)
    ```

    **Output:**

    ```
    Capstone data prepared:
      monthly_summary:  (6, 5)
      product_summary:  (3, 6)
      region_product:   (6, 4)

    product_summary (the dashboard's main source table):
    shape: (3, 6)
    ┌──────────┬───────────────┬────────────┬─────────────┬────────┬────────────┐
    │ product  ┆ total_revenue ┆ total_cost ┆ total_units ┆ profit ┆ margin_pct │
    │ ---      ┆ ---           ┆ ---        ┆ ---         ┆ ---    ┆ ---        │
    │ str      ┆ i64           ┆ i64        ┆ i64         ┆ i64    ┆ f64        │
    ╞══════════╪═══════════════╪════════════╪═════════════╪════════╪════════════╡
    │ Laptop   ┆ 1840465       ┆ 1156650    ┆ 1535        ┆ 683815 ┆ 37.2       │
    │ Monitor  ┆ 835305        ┆ 501900     ┆ 2390        ┆ 333405 ┆ 39.9       │
    │ Keyboard ┆ 376333        ┆ 188400     ┆ 4710        ┆ 187933 ┆ 49.9       │
    └──────────┴───────────────┴────────────┴─────────────┴────────┴────────────┘
    ```

    **Interpretation:** Thirty-six raw rows reduce to three small tables — the monthly view is (6, 5), the product view (3, 6), and the region-product view (6, 4). The product table already contains the dashboard's headline finding: Laptop earns the most revenue at a 37.2% margin, while Keyboard earns the least revenue at the best margin, 49.9%.

    *Source: `computations/module11_examples.py` — `demo_capstone_summaries()`*

### Step 2: The Static Dashboard (matplotlib)

Four panels in a 2x2 grid, each answering one facet of the portfolio question: revenue vs. profit by product, the monthly trend of both, profit margins with a conditional color rule, and unit volumes.

!!! example "Worked Example: The 2x2 Portfolio Dashboard"

    ```python
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(13, 9))

    # Panel 1: revenue and profit by product (grouped bar)
    products = product_summary["product"].to_list()
    rev = product_summary["total_revenue"].to_list()
    profit = product_summary["profit"].to_list()
    x = range(len(products))
    axes[0, 0].bar([i - 0.2 for i in x], rev, width=0.4,
                   label="Revenue", color="#1976D2")
    axes[0, 0].bar([i + 0.2 for i in x], profit, width=0.4,
                   label="Profit", color="#4CAF50")
    axes[0, 0].set_xticks(list(x))
    axes[0, 0].set_xticklabels(products)
    axes[0, 0].set_title("Revenue vs. Profit by Product")
    axes[0, 0].legend()

    # Panel 2: monthly revenue and profit trend (two lines)
    rev_vals, profit_vals = [], []
    for m in month_order:
        row = monthly_summary.filter(pl.col("month") == m)
        rev_vals.append(row["total_revenue"][0])
        profit_vals.append(row["profit"][0])
    axes[0, 1].plot(month_order, rev_vals, marker="o",
                    color="#1976D2", linewidth=2, label="Revenue")
    axes[0, 1].plot(month_order, profit_vals, marker="s",
                    color="#4CAF50", linewidth=2, label="Profit")
    axes[0, 1].set_title("Monthly Revenue & Profit Trend")
    axes[0, 1].legend()

    # Panel 3: profit margin by product (horizontal bar, conditional color)
    margins = product_summary["margin_pct"].to_list()
    colors = ["#4CAF50" if m > 30 else "#FF9800" for m in margins]
    axes[1, 0].barh(products, margins, color=colors)
    axes[1, 0].set_title("Profit Margin by Product")
    for i, val in enumerate(margins):
        axes[1, 0].text(val + 0.5, i, f"{val}%", va="center", fontsize=10)

    # Panel 4: units sold by product (bar)
    units = product_summary["total_units"].to_list()
    axes[1, 1].bar(products, units, color=["#1976D2", "#4CAF50", "#FF9800"])
    axes[1, 1].set_title("Total Units Sold by Product")

    fig.suptitle("Product Portfolio Performance Dashboard",
                 fontsize=15, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    ```

    **Output:**

    ```
    Dashboard: 'Product Portfolio Performance Dashboard' -- 2x2 panels

    Panel 1 -- Revenue vs. Profit by Product (grouped bars):
      Laptop     revenue $1,840,465   profit $683,815
      Monitor    revenue   $835,305   profit $333,405
      Keyboard   revenue   $376,333   profit $187,933

    Panel 2 -- Monthly Revenue & Profit Trend (lines):
      Jan  revenue $430,045   profit $165,645
      Feb  revenue $473,598   profit $188,398
      Mar  revenue $489,593   profit $194,043
      Apr  revenue $461,211   profit $182,961
      May  revenue $577,002   profit $228,552
      Jun  revenue $620,654   profit $245,554

    Panel 3 -- Profit Margin by Product (horizontal bars, labels drawn on chart):
      Laptop     37.2%  (green -- margin above the 30% threshold)
      Monitor    39.9%  (green -- margin above the 30% threshold)
      Keyboard   49.9%  (green -- margin above the 30% threshold)

    Panel 4 -- Total Units Sold by Product (bars):
      Laptop     1,535 units
      Monitor    2,390 units
      Keyboard   4,710 units
    ```

    **Interpretation:** The four panels answer the portfolio question from four angles. Revenue peaks in Jun at $620,654 with profit following at $245,554; every product clears the 30% margin threshold, so all margin bars render green under the conditional color rule; and the volume panel completes the picture — Keyboard moves 4,710 units, the most of any product, while earning the least revenue at the best margin (49.9%). That combination — high volume, low ticket, strong margin — is the kind of insight a dashboard exists to surface.

    *Source: `computations/module11_examples.py` — `demo_capstone_dashboard()`*

### Step 3: The Interactive Views (Plotly)

The static dashboard goes in the deck; the interactive versions answer the follow-up questions in the meeting. The grouped bar adds on-bar dollar labels through `texttemplate`, and the scatter uses `facet_col` to split into one panel per region so the two markets can be compared point for point.

!!! example "Worked Example: Interactive Dashboard Views with Labels and Facets"

    ```python
    # Interactive grouped bar with dollar labels on every bar
    bar_fig = px.bar(
        region_product.sort("product").to_pandas(),
        x="product",
        y="total_revenue",
        color="region",
        barmode="group",
        title="Interactive: Revenue by Product and Region",
        labels={"total_revenue": "Revenue ($)", "product": "Product",
                "region": "Region"},
        text="total_revenue",
    )
    bar_fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    bar_fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")

    # Faceted scatter: one panel per region, bubble size = profit
    detail = sales.with_columns(
        (pl.col("revenue") - pl.col("cost")).alias("profit"),
    )
    scatter_fig = px.scatter(
        detail.to_pandas(),
        x="units",
        y="revenue",
        color="product",
        size="profit",
        facet_col="region",
        hover_data=["month", "cost", "profit"],
        title="Units vs. Revenue by Region (bubble size = profit)",
        labels={"units": "Units Sold", "revenue": "Revenue ($)"},
    )
    ```

    **Output:**

    ```
    Interactive bar chart -- region_product data:
    shape: (6, 4)
    ┌────────┬──────────┬───────────────┬─────────────┐
    │ region ┆ product  ┆ total_revenue ┆ total_units │
    │ ---    ┆ ---      ┆ ---           ┆ ---         │
    │ str    ┆ str      ┆ i64           ┆ i64         │
    ╞════════╪══════════╪═══════════════╪═════════════╡
    │ North  ┆ Keyboard ┆ 213333        ┆ 2670        │
    │ South  ┆ Keyboard ┆ 163000        ┆ 2040        │
    │ North  ┆ Laptop   ┆ 1031140       ┆ 860         │
    │ South  ┆ Laptop   ┆ 809325        ┆ 675         │
    │ North  ┆ Monitor  ┆ 461340        ┆ 1320        │
    │ South  ┆ Monitor  ┆ 373965        ┆ 1070        │
    └────────┴──────────┴───────────────┴─────────────┘

    Bar chart: 2 traces | barmode: group | Title: 'Interactive: Revenue by Product and Region'
    Each bar carries a dollar label via texttemplate

    Faceted scatter: 36 points, 18 per region facet | 6 traces (3 products x 2 region facets)
    Bubble size = profit, from $11,970 (Keyboard, South, Jan) to $80,820 (Laptop, North, Jun)
    Title: 'Units vs. Revenue by Region (bubble size = profit)'
    ```

    **Interpretation:** `text=` plus `texttemplate` prints a formatted dollar value on every bar, so the exact figures travel with the chart even in a screenshot. In the faceted scatter, `facet_col="region"` splits the 36 points into two panels of 18, producing 6 traces (3 products x 2 region facets); bubble area maps profit, from $11,970 on the smallest bubble to $80,820 on the largest. North's panel visibly carries the bigger bubbles — the profit story told spatially.

    *Source: `computations/module11_examples.py` — `demo_capstone_interactive()`*

!!! question "Try It Yourself: Capstone Challenge — Which Region Is Growing Faster?"

    Create your own 2-panel figure (1 row, 2 columns) that answers this business question: **"Which region is growing faster?"**

    - Left panel: line chart of monthly revenue for each region
    - Right panel: line chart of monthly units for each region

    Use different colors for North and South, add legends and titles, and remember the calendar-ordering pattern so both x-axes read Jan through Jun.

---

## Reflection Questions

1. You need to deliver the same analysis twice: once as a printed quarterly report for the board, once as a tool the sales team can explore on their laptops. Which library do you reach for in each case, and what specifically about each output format drives the choice?
2. The module insists on "aggregate first, then visualize." What goes wrong — technically and visually — if you hand a plotting library a million raw transaction rows instead of a grouped summary?
3. Month names sorted alphabetically put April first and May last. Explain why this happens, how the `pl.Enum` pattern fixes it, and name two other columns in business data that would suffer the same problem.
4. matplotlib takes column data via `.to_list()` while Plotly Express takes a whole DataFrame via `.to_pandas()`. What does this difference tell you about the level each library operates at — and which style do you find less error-prone?
5. For each question, name the chart type you would use and why: "How did weekly sign-ups change this year?", "Which of our five stores sells the most?", "Do larger discounts produce larger orders?", "What does a typical invoice amount look like?"
6. A colleague proposes replacing your four-panel dashboard with four separate one-chart emails. What is gained and lost by keeping the panels together in a single figure?

---

## Your Assignment

The Module 11 assignment is worth **100 points plus a 10-point bonus**. You complete it in a **marimo notebook (`.py` file)** and submit the file to **Brightspace**. The final reflection section is not graded separately — it counts toward participation. Setup cells in the notebook create every CSV file the tasks read (under `/tmp/`), so you only write the analysis and charting code. Three module rules apply throughout: matplotlib needs Python lists (`.to_list()`), Plotly Express needs pandas DataFrames (`.to_pandas()`), and in every case you aggregate with Polars before plotting.

**Task 1: Simple Bar Chart (10 points).** A city parks department tracks average monthly visitors at its five community parks. You read the CSV and build a vertical matplotlib bar chart of visitors by park in a specified green color, with a title and both axis labels, finished with `plt.tight_layout()`. This is the §11.1 chart-building recipe applied with the §11.2 bar-chart pattern.

**Task 2: Line Chart with Customization (15 points).** A weather station recorded average monthly temperatures for two cities across six months. You draw one line per city with specified colors, markers, and line width, then add the full customization set — a sized title, axis labels, a legend naming the cities, and a light y-axis grid. The multi-line loop and month handling are §11.2; the styling calls come from §11.3.

**Task 3: Scatter Plot and Histogram (15 points).** A restaurant review site collected meal prices and customer ratings. Part A is a styled scatter plot of price against rating (color, marker size, edge color, transparency, and grid all specified); Part B is a separate figure containing a histogram of the ratings with a specified bin count. Both chart types are covered in §11.2 — note that the task requires two distinct figures, not two panels.

**Task 4: Plotly Express Interactive Charts (15 points).** An app store dataset tracks downloads, ratings, and file sizes by category. Part A: aggregate downloads by category with Polars, sort, and build an interactive `px.bar` colored by category with relabeled axes. Part B: an interactive `px.scatter` of downloads against rating on the full dataset, colored by category, sized by file size, with the app name added to the hover data. The one-call Plotly patterns and the `labels` dictionary are in §11.4.

**Task 5: Subplots — Multi-Panel Figure (20 points).** A fitness tracker dataset records workouts over six months. You build a 2x2 subplot figure: a bar chart of total calories by workout type (sorted, multi-colored), a line chart of total monthly duration in calendar order, a histogram of calories per session, and a scatter of duration against calories — topped with a bold super-title. The grid indexing and `suptitle` mechanics are §11.3; each individual panel is a §11.2 chart type.

**Task 6: Full Visualization Dashboard Challenge (25 points).** A movie studio wants a visual report on its recent releases (budgets, box office, critic and audience scores, genres). Part A is a matplotlib 2x2 dashboard: grouped side-by-side bars of average critic versus audience scores by genre, a budget-versus-box-office scatter, horizontal bars of the top five films by return on investment with a conditional color rule for positive versus negative ROI, and a box-office histogram — all under a super-title. Part B is an interactive Plotly scatter of budget against box office, colored by genre, sized by critic score, with the film title and audience score in the hover data. This task combines §11.3 (grouped bars, conditional colors, subplots), §11.4 (Plotly), and the dashboard thinking of §11.5.

**Task 7: Creative Exercise — Bonus (10 points).** Design a visualization that tells a story with data of your own invention — a coffee shop menu, a music playlist, a travel log, a pet adoption ledger, or any scenario you like. Requirements: a DataFrame of at least eight rows and four columns, at least two different chart types, at least one matplotlib chart and one Plotly Express chart, customization on every chart (titles, axis labels, colors, plus at least one annotation, legend, or grid), and formatted print output explaining what your visualization reveals.

---

## Chapter Summary

This module turned the summary tables you learned to build in Module 10 into charts a decision-maker can read in seconds. In matplotlib, every figure starts with `fig, ax = plt.subplots()`, and four chart types answer four kinds of questions: bar charts compare categories, line charts track values over time, scatter plots expose relationships between two variables, and histograms reveal how one variable is distributed. Along the way you picked up the defensive habits that separate working charts from misleading ones — casting month names to `pl.Enum` so time axes follow the calendar, and computing shared bin edges before overlaying histograms.

Customization is what makes a chart presentable: `set_title()`, axis labels, legends, light gridlines, and `annotate()` for pointing an arrow at the number that matters. Subplots compose several charts into one figure — `plt.subplots(nrows, ncols)` returns an array of axes, one-dimensional for a row, two-dimensional for a grid — and `fig.suptitle()` names the whole exhibit. Plotly Express reaches the same chart types through single function calls where `color=` replaces the grouping loop, and adds what static figures cannot: hover tooltips, zooming, bubble sizing, and facets.

The bridge between Polars and both libraries is a workflow, not a function: aggregate first, then visualize. matplotlib takes lists via `.to_list()`; Plotly Express takes a DataFrame via `.to_pandas()`. Chart selection starts from the data question, exporting is `savefig()` for static images and `write_html()` for interactive pages, and the capstone assembled all of it — three Polars summary tables feeding a 2x2 static dashboard plus labeled and faceted interactive views — into the kind of portfolio review you would present to management.

---

## What's Next

Your charts so far are fixed the moment the cell runs — changing the region or the month range means editing code. In Module 12 you will learn **Marimo Interactive Features**: sliders, dropdowns, and other reactive UI elements that let a user drive your analysis without touching the code. Because marimo re-runs dependent cells automatically, a dropdown wired to a Polars filter and a chart becomes a live dashboard — the visualizations you built in this module are exactly what those widgets will control.
