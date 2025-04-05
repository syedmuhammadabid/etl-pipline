from sqlalchemy import create_engine
import pandas as pd
import json

def load_data_to_db(dataframe, table_name, db_config_path='config/db_config.json'):
    with open(db_config_path) as config_file:
        config = json.load(config_file)

    # Create a database connection
    engine = create_engine(f"{config['db_type']}://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}")

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