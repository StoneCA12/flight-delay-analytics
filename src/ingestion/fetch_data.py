import os
import pandas as pd
import requests

from config import USE_API, API_KEY, API_BASE_URL, RAW_PATH, SAMPLE_PATH


def get_sample_data():
    return pd.read_csv(SAMPLE_PATH).to_dict(orient="records")


def calculate_delay_minutes(scheduled_departure, actual_departure):
    if not scheduled_departure or not actual_departure:
        return None

    try:
        scheduled_dt = pd.to_datetime(scheduled_departure, utc=True)
        actual_dt = pd.to_datetime(actual_departure, utc=True)
        delay_minutes = int((actual_dt - scheduled_dt).total_seconds() / 60)
        return delay_minutes
    except Exception:
        return None


def get_api_data():
    params = {
        "access_key": API_KEY,
        "limit": 10000,
        "flight_status": "landed"
    }

    response = requests.get(API_BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    records = payload.get("data", [])

    cleaned_records = []

    month_map = {
        "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
        "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
        "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
    }

    for record in records:
        airline_info = record.get("airline") or {}
        departure_info = record.get("departure") or {}

        carrier = airline_info.get("name")
        airport = departure_info.get("airport")
        scheduled_departure = departure_info.get("scheduled")
        actual_departure = departure_info.get("actual")

        delay = calculate_delay_minutes(scheduled_departure, actual_departure)

        source_date = None
        if scheduled_departure and len(scheduled_departure) >= 10:
            source_date = scheduled_departure[:10]
        else:
            flight_date = record.get("flight_date")
            if flight_date and len(flight_date) >= 10:
                source_date = flight_date[:10]

        date = None
        day = None
        month = None

        if source_date:
            date = source_date
            day = source_date[8:10]
            month_num = source_date[5:7]
            month = month_map.get(month_num)

        cleaned_records.append({
            "carrier": carrier,
            "airport": airport,
            "scheduled_departure": scheduled_departure,
            "actual_departure": actual_departure,
            "delay": delay,
            "date": date,
            "day": day,
            "month": month
        })

    return cleaned_records


def fetch_data():
    print("Fetching data...")
    os.makedirs("data/raw", exist_ok=True)

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

    print("\nSample raw records:")
    for row in data[:2]:
        print(row)
    df = pd.DataFrame(data)
    print("\nPreview cleaned data (first 2 rows):")
    print(df.head(2))
    df.to_csv(RAW_PATH, index=False)

    print(f"Saved raw data to {RAW_PATH}")


if __name__ == "__main__":
    fetch_data()