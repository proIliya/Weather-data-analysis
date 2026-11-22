
import pandas as pd
import numpy as np

from pathlib import Path


# Load dataset

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "tehran_weather_cleaned.csv"
)

df = pd.read_csv(DATA_FILE)

df["time"] = pd.to_datetime(df["time"])


# Temperature Analysis

print("\n========== TEMPERATURE ANALYSIS ==========")

average_temp = np.mean(df["temperature_2m_mean"])

max_temp = df["temperature_2m_max"].max()

min_temp = df["temperature_2m_min"].min()

print("Average Temperature:", round(average_temp, 2))
print("Maximum Temperature:", max_temp)
print("Minimum Temperature:", min_temp)


# Hottest Day

hottest_day = df.loc[
    df["temperature_2m_max"].idxmax()
]

print("\nHottest Day:")
print("Date:", hottest_day["time"].date())
print("Temperature:", hottest_day["temperature_2m_max"])


# Coldest Day

coldest_day = df.loc[
    df["temperature_2m_min"].idxmin()
]

print("\nColdest Day:")
print("Date:", coldest_day["time"].date())
print("Temperature:", coldest_day["temperature_2m_min"])

## rainfall analysis
print("\n========== RAINFALL ANALYSIS ==========")

total_rainfall = df["precipitation_sum"].sum()

average_rainfall = df["precipitation_sum"].mean()

rainy_days = (df["precipitation_sum"] > 0).sum()

max_rainfall = df["precipitation_sum"].max()

print("Total Rainfall:", round(total_rainfall, 2), "mm")

print("Average Daily Rainfall:", round(average_rainfall, 2), "mm")

print("Rainy Days:", rainy_days)

print("Maximum Daily Rainfall:", max_rainfall, "mm")

#HUMIDITY ANALYSIS

print("\n========== HUMIDITY ANALYSIS ==========")

average_humidity = df["relative_humidity_2m_mean"].mean()

max_humidity = df["relative_humidity_2m_mean"].max()

min_humidity = df["relative_humidity_2m_mean"].min()

print("Average Humidity:", round(average_humidity, 2), "%")

print("Maximum Humidity:", max_humidity, "%")

print("Minimum Humidity:", min_humidity, "%")

# monthly temp
# Extract year and month

df["year_month"] = df["time"].dt.to_period("M")

monthly_temperature = df.groupby(
    "year_month"
)["temperature_2m_mean"].mean()

print("\n========== MONTHLY TEMPERATURE ==========")

print(monthly_temperature.round(2))

## check coldest day
print("\n========== COLD TEMPERATURE CHECK ==========")

coldest_index = df["temperature_2m_min"].idxmin()

print(
    df.loc[
        coldest_index,
        [
            "time",
            "temperature_2m_min",
            "temperature_2m_mean",
            "temperature_2m_max"
        ]
    ]
)

# Check surrounding days

print("\nSurrounding days:")

print(
    df.loc[
        max(0, coldest_index - 2):
        coldest_index + 2,
        [
            "time",
            "temperature_2m_min",
            "temperature_2m_mean",
            "temperature_2m_max"
        ]
    ]
)