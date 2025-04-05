# ETL Pipeline Project

## Overview
This ETL (Extract, Transform, Load) pipeline project is designed to automate the process of gathering data from various sources, transforming it into a usable format, and loading it into a SQL database. The project utilizes Python for scripting and includes various data sources such as CSV files, JSON data from APIs, and Google Sheets.

## Project Structure
The project is organized into the following directories and files:

- **etl_pipeline.py**: The main script that orchestrates the ETL process.
- **config/db_config.json**: Contains database configuration settings and API keys.
- **data/**: Directory containing sample datasets for extraction:
  - **sample_data.csv**: Example structured dataset.
  - **sample_weather.json**: Weather data sourced from an API.
  - **google_sheet_sample.csv**: Exported Google Sheets data.
- **scheduler.py**: Script for scheduling the ETL pipeline execution.
- **requirements.txt**: Lists the required Python packages for the project.
- **output/**: Directory for processed output data.
  - **final_cleaned_data.csv**: Contains the cleaned data after ETL processing.
- **load_to_db.py**: Handles the loading of cleaned data into the SQL database.
- **.github/workflows/ci_cd.yml**: Configuration for CI/CD using GitHub Actions.
- **report.pdf**: Advanced technical documentation of the project.

## Setup Instructions
1. **Clone the Repository**: 
   Clone this repository to your local machine using:
   ```
   git clone <repository-url>
   ```

2. **Install Dependencies**: 
   Navigate to the project directory and install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. **Configure Database Settings**: 
   Update the `config/db_config.json` file with your database connection details and API keys.

4. **Run the ETL Pipeline**: 
   Execute the main ETL script:
   ```
   python etl_pipeline.py
   ```

5. **Schedule the Pipeline**: 
   Use `scheduler.py` to set up a schedule for the ETL process to run at specified intervals.

## Usage Guidelines
- Ensure that the data sources are accessible and correctly formatted.
- Modify the transformation logic in `etl_pipeline.py` as needed to suit your data processing requirements.
- Monitor the output directory for the cleaned data file after execution.

## CI/CD Integration
This project includes a CI/CD pipeline defined in `.github/workflows/ci_cd.yml`, which automates testing and deployment processes. Ensure that your GitHub repository is set up to utilize GitHub Actions for continuous integration and delivery.

## Conclusion
This ETL pipeline project serves as a robust framework for data processing and integration, leveraging various data sources and automation techniques to streamline workflows. For further details, refer to the `report.pdf` for technical documentation and design explanations.