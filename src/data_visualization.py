import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path
from matplotlib.widgets import Button


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

df = pd.read_csv(DATA_FILE)

df["time"] = pd.to_datetime(df["time"])

sns.set_theme(style="whitegrid")


# ==============================
# 2. Prepare Charts Data
# ==============================

monthly_temp = df.groupby(
    df["time"].dt.to_period("M")
)["temperature_2m_mean"].mean()

weather_columns = [
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "relative_humidity_2m_mean",
    "precipitation_sum",
    "wind_speed_10m_max",
    "sunshine_duration"
]

correlation = df[weather_columns].corr()


# ==============================
# 3. Create Figure
# ==============================

fig, ax = plt.subplots(figsize=(13, 8))

plt.subplots_adjust(
    left=0.12,
    right=0.95,
    top=0.88,
    bottom=0.15
)

chart_index = 0

chart_names = [
    "Daily Temperature Trend",
    "Monthly Average Temperature",
    "Rainfall Distribution",
    "Weather Correlation Heatmap"
]



# ==============================
# 4. Chart Functions
# ==============================

def draw_temperature():
    ax.plot(
        df["time"],
        df["temperature_2m_mean"],
        linewidth=1.5,
        label="Average Temperature"
    )

    ax.set_title("Daily Average Temperature - Tehran")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()


def draw_monthly_temperature():
    ax.bar(
        monthly_temp.index.astype(str),
        monthly_temp.values
    )

    ax.set_title("Monthly Average Temperature - Tehran")
    ax.set_xlabel("Month")
    ax.set_ylabel("Temperature (°C)")

    ax.tick_params(
        axis="x",
        rotation=35,
        labelsize=9
    )

    ax.margins(x=0.03)
    ax.tick_params(
        axis="x",
        rotation=45,
        labelsize=9
    )

    ax.set_aspect("auto")


def draw_rainfall():

    rainy_days = df[
        df["precipitation_sum"] > 0
    ]

    sns.histplot(
        data=rainy_days,
        x="precipitation_sum",
        bins=20,
        kde=True,
        ax=ax
    )

    ax.set_title("Rainfall Distribution - Rainy Days")

    ax.set_xlabel("Rainfall (mm)")

    ax.set_ylabel("Number of Days")

    ax.set_aspect("auto")


def draw_correlation():

    short_names = {
        "temperature_2m_max": "Max Temp",
        "temperature_2m_min": "Min Temp",
        "temperature_2m_mean": "Mean Temp",
        "relative_humidity_2m_mean": "Humidity",
        "precipitation_sum": "Rainfall",
        "wind_speed_10m_max": "Wind Speed",
        "sunshine_duration": "Sunshine"
    }

    short_correlation = correlation.rename(
        index=short_names,
        columns=short_names
    )

    sns.heatmap(
        short_correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5,
        ax=ax,
        cbar=False,
        square=True
    )

    ax.set_title("Weather Variables Correlation")

    ax.tick_params(axis="x", rotation=35)
    ax.tick_params(axis="y", rotation=0)



# ==============================
# 5. Display Selected Chart
# ==============================


def show_chart(index):

    global chart_index

    chart_index = index % len(chart_names)

    # Clear previous chart
    ax.clear()

    # Reset aspect ratio
    ax.set_aspect("auto")
    ax.set_box_aspect(None)

    # Reset axis position
    ax.set_position([0.12, 0.22, 0.80, 0.58])

    if chart_index == 0:
        draw_temperature()

    elif chart_index == 1:
        draw_monthly_temperature()

    elif chart_index == 2:
        draw_rainfall()

    elif chart_index == 3:
        draw_correlation()

    fig.suptitle(
        f"Tehran Weather Analysis | "
        f"{chart_index + 1}/{len(chart_names)}",
        fontsize=15,
        fontweight="bold"
    )

    fig.canvas.draw_idle()



# ==============================
# 6. Navigation Functions
# ==============================

def next_chart(event):

    show_chart(chart_index + 1)


def previous_chart(event):

    show_chart(chart_index - 1)



# ==============================
# Keyboard Navigation
# ==============================

def on_key(event):

    if event.key == "right":
        show_chart(chart_index + 1)

    elif event.key == "left":
        show_chart(chart_index - 1)


fig.canvas.mpl_connect(
    "key_press_event",
    on_key
)

# ==============================
# 9. Show First Chart
# ==============================

show_chart(0)

plt.show()
