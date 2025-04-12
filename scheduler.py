import schedule
import time
import subprocess
from datetime import datetime

def run_etl():
    print("⏳ Starting ETL pipeline with incremental approach...")
    last_run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Pass the last run time as an argument to the ETL pipeline
    subprocess.run(["python", "etl_pipeline.py", "--last_run_time", last_run_time])
    print("✅ ETL pipeline completed.")

    print("⏳ Loading incremental data to database...")
    # Pass the last run time as an argument to the database loading script
    subprocess.run(["python", "load_to_db.py", "--last_run_time", last_run_time])
    print("✅ Incremental data loading completed.")

# Schedule the ETL to run daily at 2 AM
schedule.every().day.at("02:00").do(run_etl)

print("🕒 Scheduler started. Waiting for the next run...")

while True:
    schedule.run_pending()
    time.sleep(1)
