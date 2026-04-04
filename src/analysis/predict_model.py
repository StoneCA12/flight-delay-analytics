import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

from config import PROCESSED_PATH


def categorize_delay(delay):
    if pd.isna(delay):
        return None
    if delay <= 5:
        return "On Time"
    elif 6 < delay <= 15:
        return "Small Delay"
    else:
        return "Delayed"


def prepare_features(df):
    df = df.copy()
    # Keep only rows with required values
    df = df.dropna(subset=["carrier", "airport", "month", "delay"])
    # Create target label from delay column
    df["label"] = df["delay"].apply(categorize_delay)
    # Drop rows where label could not be created
    df = df.dropna(subset=["label"])
    X = df[["carrier", "airport", "month"]].copy()
    y = df["label"]

    # Encode text features into numeric values
    carrier_encoder = LabelEncoder()
    airport_encoder = LabelEncoder()
    month_encoder = LabelEncoder()

    X["carrier"] = carrier_encoder.fit_transform(X["carrier"])
    X["airport"] = airport_encoder.fit_transform(X["airport"])
    X["month"] = month_encoder.fit_transform(X["month"])

    return X, y, carrier_encoder, airport_encoder, month_encoder


def train_model():
    print("Training model...")
    df = pd.read_csv(PROCESSED_PATH)

    if df.empty:
        print("No data available for training.")
        return None

    X, y, carrier_encoder, airport_encoder, month_encoder = prepare_features(df)

    if len(X) == 0:
        print("No valid rows available for training after cleaning.")
        return None

    print(f"Total rows used for modeling: {len(X)}")
    print("\nLabel distribution:")
    print(y.value_counts())

    if len(X) < 6 or y.nunique() < 2:
        print("Dataset is too small or has only one class, training on full dataset without test split.")
        model = DecisionTreeClassifier(random_state=42)
        model.fit(X, y)
        print("Model trained.")
        return {
            "model": model,
            "carrier_encoder": carrier_encoder,
            "airport_encoder": airport_encoder,
            "month_encoder": month_encoder,
        }

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print(f"Training rows: {len(X_train)}")
    print(f"Testing rows: {len(X_test)}")

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Model accuracy: {accuracy:.2f}")
    print("\nClassification report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    results = pd.DataFrame({
        "actual": y_test.values,
        "predicted": y_pred
    })

    print("\nSample predictions:")
    print(results.head())
    print("Model trained.")

    return {
        "model": model,
        "carrier_encoder": carrier_encoder,
        "airport_encoder": airport_encoder,
        "month_encoder": month_encoder,
    }