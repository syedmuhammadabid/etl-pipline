import schedule
import time
import subprocess

def run_etl_pipeline():
    subprocess.run(["python", "etl_pipeline.py"])

# Schedule the ETL pipeline to run daily at a specified time
schedule.every().day.at("02:00").do(run_etl_pipeline)

while True:
    schedule.run_pending()
    time.sleep(1)