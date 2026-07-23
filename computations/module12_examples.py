"""Module 12 computation examples: Marimo Interactive Features.

Every demo function below backs one Worked Example in the Module 12 chapter of
the MIS 501 Course Companion. The chapter pastes each function's stdout
verbatim, so do not edit outputs by hand — rerun this script instead.

Module 12 teaches marimo UI widgets (dropdown, slider, text, checkbox, table,
tabs). Widgets need a live marimo session, so this script — which runs as a
plain Python program with no marimo installed — SIMULATES each widget's
``.value`` with an ordinary variable (e.g. ``selected_region = "North"``) and
then runs the exact downstream filtering/aggregation logic from the teaching
notebook (m12_teaching.py). Each demo states its simulated widget values in
its printed output. Chart-building code (Plotly Express) appears only in the
chapter's python fences; demos print the numbers behind each chart instead of
rendering figures.

References in Course Companion:
    demo_sales_dataset()            -> Module 12, Section 12.1 (From Static Notebooks to Interactive Tools)
    demo_dropdown_region_filter()   -> Module 12, Section 12.2 (The Core Widgets: Dropdown, Slider, Text, and Checkbox)
    demo_slider_revenue_threshold() -> Module 12, Section 12.2 (The Core Widgets: Dropdown, Slider, Text, and Checkbox)
    demo_text_search()              -> Module 12, Section 12.2 (The Core Widgets: Dropdown, Slider, Text, and Checkbox)
    demo_checkbox_region_toggle()   -> Module 12, Section 12.2 (The Core Widgets: Dropdown, Slider, Text, and Checkbox)
    demo_combined_filters()         -> Module 12, Section 12.3 (Combining Widgets and Interactive Tables)
    demo_table_selection()          -> Module 12, Section 12.3 (Combining Widgets and Interactive Tables)
    demo_side_by_side_summaries()   -> Module 12, Section 12.4 (Layout Composition and Live Charts)
    demo_metric_dropdown()          -> Module 12, Section 12.4 (Layout Composition and Live Charts)
    demo_data_explorer()            -> Module 12, Section 12.4 (Layout Composition and Live Charts)
    demo_capstone_filters()         -> Module 12, Section 12.5 (Design Patterns and the Capstone Dashboard)
    demo_capstone_overview()        -> Module 12, Section 12.5 (Design Patterns and the Capstone Dashboard)

Data: the 54-row product-sales dataset from the Module 12 teaching notebook,
embedded as a literal so the script is self-contained. Deterministic — no
randomness, no network, no marimo import.

Last updated: 2026-07-23
"""

import io

import polars as pl

# The product-sales dataset used throughout the Module 12 teaching notebook.
# The notebook writes this text to /tmp/m12_sales.csv in a setup cell and
# reads it back; here it is embedded directly.
SALES_CSV = """month,region,category,product,units,revenue,cost
Jan,North,Electronics,Laptop,120,143880,95400
Feb,North,Electronics,Laptop,135,161865,101250
Mar,North,Electronics,Laptop,150,179850,112500
Apr,North,Electronics,Laptop,110,131890,82500
May,North,Electronics,Laptop,165,197835,123750
Jun,North,Electronics,Laptop,180,215820,135000
Jan,South,Electronics,Laptop,90,107910,67500
Feb,South,Electronics,Laptop,95,113905,71250
Mar,South,Electronics,Laptop,105,125895,78750
Apr,South,Electronics,Laptop,115,137885,86250
May,South,Electronics,Laptop,130,155870,97500
Jun,South,Electronics,Laptop,140,167860,105000
Jan,North,Electronics,Monitor,200,69900,42000
Feb,North,Electronics,Monitor,220,76890,46200
Mar,North,Electronics,Monitor,190,66405,39900
Apr,North,Electronics,Monitor,210,73395,44100
May,North,Electronics,Monitor,240,83880,50400
Jun,North,Electronics,Monitor,260,90870,54600
Jan,South,Electronics,Monitor,150,52425,31500
Feb,South,Electronics,Monitor,170,59415,35700
Mar,South,Electronics,Monitor,160,55920,33600
Apr,South,Electronics,Monitor,180,62910,37800
May,South,Electronics,Monitor,200,69900,42000
Jun,South,Electronics,Monitor,210,73395,44100
Jan,North,Accessories,Keyboard,400,31960,16000
Feb,North,Accessories,Keyboard,450,35955,18000
Mar,North,Accessories,Keyboard,420,33558,16800
Apr,North,Accessories,Keyboard,380,30362,15200
May,North,Accessories,Keyboard,500,39950,20000
Jun,North,Accessories,Keyboard,520,41548,20800
Jan,South,Accessories,Keyboard,300,23970,12000
Feb,South,Accessories,Keyboard,320,25568,12800
Mar,South,Accessories,Keyboard,350,27965,14000
Apr,South,Accessories,Keyboard,310,24769,12400
May,South,Accessories,Keyboard,370,29567,14800
Jun,South,Accessories,Keyboard,390,31161,15600
Jan,East,Electronics,Laptop,100,119900,75000
Feb,East,Electronics,Laptop,115,137885,86250
Mar,East,Electronics,Laptop,125,149875,93750
Apr,East,Electronics,Laptop,95,113905,71250
May,East,Electronics,Laptop,140,167860,105000
Jun,East,Electronics,Laptop,155,185845,116250
Jan,West,Accessories,Mouse,600,17940,6000
Feb,West,Accessories,Mouse,650,19435,6500
Mar,West,Accessories,Mouse,620,18538,6200
Apr,West,Accessories,Mouse,580,17342,5800
May,West,Accessories,Mouse,700,20930,7000
Jun,West,Accessories,Mouse,720,21528,7200
Jan,East,Accessories,Keyboard,280,22372,11200
Feb,East,Accessories,Keyboard,310,24769,12400
Mar,East,Accessories,Keyboard,330,26367,13200
Apr,East,Accessories,Keyboard,290,23171,11600
May,East,Accessories,Keyboard,350,27965,14000
Jun,East,Accessories,Keyboard,380,30362,15200
"""

MONTH_MAP = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6}


def make_sales():
    """The 54-row product-sales dataset used throughout the module."""
    return pl.read_csv(io.StringIO(SALES_CSV))


def capstone_filtered(
    region_choice,
    category_choice,
    min_revenue,
    search_text,
):
    """Apply the capstone control panel's four filters, notebook-style.

    Mirrors the filter cell of the capstone dashboard: adds a per-row profit
    column, then applies the region dropdown, category dropdown, minimum-
    revenue slider, and product-search text box in order.
    """
    filtered = make_sales().with_columns(
        (pl.col("revenue") - pl.col("cost")).alias("profit"),
    )

    if region_choice != "All":
        filtered = filtered.filter(pl.col("region") == region_choice)

    if category_choice != "All":
        filtered = filtered.filter(pl.col("category") == category_choice)

    filtered = filtered.filter(pl.col("revenue") >= min_revenue)

    query = search_text.strip().lower()
    if query:
        filtered = filtered.filter(
            pl.col("product").str.to_lowercase().str.contains(query, literal=True)
        )

    return filtered


# ---------------------------------------------------------------------------
# Section 12.1 — From Static Notebooks to Interactive Tools
# ---------------------------------------------------------------------------

def demo_sales_dataset():
    """Load the module's sales dataset and inspect its shape and categories."""
    sales = make_sales()

    print(f"Loaded sales data: {sales.shape[0]} rows, {sales.shape[1]} columns")
    print(f"Regions: {sales['region'].unique().sort().to_list()}")
    print(f"Categories: {sales['category'].unique().sort().to_list()}")
    print(f"Products: {sales['product'].unique().sort().to_list()}")

    print("\nFirst 5 rows:")
    print(sales.head(5))


# ---------------------------------------------------------------------------
# Section 12.2 — The Core Widgets: Dropdown, Slider, Text, and Checkbox
# ---------------------------------------------------------------------------

def demo_dropdown_region_filter():
    """Simulate a region dropdown selection and run the downstream filter."""
    sales = make_sales()

    # Stands in for region_dropdown.value in the notebook
    selected_region = "North"
    print(f"Simulating dropdown selection: {selected_region}")

    filtered = sales.filter(pl.col("region") == selected_region)

    summary = (
        filtered
        .group_by("product")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
        .sort("total_revenue", descending=True)
    )

    print(f"\nRows for the {selected_region} region: {filtered.shape[0]}")
    print("\nRevenue by product (the data behind the bar chart):")
    print(summary)


def demo_slider_revenue_threshold():
    """Simulate a minimum-revenue slider and count the rows that qualify."""
    sales = make_sales()

    # Stands in for revenue_slider.value in the notebook
    threshold = 50000
    print(f"Simulating slider value: {threshold} (Minimum Revenue)")

    filtered = sales.filter(pl.col("revenue") >= threshold)

    print(f"\nThreshold: ${threshold:,}")
    print(
        f"Rows matching: {filtered.shape[0]} of {sales.shape[0]} "
        f"({filtered.shape[0] / sales.shape[0] * 100:.0f}%)"
    )

    per_product = (
        filtered
        .group_by("product")
        .agg(pl.len().alias("rows_above_threshold"))
        .sort("rows_above_threshold", descending=True)
    )
    print("\nRows above the threshold by product (the points on the scatter plot):")
    print(per_product)


def demo_text_search():
    """Simulate a text-box search string and filter products by substring."""
    sales = make_sales()

    # Stands in for search_box.value in the notebook
    search_text = "key"
    print(f"Simulating text input: '{search_text}'")
    print()

    query = search_text.strip().lower()
    if query:
        filtered = sales.filter(
            pl.col("product").str.to_lowercase().str.contains(query, literal=True)
        )
    else:
        filtered = sales

    print(f"Search: '{search_text}' — {filtered.shape[0]} rows found")
    print("\nFirst 10 matching rows:")
    print(filtered.head(10))


def demo_checkbox_region_toggle():
    """Simulate four region checkboxes and build the monthly line-chart data."""
    sales = make_sales()

    # Stand in for show_north.value, show_south.value, etc. in the notebook
    show_north = True
    show_south = False
    show_east = False
    show_west = True
    print(
        "Simulating checkbox states: "
        f"North={show_north}, South={show_south}, "
        f"East={show_east}, West={show_west}"
    )

    regions = []
    if show_north:
        regions.append("North")
    if show_south:
        regions.append("South")
    if show_east:
        regions.append("East")
    if show_west:
        regions.append("West")

    print(f"Regions included: {regions}")

    filtered = sales.filter(pl.col("region").is_in(regions))
    summary = (
        filtered
        .group_by("month", "region")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
        .with_columns(
            pl.col("month").replace_strict(MONTH_MAP).alias("month_num"),
        )
        .sort("month_num", "region")
        .select("month", "region", "total_revenue")
    )

    print("\nMonthly revenue for the selected regions (the data behind the line chart):")
    print(summary)


# ---------------------------------------------------------------------------
# Section 12.3 — Combining Widgets and Interactive Tables
# ---------------------------------------------------------------------------

def demo_combined_filters():
    """Simulate two dropdowns plus a slider and apply all filters at once."""
    sales = make_sales()

    # Stand in for filter_region.value, filter_category.value,
    # filter_min_rev.value in the notebook
    region_choice = "North"
    category_choice = "Electronics"
    min_revenue = 100000
    print(
        "Simulating control panel: "
        f"Region={region_choice}, Category={category_choice}, "
        f"Min Revenue=${min_revenue:,}"
    )
    print()

    filtered_data = sales

    if region_choice != "All":
        filtered_data = filtered_data.filter(pl.col("region") == region_choice)

    if category_choice != "All":
        filtered_data = filtered_data.filter(pl.col("category") == category_choice)

    filtered_data = filtered_data.filter(pl.col("revenue") >= min_revenue)

    print(
        f"Filters: region={region_choice}, "
        f"category={category_choice}, "
        f"min_revenue=${min_revenue:,}"
    )
    print(f"Rows after filtering: {filtered_data.shape[0]}")

    summary = (
        filtered_data
        .group_by("product")
        .agg(
            pl.col("revenue").sum().alias("total_revenue"),
            pl.col("units").sum().alias("total_units"),
        )
        .sort("total_revenue", descending=True)
    )
    print("\nFiltered revenue by product (the data behind the bar chart):")
    print(summary)


def demo_table_selection():
    """Build the product-region summary table and simulate a row selection."""
    sales = make_sales()

    summary = (
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

    print("The summary shown in mo.ui.table (sortable, selectable):")
    print(summary)

    # Stands in for product_table.value in the notebook: the user clicked
    # the three Laptop rows
    selected = summary.filter(pl.col("product") == "Laptop")
    print("\nSimulating table selection: the Laptop rows")
    print(f"{selected.shape[0]} rows selected — chart below shows only selected data.")
    print("\nSelected rows (the data behind the grouped bar chart):")
    print(selected.select("product", "region", "total_revenue"))


# ---------------------------------------------------------------------------
# Section 12.4 — Layout Composition and Live Charts
# ---------------------------------------------------------------------------

def demo_side_by_side_summaries():
    """Compute the two aggregations behind the mo.hstack side-by-side charts."""
    sales = make_sales()

    by_region = (
        sales
        .group_by("region")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
        .sort("total_revenue", descending=True)
    )

    by_category = (
        sales
        .group_by("category")
        .agg(pl.col("revenue").sum().alias("total_revenue"))
        .sort("total_revenue", descending=True)
    )

    print("Left chart — Revenue by Region:")
    print(by_region)
    print("\nRight chart — Revenue by Category:")
    print(by_category)


def demo_metric_dropdown():
    """Simulate the metric dropdown that picks the chart's y-axis column."""
    sales = make_sales()

    # Stands in for metric_dropdown.value in the notebook
    metric = "units"
    print(f"Simulating metric selection: {metric}")

    summary = (
        sales
        .group_by("product", "region")
        .agg(pl.col(metric).sum().alias("total"))
        .sort("total", descending=True)
    )

    print(f"\nTotal {metric} by product and region (the data behind the grouped bar chart):")
    print(summary)


def demo_data_explorer():
    """Simulate the three explorer controls: column, group-by, and min units."""
    sales = make_sales()

    # Stand in for explore_column.value, explore_group.value,
    # explore_min.value in the notebook
    column_choice = "revenue"
    group_choice = "region"
    min_units = 200
    print(
        "Simulating explorer controls: "
        f"Column={column_choice}, Group By={group_choice}, "
        f"Minimum Units={min_units}"
    )
    print()

    filtered = sales.filter(pl.col("units") >= min_units)
    print(f"{filtered.shape[0]} rows after filtering (min units = {min_units})")

    agg = (
        filtered
        .group_by(group_choice)
        .agg(pl.col(column_choice).sum().alias("total"))
        .sort("total", descending=True)
    )

    print(f"\nTotal {column_choice} by {group_choice} (units >= {min_units}):")
    print(agg)


# ---------------------------------------------------------------------------
# Section 12.5 — Design Patterns and the Capstone Dashboard
# ---------------------------------------------------------------------------

def demo_capstone_filters():
    """Simulate the capstone control panel and apply all four filters."""
    sales = make_sales()

    # Stand in for cap_region.value, cap_category.value,
    # cap_min_revenue.value, cap_search.value in the notebook
    region_choice = "North"
    category_choice = "All"
    min_revenue = 50000
    search_text = ""
    print(
        "Simulating control panel: "
        f"Region={region_choice}, Category={category_choice}, "
        f"Min Revenue=${min_revenue:,}, Search='{search_text}'"
    )
    print()

    filtered = capstone_filtered(
        region_choice=region_choice,
        category_choice=category_choice,
        min_revenue=min_revenue,
        search_text=search_text,
    )

    print(
        f"Showing {filtered.shape[0]} of {sales.shape[0]} rows | "
        f"Region: {region_choice} | Category: {category_choice} | "
        f"Min Revenue: ${min_revenue:,} | Search: '{search_text}'"
    )

    print("\nFirst 5 filtered rows (with the computed profit column):")
    print(filtered.select("month", "product", "units", "revenue", "cost", "profit").head(5))


def demo_capstone_overview():
    """Compute the Overview and Trends tab data for the capstone dashboard."""
    # Same simulated control panel as the previous demo
    print(
        "Capstone filters still applied: "
        "Region=North, Category=All, Min Revenue=$50,000, Search=''"
    )

    filtered = capstone_filtered(
        region_choice="North",
        category_choice="All",
        min_revenue=50000,
        search_text="",
    )

    by_product = (
        filtered
        .group_by("product")
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

    print("\nOverview tab — revenue and profit by product:")
    print(by_product)

    total_revenue = filtered["revenue"].sum()
    total_units = filtered["units"].sum()
    total_profit = filtered["revenue"].sum() - filtered["cost"].sum()
    print(
        f"\nTotal Revenue: ${total_revenue:,} | "
        f"Total Units: {total_units:,} | "
        f"Total Profit: ${total_profit:,}"
    )

    monthly = (
        filtered
        .group_by("month")
        .agg(
            pl.col("revenue").sum().alias("total_revenue"),
            pl.col("units").sum().alias("total_units"),
        )
        .with_columns(
            pl.col("month").replace_strict(MONTH_MAP).alias("month_num"),
        )
        .sort("month_num")
        .select("month", "total_revenue", "total_units")
    )

    print("\nTrends tab — monthly totals (the data behind the line charts):")
    print(monthly)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    demos = [
        demo_sales_dataset,
        demo_dropdown_region_filter,
        demo_slider_revenue_threshold,
        demo_text_search,
        demo_checkbox_region_toggle,
        demo_combined_filters,
        demo_table_selection,
        demo_side_by_side_summaries,
        demo_metric_dropdown,
        demo_data_explorer,
        demo_capstone_filters,
        demo_capstone_overview,
    ]

    for demo in demos:
        print("=" * 70)
        print(f"# {demo.__name__}")
        print("=" * 70)
        demo()
        print()
