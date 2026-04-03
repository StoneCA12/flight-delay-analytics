import os

USE_API = False
API_KEY = os.getenv("AVIATIONSTACK_API_KEY", "")
API_BASE_URL = "https://api.aviationstack.com/v1/flights"
RAW_PATH = "data/raw/flights_raw.csv"
PROCESSED_PATH = "data/processed/flights_clean.csv"
DB_PATH = "data/flights.db"
OUTPUT_DIR = "data/processed"