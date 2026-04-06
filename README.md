# Flight Delay Analytics Pipeline

## Overview

This project builds an end-to-end data analytics pipeline to analyze flight delays across Canadian airlines and airports.

The pipeline covers the full workflow:
- data fetching (API or sample data)
- data cleaning (ETL)
- data storage (SQLite and BigQuery)
- analysis using SQL
- visualization using Tableau

The goal is to understand how delays vary across carriers, airports, and time.

---

## How to run the pipeline

### 1. Install dependencies

Make sure Python is installed, then run: pip install -r requirements.txt

---

### 2. (Optional) Set API key

Create a `.env` file in the root folder with content: AVIATIONSTACK_API_KEY=your_api_key_here

If no API key is provided, the pipeline will use the sample dataset.

---

### 3. Run the pipeline

python main.py

---

## What the pipeline does

When you run the pipeline, it will:

1. Fetch data  
   - from API (if key is provided)  
   - otherwise from sample CSV  

2. Clean the data  
   - convert timestamps  
   - calculate delay  
   - remove missing or invalid records  

3. Save cleaned data  
   - as CSV (`data/processed/flights_clean.csv`)  
   - into SQLite database (`data/flights.db`)  

4. Run analysis  
   - average delay by carrier  
   - delay by airport  
   - monthly and daily trends  

5. Generate output files for Tableau  

---

## Output files

After running the pipeline, you will see files in: data/processed/ 
Main outputs include:

- flights_clean.csv  
- carrier_stats.csv  
- airport_stats.csv  
- monthly_trend.csv  
- daily_trend.csv  
- delay_distribution.csv  

These files are used for visualization.

---

## Cloud (BigQuery)

The cleaned dataset can also be uploaded to BigQuery.

We use BigQuery to:
- store data in the cloud  
- run SQL queries  
- show that the pipeline can scale beyond local database  

---

## Machine learning

A simple Decision Tree model is used to classify delays into:
- On Time  
- Small Delay  
- Delayed  

This is just to demonstrate how prediction can be added to the pipeline.

---

## Notes

- API has limited data (free tier), so sample data is used for testing  
- Pipeline can be extended with more data sources later  
- Tableau dashboard uses the generated CSV files  

---

## Authors

Bao Tran  
Ahmed Maruf


