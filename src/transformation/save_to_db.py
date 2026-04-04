import pandas as pd
import sqlite3

PROCESSED_PATH = "data/processed/flights_clean.csv"
DB_PATH = "data/flights.db"

def save_to_db():
    print("Saving to database...")
    df = pd.read_csv(PROCESSED_PATH)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("flights", conn, if_exists="replace", index=False)
    conn.close()

    print("Saved to SQLite.")