# ETL Pipeline Project

## Overview

This ETL (Extract, Transform, Load) pipeline automates gathering weather and city data from multiple sources, cleaning and transforming it, and loading the results into a PostgreSQL database. A scheduler enables daily automated runs, and a GitHub Actions CI/CD workflow handles continuous deployment.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.9 |
| **Data Processing** | Pandas, NumPy |
| **Database** | PostgreSQL (Neon serverless) |
| **ORM / DB Driver** | SQLAlchemy, psycopg2 |
| **External API** | OpenWeatherMap API |
| **Scheduling** | `schedule` (Python library) |
| **Validation** | Pydantic |
| **Config Management** | JSON config, python-dotenv |
| **CI/CD** | GitHub Actions |
| **Testing** | pytest |

## Data Sources

| Source | Format | Description |
|---|---|---|
| `data/sample_data.csv` | CSV | Historical weather observations (temperature, humidity, wind speed, precipitation) |
| `data/sample_weather.json` | JSON | Multi-city weather data with nested temperature objects |
| `data/google_sheet_sample.csv` | CSV | Enriched weather data exported from Google Sheets (includes derived columns like `temp_range`) |
| OpenWeatherMap API | REST API | Real-time weather data fetched for a configured city |

## Project Structure

```
etl-pipline/
├── etl_pipeline.py          # Main ETL orchestration script (extract → clean → transform → load)
├── load_to_db.py             # Standalone database loader for pre-cleaned CSV data
├── scheduler.py              # Cron-style scheduler — runs ETL daily at 02:00
├── requirements.txt          # Python dependencies
├── config/
│   └── db_config.json        # Database connection settings & API keys
├── data/
│   ├── sample_data.csv       # Sample weather CSV dataset
│   ├── sample_weather.json   # Sample weather JSON dataset
│   └── google_sheet_sample.csv  # Google Sheets exported data
├── output/
│   └── final_cleaned_data.csv   # Cleaned output after ETL processing
├── .github/
│   └── workflows/
│       └── ci_cd.yml         # GitHub Actions CI/CD pipeline
├── report.pdf                # Technical documentation
└── ETL_Pipeline_Project_Report.pdf  # Detailed project report
```

## ETL Pipeline Stages

### 1. Extract (`extract_data`)
- Reads CSV files using Pandas
- Parses local JSON weather data
- Fetches live weather data from the OpenWeatherMap REST API

### 2. Clean (`clean_data`)
- Merges CSV and Google Sheets datasets via `pd.concat`
- Appends real-time API weather data as a new row
- Drops rows with missing `temperature`, `humidity`, or `wind_speed`
- Removes duplicate records
- Converts Fahrenheit values (>50) to Celsius automatically

### 3. Transform (`transform_data`)
- Normalizes timestamps to UTC via `pd.to_datetime` with timezone localization
- Engineers a `weather_impact_score` feature: average of temperature, humidity, and wind speed

### 4. Load (`load_data_to_db`)
- Connects to a Neon PostgreSQL database using SQLAlchemy + psycopg2
- Writes the final DataFrame to the `final_table` table (replaces on each run)

## CI/CD Pipeline

Defined in `.github/workflows/ci_cd.yml` — triggered on push to the `master` branch:

1. Checks out the repository
2. Sets up Python 3.9
3. Installs dependencies from `requirements.txt`
4. Runs `etl_pipeline.py`
5. Runs `load_to_db.py`

## Scheduling

`scheduler.py` uses the `schedule` library to run the full ETL pipeline daily at **02:00 AM**. It invokes both `etl_pipeline.py` and `load_to_db.py` as subprocesses with incremental timestamps.

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd etl-pipline
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure settings**
   Update `config/db_config.json` with your own database credentials and OpenWeatherMap API key:
   ```json
   {
     "db_type": "postgresql",
     "user": "<your-db-user>",
     "password": "<your-db-password>",
     "host": "<your-db-host>",
     "port": 5432,
     "database": "<your-db-name>",
     "openweathermap_api_key": "<your-api-key>",
     "city": "New York"
   }
   ```

4. **Run the ETL pipeline**
   ```bash
   python etl_pipeline.py
   ```

5. **Or start the scheduler for automated daily runs**
   ```bash
   python scheduler.py
   ```

## Dependencies

```
numpy
pandas
requests
sqlalchemy
schedule
pytest
pydantic
python-dotenv
psycopg2
psycopg2-binary
pymongo
```
- Monitor the output directory for the cleaned data file after execution.

## CI/CD Integration
This project includes a CI/CD pipeline defined in `.github/workflows/ci_cd.yml`, which automates testing and deployment processes. Ensure that your GitHub repository is set up to utilize GitHub Actions for continuous integration and delivery.

## Conclusion
This ETL pipeline project serves as a robust framework for data processing and integration, leveraging various data sources and automation techniques to streamline workflows. For further details, refer to the `report.pdf` for technical documentation and design explanations.