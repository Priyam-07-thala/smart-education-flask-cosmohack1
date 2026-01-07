import pandas as pd

def assign_risk(row):
    score = (
        0.4 * row["avg_marks"] +
        0.25 * row["attendance"] +
        0.2 * row["assignment_completion"] +
        0.15 * (row["behavior_score"] * 10)
    )

    if score >= 85:
        return "Very Low"
    elif score >= 70:
        return "Low"
    elif score >= 50:
        return "Medium"
    else:
        return "High"


def preprocess_df(df):
    df = df.copy()

    df["avg_marks"] = df[["math score","reading score","writing score"]].mean(axis=1)

    import numpy as np
    df["attendance"] = np.clip(df["avg_marks"] + np.random.normal(0, 5, len(df)), 50, 100)
    df["assignment_completion"] = np.clip(df["avg_marks"] + np.random.normal(0, 10, len(df)), 40, 100)

    df["behavior_score"] = df["test preparation course"].apply(
        lambda x: 8 if x == "completed" else 5
    )

    df["risk_level"] = df.apply(assign_risk, axis=1)
    return df


def summarize_students(df):
    """Return a list of student summary dicts with heuristic improvement flags.

    This function is tolerant of different input CSV schemas. It attempts to
    normalize fields to: student_id, name, math, reading, writing, attendance,
    assignment_completion, behavior_score, avg_marks.
    """
    import numpy as np

    df = df.copy()

    # Normalize common fields
    if "student_id" not in df.columns:
        df["student_id"] = df.index.astype(str)
    if "name" not in df.columns:
        df["name"] = df["student_id"].astype(str)

    # If the three subject columns are present, use them; otherwise fallback to avg_marks
    subject_cols = [c for c in ["math score", "reading score", "writing score"] if c in df.columns]
    if len(subject_cols) == 3:
        df["math"] = df["math score"]
        df["reading"] = df["reading score"]
        df["writing"] = df["writing score"]
        subject_series = df[["math", "reading", "writing"]].mean(axis=1)
    else:
        # use avg_marks if available
        if "avg_marks" not in df.columns:
            df["avg_marks"] = df.get("avg_marks", df.get("avg mark", np.nan))
        df["math"] = df["avg_marks"]
        df["reading"] = df["avg_marks"]
        df["writing"] = df["avg_marks"]
        subject_series = df["avg_marks"]

    # Standard columns fallbacks
    df["attendance"] = df.get("attendance", df.get("att", np.nan))
    df["assignment_completion"] = df.get("assignment_completion", df.get("assignment completion", df.get("homework", np.nan)))
    df["behavior_score"] = df.get("behavior_score", df.get("behavior", df.get("behavior rating", np.nan)))

    # Compute class-level stats for subjects
    class_mean = subject_series.mean()
    class_std = subject_series.std(ddof=0) if not np.isnan(subject_series.std(ddof=0)) else 0

    summaries = []
    for _, row in df.iterrows():
        needs = []

        # Subjects: flag if below mean - 1*std or below absolute threshold 50
        for subj in ["math", "reading", "writing"]:
            val = row.get(subj, np.nan)
            if np.isnan(val):
                continue
            why = None
            if val < class_mean - class_std:
                why = f"{subj} is below class average by more than 1 std ({val:.1f} < {class_mean - class_std:.1f})"
            elif val < 50:
                why = f"{subj} score is low ({val:.1f} < 50)"

            if why:
                rec = f"Targeted practice in {subj} and formative assessments to monitor progress."
                needs.append({"parameter": subj, "current_value": float(val), "why": why, "recommendation": rec})

        # Attendance
        att = row.get("attendance", np.nan)
        if not np.isnan(att) and att < 90:
            why = f"Attendance below 90% ({att:.1f}%)"
            rec = "Contact guardians, set attendance goals, provide catch-up resources."
            needs.append({"parameter": "attendance", "current_value": float(att), "why": why, "recommendation": rec})

        # Assignment / homework
        ac = row.get("assignment_completion", np.nan)
        if not np.isnan(ac) and ac < 70:
            why = f"Assignment completion low ({ac:.1f}%)"
            rec = "Introduce checkpoints, scaffold assignments, and provide reminders."
            needs.append({"parameter": "assignment_completion", "current_value": float(ac), "why": why, "recommendation": rec})

        # Behavior / engagement
        bs = row.get("behavior_score", np.nan)
        if not np.isnan(bs) and bs < 6:
            why = f"Behavior/engagement score is low ({bs:.1f})"
            rec = "Implement positive behavior supports and engagement strategies."
            needs.append({"parameter": "behavior_score", "current_value": float(bs), "why": why, "recommendation": rec})

        # Overall risk (map existing assign_risk if available)
        risk = None
        try:
            risk = assign_risk(row)
        except Exception:
            # Fallback: derive from avg marks
            avg = row.get("avg_marks", np.nan)
            if not np.isnan(avg):
                if avg >= 85:
                    risk = "Very Low"
                elif avg >= 70:
                    risk = "Low"
                elif avg >= 50:
                    risk = "Medium"
                else:
                    risk = "High"
            else:
                risk = "Medium"

        # Simplify risk label
        overall_risk = "low" if risk in ["Very Low", "Low"] else ("medium" if risk == "Medium" else "high")

        summaries.append({
            "student_id": row.get("student_id"),
            "name": row.get("name"),
            "needs_improvement": needs,
            "overall_risk": overall_risk,
        })

    return summaries

