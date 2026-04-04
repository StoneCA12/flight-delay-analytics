import os
import pandas as pd

RAW_PATH = "data/raw/flights_raw.csv"
PROCESSED_PATH = "data/processed/flights_clean.csv"


def clean_data():
    print("Cleaning data...")
    df = pd.read_csv(RAW_PATH).copy()

    df["delay"] = pd.to_numeric(df["delay"], errors="coerce")
    print(f"After delay conversion: {len(df)}")

    df = df.dropna(subset=["carrier", "airport", "month", "delay"])
    print(f"After dropna core fields: {len(df)}")

    df["carrier"] = df["carrier"].astype(str).str.strip()
    df["airport"] = df["airport"].astype(str).str.strip()
    df["month"] = df["month"].astype(str).str.strip()

    df = df[
        (df["carrier"] != "") &
        (df["airport"] != "") &
        (df["month"] != "")
    ]
    print(f"After empty string filter: {len(df)}")

    df = df.drop_duplicates()
    print(f"After drop_duplicates: {len(df)}")
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    print("Saved cleaned data.")