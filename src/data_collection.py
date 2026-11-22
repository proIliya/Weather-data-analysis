
import pandas as pd
import requests

from pathlib import Path
from datetime import date, timedelta


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


# Last year
end_date = date.today() - timedelta(days=6)
start_date = end_date - timedelta(days=364)


url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": 35.6892,
    "longitude": 51.3890,

    "start_date": str(start_date),
    "end_date": str(end_date),

    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "temperature_2m_mean",
        "relative_humidity_2m_mean",
        "precipitation_sum",
        "wind_speed_10m_max",
        "sunshine_duration"
    ],

    "timezone": "Asia/Tehran",
    "models": "era5"
}


response = requests.get(
    url,
    params=params,
    timeout=60
)

response.raise_for_status()

data = response.json()

df = pd.DataFrame(data["daily"])

df["city"] = "Tehran"

df["time"] = pd.to_datetime(df["time"])

df = df.sort_values("time").reset_index(drop=True)


file_path = RAW_DIR / "tehran_weather.csv"

df.to_csv(file_path, index=False)

print("Weather data downloaded successfully!")

print("\nDate range:", start_date, "to", end_date)
print("\nDataset shape:", df.shape)
print("\n")

print(df.head())
