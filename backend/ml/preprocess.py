import pandas as pd
import numpy as np

# =============================
# RISK ASSIGNMENT (CONSISTENT)
# =============================
def assign_risk(row):
    """
    Deterministic heuristic risk assignment
    Output labels: Low / Medium / High
    """

    score = (
        0.4 * row["avg_marks"] +
        0.25 * row["attendance"] +
        0.2 * row["assignment_completion"] +
        0.15 * (row["behavior_score"] * 10)
    )

    if score >= 75:
        return "Low"
    elif score >= 55:
        return "Medium"
    else:
        return "High"


# =============================
# MAIN PREPROCESSING PIPELINE
# =============================
def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw student CSV and produces ML-ready dataframe
    """

    df = df.copy()

    # ---- Average Marks ----
    if all(col in df.columns for col in ["math score", "reading score", "writing score"]):
        df["avg_marks"] = df[["math score", "reading score", "writing score"]].mean(axis=1)
    elif "avg_marks" in df.columns:
        df["avg_marks"] = df["avg_marks"]
    else:
        raise ValueError("No marks data available")

    # ---- Attendance (safe fallback) ----
    if "attendance" not in df.columns:
        df["attendance"] = df["avg_marks"].clip(50, 100)

    # ---- Assignment Completion ----
    if "assignment_completion" not in df.columns:
        df["assignment_completion"] = df["avg_marks"].clip(40, 100)

    # ---- Behavior Score ----
    if "behavior_score" not in df.columns:
        if "test preparation course" in df.columns:
            df["behavior_score"] = df["test preparation course"].apply(
                lambda x: 8 if x == "completed" else 5
            )
        else:
            df["behavior_score"] = 6  # neutral default

    # ---- Normalize numeric ranges ----
    df["attendance"] = df["attendance"].clip(0, 100)
    df["assignment_completion"] = df["assignment_completion"].clip(0, 100)
    df["behavior_score"] = df["behavior_score"].clip(1, 10)

    # ---- Risk Label ----
    df["risk_level"] = df.apply(assign_risk, axis=1)

    return df


# =============================
# STUDENT LOOKUP (OPTIONAL)
# =============================
def get_student_by_id(student_id, df):
    row = df[df["student_id"].astype(str) == str(student_id)]
    if row.empty:
        return None

    r = row.iloc[0]
    return {
        "attendance": float(r["attendance"]),
        "marks": float(r["avg_marks"]),
        "assignments": float(r["assignment_completion"]),
        "behavior": float(r["behavior_score"]),
        "risk_level": r["risk_level"]
    }


# =============================
# ANALYTICS FOR GEMINI (SAFE)
# =============================
def summarize_students(df):
    """
    Lightweight analytics summary for explainable AI
    """

    summaries = []

    for _, row in df.iterrows():
        needs = []

        if row["avg_marks"] < 60:
            needs.append("Academic performance is below average")

        if row["attendance"] < 85:
            needs.append("Attendance needs improvement")

        if row["assignment_completion"] < 70:
            needs.append("Assignments are frequently incomplete")

        if row["behavior_score"] < 6:
            needs.append("Low engagement or behavior issues")

        summaries.append({
            "student_id": row.get("student_id"),
            "risk_level": row["risk_level"],
            "issues": needs
        })

    return summaries
