import pandas as pd
import numpy as np

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "tehran_weather.csv"

PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


df = pd.read_csv(RAW_FILE)

print(df.head())

# Dataset information
print("\nDataset Info:")
print(df.info())


# Dataset shape
print("\nDataset Shape:")
print(df.shape)


# Statistical summary
print("\nStatistical Summary:")
print(df.describe())


# Missing values
print("\nMissing Values:")
print(df.isnull().sum())


# Duplicate rows
print("\nDuplicate Rows:")
print(df.duplicated().sum())

df["time"] = pd.to_datetime(
    df["time"],
    errors="coerce"
)

print(df.dtypes)

# delete duplicates
print("Duplicates before cleaning:", df.duplicated(subset=["time"]).sum())

df = df.drop_duplicates(
    subset=["time"],
    keep="last"
)

print("Duplicates after cleaning:", df.duplicated(subset=["time"]).sum())

# Convert numerical columns
numeric_columns = [
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "relative_humidity_2m_mean",
    "precipitation_sum",
    "wind_speed_10m_max",
    "sunshine_duration"
]

df[numeric_columns] = df[numeric_columns].apply(
    pd.to_numeric,
    errors="coerce"
)


# Check humidity
df.loc[
    (df["relative_humidity_2m_mean"] < 0) |
    (df["relative_humidity_2m_mean"] > 100),
    "relative_humidity_2m_mean"
] = np.nan


# Check precipitation
df.loc[
    df["precipitation_sum"] < 0,
    "precipitation_sum"
] = np.nan


# Check wind speed
df.loc[
    df["wind_speed_10m_max"] < 0,
    "wind_speed_10m_max"
] = np.nan


# Check sunshine duration
df.loc[
    (df["sunshine_duration"] < 0) |
    (df["sunshine_duration"] > 86400),
    "sunshine_duration"
] = np.nan

# check temprature
invalid_temperature = (
    (df["temperature_2m_max"] < df["temperature_2m_min"]) |
    (df["temperature_2m_mean"] > df["temperature_2m_max"]) |
    (df["temperature_2m_mean"] < df["temperature_2m_min"])
)

df.loc[
    invalid_temperature,
    [
        "temperature_2m_max",
        "temperature_2m_min",
        "temperature_2m_mean"
    ]
] = np.nan

print(
    "Invalid temperature records:",
    invalid_temperature.sum()
)

# Remove rows without valid dates
df = df.dropna(subset=["time"])

# Sort by date
df = df.sort_values("time")

# Reset index
df = df.reset_index(drop=True)


# Save cleaned dataset
output_file = PROCESSED_DIR / "tehran_weather_cleaned.csv"

df.to_csv(output_file, index=False)


print("\nCleaning completed!")

print("Final dataset shape:", df.shape)

print("\nRemaining missing values:")
print(df.isnull().sum())

print("\nSaved to:", output_file)

# Find missing data dates

missing_dates = df.loc[
    df["temperature_2m_mean"].isna(),
    ["time"]
]

print("\nDates with missing weather data:")
print(missing_dates)
### test for clean data
'''print("Dataset shape:", df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate dates:")
print(df.duplicated(subset=["time"]).sum())

print("\nDate range:")
print(df["time"].min(), "to", df["time"].max())'''