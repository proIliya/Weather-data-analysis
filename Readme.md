# 🌤️ Tehran Weather Data Analysis

An end-to-end weather data analysis project focused on exploring, analyzing, and visualizing daily weather conditions in Tehran, Iran.

The project combines Python data analysis libraries with an interactive Streamlit dashboard to discover weather patterns and present meaningful insights.

## 📌 Project Overview

This project analyzes 365 days of weather data for Tehran, covering **November 17, 2025 to November 16, 2026**.

It explores temperature, precipitation, humidity, wind speed, and sunshine duration through data cleaning, exploratory analysis, statistical summaries, and interactive visualizations.

## ✨ Features

- Data cleaning and preprocessing with Pandas and NumPy
- Exploratory Data Analysis (EDA)
- Daily and monthly weather trend analysis
- Seasonal weather comparisons
- Temperature, rainfall, humidity, wind, and sunshine analysis
- Correlation analysis between weather variables
- Interactive charts using Plotly
- Interactive dashboard built with Streamlit
- Exportable weather data and analysis summaries

## 📊 Dashboard Preview

<!-- Add dashboard screenshots here -->

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit

## 📁 Project Structure

```text
weather_data_analysis/
│
├── data/
│   └── processed/
│       └── tehran_weather_cleaned.csv
│
├── src/
│   ├── exploratory_analysis.py
│   ├── data_visualization.py
│   └── insights.py
│
├── reports/
│   ├── monthly_weather_insights.csv
│   ├── seasonal_weather_insights.csv
│   └── analysis_summary.md
│
├── app.py
├── run_dashboard.py
├── requirements.txt
└── README.md
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/proIliya/Weather-data-analysis.git
cd weather_data_analysis
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows:

```powershell
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your default browser.

## 📈 Analysis Areas

### Temperature Analysis
- Daily maximum, minimum, and mean temperatures
- Monthly temperature trends
- Seasonal temperature comparisons

### Precipitation Analysis
- Daily rainfall patterns
- Monthly and seasonal rainfall totals
- Rainy-day statistics

### Humidity and Wind
- Daily average relative humidity
- Daily maximum wind speed

### Sunshine Analysis
- Daily sunshine duration
- Sunshine trends over the selected period

### Correlation Analysis
- Relationships between selected weather variables

## 📋 Data Information

The processed dataset contains the following fields:

- `time`
- `temperature_2m_max`
- `temperature_2m_min`
- `temperature_2m_mean`
- `relative_humidity_2m_mean`
- `precipitation_sum`
- `wind_speed_10m_max`
- `sunshine_duration`
- `city`

Sunshine duration is converted from seconds into hours for analysis and visualization.

## ⚠️ Notes and Limitations

- The dataset covers one year of daily observations, with partial November coverage at both ends.
- Seasonal and monthly comparisons should account for incomplete periods.
- Correlation does not necessarily imply causation.
- Results describe the available dataset and should not be interpreted as long-term climate conclusions.

## 👤 Author

**ILIYA FELEGARY**

Python Data Analysis Project

---

If you find this project useful, feel free to star the repository!