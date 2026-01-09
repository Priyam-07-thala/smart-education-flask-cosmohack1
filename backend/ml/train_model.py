import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

from backend.ml.preprocess import preprocess_df


# =============================
# PATHS
# =============================
BASE = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE, "..", "..", "data", "StudentsPerformance.csv")
MODEL_PATH = os.path.join(BASE, "model.pkl")


# =============================
# TRAIN MODEL (RUN ONCE)
# =============================
def train_model():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("Training dataset not found")

    df = pd.read_csv(DATA_PATH)
    df = preprocess_df(df)

    FEATURES = [
        "attendance",
        "avg_marks",
        "assignment_completion",
        "behavior_score"
    ]

    X = df[FEATURES]
    y = df["risk_level"].astype(str)

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=0.2,
        stratify=y_encoded,
        random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\nModel Evaluation")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    joblib.dump(
        {
            "model": model,
            "label_encoder": le,
            "features": FEATURES,
            "version": "v1.0"
        },
        MODEL_PATH
    )

    print(f"\nModel saved at: {MODEL_PATH}")


# =============================
# LOAD MODEL (SAFE)
# =============================
_model_bundle = None

def load_model():
    global _model_bundle

    if _model_bundle is None:
        if not os.path.exists(MODEL_PATH):
            train_model()
        _model_bundle = joblib.load(MODEL_PATH)

    return _model_bundle


# =============================
# PREDICT RISK (RUNTIME)
# =============================
def predict_risk(student):
    """
    student = {
        attendance: float,
        marks: float,
        assignments: float,
        behavior: float
    }
    """

    bundle = load_model()
    model = bundle["model"]
    le = bundle["label_encoder"]
    features = bundle["features"]

    # Validate & sanitize input
    row = {
        "attendance": float(student.get("attendance", 0)),
        "avg_marks": float(student.get("marks", 0)),
        "assignment_completion": float(student.get("assignments", 0)),
        "behavior_score": float(student.get("behavior", 0))
    }

    X = pd.DataFrame([row], columns=features)

    pred_encoded = model.predict(X)[0]
    risk_label = le.inverse_transform([pred_encoded])[0]

    # Normalize labels for UI
    risk_map = {
        "low": "Low",
        "medium": "Medium",
        "high": "High"
    }

    return risk_map.get(risk_label.lower(), risk_label)


# =============================
# CLI TRAINING
# =============================
if __name__ == "__main__":
    train_model()

