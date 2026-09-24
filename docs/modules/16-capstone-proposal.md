# Module 16.1: Capstone: Proposal & Data Acquisition

## Introduction

Fifteen modules ago you wrote your first line of Python; since then you have built functions, cleaned strings, structured data in lists and dictionaries, read and written files, transformed DataFrames with Polars, drawn charts with Plotly Express, queried data with DuckDB, scraped web pages, and pulled records from REST APIs. The capstone project asks you to put those pieces together on a question *you* choose — the same end-to-end workflow an analyst follows on the job: frame a business question, find and evaluate data, load and inspect it, explore it, and report what you find. This module covers the first half of that arc — the proposal and the data acquisition — and walks through a complete model project (bike-sharing ridership) so you can see what a strong start looks like before you begin your own.

---

## Learning Objectives

By the end of this module, you should be able to:

1. **Identify** a business-relevant research question suitable for a data analysis project
2. **Evaluate** and select appropriate data sources (files, APIs, web scraping)
3. **Write** a structured project proposal with clear scope and methodology
4. **Acquire** and load data into a Polars DataFrame
5. **Perform** initial exploratory data analysis (shape, types, missing values, distributions)
6. **Create** a preliminary visualization that supports the research question

---

## 16.1.1 What Makes a Good Capstone Project?

Your capstone project is an opportunity to apply everything you have learned in this course to a question you genuinely care about. Before writing any code, it pays to know what "good" looks like. A strong project shares five characteristics:

| Criterion | What It Means |
|-----------|--------------|
| **Clear research question** | A specific, answerable question — not a vague topic |
| **Available data** | At least 100 rows and multiple columns you can actually obtain |
| **Business relevance** | The answer would inform a real decision or provide actionable insight |
| **Appropriate scope** | Completable in roughly two weeks with the tools you know |
| **Uses course skills** | Polars, visualization, and optionally DuckDB, scraping, or APIs |

Two of these criteria deserve emphasis because they are where projects most often go wrong. **Appropriate scope** means resisting the urge to take on too much: a focused answer to a modest question beats an unfinished attempt at a grand one. **Available data** means confirming — before you commit — that you can actually get your hands on the rows and columns your question requires. A brilliant question with no obtainable data is not a project; it is a wish.

Think of the capstone as a "proof of concept" analysis, not a doctoral dissertation. You are demonstrating that you can frame a question, acquire data, explore it, and present findings — the core workflow of applied analytics. That workflow, executed cleanly on a well-chosen question, is exactly what the project (and a portfolio reviewer, or a hiring manager) is looking for.

---

## 16.1.2 Choosing a Research Question

The research question is the foundation of your project. It determines what data you need, what analysis you perform, and how you present your results. Time spent sharpening the question is the highest-leverage work you will do in the whole capstone.

### Good Research Questions

Good questions are **specific**, **measurable**, and **answerable with data**:

- "How does pricing tier affect customer churn rate for a SaaS product?"
- "Which product categories drive the highest revenue per square foot in retail stores?"
- "How do weather conditions and time of day affect bike-sharing ridership?"
- "What factors predict whether a restaurant will receive a health-code violation?"

Each of these identifies a **dependent variable** — the outcome being measured (churn rate, revenue, ridership, violation) — and one or more **independent variables** — the factors thought to influence that outcome (pricing tier, category, weather, time of day). Naming both explicitly is the fastest way to test whether your question is really a question: if you cannot say what the outcome column would be, you do not yet have a research question.

### Weak Research Questions

| Question | Problem |
|----------|---------|
| "What is business?" | Too vague — no measurable outcome |
| "Can we predict the stock market?" | Too ambitious — even professionals struggle with this |
| "Is Python good?" | Not data-driven — this is an opinion |
| "Analyze sales data" | Not a question at all — what specifically about sales? |

Notice that a weak question can usually be repaired rather than discarded. "Analyze sales data" becomes workable the moment you ask *what about* sales: "Which region's sales grew fastest last year?" or "Do discounted orders have higher return rates?" Narrowing is almost always the fix.

### The Chart Test

A useful test: can you imagine a chart or table that **answers** your question? If yes, the question is probably specific enough. "How do weather conditions affect ridership?" passes — you can picture a bar chart with weather categories on the x-axis and average ridership on the y-axis. "What is business?" fails — no chart answers it. Keep this test in mind through the rest of the module: the example walkthrough ends with exactly the charts its research question implies.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "A topic is a research question." | "Airline delays" is a topic. "Which routes and times of day have the worst average delays?" is a question. A question names an outcome and the factors that might drive it. |
| "A more ambitious question makes a better project." | Scope is a grading criterion in reverse: the project must be completable in about two weeks. "Predict the stock market" fails where "compare ridership across weather conditions" succeeds. |
| "The question must survive unchanged to the end." | Questions evolve as you meet the data. Refining your question after exploratory analysis is normal analytics practice, not a failure of planning. |

---

## 16.1.3 Evaluating Data Sources

Once you have a question, you need data. You have already practiced every acquisition route this course offers: files (Modules 8-9), web scraping (Module 14), and REST APIs (Module 15). The decision framework below summarizes when each route makes sense:

| Source Type | Examples | Pros | Cons |
|-------------|----------|------|------|
| **CSV / Excel files** | Kaggle, data.gov, UCI ML Repository, university data repos | Easy to load, well-documented | May be stale or pre-cleaned |
| **APIs** | OpenWeather, Census Bureau, Spotify, Reddit | Fresh, structured data | Rate limits, authentication |
| **Web scraping** | Product pages, public directories, sports stats | Get exactly what you need | Fragile, ethical considerations |
| **Internal / synthetic** | Company databases, generated data | Tailored to your question | May lack realism or volume |

For most capstone projects, a downloadable CSV is the pragmatic choice: `pl.read_csv()` and you are analyzing within minutes. Reach for an API or scraping when the question demands data that only lives there — and budget extra time for the error handling, pagination, and politeness practices those routes require.

### The Data Quality Checklist

Before committing to a data source, verify six things:

| Criterion | What to Check |
|-----------|--------------|
| **Size** | At least 100 rows (more is better for meaningful analysis) |
| **Completeness** | How many missing values? Can you handle them? |
| **Relevance** | Does it contain the columns you actually need? |
| **Recency** | Is the data recent enough for your question? |
| **Accessibility** | Can you actually download or fetch it without barriers? |
| **License** | Are you allowed to use it for a class project? |

Relevance is the criterion beginners most often skip: a dataset can be large, fresh, and free — and still lack the one column your dependent variable requires. Open the data (or its documentation) and confirm the columns exist before you commit.

Spending 30 minutes evaluating your data source up front can save hours of frustration later. The Module 16.1 assignment formalizes this habit: you will run two candidate sources through this exact checklist and justify your selection.

---

## 16.1.4 Writing the Proposal

A project proposal is a short document (roughly one page) that tells the reader what you plan to do and why. It is also a planning device for you: filling in the template forces every vague intention to become a concrete commitment. Use the following seven-part structure:

**1. Title.** A concise, descriptive title for your project.

**2. Research Question.** State your question in one or two sentences.

**3. Background & Motivation.** Why does this question matter? Who would benefit from the answer? (Two to three sentences is sufficient.)

**4. Data Source(s).** Where will you get your data? Include the URL or description. Note the approximate size (rows and columns).

**5. Methodology.** What analyses do you plan to perform? Which tools and techniques will you use? (e.g., "Group by region using Polars, compute summary statistics, visualize trends with Plotly Express.")

**6. Expected Deliverables.** What will you produce? Typical deliverables include a marimo notebook with analysis and visualizations, and a written executive summary of key findings and recommendations.

**7. Timeline.** Break the remaining two weeks into milestones — Week 1: data acquisition, cleaning, exploratory analysis; Week 2: focused analysis, visualization, write-up.

The proposal does not lock you in — it is a starting point. If your question evolves as you explore the data, that is normal and expected.

### From Blank Page to Draft

The teaching notebook suggests a concrete drafting sequence rather than staring at the empty template:

1. List two or three topics that interest you
2. For each, write a one-sentence research question
3. Check whether data is available (spend 10-15 minutes searching per topic)
4. Pick the topic with the best combination of interest and data availability
5. Fill in the proposal template

Notice that data availability enters at step 3, *before* you commit. Interest and availability are both requirements: a fascinating question without data stalls, and available data on a topic you do not care about produces a joyless project.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "The proposal is a contract — deviating from it is a failure." | The proposal is a starting point. Questions and methods routinely evolve once you meet the data; the notebook says so explicitly. |
| "Longer proposals are stronger proposals." | One page is the target. Each of the seven sections needs only a few sentences; precision beats length. |
| "Methodology means naming advanced techniques." | Methodology means naming *your* concrete steps with the tools you know: which columns you will group by, which statistics you will compute, which chart types you will build. |

---

## 16.1.5 Example Walkthrough: Bike-Sharing Usage Patterns

The rest of this module works through a **complete example** of the capstone's first phase, from proposal to preliminary findings. Treat it as a model for your own project — the same steps, in the same order, that your assignment asks of you.

### The Model Proposal

**Title:** Analyzing City Bike-Sharing Usage Patterns

**Research Question:** How do weather conditions and time of day affect bike-sharing ridership in a mid-sized city?

**Background & Motivation:** Cities invest heavily in bike-sharing infrastructure. Understanding what drives ridership helps city planners optimize station placement, predict demand, and schedule maintenance. Operators can also use these insights to adjust pricing or offer promotions during low-demand periods.

**Data Source:** Historical ridership records with weather observations, covering one year of daily data across multiple stations (~200 records).

**Methodology:** Load the data into a Polars DataFrame. Compute ridership statistics grouped by weather condition, hour of day, day of week, and season. Visualize patterns using Plotly Express bar and line charts.

**Expected Deliverables:** A Marimo notebook containing exploratory analysis and 4-6 visualizations with written interpretation of findings.

**Timeline:** Week 1 — acquire data, clean, and perform exploratory analysis. Week 2 — build final visualizations, write findings, and assemble the executive summary.

Check this proposal against §16.1.1's five criteria: the question names a dependent variable (ridership) and independent variables (weather, time of day); the data is obtainable and above the size minimum; the answer informs real operational decisions; the scope fits two weeks; and the methodology uses course tools. That is the standard your own proposal should meet.

### Step 1 — Acquire the Data

In a real project this step would be `pl.read_csv()` on a downloaded file, an API-fetching loop like Module 15's, or a scraper like Module 14's. Here we *generate* a synthetic dataset that mimics realistic bike-sharing patterns — seasonal swings, commute-hour peaks, weather effects, and random noise. What matters for the walkthrough is that the result is structured and large enough to analyze; the inspection and exploration steps that follow are identical no matter how the data arrived.

!!! example "Worked Example: Acquiring the Data — Generate, Load, and Check the Shape"

    ```python
    import datetime
    import random
    import polars as pl

    # Seed the RNG for reproducibility (a course-long best practice)
    random.seed(501)

    hours = [7, 8, 9, 12, 13, 17, 18, 19, 21]   # commute & off-peak hours
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday",
                    "Friday", "Saturday", "Sunday"]
    weather_options = ["Sunny", "Cloudy", "Rainy", "Snowy"]
    stations = ["Central Park", "Union Station", "Riverside", "Market Square"]

    rows = []
    for month in range(1, 13):
        # Seasonal base ridership: high in summer, low in winter
        if month in (6, 7, 8):
            season_base, season = 180, "Summer"
        elif month in (3, 4, 5):
            season_base, season = 120, "Spring"
        elif month in (9, 10, 11):
            season_base, season = 110, "Fall"
        else:
            season_base, season = 60, "Winter"

        for _ in range(17):   # ~17 records per month
            hour = random.choice(hours)
            day = random.choice(days_of_week)
            weather = random.choice(weather_options)
            station = random.choice(stations)
            member = random.choice(["casual", "annual"])

            # Temperature drawn from a season-appropriate range (Celsius)
            temp = {
                "Winter": random.randint(-5, 5),
                "Spring": random.randint(8, 20),
                "Summer": random.randint(22, 35),
                "Fall": random.randint(5, 18),
            }[season]
            humidity = random.randint(30, 95)

            # Ridership model: base + hour effect + weather effect + noise
            hour_effect = {7: 30, 8: 70, 9: 40, 12: 25, 13: 20,
                           17: 75, 18: 65, 19: 30, 21: 10}[hour]
            weather_effect = {"Sunny": 40, "Cloudy": 10,
                              "Rainy": -30, "Snowy": -50}[weather]
            weekend_effect = 15 if day in ("Saturday", "Sunday") else 0
            noise = random.randint(-20, 20)
            count = max(5, season_base + hour_effect + weather_effect
                        + weekend_effect + noise)

            # Pick a day of the month, then move it forward to the first
            # date on the chosen weekday (back a week if past the 28th)
            dom = random.randint(1, 28)
            shift = (days_of_week.index(day)
                     - datetime.date(2025, month, dom).weekday()) % 7
            dom = dom + shift if dom + shift <= 28 else dom + shift - 7

            rows.append({
                "date": f"2025-{month:02d}-{dom:02d}",
                "hour": hour,
                "day_of_week": day,
                "season": season,
                "temperature_c": temp,
                "humidity_pct": humidity,
                "weather": weather,
                "station": station,
                "member_type": member,
                "ridership_count": count,
            })

    bike_data = pl.DataFrame(rows).with_columns(
        pl.col("date").str.to_date("%Y-%m-%d"),
    )

    print(f"Dataset shape: {bike_data.shape[0]} rows x {bike_data.shape[1]} columns")
    print()
    print(bike_data.head(10))
    ```

    **Output:**

    ```
    Dataset shape: 204 rows x 10 columns

    shape: (10, 10)
    ┌────────────┬──────┬─────────────┬────────┬───┬─────────┬─────────────┬─────────────┬─────────────┐
    │ date       ┆ hour ┆ day_of_week ┆ season ┆ … ┆ weather ┆ station     ┆ member_type ┆ ridership_c │
    │ ---        ┆ ---  ┆ ---         ┆ ---    ┆   ┆ ---     ┆ ---         ┆ ---         ┆ ount        │
    │ date       ┆ i64  ┆ str         ┆ str    ┆   ┆ str     ┆ str         ┆ str         ┆ ---         │
    │            ┆      ┆             ┆        ┆   ┆         ┆             ┆             ┆ i64         │
    ╞════════════╪══════╪═════════════╪════════╪═══╪═════════╪═════════════╪═════════════╪═════════════╡
    │ 2025-01-18 ┆ 13   ┆ Saturday    ┆ Winter ┆ … ┆ Rainy   ┆ Union       ┆ annual      ┆ 67          │
    │            ┆      ┆             ┆        ┆   ┆         ┆ Station     ┆             ┆             │
    │ 2025-01-06 ┆ 19   ┆ Monday      ┆ Winter ┆ … ┆ Rainy   ┆ Market      ┆ casual      ┆ 69          │
    │            ┆      ┆             ┆        ┆   ┆         ┆ Square      ┆             ┆             │
    │ 2025-01-16 ┆ 12   ┆ Thursday    ┆ Winter ┆ … ┆ Rainy   ┆ Riverside   ┆ casual      ┆ 44          │
    │ 2025-01-14 ┆ 13   ┆ Tuesday     ┆ Winter ┆ … ┆ Sunny   ┆ Union       ┆ casual      ┆ 126         │
    │            ┆      ┆             ┆        ┆   ┆         ┆ Station     ┆             ┆             │
    │ 2025-01-17 ┆ 8    ┆ Friday      ┆ Winter ┆ … ┆ Snowy   ┆ Market      ┆ casual      ┆ 86          │
    │            ┆      ┆             ┆        ┆   ┆         ┆ Square      ┆             ┆             │
    │ 2025-01-11 ┆ 18   ┆ Saturday    ┆ Winter ┆ … ┆ Snowy   ┆ Riverside   ┆ casual      ┆ 86          │
    │ 2025-01-06 ┆ 7    ┆ Monday      ┆ Winter ┆ … ┆ Rainy   ┆ Market      ┆ annual      ┆ 66          │
    │            ┆      ┆             ┆        ┆   ┆         ┆ Square      ┆             ┆             │
    │ 2025-01-01 ┆ 21   ┆ Wednesday   ┆ Winter ┆ … ┆ Sunny   ┆ Riverside   ┆ casual      ┆ 97          │
    │ 2025-01-03 ┆ 9    ┆ Friday      ┆ Winter ┆ … ┆ Rainy   ┆ Riverside   ┆ annual      ┆ 58          │
    │ 2025-01-24 ┆ 21   ┆ Friday      ┆ Winter ┆ … ┆ Cloudy  ┆ Riverside   ┆ casual      ┆ 99          │
    └────────────┴──────┴─────────────┴────────┴───┴─────────┴─────────────┴─────────────┴─────────────┘
    ```

    **Interpretation:** The dataset lands at 204 rows x 10 columns — a realistic size for a capstone, and one your own project should match or exceed. Two display details are worth knowing before you inspect your own data: Polars elides middle columns (the `…` marker hides `temperature_c` and `humidity_pct`) to fit the table width, and wraps long values like station names onto a second line. All 10 columns are still in the DataFrame — the shape line printed above the table proves it.

    *Source: `computations/module16_examples.py` — `demo_generate_bike_data()`*

The synthetic generator plays the role that a download, API, or scraper plays in a real project. Notice that it *builds in* the effects the research question asks about — a commute-hour bump, a weather penalty, a weekend lift — plus noise. That is what makes it a good teaching dataset: we know the ground truth, so we can check whether exploratory analysis recovers it.

### Step 2 — Inspect the Data

Before any analysis, answer three basic questions:

1. **What columns do I have and what are their types?**
2. **How much data is there?**
3. **Are there missing values?**

These checks take only a few seconds and can reveal problems early — a date column that loaded as text, a numeric column full of nulls, far fewer rows than the download page promised. Making them a reflex is one of the habits this course has been building since Module 9.

!!! example "Worked Example: Schema and Null Counts"

    ```python
    # What columns and types do we have?
    print("Schema (column name -> data type):")
    for name, dtype in bike_data.schema.items():
        print(f"  {name}: {dtype}")

    # Are there missing values?
    print()
    print("Null values per column:")
    print(bike_data.null_count())
    ```

    **Output:**

    ```
    Schema (column name -> data type):
      date: Date
      hour: Int64
      day_of_week: String
      season: String
      temperature_c: Int64
      humidity_pct: Int64
      weather: String
      station: String
      member_type: String
      ridership_count: Int64

    Null values per column:
    shape: (1, 10)
    ┌──────┬──────┬─────────────┬────────┬───┬─────────┬─────────┬─────────────┬─────────────────┐
    │ date ┆ hour ┆ day_of_week ┆ season ┆ … ┆ weather ┆ station ┆ member_type ┆ ridership_count │
    │ ---  ┆ ---  ┆ ---         ┆ ---    ┆   ┆ ---     ┆ ---     ┆ ---         ┆ ---             │
    │ u32  ┆ u32  ┆ u32         ┆ u32    ┆   ┆ u32     ┆ u32     ┆ u32         ┆ u32             │
    ╞══════╪══════╪═════════════╪════════╪═══╪═════════╪═════════╪═════════════╪═════════════════╡
    │ 0    ┆ 0    ┆ 0           ┆ 0      ┆ … ┆ 0       ┆ 0       ┆ 0           ┆ 0               │
    └──────┴──────┴─────────────┴────────┴───┴─────────┴─────────┴─────────────┴─────────────────┘
    ```

    **Interpretation:** The schema confirms the types are analysis-ready: `date` is a true `Date` (because Step 1 cast it with `str.to_date()` — without that cast it would still be a string), the measurements are `Int64` integers, and the categories are `String`. `null_count()` returns a one-row DataFrame with a missing-value count per column, and every column reports 0 — no cleaning required before analysis.

    *Source: `computations/module16_examples.py` — `demo_schema_and_null_counts()`*

!!! example "Worked Example: Summary Statistics with describe()"

    ```python
    # Summary statistics for the numeric columns
    print(
        bike_data
        .select("hour", "temperature_c", "humidity_pct", "ridership_count")
        .describe()
    )
    ```

    **Output:**

    ```
    shape: (9, 5)
    ┌────────────┬───────────┬───────────────┬──────────────┬─────────────────┐
    │ statistic  ┆ hour      ┆ temperature_c ┆ humidity_pct ┆ ridership_count │
    │ ---        ┆ ---       ┆ ---           ┆ ---          ┆ ---             │
    │ str        ┆ f64       ┆ f64           ┆ f64          ┆ f64             │
    ╞════════════╪═══════════╪═══════════════╪══════════════╪═════════════════╡
    │ count      ┆ 204.0     ┆ 204.0         ┆ 204.0        ┆ 204.0           │
    │ null_count ┆ 0.0       ┆ 0.0           ┆ 0.0          ┆ 0.0             │
    │ mean       ┆ 14.166667 ┆ 13.710784     ┆ 63.813725    ┆ 154.867647      │
    │ std        ┆ 4.982894  ┆ 10.646569     ┆ 19.855007    ┆ 65.73433        │
    │ min        ┆ 7.0       ┆ -5.0          ┆ 30.0         ┆ 18.0            │
    │ 25%        ┆ 9.0       ┆ 5.0           ┆ 46.0         ┆ 104.0           │
    │ 50%        ┆ 13.0      ┆ 14.0          ┆ 64.0         ┆ 150.0           │
    │ 75%        ┆ 18.0      ┆ 20.0          ┆ 82.0         ┆ 199.0           │
    │ max        ┆ 21.0      ┆ 35.0          ┆ 95.0         ┆ 328.0           │
    └────────────┴───────────┴───────────────┴──────────────┴─────────────────┘
    ```

    **Interpretation:** `describe()` is a plausibility check in one call. Temperatures run from -5 to 35 degrees Celsius — sub-zero winter to mid-summer heat — humidity spans 30 to 95 percent, and ridership ranges from 18 on the quietest record to 328 on the busiest, with a median of 150 and a mean of about 155. Nothing is impossible (no negative counts, no thousand-degree days), so the data passes the sanity test. In your own project, an implausible min or max here is often the first sign of a data-quality problem.

    *Source: `computations/module16_examples.py` — `demo_summary_statistics()`*

The dataset has no missing values and the numeric ranges look reasonable. This is a clean starting point — in your own project, you may need to handle nulls and outliers (with the Module 10 techniques) before proceeding.

### Step 3 — Exploratory Analysis with Polars

With the data verified, we compute grouped statistics to start answering the research question. Each `group_by` targets one independent variable from the proposal: hour of day, weather condition, and day of week. This is the Module 10 split-apply-combine pattern doing capstone work.

!!! example "Worked Example: Average Ridership by Hour of Day"

    ```python
    ridership_by_hour = (
        bike_data
        .group_by("hour")
        .agg(
            pl.col("ridership_count").mean().alias("avg_ridership"),
            pl.col("ridership_count").count().alias("num_records"),
        )
        .sort("hour")
    )
    print(ridership_by_hour)
    ```

    **Output:**

    ```
    shape: (9, 3)
    ┌──────┬───────────────┬─────────────┐
    │ hour ┆ avg_ridership ┆ num_records │
    │ ---  ┆ ---           ┆ ---         │
    │ i64  ┆ f64           ┆ u32         │
    ╞══════╪═══════════════╪═════════════╡
    │ 7    ┆ 153.173913    ┆ 23          │
    │ 8    ┆ 190.65        ┆ 20          │
    │ 9    ┆ 139.136364    ┆ 22          │
    │ 12   ┆ 102.705882    ┆ 17          │
    │ 13   ┆ 122.272727    ┆ 22          │
    │ 17   ┆ 205.178571    ┆ 28          │
    │ 18   ┆ 184.714286    ┆ 21          │
    │ 19   ┆ 155.909091    ┆ 22          │
    │ 21   ┆ 127.793103    ┆ 29          │
    └──────┴───────────────┴─────────────┘
    ```

    **Interpretation:** The commute windows dominate: hour 17 tops the table at just over 205 average riders, with the morning peak at hour 8 (190.65) close behind, while midday hour 12 is quietest at about 103. Including `num_records` alongside the mean is deliberate — each hourly average rests on 17 to 29 observations, so no row is a one-off fluke. Averages presented without their sample sizes are a classic way to fool yourself.

    *Source: `computations/module16_examples.py` — `demo_ridership_by_hour()`*

!!! example "Worked Example: Average Ridership by Weather Condition"

    ```python
    ridership_by_weather = (
        bike_data
        .group_by("weather")
        .agg(
            pl.col("ridership_count").mean().alias("avg_ridership"),
            pl.col("ridership_count").median().alias("median_ridership"),
            pl.col("ridership_count").count().alias("num_records"),
        )
        .sort("avg_ridership", descending=True)
    )
    print(ridership_by_weather)
    ```

    **Output:**

    ```
    shape: (4, 4)
    ┌─────────┬───────────────┬──────────────────┬─────────────┐
    │ weather ┆ avg_ridership ┆ median_ridership ┆ num_records │
    │ ---     ┆ ---           ┆ ---              ┆ ---         │
    │ str     ┆ f64           ┆ f64              ┆ u32         │
    ╞═════════╪═══════════════╪══════════════════╪═════════════╡
    │ Sunny   ┆ 205.367347    ┆ 193.0            ┆ 49          │
    │ Cloudy  ┆ 182.142857    ┆ 164.0            ┆ 49          │
    │ Rainy   ┆ 127.109091    ┆ 121.0            ┆ 55          │
    │ Snowy   ┆ 110.078431    ┆ 97.0             ┆ 51          │
    └─────────┴───────────────┴──────────────────┴─────────────┘
    ```

    **Interpretation:** Weather sorts exactly as intuition predicts: Sunny leads at about 205 average riders and Snowy trails at about 110. The medians (193 down to 97) tell the same story as the means, so the gap is not the artifact of a few extreme days. Each condition has a healthy sample — between 49 and 55 records — which is why sorting by `avg_ridership` descending produces a ranking you can trust.

    *Source: `computations/module16_examples.py` — `demo_ridership_by_weather()`*

!!! example "Worked Example: Average Ridership by Day of Week"

    ```python
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday",
                 "Friday", "Saturday", "Sunday"]

    ridership_by_day = (
        bike_data
        .group_by("day_of_week")
        .agg(
            pl.col("ridership_count").mean().alias("avg_ridership"),
        )
        # Cast to an ordered Enum so a plain .sort() orders Mon -> Sun
        # (the same idiom used for month ordering in Module 11)
        .with_columns(pl.col("day_of_week").cast(pl.Enum(day_order)))
        .sort("day_of_week")
    )
    print(ridership_by_day)
    ```

    **Output:**

    ```
    shape: (7, 2)
    ┌─────────────┬───────────────┐
    │ day_of_week ┆ avg_ridership │
    │ ---         ┆ ---           │
    │ enum        ┆ f64           │
    ╞═════════════╪═══════════════╡
    │ Monday      ┆ 146.36        │
    │ Tuesday     ┆ 152.333333    │
    │ Wednesday   ┆ 147.9375      │
    │ Thursday    ┆ 141.677419    │
    │ Friday      ┆ 147.827586    │
    │ Saturday    ┆ 173.0         │
    │ Sunday      ┆ 176.6         │
    └─────────────┴───────────────┘
    ```

    **Interpretation:** Saturday (173) and Sunday (176.6) rise above every weekday, which cluster between about 142 and 152. The `Enum` cast is the technique to notice: `day_of_week` is text, so a plain sort would order the rows alphabetically (Friday first, Wednesday last). Casting to an ordered `Enum` — note the `enum` dtype in the output header — makes `.sort()` respect calendar order, which is what a reader (and the upcoming chart) expects.

    *Source: `computations/module16_examples.py` — `demo_ridership_by_day()`*

### Step 4 — Initial Visualizations

The summary tables hint at patterns; charts make them visible at a glance. Each chart addresses one facet of the research question, and each is built from a summary DataFrame computed in Step 3 — the chart is the last step of the pipeline, not a separate analysis. As in Module 11, Plotly Express receives the table via `.to_pandas()`:

```python
import plotly.express as px

# Chart 1: Ridership by hour of day
fig = px.bar(
    ridership_by_hour.to_pandas(),
    x="hour",
    y="avg_ridership",
    title="Average Ridership by Hour of Day",
    labels={
        "hour": "Hour of Day",
        "avg_ridership": "Average Ridership",
    },
    color_discrete_sequence=["#4C78A8"],
)
fig.update_layout(
    xaxis=dict(dtick=1),
    template="plotly_white",
)
fig
```

The bar chart confirms a clear **commute-hour pattern**: ridership peaks at 8 AM and again in the 17:00-18:00 evening rush, with lower usage at midday and late evening. This bimodal shape suggests that a large share of riders are commuters.

```python
# Chart 2: Ridership by weather condition
fig = px.bar(
    ridership_by_weather.to_pandas(),
    x="weather",
    y="avg_ridership",
    title="Average Ridership by Weather Condition",
    labels={
        "weather": "Weather",
        "avg_ridership": "Average Ridership",
    },
    color="weather",
    color_discrete_map={
        "Sunny": "#F4A261",
        "Cloudy": "#A8DADC",
        "Rainy": "#457B9D",
        "Snowy": "#E9ECEF",
    },
)
fig.update_layout(showlegend=False, template="plotly_white")
fig
```

The weather chart shows the descending staircase from Sunny to Snowy that the Step 3 table computed. The `color_discrete_map` assigns an evocative color to each condition — a small touch that makes the chart read instantly. This is actionable information: an operator might offer discounts on bad-weather days to boost utilization, or deploy fewer bikes ahead of forecasted storms.

The third chart repeats the same `px.bar` pattern on `ridership_by_day` (a single green `color_discrete_sequence`, no other changes) and shows the weekend lift — a visual argument that recreational riders supplement the commuter base on Saturdays and Sundays.

### Step 5 — Reflecting on Initial Findings

Exploration ends by asking: what preliminary answers do we have, and how big are the effects? The demo below distills the three charts into headline numbers — the kind of quantified statements an executive summary is made of.

!!! example "Worked Example: The Numbers Behind the Charts"

    ```python
    # Peak hours
    top_hours = (
        bike_data
        .group_by("hour")
        .agg(pl.col("ridership_count").mean().alias("avg_ridership"))
        .sort("avg_ridership", descending=True)
        .head(3)
    )
    print("Top 3 hours by average ridership:")
    for row in top_hours.iter_rows(named=True):
        print(f"  Hour {row['hour']:>2}: {row['avg_ridership']:.1f} riders")

    # Weather uplift: sunny vs. bad-weather averages
    weather_avg = {
        row["weather"]: row["avg_ridership"]
        for row in (
            bike_data
            .group_by("weather")
            .agg(pl.col("ridership_count").mean().alias("avg_ridership"))
            .iter_rows(named=True)
        )
    }
    print()
    print("Average ridership by weather:")
    print(f"  Sunny: {weather_avg['Sunny']:.1f}   Cloudy: {weather_avg['Cloudy']:.1f}   "
          f"Rainy: {weather_avg['Rainy']:.1f}   Snowy: {weather_avg['Snowy']:.1f}")
    print(f"  Sunny vs. Rainy uplift: +{(weather_avg['Sunny'] / weather_avg['Rainy'] - 1) * 100:.0f}%")
    print(f"  Sunny vs. Snowy uplift: +{(weather_avg['Sunny'] / weather_avg['Snowy'] - 1) * 100:.0f}%")

    # Weekend bump
    weekend_avg = (
        bike_data
        .filter(pl.col("day_of_week").is_in(["Saturday", "Sunday"]))
        .get_column("ridership_count").mean()
    )
    weekday_avg = (
        bike_data
        .filter(~pl.col("day_of_week").is_in(["Saturday", "Sunday"]))
        .get_column("ridership_count").mean()
    )
    print()
    print("Weekend vs. weekday average ridership:")
    print(f"  Weekend: {weekend_avg:.1f}   Weekday: {weekday_avg:.1f}")
    print(f"  Weekend bump: +{(weekend_avg / weekday_avg - 1) * 100:.0f}%")
    ```

    **Output:**

    ```
    Top 3 hours by average ridership:
      Hour 17: 205.2 riders
      Hour  8: 190.7 riders
      Hour 18: 184.7 riders

    Average ridership by weather:
      Sunny: 205.4   Cloudy: 182.1   Rainy: 127.1   Snowy: 110.1
      Sunny vs. Rainy uplift: +62%
      Sunny vs. Snowy uplift: +87%

    Weekend vs. weekday average ridership:
      Weekend: 174.6   Weekday: 147.2
      Weekend bump: +19%
    ```

    **Interpretation:** Three quantified findings emerge. **Time of day matters most:** the top hours are 17, 8, and 18 — both commute windows — with the leader at 205.2 average riders. **Weather is a strong driver:** sunny conditions carry a +62% uplift over rain and +87% over snow, a spread wide enough to make weather forecasts useful for demand prediction. **Weekends draw more riders:** 174.6 versus 147.2 on weekdays, a +19% bump likely reflecting recreational riders on top of the commuter base. Effects this clear also *validate the research question* — the data demonstrably contains the patterns the proposal set out to study.

    *Source: `computations/module16_examples.py` — `demo_effect_sizes()`*

In Module 16.2, this analysis would continue with deeper dives: cross-tabulations (weather by hour), seasonal trends, station-level comparisons, and a polished executive summary presenting the results.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| "My real dataset will be as clean as this example." | The walkthrough data has zero nulls and plausible ranges by construction. Real downloads routinely need the Module 10 null-handling and casting steps before Step 3 is possible. |
| "Exploratory charts are decoration for the final report." | Early charts *validate the question*. If Step 4 had shown four flat bars, the honest conclusion would be to refine the question or the data — better to learn that in week one than at submission. |
| "A group-by table alone proves an effect." | Check the supporting evidence: sample sizes per group (`num_records`) and a second statistic (the median) guard against averages driven by a handful of extreme rows. |
| "Synthetic data defeats the purpose of the walkthrough." | The acquisition step differs; every later step — inspect, explore, visualize, interpret — is identical for downloaded, fetched, scraped, or generated data. And with synthetic data the ground truth is known, so you can verify the analysis recovers it. |

---

## Reflection Questions

1. Take a weak question from §16.1.2 — say, "Can we predict the stock market?" — and repair it: write two narrower versions that would pass the five criteria from §16.1.1, and name the dependent and independent variables for each.
2. The chart test says a question is specific enough when you can imagine the chart that answers it. Why does this test work? What does being able to picture the chart force you to have already decided?
3. You need a year of competitor pricing data. It exists as a Kaggle CSV (updated annually), a commercial API (fresh, rate-limited, requires a key), and on the competitor's website (scrapable). Using the §16.1.3 framework, argue for one route for a two-week capstone — and name the condition under which you would switch.
4. The walkthrough generated its own data with known built-in effects, and Step 5 recovered them. What can this "known ground truth" setup teach you that a real dataset cannot — and what can it never teach you about real analysis work?
5. Your proposal names one research question, but week-one exploration reveals the data cannot answer it — though it *can* answer a neighboring question. What should you do, and why is this an expected outcome rather than a failure of planning?
6. Why does the module insist on the inspection ritual (shape, schema, nulls, `describe()`) *before* any group-by or chart? For each of the four checks, name one concrete problem it would catch early.

---

## Your Assignment

The Module 16.1 assignment is worth **100 points plus a 10-point bonus**. You complete it in a **marimo notebook (`.py` file)** and submit the file to **Blackboard**. The final reflection section is not graded separately — it counts toward participation.

This is **not a typical coding-drill assignment**: it is the first half of your capstone, and most tasks ask you to write about *your own* project. So that you can complete the technical tasks even if you have not yet found your own data, the notebook provides a fictional hotel-reviews sample dataset (well above the size minimums) as a stand-in — you can swap in your real data later. The tasks follow this module's sections in order: question, source evaluation, acquisition, inspection, exploration, proposal.

**Task 1: Research Question (15 points).** In prose (a `mo.md()` cell), state your research question in one to two sentences, explain in two to three sentences who benefits from the answer and what decision it informs, and identify your dependent variable plus at least two independent variables. §16.1.2 defines all three requirements — the grading rubric mirrors its specific/motivated/variables structure.

**Task 2: Data Source Evaluation (15 points).** Evaluate at least two candidate data sources for your project by filling in the six-point quality checklist (size, completeness, relevance, recency, accessibility, license) for each, then select one and justify the choice. The checklist and the source-type trade-offs are §16.1.3.

**Task 3: Data Acquisition & Loading (20 points).** Load your chosen dataset into a Polars DataFrame named `my_data` — from your own CSV, API, or scraped data, or the provided sample. The DataFrame must have at least 100 rows and at least 5 columns; you print its shape in the rows-by-columns format the task specifies and display the first ten rows. This is §16.1.5 Step 1; the loading routes themselves are Module 9 (`read_csv`), Module 15 (APIs), and Module 14 (scraping).

**Task 4: Data Inspection (15 points).** Run the four inspection checks on `my_data` — shape, schema, `describe()`, and null counts — then answer three written questions: the dataset's dimensions, whether (and where) values are missing, and whether any data types need fixing. This is §16.1.5 Step 2 applied to your data.

**Task 5: Exploratory Analysis (20 points).** Perform at least two `group_by` aggregations on different columns (each computing at least one summary statistic), build at least one labeled Plotly Express chart, and write a two-to-three-sentence interpretation for each aggregation and for the chart. §16.1.5 Steps 3-4 model exactly this sequence; the aggregation mechanics are Module 10 and the charting is Module 11.

**Task 6: Written Proposal (15 points).** Complete the seven-section proposal template — title, research question, background and motivation, data source(s), methodology, expected deliverables, timeline — with substantive content in every section. Grading also rewards internal consistency: the question must match the data, the methodology must match your tools, and the timeline must be realistic. The template is §16.1.4; the model proposal in §16.1.5 shows one filled in.

**Bonus: Additional Visualization (10 points).** Create a second Plotly Express chart that examines your data from a different angle than your Task 5 chart — a different chart type or different columns — with a title, axis labels, and a written explanation connecting it to your research question. §16.1.5 Step 4 and Module 11's chart-type catalog are the references.

**Reflection (participation).** Four questions about how you chose your question, what was hardest about finding data, what exploration revealed, and what risks you see for the full capstone. Honest answers help your instructor see where to support you in Module 16.2.

A final mechanical note from the assignment instructions: cell-scoped variables (loop variables, temporaries, figures) take the underscore prefix, while variables returned from a cell — like `my_data` — do not.

---

## Chapter Summary

This module opened the capstone by teaching you to engineer its foundation: the question. A strong project pairs a specific, measurable, data-answerable research question — one that names a dependent variable and the independent variables that might drive it — with the five criteria of a good capstone: clear question, available data, business relevance, two-week scope, and course tools. The chart test gives you a fast filter: if you can picture the chart that answers your question, the question is probably sharp enough.

Data acquisition starts before any download: the source-type framework (files, APIs, scraping, internal/synthetic) matches the acquisition route to the question, and the six-point quality checklist — size, completeness, relevance, recency, accessibility, license — catches doomed data sources in minutes instead of hours. The seven-part proposal then converts intentions into a plan: title, question, background, data, methodology, deliverables, timeline. The proposal is a starting point, not a contract; questions legitimately evolve on contact with data.

The bike-sharing walkthrough modeled the whole first phase. Acquire the data (generated here; downloaded, fetched, or scraped in your project) and confirm its shape. Inspect it — schema, null counts, `describe()` — before trusting it. Explore it with `group_by` aggregations aimed at each independent variable, reading sample sizes and medians alongside means. Visualize the summaries with Plotly Express, and distill the findings into quantified statements: commute-hour peaks, a sunny-weather uplift, a weekend bump. That closing move — numbers attached to claims — is what turns exploration into the raw material of an executive summary, and it is precisely where Module 16.2 picks up.

---

## What's Next

Module 16.2 — **Capstone: Analysis & Presentation** — takes your project from exploration to completion. You will deepen the analysis begun here (cross-tabulations, trends over time, comparisons across segments), build polished visualizations, and write up findings and recommendations in an executive summary suitable for a decision-maker — a finished, professional-quality analysis you can include in your portfolio. Everything you drafted in this module's proposal becomes the roadmap: week two of your timeline starts now.
