
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Tehran Weather Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
    }

    [data-testid="stSidebar"] {
        background-color: #161B22;
    }

    h1, h2, h3 {
        color: #E6EDF3;
    }

    [data-testid="stMetric"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 18px;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        color: #9BA7B4;
    }

    [data-testid="stMetricValue"] {
        color: #58A6FF;
    }

    .dashboard-subtitle {
        color: #9BA7B4;
        font-size: 16px;
        margin-top: -10px;
    }

    .section-caption {
        color: #8B949E;
        font-size: 13px;
    }

    div[data-testid="stDownloadButton"] button {
        background-color: #238636;
        color: white;
        border: none;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. LOAD DATA
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "tehran_weather_cleaned.csv"
)

if not DATA_FILE.exists():
    st.error(f"Dataset not found: {DATA_FILE}")
    st.stop()


@st.cache_data
def load_data():

    data = pd.read_csv(DATA_FILE)

    data["time"] = pd.to_datetime(data["time"])

    numeric_columns = [
        "temperature_2m_max",
        "temperature_2m_min",
        "temperature_2m_mean",
        "relative_humidity_2m_mean",
        "precipitation_sum",
        "wind_speed_10m_max",
        "sunshine_duration"
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    data["sunshine_hours"] = (
        data["sunshine_duration"] / 3600
    )

    data = data.sort_values("time")

    return data


df = load_data()

# ==========================================
# 4. CHART THEME
# ==========================================

CHART_TEMPLATE = "plotly_dark"

def style_chart(fig, height=380):

    fig.update_layout(
        template=CHART_TEMPLATE,
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Arial",
            color="#E6EDF3"
        ),
        margin=dict(
            l=20,
            r=20,
            t=65,
            b=25
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#30363D"
    )

    fig.update_yaxes(
        gridcolor="#30363D",
        zerolinecolor="#30363D"
    )

    return fig


# ==========================================
# 5. HEADER
# ==========================================

st.title("🌤️ Tehran Weather Dashboard")

st.markdown(
    '<p class="dashboard-subtitle">'
    'Interactive Weather Data Analysis | '
    '365 Days of Weather Insights'
    '</p>',
    unsafe_allow_html=True
)

st.markdown("---")


# ==========================================
# 6. SIDEBAR FILTERS
# ==========================================

st.sidebar.title("⚙️ Dashboard Controls")

st.sidebar.markdown(
    "Customize your weather analysis."
)

min_date = df["time"].min().date()
max_date = df["time"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if not isinstance(selected_dates, (tuple, list)) or len(selected_dates) != 2:
    st.warning("Please select both a start date and an end date.")
    st.stop()

start_date, end_date = selected_dates

if start_date > end_date:
    st.error("Start date cannot be after end date.")
    st.stop()

filtered_df = df[
    (df["time"].dt.date >= start_date)
    &
    (df["time"].dt.date <= end_date)
].copy()

if filtered_df.empty:
    st.warning("No weather data available for this period.")
    st.stop()

st.sidebar.success(
    f"{len(filtered_df)} days selected"
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Data source: Tehran Weather Dataset"
)


# ==========================================
# 7. KPI CARDS
# ==========================================

st.subheader("📊 Weather Overview")

col1, col2, col3, col4 = st.columns(4)

average_temp = filtered_df[
    "temperature_2m_mean"
].mean()

max_temp = filtered_df[
    "temperature_2m_max"
].max()

min_temp = filtered_df[
    "temperature_2m_min"
].min()

total_rainfall = filtered_df[
    "precipitation_sum"
].sum()

col1.metric(
    "Average Temperature",
    f"{average_temp:.1f} °C"
)

col2.metric(
    "Highest Temperature",
    f"{max_temp:.1f} °C"
)

col3.metric(
    "Lowest Temperature",
    f"{min_temp:.1f} °C"
)

col4.metric(
    "Total Rainfall",
    f"{total_rainfall:.1f} mm"
)

st.markdown("---")


# ==========================================
# 8. DAILY WEATHER TREND
# ==========================================

st.subheader("📈 Daily Weather Trends")

variable_options = {
    "Mean Temperature": (
        "temperature_2m_mean",
        "Temperature (°C)"
    ),
    "Maximum Temperature": (
        "temperature_2m_max",
        "Temperature (°C)"
    ),
    "Minimum Temperature": (
        "temperature_2m_min",
        "Temperature (°C)"
    ),
    "Humidity": (
        "relative_humidity_2m_mean",
        "Humidity (%)"
    ),
    "Rainfall": (
        "precipitation_sum",
        "Rainfall (mm)"
    ),
    "Wind Speed": (
        "wind_speed_10m_max",
        "Wind Speed (km/h)"
    ),
    "Sunshine Duration": (
        "sunshine_hours",
        "Sunshine (hours)"
    )
}

selected_variable = st.selectbox(
    "Select Weather Variable",
    options=list(variable_options.keys())
)

column_name, axis_label = variable_options[
    selected_variable
]

trend_chart = px.line(
    filtered_df,
    x="time",
    y=column_name,
    title=f"Daily {selected_variable}",
    labels={
        "time": "Date",
        column_name: axis_label
    }
)

trend_chart.update_traces(
    line=dict(width=2.5),
    hovertemplate="%{x|%Y-%m-%d}<br>%{y:.2f}<extra></extra>"
)

st.plotly_chart(
    style_chart(trend_chart),
    width='stretch'
)


# ==========================================
# 9. TEMPERATURE ANALYSIS
# ==========================================

st.markdown("---")

st.subheader("🌡️ Temperature Analysis")

temperature_chart = px.line(
    filtered_df,
    x="time",
    y=[
        "temperature_2m_max",
        "temperature_2m_min",
        "temperature_2m_mean"
    ],
    labels={
        "time": "Date",
        "value": "Temperature (°C)",
        "variable": "Temperature Type"
    },
    title="Daily Temperature Changes"
)

temperature_chart.update_layout(
    hovermode="x unified"
)

st.plotly_chart(
    style_chart(temperature_chart),
    #use_container_width=True
    width="stretch"
)


# ==========================================
# 10. MONTHLY COMPARISON
# ==========================================

st.markdown("---")

st.subheader("📅 Monthly Weather Comparison")

monthly_df = filtered_df.copy()

monthly_df["month"] = (
    monthly_df["time"]
    .dt.to_period("M")
    .astype(str)
)

available_months = sorted(
    monthly_df["month"].unique()
)

selected_months = st.multiselect(
    "Choose months to compare",
    options=available_months,
    default=available_months
)

if selected_months:

    comparison_df = monthly_df[
        monthly_df["month"].isin(selected_months)
    ]

    monthly_summary = comparison_df.groupby(
        "month",
        as_index=False
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

    month_col1, month_col2 = st.columns(2)

    with month_col1:

        monthly_temp_chart = px.bar(
            monthly_summary,
            x="month",
            y="average_temperature",
            title="Monthly Average Temperature",
            labels={
                "month": "Month",
                "average_temperature": "Temperature (°C)"
            },
            text_auto=".1f"
        )

        st.plotly_chart(
            style_chart(monthly_temp_chart),
            width="stretch"
        )

    with month_col2:

        monthly_rain_chart = px.bar(
            monthly_summary,
            x="month",
            y="total_rainfall",
            title="Monthly Total Rainfall",
            labels={
                "month": "Month",
                "total_rainfall": "Rainfall (mm)"
            },
            text_auto=".1f"
        )

        st.plotly_chart(
            style_chart(monthly_rain_chart),
            width="stretch"
        )

else:
    st.info("Select at least one month to compare.")


# ==========================================
# 11. SEASONAL ANALYSIS
# ==========================================

st.markdown("---")

st.subheader("🍂 Seasonal Weather Analysis")

season_map = {
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

season_order = [
    "Winter",
    "Spring",
    "Summer",
    "Autumn"
]

seasonal_df = filtered_df.copy()

seasonal_df["season"] = (
    seasonal_df["time"].dt.month.map(season_map)
)

seasonal_summary = seasonal_df.groupby(
    "season",
    as_index=False
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

seasonal_summary["season"] = pd.Categorical(
    seasonal_summary["season"],
    categories=season_order,
    ordered=True
)

seasonal_summary = seasonal_summary.sort_values(
    "season"
)

season_col1, season_col2 = st.columns(2)

with season_col1:

    seasonal_temp_chart = px.bar(
        seasonal_summary,
        x="season",
        y="average_temperature",
        title="Average Temperature by Season",
        labels={
            "season": "Season",
            "average_temperature": "Temperature (°C)"
        },
        text_auto=".1f"
    )

    st.plotly_chart(
        style_chart(seasonal_temp_chart),
        width="stretch"
    )

with season_col2:

    seasonal_rain_chart = px.bar(
        seasonal_summary,
        x="season",
        y="total_rainfall",
        title="Total Rainfall by Season",
        labels={
            "season": "Season",
            "total_rainfall": "Rainfall (mm)"
        },
        text_auto=".1f"
    )

    st.plotly_chart(
        style_chart(seasonal_rain_chart),
        width="stretch"
    )

st.markdown("#### Seasonal Summary")

st.dataframe(
    seasonal_summary,
    width="stretch",
    hide_index=True
)

st.caption(
    "Note: Seasonal results depend on the selected date range. "
    "Seasons with incomplete date coverage should be interpreted carefully."
)


# ==========================================
# 12. RAINFALL ANALYSIS
# ==========================================

st.markdown("---")

st.subheader("🌧️ Rainfall Analysis")

rain_col1, rain_col2 = st.columns(2)

with rain_col1:

    rainfall_chart = px.bar(
        filtered_df,
        x="time",
        y="precipitation_sum",
        title="Daily Rainfall",
        labels={
            "time": "Date",
            "precipitation_sum": "Rainfall (mm)"
        }
    )

    st.plotly_chart(
        style_chart(rainfall_chart),
        width="stretch"
    )

with rain_col2:

    rainy_days = filtered_df[
        filtered_df["precipitation_sum"] > 0
    ]

    st.metric(
        "Rainy Days",
        len(rainy_days)
    )

    st.metric(
        "Average Daily Rainfall",
        f"{filtered_df['precipitation_sum'].mean():.2f} mm"
    )

    st.metric(
        "Maximum Daily Rainfall",
        f"{filtered_df['precipitation_sum'].max():.2f} mm"
    )


# ==========================================
# 13. HUMIDITY AND WIND
# ==========================================

st.markdown("---")

st.subheader("💧 Humidity & 💨 Wind Analysis")

humidity_col, wind_col = st.columns(2)

with humidity_col:

    humidity_chart = px.line(
        filtered_df,
        x="time",
        y="relative_humidity_2m_mean",
        title="Daily Average Humidity",
        labels={
            "time": "Date",
            "relative_humidity_2m_mean": "Humidity (%)"
        }
    )

    st.plotly_chart(
        style_chart(humidity_chart),
        width="stretch"
    )

with wind_col:

    wind_chart = px.line(
        filtered_df,
        x="time",
        y="wind_speed_10m_max",
        title="Daily Maximum Wind Speed",
        labels={
            "time": "Date",
            "wind_speed_10m_max": "Wind Speed (km/h)"
        }
    )

    st.plotly_chart(
        style_chart(wind_chart),
        width="stretch"
    )


# ==========================================
# 14. SUNSHINE ANALYSIS
# ==========================================

st.markdown("---")

st.subheader("☀️ Sunshine Duration")

sunshine_chart = px.area(
    filtered_df,
    x="time",
    y="sunshine_hours",
    title="Daily Sunshine Duration",
    labels={
        "time": "Date",
        "sunshine_hours": "Sunshine (hours)"
    }
)

st.plotly_chart(
    style_chart(sunshine_chart),
    width="stretch"
)


# ==========================================
# 15. CORRELATION ANALYSIS
# ==========================================

st.markdown("---")

st.subheader("🔗 Weather Variables Correlation")

correlation_columns = [
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "relative_humidity_2m_mean",
    "precipitation_sum",
    "wind_speed_10m_max",
    "sunshine_hours"
]

correlation = filtered_df[
    correlation_columns
].corr()

correlation_chart = px.imshow(
    correlation,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    zmin=-1,
    zmax=1,
    title="Weather Variables Correlation"
)

st.plotly_chart(
    style_chart(correlation_chart, height=520),
    width="stretch"
)


# ==========================================
# 16. DATA TABLE
# ==========================================

st.markdown("---")

st.subheader("📋 Weather Data Explorer")

search_text = st.text_input(
    "Search in the dataset",
    placeholder="Enter a value or date..."
)

display_df = filtered_df.copy()

if search_text:
    mask = display_df.astype(str).apply(
        lambda column: column.str.contains(
            search_text,
            case=False,
            na=False
        )
    ).any(axis=1)

    display_df = display_df[mask]

st.caption(
    f"Displaying {len(display_df)} of {len(filtered_df)} records"
)

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)


# ==========================================
# 17. DOWNLOAD DATA
# ==========================================

st.markdown("---")

st.subheader("📥 Export Data")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="Download Filtered Weather Data",
    data=csv_data,
    file_name="tehran_weather_filtered.csv",
    mime="text/csv"
)

if not seasonal_summary.empty:

    seasonal_csv = seasonal_summary.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="Download Seasonal Summary",
        data=seasonal_csv,
        file_name="tehran_seasonal_summary.csv",
        mime="text/csv"
    )


# ==========================================
# 18. FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#8B949E;">
        <p><b>Tehran Weather Dashboard</b></p>
        <p>Built with Python | Pandas | Plotly | Streamlit</p>
        <p>Weather Data Analysis Portfolio Project</p>
    </div>
    """,
    unsafe_allow_html=True
)
