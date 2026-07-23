"""Module 11 computation examples: Visualization with Matplotlib & Plotly Express.

Every demo function below backs one Worked Example in the Module 11 chapter of
the MIS 501 Course Companion. The chapter pastes each function's stdout
verbatim, so do not edit outputs by hand -- rerun this script instead.

Module 11 demos do NOT render figures on screen. Each demo builds the same
data its chart draws, constructs the figure headlessly (Agg backend), and
prints the numbers behind the chart -- aggregations, extremes, counts -- plus
a text confirmation of the figure's structure (titles, labels, bar/trace
counts). In the marimo teaching notebook a figure displays automatically when
it is the last expression in a cell, so neither the notebook nor these demos
ever call plt.show().

References in Course Companion:
    demo_sales_dataset()              -> Module 11, Section 11.1 (Getting Started: The Sales Dataset, Figures, and Axes)
    demo_first_bar_chart()            -> Module 11, Section 11.1 (Getting Started: The Sales Dataset, Figures, and Axes)
    demo_bar_charts()                 -> Module 11, Section 11.2 (The Four Core Chart Types)
    demo_line_calendar_order()        -> Module 11, Section 11.2 (The Four Core Chart Types)
    demo_line_by_region()             -> Module 11, Section 11.2 (The Four Core Chart Types)
    demo_scatter_by_product()         -> Module 11, Section 11.2 (The Four Core Chart Types)
    demo_histograms()                 -> Module 11, Section 11.2 (The Four Core Chart Types)
    demo_grouped_bar_revenue_profit() -> Module 11, Section 11.3 (Customization and Multi-Panel Figures)
    demo_annotate_peak()              -> Module 11, Section 11.3 (Customization and Multi-Panel Figures)
    demo_subplot_grid()               -> Module 11, Section 11.3 (Customization and Multi-Panel Figures)
    demo_plotly_bar()                 -> Module 11, Section 11.4 (Plotly Express and the Polars-to-Visualization Workflow)
    demo_plotly_scatter()             -> Module 11, Section 11.4 (Plotly Express and the Polars-to-Visualization Workflow)
    demo_save_figure()                -> Module 11, Section 11.4 (Plotly Express and the Polars-to-Visualization Workflow)
    demo_capstone_summaries()         -> Module 11, Section 11.5 (Capstone: A Multi-Chart Business Dashboard)
    demo_capstone_dashboard()         -> Module 11, Section 11.5 (Capstone: A Multi-Chart Business Dashboard)
    demo_capstone_interactive()       -> Module 11, Section 11.5 (Capstone: A Multi-Chart Business Dashboard)

Data: the 36-row sales dataset from the Module 11 teaching notebook
(m11_teaching.py) -- 6 months x 2 regions x 3 products -- embedded as a CSV
literal so the script is self-contained. Deterministic -- no randomness, no
network. File output goes to computations/_scratch/module11/ (relative paths
only -- never print absolute paths).

Last updated: 2026-07-23
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless backend; must be set before importing pyplot

import matplotlib.pyplot as plt
import plotly.express as px
import polars as pl

SCRATCH_DIR = Path(__file__).parent / "_scratch" / "module11"

MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

SALES_CSV = """month,region,product,category,units,revenue,cost
Jan,North,Laptop,Electronics,120,143880,95400
Feb,North,Laptop,Electronics,135,161865,101250
Mar,North,Laptop,Electronics,150,179850,112500
Apr,North,Laptop,Electronics,110,131890,82500
May,North,Laptop,Electronics,165,197835,123750
Jun,North,Laptop,Electronics,180,215820,135000
Jan,South,Laptop,Electronics,90,107910,67500
Feb,South,Laptop,Electronics,95,113905,71250
Mar,South,Laptop,Electronics,105,125895,78750
Apr,South,Laptop,Electronics,115,137885,86250
May,South,Laptop,Electronics,130,155870,97500
Jun,South,Laptop,Electronics,140,167860,105000
Jan,North,Monitor,Electronics,200,69900,42000
Feb,North,Monitor,Electronics,220,76890,46200
Mar,North,Monitor,Electronics,190,66405,39900
Apr,North,Monitor,Electronics,210,73395,44100
May,North,Monitor,Electronics,240,83880,50400
Jun,North,Monitor,Electronics,260,90870,54600
Jan,South,Monitor,Electronics,150,52425,31500
Feb,South,Monitor,Electronics,170,59415,35700
Mar,South,Monitor,Electronics,160,55920,33600
Apr,South,Monitor,Electronics,180,62910,37800
May,South,Monitor,Electronics,200,69900,42000
Jun,South,Monitor,Electronics,210,73395,44100
Jan,North,Keyboard,Accessories,400,31960,16000
Feb,North,Keyboard,Accessories,450,35955,18000
Mar,North,Keyboard,Accessories,420,33558,16800
Apr,North,Keyboard,Accessories,380,30362,15200
May,North,Keyboard,Accessories,500,39950,20000
Jun,North,Keyboard,Accessories,520,41548,20800
Jan,South,Keyboard,Accessories,300,23970,12000
Feb,South,Keyboard,Accessories,320,25568,12800
Mar,South,Keyboard,Accessories,350,27965,14000
Apr,South,Keyboard,Accessories,310,24769,12400
May,South,Keyboard,Accessories,370,29567,14800
Jun,South,Keyboard,Accessories,390,31161,15600
"""


def make_sales():
    """Write the module CSV under the scratch dir and read it back with Polars.

    Mirrors the teaching notebook, which writes the CSV to a temp path and
    loads it with pl.read_csv().
    """
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = SCRATCH_DIR / "m11_sales.csv"
    csv_path.write_text(SALES_CSV, encoding="utf-8")
    return pl.read_csv(csv_path)


# ---------------------------------------------------------------------------
# Section 11.1 -- Getting Started: The Sales Dataset, Figures, and Axes
# ---------------------------------------------------------------------------

def demo_sales_dataset():
    """Load the module's 36-row sales dataset and describe its shape."""
    sales = make_sales()

    print(f"Loaded sales data: {sales.shape[0]} rows, {sales.shape[1]} columns")
    print(
        f"Coverage: {sales['month'].n_unique()} months x "
        f"{sales['region'].n_unique()} regions x "
        f"{sales['product'].n_unique()} products"
    )
    print("\nFirst five rows:")
    print(sales.head(5))


def demo_first_bar_chart():
    """The first matplotlib chart: quarterly revenue as a simple bar chart."""
    categories = ["Q1", "Q2", "Q3", "Q4"]
    revenue = [245000, 312000, 289000, 378000]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(categories, revenue, color="steelblue")
    ax.set_title("Quarterly Revenue")
    ax.set_ylabel("Revenue ($)")
    ax.set_xlabel("Quarter")
    plt.tight_layout()

    print("Data behind the bars:")
    for quarter, value in zip(categories, revenue):
        print(f"  {quarter}: ${value:,}")

    tallest = categories[revenue.index(max(revenue))]
    print(f"\nTallest bar: {tallest} (${max(revenue):,})")
    print(
        f"Figure structure: {len(ax.patches)} bars | "
        f"title='{ax.get_title()}' | xlabel='{ax.get_xlabel()}' | "
        f"ylabel='{ax.get_ylabel()}'"
    )
    plt.close(fig)


# ---------------------------------------------------------------------------
# Section 11.2 -- The Four Core Chart Types
# ---------------------------------------------------------------------------

def demo_bar_charts():
    """Vertical bars (revenue by product) and horizontal bars (by region)."""
    sales = make_sales()

    by_product = (
        sales
        .group_by("product")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
        .sort("total_revenue", descending=True)
    )

    fig1, ax1 = plt.subplots(figsize=(7, 4))
    ax1.bar(
        by_product["product"].to_list(),
        by_product["total_revenue"].to_list(),
        color=["#2196F3", "#4CAF50", "#FF9800"],
    )
    ax1.set_title("Total Revenue by Product")
    for i, val in enumerate(by_product["total_revenue"].to_list()):
        ax1.text(i, val + 5000, f"${val:,.0f}", ha="center", fontsize=9)

    print("Vertical bar chart -- total revenue by product:")
    for product, value in zip(
        by_product["product"].to_list(),
        by_product["total_revenue"].to_list(),
    ):
        print(f"  {product:<10}{'$' + format(value, ','):>11}")
    print(
        f"Largest bar: {by_product['product'][0]} "
        f"(${by_product['total_revenue'][0]:,}) | "
        f"Smallest bar: {by_product['product'][-1]} "
        f"(${by_product['total_revenue'][-1]:,})"
    )

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

    print("\nHorizontal bar chart -- total revenue by region:")
    for region, value in zip(
        by_region["region"].to_list(),
        by_region["total_revenue"].to_list(),
    ):
        print(f"  {region:<10}{'$' + format(value, ','):>11}")
    gap = by_region["total_revenue"][-1] - by_region["total_revenue"][0]
    print(
        f"{by_region['region'][-1]} leads {by_region['region'][0]} "
        f"by ${gap:,}"
    )
    print(
        f"Figure structure: {len(ax1.patches)} vertical bars, "
        f"{len(ax2.patches)} horizontal bars"
    )
    plt.close(fig1)
    plt.close(fig2)


def demo_line_calendar_order():
    """Monthly revenue line for the North region, with calendar month order."""
    sales = make_sales()

    north = (
        sales
        .filter(pl.col("region") == "North")
        .group_by("month")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
    )

    alphabetical = north.sort("month")
    print("Months sorted as plain strings (alphabetical -- scrambles the timeline):")
    print("  " + " -> ".join(alphabetical["month"].to_list()))

    north_sorted = (
        north
        .with_columns(pl.col("month").cast(pl.Enum(MONTH_ORDER)))
        .sort("month")
    )
    print("\nMonths sorted with pl.Enum (calendar order):")
    print("  " + " -> ".join(north_sorted["month"].to_list()))

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(
        north_sorted["month"].to_list(),
        north_sorted["total_revenue"].to_list(),
        marker="o",
        color="#1976D2",
        linewidth=2,
    )
    ax.set_title("Monthly Revenue — North Region")
    ax.set_ylabel("Revenue ($)")
    ax.set_xlabel("Month")
    ax.grid(axis="y", alpha=0.3)

    print("\nLine chart data -- monthly revenue, North region:")
    months = north_sorted["month"].to_list()
    values = north_sorted["total_revenue"].to_list()
    for month, value in zip(months, values):
        print(f"  {month}  ${value:,}")
    low_i = values.index(min(values))
    high_i = values.index(max(values))
    print(
        f"Lowest month: {months[low_i]} (${values[low_i]:,}) | "
        f"Highest month: {months[high_i]} (${values[high_i]:,})"
    )
    print(
        f"Figure structure: {len(ax.lines)} line with {len(values)} points | "
        f"title='{ax.get_title()}'"
    )
    plt.close(fig)


def demo_line_by_region():
    """Two lines on one axes: monthly revenue for North and South."""
    sales = make_sales()

    by_region_month = (
        sales
        .group_by("region", "month")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
        .with_columns(pl.col("month").cast(pl.Enum(MONTH_ORDER)))
        .sort("month")
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    series = {}
    for region, color in [("North", "#1976D2"), ("South", "#E53935")]:
        data = by_region_month.filter(pl.col("region") == region)
        ax.plot(
            data["month"].to_list(),
            data["total_revenue"].to_list(),
            marker="o",
            color=color,
            linewidth=2,
            label=region,
        )
        series[region] = dict(
            zip(data["month"].to_list(), data["total_revenue"].to_list())
        )

    ax.set_title("Monthly Revenue by Region")
    ax.set_ylabel("Revenue ($)")
    ax.set_xlabel("Month")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    print("Line chart data -- monthly revenue by region:")
    print(f"  {'Month':<7}{'North':>10}{'South':>10}{'Gap':>10}")
    for month in MONTH_ORDER:
        north_val = series["North"][month]
        south_val = series["South"][month]
        print(
            f"  {month:<7}{north_val:>10,}{south_val:>10,}"
            f"{north_val - south_val:>10,}"
        )

    north_growth = series["North"]["Jun"] - series["North"]["Jan"]
    south_growth = series["South"]["Jun"] - series["South"]["Jan"]
    print(f"\nJan-to-Jun growth: North ${north_growth:,}, South ${south_growth:,}")
    legend_labels = [t.get_text() for t in ax.get_legend().get_texts()]
    print(
        f"Figure structure: {len(ax.lines)} lines | "
        f"legend: {', '.join(legend_labels)}"
    )
    plt.close(fig)


def demo_scatter_by_product():
    """Scatter of units vs. revenue with one color per product."""
    sales = make_sales()

    colors = {"Laptop": "#1976D2", "Monitor": "#4CAF50", "Keyboard": "#FF9800"}

    fig, ax = plt.subplots(figsize=(7, 5))
    print(f"Scatter plot: {sales.shape[0]} points (one per month-region-product row)")
    for product, color in colors.items():
        subset = sales.filter(pl.col("product") == product)
        ax.scatter(
            subset["units"].to_list(),
            subset["revenue"].to_list(),
            alpha=0.7,
            color=color,
            edgecolors="white",
            s=60,
            label=product,
        )
        price_per_unit = (subset["revenue"] / subset["units"]).mean()
        print(
            f"  {product:<9} {subset.shape[0]} points | "
            f"units {subset['units'].min()}-{subset['units'].max()} | "
            f"revenue ${subset['revenue'].min():,}-${subset['revenue'].max():,} | "
            f"price per unit ${price_per_unit:,.2f}"
        )

    ax.set_title("Units vs. Revenue by Product")
    ax.set_xlabel("Units Sold")
    ax.set_ylabel("Revenue ($)")
    ax.legend()
    ax.grid(alpha=0.3)

    print(
        "Within each product the points climb together: more units sold, "
        "more revenue."
    )
    print(
        f"Figure structure: {len(ax.collections)} color groups | "
        f"title='{ax.get_title()}'"
    )
    plt.close(fig)


def demo_histograms():
    """A revenue histogram, then overlaid per-region histograms on shared bins."""
    sales = make_sales()

    fig1, ax1 = plt.subplots(figsize=(7, 4))
    counts, edges, _ = ax1.hist(
        sales["revenue"].to_list(),
        bins=12,
        color="#00897B",
        edgecolor="white",
    )
    ax1.set_title("Distribution of Monthly Revenue Values")
    ax1.set_xlabel("Revenue ($)")
    ax1.set_ylabel("Frequency")

    print(f"Histogram of {sales.shape[0]} revenue values in {len(counts)} bins:")
    for lo, hi, count in zip(edges[:-1], edges[1:], counts):
        bar = "#" * int(count)
        print(f"  ${lo:>10,.1f} - ${hi:>10,.1f} | {int(count):>2} {bar}")
    tallest = int(max(counts))
    print(f"Tallest bin: {tallest} of the {sales.shape[0]} values")

    # Overlaid histograms: one shared set of bin edges for both regions
    revenue = sales.filter(pl.col("region").is_in(["North", "South"]))["revenue"]
    low, high = revenue.min(), revenue.max()
    bin_edges = [low + (high - low) * i / 10 for i in range(11)]

    fig2, ax2 = plt.subplots(figsize=(7, 4))
    region_counts = {}
    for region, color in [("North", "#1976D2"), ("South", "#E53935")]:
        data = sales.filter(pl.col("region") == region)["revenue"].to_list()
        r_counts, _, _ = ax2.hist(
            data,
            bins=bin_edges,
            alpha=0.5,
            color=color,
            edgecolor="white",
            label=region,
        )
        region_counts[region] = [int(c) for c in r_counts]

    ax2.set_title("Revenue Distribution by Region")
    ax2.legend()

    print(
        f"\nOverlaid histograms -- shared bin edges from ${low:,} to ${high:,}:"
    )
    print(f"  {'Bin range':<22}{'North':>6}{'South':>6}")
    for i in range(10):
        label = f"${bin_edges[i]:,.0f}-${bin_edges[i + 1]:,.0f}"
        print(
            f"  {label:<22}{region_counts['North'][i]:>6}"
            f"{region_counts['South'][i]:>6}"
        )
    plt.close(fig1)
    plt.close(fig2)


# ---------------------------------------------------------------------------
# Section 11.3 -- Customization and Multi-Panel Figures
# ---------------------------------------------------------------------------

def demo_grouped_bar_revenue_profit():
    """A polished grouped bar chart: revenue and profit side by side."""
    sales = make_sales()

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
        color="#4CAF50",
        label="Profit",
        width=0.4,
    )
    ax.set_xticks([i + 0.2 for i in range(len(products))])
    ax.set_xticklabels(products)
    ax.set_title("Revenue vs. Profit by Product", fontsize=14, fontweight="bold")
    ax.set_ylabel("Amount ($)", fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.3)

    print("Grouped bar chart data -- revenue vs. profit by product:")
    print(f"  {'Product':<10}{'Revenue':>12}{'Profit':>12}")
    for product, rev, prof in zip(products, revenue, profit):
        print(f"  {product:<10}{rev:>12,}{prof:>12,}")

    legend_labels = [t.get_text() for t in ax.get_legend().get_texts()]
    print(
        f"\nFigure structure: {len(ax.patches)} bars "
        f"({len(products)} products x {len(legend_labels)} series) | "
        f"legend: {', '.join(legend_labels)}"
    )
    print(f"Title: '{ax.get_title()}'")
    plt.close(fig)


def demo_annotate_peak():
    """A line chart with the peak month annotated."""
    sales = make_sales()

    monthly = (
        sales
        .group_by("month")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
    )

    vals = []
    for m in MONTH_ORDER:
        row = monthly.filter(pl.col("month") == m)
        vals.append(row["total_revenue"][0])

    max_idx = vals.index(max(vals))

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(MONTH_ORDER, vals, marker="o", color="#1976D2", linewidth=2)
    ax.set_ylim(top=max(vals) * 1.15)
    annotation_text = f"Peak: ${vals[max_idx]:,.0f}"
    ax.annotate(
        annotation_text,
        xy=(max_idx, vals[max_idx]),
        xytext=(max_idx - 1.5, vals[max_idx] + 15000),
        arrowprops=dict(arrowstyle="->", color="#E53935"),
        fontsize=11,
        color="#E53935",
        fontweight="bold",
    )
    ax.set_title("Monthly Revenue with Peak Annotated")
    ax.set_ylabel("Revenue ($)")
    ax.grid(axis="y", alpha=0.3)

    print("Monthly total revenue (all regions, all products):")
    for month, value in zip(MONTH_ORDER, vals):
        print(f"  {month}  ${value:,}")
    print(f"\nPeak month: {MONTH_ORDER[max_idx]}")
    print(f"Annotation drawn on the chart: '{annotation_text}'")
    print(f"y-axis top extended to ${max(vals) * 1.15:,.0f} to make room for the label")
    plt.close(fig)


def demo_subplot_grid():
    """A 2x2 subplot grid showing four views of the sales data."""
    sales = make_sales()

    product_colors = {"Keyboard": "#1976D2", "Laptop": "#4CAF50", "Monitor": "#FF9800"}

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

    # Top-left: revenue by product (bar)
    by_prod = sales.group_by("product").agg(pl.col("revenue").sum()).sort("product")
    axes[0, 0].bar(
        by_prod["product"].to_list(),
        by_prod["revenue"].to_list(),
        color=["#1976D2", "#4CAF50", "#FF9800"],
    )
    axes[0, 0].set_title("Revenue by Product")

    # Top-right: monthly trend (line)
    monthly = sales.group_by("month").agg(pl.col("revenue").sum())
    vals = []
    for m in MONTH_ORDER:
        row = monthly.filter(pl.col("month") == m)
        vals.append(row["revenue"][0])
    axes[0, 1].plot(MONTH_ORDER, vals, marker="o", color="#1976D2")
    axes[0, 1].set_title("Monthly Revenue Trend")

    # Bottom-left: revenue distribution (histogram)
    counts, _, _ = axes[1, 0].hist(
        sales["revenue"].to_list(), bins=12, color="#00897B", edgecolor="white"
    )
    axes[1, 0].set_title("Revenue Distribution")

    # Bottom-right: units vs. revenue (scatter), color by product
    for product, color in product_colors.items():
        subset = sales.filter(pl.col("product") == product)
        axes[1, 1].scatter(
            subset["units"].to_list(),
            subset["revenue"].to_list(),
            alpha=0.7,
            color=color,
            edgecolors="white",
            label=product,
        )
    axes[1, 1].set_title("Units vs. Revenue by Product")
    axes[1, 1].legend(fontsize=8)

    suptitle = "Sales Data — Four Perspectives"
    fig.suptitle(suptitle, fontsize=14, fontweight="bold")

    print(f"Figure: {axes.shape[0]}x{axes.shape[1]} subplot grid — '{suptitle}'")
    prods = by_prod["product"].to_list()
    revs = by_prod["revenue"].to_list()
    panel1 = " | ".join(f"{p} ${r:,}" for p, r in zip(prods, revs))
    print(f"  Panel [0, 0] {axes[0, 0].get_title()} (bar): {panel1}")
    print(
        f"  Panel [0, 1] {axes[0, 1].get_title()} (line): "
        f"Jan ${vals[0]:,} rising to Jun ${vals[-1]:,}"
    )
    print(
        f"  Panel [1, 0] {axes[1, 0].get_title()} (histogram): "
        f"{sales.shape[0]} values in {len(counts)} bins, tallest bin {int(max(counts))}"
    )
    print(
        f"  Panel [1, 1] {axes[1, 1].get_title()} (scatter): "
        f"{sales.shape[0]} points in {len(product_colors)} color groups"
    )
    plt.close(fig)


# ---------------------------------------------------------------------------
# Section 11.4 -- Plotly Express and the Polars-to-Visualization Workflow
# ---------------------------------------------------------------------------

def demo_plotly_bar():
    """An interactive Plotly Express bar chart: revenue by product and region."""
    sales = make_sales()

    summary = (
        sales
        .group_by("product", "region")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
        .sort("total_revenue", descending=True)
    )

    # The notebook hands Plotly a pandas DataFrame via .to_pandas(). The
    # compute environment has no pandas, and plotly >= 6 accepts Polars
    # DataFrames directly, so the demos pass the Polars frame -- the chart
    # (and every number) is identical either way.
    fig = px.bar(
        summary,
        x="product",
        y="total_revenue",
        color="region",
        barmode="group",
        title="Revenue by Product and Region",
        labels={"total_revenue": "Revenue ($)", "product": "Product"},
    )

    print("Aggregated data handed to px.bar():")
    print(summary)
    trace_names = [trace.name for trace in fig.data]
    print(
        f"\nFigure structure: {len(fig.data)} traces (one per region): "
        f"{', '.join(trace_names)}"
    )
    print(f"Bar mode: {fig.layout.barmode} | Title: '{fig.layout.title.text}'")
    print(
        f"Tallest bar: {summary['product'][0]} / {summary['region'][0]} "
        f"(${summary['total_revenue'][0]:,})"
    )


def demo_plotly_scatter():
    """An interactive Plotly Express scatter with bubble size and hover data."""
    sales = make_sales()

    fig = px.scatter(
        sales,  # plotly >= 6 accepts Polars directly (see note in demo_plotly_bar)
        x="units",
        y="revenue",
        color="product",
        size="cost",
        hover_data=["month", "region"],
        title="Units vs. Revenue (bubble size = cost)",
        labels={"units": "Units Sold", "revenue": "Revenue ($)"},
    )

    print(
        f"px.scatter() input: {sales.shape[0]} rows -- "
        "x=units, y=revenue, color=product, size=cost"
    )
    trace_names = [trace.name for trace in fig.data]
    print(f"Traces: {len(fig.data)} ({', '.join(trace_names)})")

    smallest = sales.sort("cost").head(1)
    largest = sales.sort("cost", descending=True).head(1)
    print(
        f"Bubble size spans cost ${smallest['cost'][0]:,} "
        f"({smallest['product'][0]}, {smallest['region'][0]}, {smallest['month'][0]}) "
        f"to ${largest['cost'][0]:,} "
        f"({largest['product'][0]}, {largest['region'][0]}, {largest['month'][0]})"
    )
    print("Hover shows: month, region (plus x, y, color, and size values)")
    print(f"Title: '{fig.layout.title.text}'")


def demo_save_figure():
    """Save a matplotlib figure to a PNG file with savefig()."""
    sales = make_sales()

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
        color="#1976D2",
    )
    ax.set_title("Revenue by Product")
    ax.set_ylabel("Revenue ($)")
    plt.tight_layout()

    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    out_path = SCRATCH_DIR / "revenue_by_product.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")

    print(f"Saved chart to {out_path.name} (dpi=150, bbox_inches='tight')")
    print(f"File exists: {out_path.exists()}")
    print(f"Chart saved with {len(ax.patches)} bars and title '{ax.get_title()}'")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Section 11.5 -- Capstone: A Multi-Chart Business Dashboard
# ---------------------------------------------------------------------------

def make_capstone_summaries():
    """The three summary tables the capstone dashboard draws from."""
    sales = make_sales()

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
            ((pl.col("total_revenue") - pl.col("total_cost")) / pl.col("total_revenue") * 100)
            .round(1)
            .alias("margin_pct"),
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

    return monthly_summary, product_summary, region_product


def demo_capstone_summaries():
    """Prepare and describe the capstone's three summary tables."""
    monthly_summary, product_summary, region_product = make_capstone_summaries()

    print("Capstone data prepared:")
    print(f"  monthly_summary:  {monthly_summary.shape}")
    print(f"  product_summary:  {product_summary.shape}")
    print(f"  region_product:   {region_product.shape}")

    print("\nproduct_summary (the dashboard's main source table):")
    print(product_summary)


def demo_capstone_dashboard():
    """The capstone matplotlib 2x2 dashboard, panel by panel."""
    monthly_summary, product_summary, _ = make_capstone_summaries()

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(13, 9))

    # Panel 1: revenue and profit by product (grouped bar)
    products = product_summary["product"].to_list()
    rev = product_summary["total_revenue"].to_list()
    profit = product_summary["profit"].to_list()
    x = range(len(products))
    axes[0, 0].bar([i - 0.2 for i in x], rev, width=0.4, label="Revenue", color="#1976D2")
    axes[0, 0].bar([i + 0.2 for i in x], profit, width=0.4, label="Profit", color="#4CAF50")
    axes[0, 0].set_xticks(list(x))
    axes[0, 0].set_xticklabels(products)
    axes[0, 0].set_title("Revenue vs. Profit by Product")
    axes[0, 0].legend()

    # Panel 2: monthly revenue and profit trend (line)
    rev_vals = []
    profit_vals = []
    for m in MONTH_ORDER:
        row = monthly_summary.filter(pl.col("month") == m)
        rev_vals.append(row["total_revenue"][0])
        profit_vals.append(row["profit"][0])
    axes[0, 1].plot(MONTH_ORDER, rev_vals, marker="o", color="#1976D2", linewidth=2, label="Revenue")
    axes[0, 1].plot(MONTH_ORDER, profit_vals, marker="s", color="#4CAF50", linewidth=2, label="Profit")
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

    suptitle = "Product Portfolio Performance Dashboard"
    fig.suptitle(suptitle, fontsize=15, fontweight="bold")

    print(f"Dashboard: '{suptitle}' -- 2x2 panels\n")

    print(f"Panel 1 -- {axes[0, 0].get_title()} (grouped bars):")
    for product, r, p in zip(products, rev, profit):
        rev_str = "$" + format(r, ",")
        profit_str = "$" + format(p, ",")
        print(f"  {product:<10} revenue {rev_str:>10}   profit {profit_str:>8}")

    print(f"\nPanel 2 -- {axes[0, 1].get_title()} (lines):")
    for month, r, p in zip(MONTH_ORDER, rev_vals, profit_vals):
        rev_str = "$" + format(r, ",")
        profit_str = "$" + format(p, ",")
        print(f"  {month}  revenue {rev_str:>8}   profit {profit_str:>8}")

    print(f"\nPanel 3 -- {axes[1, 0].get_title()} (horizontal bars, labels drawn on chart):")
    for product, margin in zip(products, margins):
        shade = "green" if margin > 30 else "orange"
        print(f"  {product:<10} {margin}%  ({shade} -- margin above the 30% threshold)")

    print(f"\nPanel 4 -- {axes[1, 1].get_title()} (bars):")
    for product, u in zip(products, units):
        print(f"  {product:<10} {u:,} units")
    plt.close(fig)


def demo_capstone_interactive():
    """The capstone's two interactive Plotly charts."""
    _, _, region_product = make_capstone_summaries()
    sales = make_sales()

    # Interactive grouped bar with value labels on the bars
    bar_fig = px.bar(
        region_product.sort("product"),  # plotly >= 6 accepts Polars directly
        x="product",
        y="total_revenue",
        color="region",
        barmode="group",
        title="Interactive: Revenue by Product and Region",
        labels={"total_revenue": "Revenue ($)", "product": "Product", "region": "Region"},
        text="total_revenue",
    )
    bar_fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    bar_fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")

    print("Interactive bar chart -- region_product data:")
    print(region_product.sort("product", "region"))
    print(
        f"\nBar chart: {len(bar_fig.data)} traces | barmode: "
        f"{bar_fig.layout.barmode} | Title: '{bar_fig.layout.title.text}'"
    )
    print("Each bar carries a dollar label via texttemplate")

    # Interactive faceted scatter: one panel per region, bubble size = profit
    detail = sales.with_columns(
        (pl.col("revenue") - pl.col("cost")).alias("profit"),
    )
    scatter_fig = px.scatter(
        detail,  # plotly >= 6 accepts Polars directly
        x="units",
        y="revenue",
        color="product",
        size="profit",
        facet_col="region",
        hover_data=["month", "cost", "profit"],
        title="Units vs. Revenue by Region (bubble size = profit)",
        labels={"units": "Units Sold", "revenue": "Revenue ($)"},
    )

    per_facet = detail.shape[0] // detail["region"].n_unique()
    smallest = detail.sort("profit").head(1)
    largest = detail.sort("profit", descending=True).head(1)
    print(
        f"\nFaceted scatter: {detail.shape[0]} points, {per_facet} per region facet | "
        f"{len(scatter_fig.data)} traces "
        f"({detail['product'].n_unique()} products x "
        f"{detail['region'].n_unique()} region facets)"
    )
    print(
        f"Bubble size = profit, from ${smallest['profit'][0]:,} "
        f"({smallest['product'][0]}, {smallest['region'][0]}, {smallest['month'][0]}) "
        f"to ${largest['profit'][0]:,} "
        f"({largest['product'][0]}, {largest['region'][0]}, {largest['month'][0]})"
    )
    print(f"Title: '{scatter_fig.layout.title.text}'")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    demos = [
        demo_sales_dataset,
        demo_first_bar_chart,
        demo_bar_charts,
        demo_line_calendar_order,
        demo_line_by_region,
        demo_scatter_by_product,
        demo_histograms,
        demo_grouped_bar_revenue_profit,
        demo_annotate_peak,
        demo_subplot_grid,
        demo_plotly_bar,
        demo_plotly_scatter,
        demo_save_figure,
        demo_capstone_summaries,
        demo_capstone_dashboard,
        demo_capstone_interactive,
    ]

    for demo in demos:
        print("=" * 70)
        print(f"# {demo.__name__}")
        print("=" * 70)
        demo()
        print()
