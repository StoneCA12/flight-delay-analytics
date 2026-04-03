from src.ingestion.fetch_data import fetch_data
from src.transformation.clean_data import clean_data
from src.transformation.save_to_db import save_to_db
from src.analysis.analyze import analyze_data
from src.analysis.predict_model import train_model

def run_pipeline():
    print("\n--- Running Pipeline ---\n")

    fetch_data()
    clean_data()
    save_to_db()
    analyze_data()
    train_model()

    print("\n--- Pipeline Complete ---\n")

if __name__ == "__main__":
    run_pipeline()