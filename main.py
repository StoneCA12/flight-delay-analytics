from src.ingestion.fetch_data import fetch_data
from src.transformation.clean_data import clean_data
from src.transformation.save_to_db import save_to_db
from src.analysis.analyze import analyze_data
from src.analysis.predict_model import train_model


def main():
    print("Starting flight delay analytics pipeline...\n")

    fetch_data()
    print()

    clean_data()
    print()

    save_to_db()
    print()

    analyze_data()
    print()

    train_model()
    print()

    print("Pipeline finished successfully.")


if __name__ == "__main__":
    main()