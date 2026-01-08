import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

from backend.ml.preprocess import preprocess_df


BASE = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE, "..", "..", "data", "StudentsPerformance.csv")
MODEL_PATH = os.path.join(BASE, "model.pkl")


# -----------------------------
# TRAINING (run once)
# -----------------------------
def train_model():
    df = pd.read_csv(DATA_PATH)
    df = preprocess_df(df)

    X = df[["attendance", "avg_marks", "assignment_completion", "behavior_score"]]
    y = df["risk_level"]

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded,
        test_size=0.2,
        stratify=y_encoded,
        random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )
    model.fit(X_train, y_train)

    joblib.dump(
        {
            "model": model,
            "label_encoder": le
        },
        MODEL_PATH
    )

    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))


# -----------------------------
# LOAD MODEL (runtime)
# -----------------------------
_model_bundle = None

def load_model():
    global _model_bundle
    if _model_bundle is None:
        _model_bundle = joblib.load(MODEL_PATH)
    return _model_bundle


# -----------------------------
# PREDICT RISK (used by Gemini)
# -----------------------------
def predict_risk(student):
    """
    student = {
        attendance,
        marks (avg_marks),
        assignments,
        behavior
    }
    """
    bundle = load_model()
    model = bundle["model"]
    le = bundle["label_encoder"]

    X = pd.DataFrame([{
        "attendance": student["attendance"],
        "avg_marks": student["marks"],
        "assignment_completion": student["assignments"],
        "behavior_score": student["behavior"]
    }])

    pred_encoded = model.predict(X)[0]
    risk_label = le.inverse_transform([pred_encoded])[0]

    return risk_label


if __name__ == "__main__":
    train_model()

