
import pandas as pd
import requests
import json
from datetime import datetime

from pathlib import Path
from datetime import date, timedelta


# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

RAW_FILE = RAW_DIR / "tehran_weather.csv"

PROCESSED_FILE = (
    PROCESSED_DIR / "tehran_weather_cleaned.csv"
)


# ==========================================
# 2. API CONFIGURATION
# ==========================================

url = "https://archive-api.open-meteo.com/v1/archive"

end_date = date.today() - timedelta(days=6)

daily_variables = [
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "relative_humidity_2m_mean",
    "precipitation_sum",
    "wind_speed_10m_max",
    "sunshine_duration"
]


# ==========================================
# 3. LOAD EXISTING DATA
# ==========================================

if RAW_FILE.exists():

    existing_df = pd.read_csv(RAW_FILE)

elif PROCESSED_FILE.exists():

    existing_df = pd.read_csv(PROCESSED_FILE)

else:

    existing_df = pd.DataFrame()


if not existing_df.empty:

    existing_df["time"] = pd.to_datetime(
        existing_df["time"],
        errors="coerce"
    )

    existing_df = existing_df.dropna(
        subset=["time"]
    )

    existing_df = existing_df.sort_values("time")

    last_saved_date = existing_df["time"].max().date()

    start_date = last_saved_date + timedelta(days=1)

else:

    # First download: previous 365 days
    start_date = end_date - timedelta(days=364)


# ==========================================
# 4. FETCH ONLY NEW DATA
# ==========================================

if start_date <= end_date:

    print("\nDownloading new weather data...")

    params = {
        "latitude": 35.6892,
        "longitude": 51.3890,

        "start_date": str(start_date),
        "end_date": str(end_date),

        "daily": daily_variables,

        "timezone": "Asia/Tehran",
        "models": "era5"
    }

    response = requests.get(
        url,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    api_data = response.json()

    if not api_data.get("daily") or not api_data["daily"].get("time"):

        print("API returned no new weather records.")

        new_df = pd.DataFrame()

    else:

        new_df = pd.DataFrame(api_data["daily"])

        new_df["city"] = "Tehran"

        new_df["time"] = pd.to_datetime(
            new_df["time"]
        )

    print("New records received:", len(new_df))

else:

    print("\nDataset is already up to date.")

    new_df = pd.DataFrame()


# ==========================================
# 5. MERGE OLD AND NEW DATA
# ==========================================

if not new_df.empty:

    if existing_df.empty:

        combined_df = new_df

    else:

        combined_df = pd.concat(
            [existing_df, new_df],
            ignore_index=True
        )

else:

    combined_df = existing_df


# ==========================================
# 6. REMOVE DUPLICATES AND SORT
# ==========================================

if not combined_df.empty:

    combined_df["time"] = pd.to_datetime(
        combined_df["time"],
        errors="coerce"
    )

    combined_df = combined_df.dropna(
        subset=["time"]
    )

    combined_df = combined_df.drop_duplicates(
        subset=["time"],
        keep="last"
    )

    combined_df = combined_df.sort_values(
        "time"
    ).reset_index(drop=True)


# ==========================================
# 7. SAVE DATA
# ==========================================

combined_df.to_csv(
    RAW_FILE,
    index=False
)


# ==========================================
# 8. FINAL INFORMATION
# ==========================================

print("\nWeather data collection completed!")

print("New records:", len(new_df))
print("Total records:", len(combined_df))

if not combined_df.empty:

    print(
        "Date range:",
        combined_df["time"].min().date(),
        "to",
        combined_df["time"].max().date()
    )

print("\nSaved to:", RAW_FILE)


# ==========================================
# 9. SAVE UPDATE STATUS
# ==========================================

REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

status = {
    "last_successful_update": datetime.now().astimezone().isoformat(
        timespec="seconds"
    ),
    "latest_data_date": (
        str(combined_df["time"].max().date())
        if not combined_df.empty
        else None
    ),
    "new_records": int(len(new_df)),
    "total_records": int(len(combined_df))
}

STATUS_FILE = REPORT_DIR / "update_status.json"

with open(STATUS_FILE, "w", encoding="utf-8") as file:
    json.dump(status, file, indent=4)

print("\nUpdate status saved successfully!")
print(status)


# ==========================================
# 10. SAVE UPDATE HISTORY
# ==========================================

HISTORY_FILE = REPORT_DIR / "update_history.csv"

history_record = pd.DataFrame([{
    "update_time": datetime.now().astimezone().isoformat(
        timespec="seconds"
    ),
    "latest_data_date": status["latest_data_date"],
    "new_records": status["new_records"],
    "total_records": status["total_records"]
}])

if HISTORY_FILE.exists():

    old_history = pd.read_csv(HISTORY_FILE)

    history_record = pd.concat(
        [old_history, history_record],
        ignore_index=True
    )

history_record.to_csv(
    HISTORY_FILE,
    index=False
)

print("Update history saved successfully!")

