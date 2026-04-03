import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

from config import PROCESSED_PATH


def categorize_delay(delay):
    """Convert delay minutes into a delay category."""
    if delay <= 5:
        return "On Time"
    elif delay <= 15:
        return "Minor"
    elif delay <= 30:
        return "Moderate"
    else:
        return "Severe"


def prepare_features(df):
    """Prepare features and labels for model training."""
    df = df.copy()

    # Create target label from delay column
    df["label"] = df["delay"].apply(categorize_delay)

    # Select features
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
    """Train and evaluate a simple delay prediction model."""
    print("Training model...")

    df = pd.read_csv(PROCESSED_PATH)

    # Safety check
    if df.empty:
        print("No data available for training.")
        return None

    X, y, carrier_encoder, airport_encoder, month_encoder = prepare_features(df)

    # If dataset is too small, train on all data and skip test split
    if len(df) < 6:
        print("Dataset is very small, training on full dataset without test split.")
        model = DecisionTreeClassifier(random_state=42)
        model.fit(X, y)
        print("Model trained.")
        return {
            "model": model,
            "carrier_encoder": carrier_encoder,
            "airport_encoder": airport_encoder,
            "month_encoder": month_encoder,
        }

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y if y.nunique() > 1 else None
    )

    # Train model
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Predict on test set
    y_pred = model.predict(X_test)

    # Evaluate
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Model accuracy: {accuracy:.2f}")
    print("\nClassification report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    # Show a few prediction examples
    results = pd.DataFrame({
        "actual": y_test.values,
        "predicted": y_pred
    })

    print("Sample predictions:")
    print(results.head())

    print("Model trained.")

    return {
        "model": model,
        "carrier_encoder": carrier_encoder,
        "airport_encoder": airport_encoder,
        "month_encoder": month_encoder,
    }