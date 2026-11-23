
import pandas as pd
from pathlib import Path


# ==============================
# 1. Load Dataset
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "tehran_weather_cleaned.csv"
)

REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE)

df["time"] = pd.to_datetime(df["time"])

df = df.sort_values("time").reset_index(drop=True)


# ==============================
# 2. Prepare Data
# ==============================

weather_columns = [
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "relative_humidity_2m_mean",
    "precipitation_sum",
    "wind_speed_10m_max",
    "sunshine_duration"
]

df[weather_columns] = df[weather_columns].apply(
    pd.to_numeric,
    errors="coerce"
)

# Create additional columns

df["year_month"] = df["time"].dt.to_period("M")

df["month"] = df["time"].dt.month

# Sunshine duration is stored in seconds
df["sunshine_hours"] = df["sunshine_duration"] / 3600

# Seasons (Northern Hemisphere)

season_mapping = {
    12: "Winter",
    1: "Winter",
    2: "Winter",
    3: "Spring",
    4: "Spring",
    5: "Spring",
    6: "Summer",
    7: "Summer",
    8: "Summer",
    9: "Autumn",
    10: "Autumn",
    11: "Autumn"
}

df["season"] = df["month"].map(season_mapping)


# ==============================
# 3. Temperature Insights
# ==============================

valid_temp = df.dropna(
    subset=["temperature_2m_mean"]
)

hottest_day = valid_temp.loc[
    valid_temp["temperature_2m_mean"].idxmax()
]

coldest_day = valid_temp.loc[
    valid_temp["temperature_2m_mean"].idxmin()
]

average_temperature = valid_temp[
    "temperature_2m_mean"
].mean()

average_max_temperature = df[
    "temperature_2m_max"
].mean()

average_min_temperature = df[
    "temperature_2m_min"
].mean()


# ==============================
# 4. Rainfall Insights
# ==============================

valid_rain = df.dropna(
    subset=["precipitation_sum"]
)

total_rainfall = valid_rain[
    "precipitation_sum"
].sum()

rainy_days = valid_rain[
    valid_rain["precipitation_sum"] > 0
]

rainy_days_count = len(rainy_days)

average_rainfall = valid_rain[
    "precipitation_sum"
].mean()

maximum_rainfall = valid_rain.loc[
    valid_rain["precipitation_sum"].idxmax()
]


# ==============================
# 5. Humidity Insights
# ==============================

average_humidity = df[
    "relative_humidity_2m_mean"
].mean()

maximum_humidity = df[
    "relative_humidity_2m_mean"
].max()

minimum_humidity = df[
    "relative_humidity_2m_mean"
].min()


# ==============================
# 6. Wind Insights
# ==============================

average_wind = df[
    "wind_speed_10m_max"
].mean()

maximum_wind = df.loc[
    df["wind_speed_10m_max"].idxmax()
]


# ==============================
# 7. Sunshine Insights
# ==============================

average_sunshine = df[
    "sunshine_hours"
].mean()

total_sunshine = df[
    "sunshine_hours"
].sum()


# ==============================
# 8. Monthly Analysis
# ==============================

monthly_analysis = df.groupby(
    "year_month"
).agg(
    average_temperature=(
        "temperature_2m_mean", "mean"
    ),
    total_rainfall=(
        "precipitation_sum", "sum"
    ),
    average_humidity=(
        "relative_humidity_2m_mean", "mean"
    ),
    average_wind=(
        "wind_speed_10m_max", "mean"
    ),
    sunshine_hours=(
        "sunshine_hours", "sum"
    )
)

wettest_month = monthly_analysis[
    "total_rainfall"
].idxmax()

sunniest_month = monthly_analysis[
    "sunshine_hours"
].idxmax()

hottest_month = monthly_analysis[
    "average_temperature"
].idxmax()


# ==============================
# 9. Seasonal Analysis
# ==============================

seasonal_analysis = df.groupby(
    "season"
).agg(
    average_temperature=(
        "temperature_2m_mean", "mean"
    ),
    total_rainfall=(
        "precipitation_sum", "sum"
    ),
    average_humidity=(
        "relative_humidity_2m_mean", "mean"
    )
)

season_order = [
    "Winter",
    "Spring",
    "Summer",
    "Autumn"
]

seasonal_analysis = seasonal_analysis.reindex(
    season_order
)


# ==============================
# 10. Print Final Report
# ==============================

print("\n" + "=" * 45)
print("       TEHRAN WEATHER INSIGHTS")
print("=" * 45)

print("\n--- TEMPERATURE ---")

print(f"Average Temperature: {average_temperature:.2f} °C")

print(
    f"Average Maximum Temperature: "
    f"{average_max_temperature:.2f} °C"
)

print(
    f"Average Minimum Temperature: "
    f"{average_min_temperature:.2f} °C"
)

print(
    f"Hottest Day: {hottest_day['time'].date()} "
    f"({hottest_day['temperature_2m_mean']:.2f} °C)"
)

print(
    f"Coldest Day: {coldest_day['time'].date()} "
    f"({coldest_day['temperature_2m_mean']:.2f} °C)"
)


print("\n--- RAINFALL ---")

print(f"Total Rainfall: {total_rainfall:.2f} mm")

print(f"Rainy Days: {rainy_days_count}")

print(f"Average Daily Rainfall: {average_rainfall:.2f} mm")

print(
    f"Maximum Rainfall: "
    f"{maximum_rainfall['precipitation_sum']:.2f} mm "
    f"on {maximum_rainfall['time'].date()}"
)


print("\n--- HUMIDITY ---")

print(f"Average Humidity: {average_humidity:.2f} %")

print(f"Maximum Humidity: {maximum_humidity:.2f} %")

print(f"Minimum Humidity: {minimum_humidity:.2f} %")


print("\n--- WIND ---")

print(f"Average Maximum Wind Speed: {average_wind:.2f} km/h")

print(
    f"Strongest Wind: "
    f"{maximum_wind['wind_speed_10m_max']:.2f} km/h "
    f"on {maximum_wind['time'].date()}"
)


print("\n--- SUNSHINE ---")

print(f"Average Daily Sunshine: {average_sunshine:.2f} hours")

print(f"Total Sunshine: {total_sunshine:.2f} hours")


print("\n--- MONTHLY INSIGHTS ---")

print(f"Wettest Month: {wettest_month}")

print(f"Sunniest Month: {sunniest_month}")

print(f"Hottest Month: {hottest_month}")


print("\n--- SEASONAL ANALYSIS ---")

print(seasonal_analysis.round(2))


# ==============================
# 11. Save Reports
# ==============================

monthly_analysis.to_csv(
    REPORT_DIR / "monthly_weather_insights.csv"
)

seasonal_analysis.to_csv(
    REPORT_DIR / "seasonal_weather_insights.csv"
)

print("\nReports saved successfully!")

print("=" * 45)

## summary

# ==============================
# 12. Generate Markdown Report
# ==============================

def dataframe_to_markdown(dataframe):

    headers = ["Metric"] + list(dataframe.columns)

    rows = []

    for index, row in dataframe.iterrows():

        rows.append(
            [str(index)] + [
                f"{value:.2f}" if pd.notna(value)
                else "N/A"
                for value in row
            ]
        )

    result = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |"
    ]

    for row in rows:
        result.append(
            "| " + " | ".join(row) + " |"
        )

    return "\n".join(result)


report = f"""
# Tehran Weather Data Analysis

## Project Overview

This project analyzes one year of daily weather
data collected for Tehran.

## Temperature Analysis

- Average Temperature: {average_temperature:.2f} °C
- Average Maximum Temperature: {average_max_temperature:.2f} °C
- Average Minimum Temperature: {average_min_temperature:.2f} °C
- Hottest Day: {hottest_day['time'].date()}
- Hottest Daily Mean: {hottest_day['temperature_2m_mean']:.2f} °C
- Coldest Day: {coldest_day['time'].date()}
- Coldest Daily Mean: {coldest_day['temperature_2m_mean']:.2f} °C

## Rainfall Analysis

- Total Rainfall: {total_rainfall:.2f} mm
- Rainy Days: {rainy_days_count}
- Average Daily Rainfall: {average_rainfall:.2f} mm
- Maximum Daily Rainfall: {maximum_rainfall['precipitation_sum']:.2f} mm

## Humidity Analysis

- Average Humidity: {average_humidity:.2f} %
- Maximum Humidity: {maximum_humidity:.2f} %
- Minimum Humidity: {minimum_humidity:.2f} %

## Wind Analysis

- Average Maximum Wind Speed: {average_wind:.2f} km/h

## Sunshine Analysis

- Average Daily Sunshine: {average_sunshine:.2f} hours
- Total Sunshine: {total_sunshine:.2f} hours

## Monthly Analysis

- Wettest Month: {wettest_month}
- Sunniest Month: {sunniest_month}
- Hottest Month: {hottest_month}

## Seasonal Analysis

{dataframe_to_markdown(seasonal_analysis.round(2))}

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn

## Conclusion

The analysis shows seasonal variations in
temperature, rainfall and humidity in Tehran.

Summer had the highest average temperature,
while winter recorded the highest seasonal rainfall.

"""

# Save report

report_file = REPORT_DIR / "analysis_summary.md"

with open(report_file, "w", encoding="utf-8") as file:
    file.write(report)

print("\nMarkdown report generated successfully!")
print(f"Report location: {report_file}")
