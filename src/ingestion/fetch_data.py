import os
import pandas as pd
import requests

from config import USE_API, API_KEY, API_BASE_URL, RAW_PATH


def get_sample_data():
    return [
        {"carrier": "Air Canada", "airport": "YVR", "delay": 10, "month": "Jan"},
        {"carrier": "WestJet", "airport": "YYZ", "delay": 5, "month": "Jan"},
        {"carrier": "Air Canada", "airport": "YYZ", "delay": 20, "month": "Feb"},
        {"carrier": "WestJet", "airport": "YVR", "delay": 30, "month": "Feb"},
        {"carrier": "Air Canada", "airport": "YVR", "delay": 3, "month": "Mar"}
    ]


def get_api_data():
    params = {
        "access_key": API_KEY,
        "limit": 100
    }

    response = requests.get(API_BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    records = payload.get("data", [])
    cleaned_records = []

    for record in records:
        airline_info = record.get("airline") or {}
        departure_info = record.get("departure") or {}
        flight_date = record.get("flight_date")

        carrier = airline_info.get("name")
        airport = departure_info.get("airport")
        delay = departure_info.get("delay")
        month = None

        if flight_date and len(flight_date) >= 7:
            month_num = flight_date[5:7]
            month_map = {
                "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
                "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
                "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
            }
            month = month_map.get(month_num)

        cleaned_records.append({
            "carrier": carrier,
            "airport": airport,
            "delay": delay,
            "month": month
        })

    return cleaned_records


def fetch_data():
    print("Fetching data...")
    os.makedirs("data/raw", exist_ok=True)
    data = None

    if USE_API and API_KEY:
        try:
            print("Using API mode...")
            data = get_api_data()
            print("API data fetched successfully.")
        except Exception as e:
            print(f"API fetch failed: {e}")
            print("Falling back to sample data...")
            data = get_sample_data()
    else:
        print("Using sample data mode...")
        data = get_sample_data()

    df = pd.DataFrame(data)
    df.to_csv(RAW_PATH, index=False)

    print(f"Saved raw data to {RAW_PATH}")