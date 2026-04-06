import os
import sqlite3
import pandas as pd

from config import DB_PATH, OUTPUT_DIR


def analyze_data():
    """Run SQL analysis and export Tableau-ready CSV outputs."""
    print("Running analysis...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    # Carrier-level statistics
    carrier_stats = pd.read_sql_query("""
        SELECT
            carrier,
            ROUND(AVG(delay), 2) AS avg_delay,
            MIN(delay) AS min_delay,
            MAX(delay) AS max_delay,
            COUNT(*) AS num_flights
        FROM flights
        WHERE carrier IS NOT NULL
          AND airport IS NOT NULL
          AND delay IS NOT NULL
        GROUP BY carrier
        ORDER BY avg_delay DESC
    """, conn)

    # Airport-level statistics
    airport_stats = pd.read_sql_query("""
        SELECT
            airport,
            ROUND(AVG(delay), 2) AS avg_delay,
            MIN(delay) AS min_delay,
            MAX(delay) AS max_delay,
            COUNT(*) AS num_flights
        FROM flights
        WHERE carrier IS NOT NULL
          AND airport IS NOT NULL
          AND delay IS NOT NULL
        GROUP BY airport
        ORDER BY avg_delay DESC
    """, conn)

    # Monthly trend
    monthly_trend = pd.read_sql_query("""
        SELECT
            month,
            CASE month
                WHEN 'Jan' THEN 1
                WHEN 'Feb' THEN 2
                WHEN 'Mar' THEN 3
                WHEN 'Apr' THEN 4
                WHEN 'May' THEN 5
                WHEN 'Jun' THEN 6
                WHEN 'Jul' THEN 7
                WHEN 'Aug' THEN 8
                WHEN 'Sep' THEN 9
                WHEN 'Oct' THEN 10
                WHEN 'Nov' THEN 11
                WHEN 'Dec' THEN 12
            END AS month_order,
            ROUND(AVG(delay), 2) AS avg_delay,
            MIN(delay) AS min_delay,
            MAX(delay) AS max_delay,
            COUNT(*) AS num_flights
        FROM flights
        WHERE delay IS NOT NULL
          AND month IS NOT NULL
        GROUP BY month
        ORDER BY month_order
    """, conn)

    # Delay distribution
    delay_distribution = pd.read_sql_query("""
        SELECT
            CASE
                WHEN delay < 0 THEN 'Early'
                WHEN delay = 0 THEN 'On Time'
                ELSE 'Delayed'
            END AS delay_category,
            COUNT(*) AS count
        FROM flights
        WHERE delay IS NOT NULL
        GROUP BY delay_category
        ORDER BY count DESC
    """, conn)

    # Carrier + Airport combined statistics
    carrier_airport_stats = pd.read_sql_query("""
        SELECT
            carrier,
            airport,
            ROUND(AVG(delay), 2) AS avg_delay,
            MIN(delay) AS min_delay,
            MAX(delay) AS max_delay,
            COUNT(*) AS num_flights
        FROM flights
        WHERE carrier IS NOT NULL
          AND airport IS NOT NULL
          AND delay IS NOT NULL
        GROUP BY carrier, airport
        ORDER BY avg_delay DESC
    """, conn)

    # Daily trend
    daily_trend = pd.read_sql_query("""
        SELECT
            date,
            ROUND(AVG(delay), 2) AS avg_delay,
            COUNT(*) AS num_flights
        FROM flights
        WHERE date IS NOT NULL
          AND delay IS NOT NULL
        GROUP BY date
        ORDER BY date
    """, conn)

    # Raw flights export for Tableau
    flights_export = pd.read_sql_query("""
        SELECT
            carrier,
            airport,
            scheduled_departure,
            actual_departure,
            delay,
            date,
            day,
            month
        FROM flights
        WHERE carrier IS NOT NULL
          AND airport IS NOT NULL
    """, conn)

    conn.close()

    # Save outputs to CSV files for Tableau
    carrier_stats.to_csv(os.path.join(OUTPUT_DIR, "carrier_stats.csv"), index=False)
    airport_stats.to_csv(os.path.join(OUTPUT_DIR, "airport_stats.csv"), index=False)
    monthly_trend.to_csv(os.path.join(OUTPUT_DIR, "monthly_trend.csv"), index=False)
    delay_distribution.to_csv(os.path.join(OUTPUT_DIR, "delay_distribution.csv"), index=False)
    carrier_airport_stats.to_csv(os.path.join(OUTPUT_DIR, "carrier_airport_stats.csv"), index=False)
    daily_trend.to_csv(os.path.join(OUTPUT_DIR, "daily_trend.csv"), index=False)
    flights_export.to_csv(os.path.join(OUTPUT_DIR, "flights_export.csv"), index=False)

    print("Analysis complete.")
    print("Generated files:")
    print("- carrier_stats.csv")
    print("- airport_stats.csv")
    print("- monthly_trend.csv")
    print("- delay_distribution.csv")
    print("- carrier_airport_stats.csv")
    print("- daily_trend.csv")
    print("- flights_export.csv")