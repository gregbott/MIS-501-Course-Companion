"""Module 16 computation examples: Capstone — Proposal & Data Acquisition.

Every demo function below backs one Worked Example in the Module 16 chapter of
the MIS 501 Course Companion. The chapter pastes each function's stdout
verbatim, so do not edit outputs by hand — rerun this script instead.

References in Course Companion:
    demo_generate_bike_data()    -> Module 16, Section 16.5 (Example Walkthrough: Bike-Sharing Usage Patterns)
    demo_schema_and_null_counts()-> Module 16, Section 16.5 (Example Walkthrough: Bike-Sharing Usage Patterns)
    demo_summary_statistics()    -> Module 16, Section 16.5 (Example Walkthrough: Bike-Sharing Usage Patterns)
    demo_ridership_by_hour()     -> Module 16, Section 16.5 (Example Walkthrough: Bike-Sharing Usage Patterns)
    demo_ridership_by_weather()  -> Module 16, Section 16.5 (Example Walkthrough: Bike-Sharing Usage Patterns)
    demo_ridership_by_day()      -> Module 16, Section 16.5 (Example Walkthrough: Bike-Sharing Usage Patterns)
    demo_effect_sizes()          -> Module 16, Section 16.5 (Example Walkthrough: Bike-Sharing Usage Patterns)

Data: the synthetic bike-sharing dataset from the Module 16 teaching notebook
(m16_teaching.py), regenerated here with the notebook's own seed (501) and the
identical sequence of random calls, so every number matches the notebook.
Deterministic — no network access. Nothing is written to disk.

Last updated: 2026-07-23
"""

import random

import polars as pl


def make_bike_data():
    """Recreate the teaching notebook's synthetic bike-sharing dataset.

    Mirrors m16_teaching.py exactly — same seed (501) and the same order of
    random calls — so every demo sees identical data on every run.
    """
    random.seed(501)

    months = list(range(1, 13))  # Jan through Dec
    hours = [7, 8, 9, 12, 13, 17, 18, 19, 21]  # commute & off-peak hours
    days_of_week = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday",
    ]
    weather_options = ["Sunny", "Cloudy", "Rainy", "Snowy"]
    stations = ["Central Park", "Union Station", "Riverside", "Market Square"]
    member_types = ["casual", "annual"]

    rows = []
    for month in months:
        # Seasonal base: higher in summer (Jun-Aug), lower in winter (Dec-Feb)
        if month in (6, 7, 8):
            season_base = 180
            season = "Summer"
        elif month in (3, 4, 5):
            season_base = 120
            season = "Spring"
        elif month in (9, 10, 11):
            season_base = 110
            season = "Fall"
        else:
            season_base = 60
            season = "Winter"

        # ~17 records per month (~204 total)
        for _ in range(17):
            hour = random.choice(hours)
            day = random.choice(days_of_week)
            weather = random.choice(weather_options)
            station = random.choice(stations)
            member = random.choice(member_types)

            # Temperature depends on season (Celsius).
            # NOTE: the dict literal evaluates all four randint calls each
            # iteration (as in the teaching notebook) — do not "optimize"
            # this away, or the random sequence (and the data) changes.
            temp = {
                "Winter": random.randint(-5, 5),
                "Spring": random.randint(8, 20),
                "Summer": random.randint(22, 35),
                "Fall": random.randint(5, 18),
            }[season]

            humidity = random.randint(30, 95)

            # Ridership model: base + hour effect + weather effect + noise
            hour_effect = {
                7: 30, 8: 70, 9: 40, 12: 25, 13: 20,
                17: 75, 18: 65, 19: 30, 21: 10,
            }[hour]

            weather_effect = {
                "Sunny": 40, "Cloudy": 10, "Rainy": -30, "Snowy": -50,
            }[weather]

            weekend_effect = 15 if day in ("Saturday", "Sunday") else 0
            noise = random.randint(-20, 20)
            count = max(
                5,
                season_base + hour_effect + weather_effect + weekend_effect + noise,
            )

            rows.append({
                "date": f"2025-{month:02d}-{random.randint(1, 28):02d}",
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

    return pl.DataFrame(rows).with_columns(
        pl.col("date").str.to_date("%Y-%m-%d"),
    )


# ---------------------------------------------------------------------------
# Section 16.5 — Example Walkthrough: Bike-Sharing Usage Patterns
# ---------------------------------------------------------------------------

def demo_generate_bike_data():
    """Step 1 — acquire the data: generate the synthetic dataset, show shape and head."""
    bike_data = make_bike_data()
    print(f"Dataset shape: {bike_data.shape[0]} rows x {bike_data.shape[1]} columns")
    print()
    print(bike_data.head(10))


def demo_schema_and_null_counts():
    """Step 2 — inspect: column names/types and null counts."""
    bike_data = make_bike_data()
    print("Schema (column name -> data type):")
    for name, dtype in bike_data.schema.items():
        print(f"  {name}: {dtype}")
    print()
    print("Null values per column:")
    print(bike_data.null_count())


def demo_summary_statistics():
    """Step 2 — inspect: describe() on the numeric columns."""
    bike_data = make_bike_data()
    print(
        bike_data
        .select("hour", "temperature_c", "humidity_pct", "ridership_count")
        .describe()
    )


def demo_ridership_by_hour():
    """Step 3 — explore: average ridership by hour of day."""
    bike_data = make_bike_data()
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


def demo_ridership_by_weather():
    """Step 3 — explore: average ridership by weather condition."""
    bike_data = make_bike_data()
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


def demo_ridership_by_day():
    """Step 3 — explore: average ridership by day of week (Enum-ordered)."""
    bike_data = make_bike_data()
    day_order = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday",
    ]
    ridership_by_day = (
        bike_data
        .group_by("day_of_week")
        .agg(
            pl.col("ridership_count").mean().alias("avg_ridership"),
        )
        # Cast to an ordered Enum so a plain .sort() orders Mon->Sun
        # (the same idiom used for month ordering in Module 11)
        .with_columns(pl.col("day_of_week").cast(pl.Enum(day_order)))
        .sort("day_of_week")
    )
    print(ridership_by_day)


def demo_effect_sizes():
    """Steps 4-5 — the numbers behind the charts: peaks, weather uplift, weekend bump."""
    bike_data = make_bike_data()

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
    print(
        f"  Sunny: {weather_avg['Sunny']:.1f}   Cloudy: {weather_avg['Cloudy']:.1f}   "
        f"Rainy: {weather_avg['Rainy']:.1f}   Snowy: {weather_avg['Snowy']:.1f}"
    )
    print(f"  Sunny vs. Rainy uplift: +{(weather_avg['Sunny'] / weather_avg['Rainy'] - 1) * 100:.0f}%")
    print(f"  Sunny vs. Snowy uplift: +{(weather_avg['Sunny'] / weather_avg['Snowy'] - 1) * 100:.0f}%")

    weekend_avg = (
        bike_data
        .filter(pl.col("day_of_week").is_in(["Saturday", "Sunday"]))
        .get_column("ridership_count")
        .mean()
    )
    weekday_avg = (
        bike_data
        .filter(~pl.col("day_of_week").is_in(["Saturday", "Sunday"]))
        .get_column("ridership_count")
        .mean()
    )
    print()
    print("Weekend vs. weekday average ridership:")
    print(f"  Weekend: {weekend_avg:.1f}   Weekday: {weekday_avg:.1f}")
    print(f"  Weekend bump: +{(weekend_avg / weekday_avg - 1) * 100:.0f}%")


if __name__ == "__main__":
    demos = [
        demo_generate_bike_data,
        demo_schema_and_null_counts,
        demo_summary_statistics,
        demo_ridership_by_hour,
        demo_ridership_by_weather,
        demo_ridership_by_day,
        demo_effect_sizes,
    ]
    for demo in demos:
        print("=" * 72)
        print(f"### {demo.__name__}")
        print("=" * 72)
        demo()
        print()
