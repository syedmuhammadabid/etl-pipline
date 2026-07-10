import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def load_data_to_db(dataframe, table_name):
    host = os.environ['DB_HOST']
    user = os.environ['DB_USER']
    password = os.environ['DB_PASSWORD']
    port = os.environ.get('DB_PORT', '5432')
    database = os.environ['DB_NAME']

    # Extract the endpoint ID from the host
    endpoint_id = host.split('.')[0]

    # Create the database engine
    engine = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}?"
        f"sslmode=require&options=endpoint%3D{endpoint_id}"
    )

    # Load the DataFrame to the specified table
    dataframe.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"Data loaded to {table_name} table successfully.")

if __name__ == "__main__":
    # Example usage
    cleaned_data_path = 'output/final_cleaned_data.csv'
    table_name = 'cleaned_data'

    # Load cleaned data
    cleaned_data = pd.read_csv(cleaned_data_path)
    load_data_to_db(cleaned_data, table_name)