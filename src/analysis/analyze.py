import pandas as pd
import sqlite3
import os

DB_PATH = "data/flights.db"
OUTPUT_DIR = "data/processed/"

def analyze_data():
    print("Running analysis...")

    conn = sqlite3.connect(DB_PATH)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    carrier = pd.read_sql_query("""
        SELECT carrier, AVG(delay) as avg_delay, COUNT(*) as num_flights
        FROM flights
        GROUP BY carrier
    """, conn)

    airport = pd.read_sql_query("""
        SELECT airport, AVG(delay) as avg_delay, COUNT(*) as num_flights
        FROM flights
        GROUP BY airport
    """, conn)

    monthly = pd.read_sql_query("""
        SELECT month, AVG(delay) as avg_delay, COUNT(*) as num_flights
        FROM flights
        GROUP BY month
    """, conn)

    carrier.to_csv(OUTPUT_DIR + "carrier_stats.csv", index=False)
    airport.to_csv(OUTPUT_DIR + "airport_stats.csv", index=False)
    monthly.to_csv(OUTPUT_DIR + "monthly_trend.csv", index=False)

    conn.close()

    print("Analysis complete.")