import pandas as pd
import json
import requests
from sqlalchemy import create_engine
from datetime import datetime

def read_csv(file_path):
    return pd.read_csv(file_path)

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def fetch_weather_data_from_api(api_key, city):
    """
    Fetch weather data from OpenWeatherMap API.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from OpenWeatherMap API. Status code: {response.status_code}")

def extract_data():
    # Load API key and city from config
    with open('config/db_config.json') as config_file:
        config = json.load(config_file)
    api_key = config['openweathermap_api_key']
    city = config['city']

    # Fetch data from OpenWeatherMap API
    weather_data_api = fetch_weather_data_from_api(api_key, city)

    # Read other data sources
    csv_data = read_csv('data/sample_data.csv')
    weather_data_file = read_json('data/sample_weather.json')
    google_sheet_data = read_csv('data/google_sheet_sample.csv')

    print("Data extraction complete.")
    print("CSV Data:", csv_data.head())
    print("Weather Data from File:", weather_data_file)
    print("Google Sheet Data:", google_sheet_data.head())
    print("Weather Data from API:", weather_data_api)

    return csv_data, weather_data_file, google_sheet_data, weather_data_api

def clean_data(csv_data, weather_data_file, google_sheet_data, weather_data_api):
    # Combine datasets
    combined_data = pd.concat([csv_data, google_sheet_data], ignore_index=True)
    
    # Add weather data from API
    weather_api_df = pd.DataFrame([{
        'temperature': weather_data_api['main']['temp'],
        'humidity': weather_data_api['main']['humidity'],
        'wind_speed': weather_data_api['wind']['speed'],
        'timestamp': datetime.utcfromtimestamp(weather_data_api['dt']).isoformat()
    }])
    combined_data = pd.concat([combined_data, weather_api_df], ignore_index=True)

    # Handle missing values
    combined_data.dropna(inplace=True)
    
    # Remove duplicates
    combined_data.drop_duplicates(inplace=True)
    
    # Example of correcting erroneous values
    combined_data['temperature'] = combined_data['temperature'].apply(lambda x: (x - 32) * 5.0/9.0 if x > 50 else x)  # Fahrenheit to Celsius if needed

    print("Data cleaning complete.", combined_data.head())

    return combined_data

def transform_data(cleaned_data):
    # Normalize datetime
    cleaned_data['timestamp'] = pd.to_datetime(cleaned_data['timestamp']).dt.tz_localize('UTC').dt.tz_convert('UTC')
    
    # Feature engineering: Create a weather impact score
    cleaned_data['weather_impact_score'] = (cleaned_data['temperature'] + cleaned_data['humidity'] + cleaned_data['wind_speed']) / 3
    
    print("Data transformation complete.", cleaned_data.head())

    return cleaned_data

def load_data_to_db(cleaned_data):
    with open('config/db_config.json') as config_file:
        db_config = json.load(config_file)

    # Extract the endpoint ID from the host
    endpoint_id = db_config['host'].split('.')[0]

    # Create the connection string with the endpoint ID
    connection_string = (
        f"postgresql+psycopg2://{db_config['user']}:endpoint={endpoint_id};{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?"
        f"sslmode=require"
    )

    # Create the SQLAlchemy engine
    engine = create_engine(connection_string)

    # Load the DataFrame to the specified table
    cleaned_data.to_sql('final_table', con=engine, if_exists='replace', index=False)
    print("Data loaded to PostgreSQL successfully.")

def main():
    csv_data, weather_data_file, google_sheet_data, weather_data_api = extract_data()
    cleaned_data = clean_data(csv_data, weather_data_file, google_sheet_data, weather_data_api)
    transformed_data = transform_data(cleaned_data)
    load_data_to_db(transformed_data)

if __name__ == "__main__":
    main()