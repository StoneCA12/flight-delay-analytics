import pandas as pd
import os

RAW_PATH = "data/raw/flights_raw.csv"
PROCESSED_PATH = "data/processed/flights_clean.csv"

def clean_data():
    print("Cleaning data...")

    df = pd.read_csv(RAW_PATH).copy()

    df = df.dropna(subset=["delay"])
    df["delay"] = pd.to_numeric(df["delay"], errors="coerce")

    df["carrier"] = df["carrier"].str.strip()
    df["airport"] = df["airport"].str.strip()

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    print("Saved cleaned data.")