import os
from dotenv import load_dotenv

load_dotenv()

USE_API = False #True for real API, False for sample data
API_KEY = os.getenv("AVIATIONSTACK_API_KEY", "")
API_BASE_URL = "https://api.aviationstack.com/v1/flights"

RAW_PATH = "data/raw/flights_raw.csv"
SAMPLE_PATH = "data/raw/sample_flights.csv"
PROCESSED_PATH = "data/processed/flights_clean.csv"
DB_PATH = "data/flights.db"
OUTPUT_DIR = "data/processed"