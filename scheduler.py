import schedule
import time
import subprocess

def run_etl():
    print("⏳ Starting ETL pipeline...")
    subprocess.run(["python", "etl_pipeline.py"])
    print("✅ ETL pipeline completed.")

    print("⏳ Loading data to database...")
    subprocess.run(["python", "load_to_db.py"])
    print("✅ Data loading completed.")

# Schedule the ETL to run daily at 2 AM
schedule.every().day.at("02:00").do(run_etl)

print("🕒 Scheduler started. Waiting for the next run...")

while True:
    schedule.run_pending()
    time.sleep(1)
