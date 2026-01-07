import pandas as pd
from backend.ml.preprocess import summarize_students


def test_sample_student_summary():
    df = pd.read_csv("data/sample_student_1.csv")
    summaries = summarize_students(df)
    assert len(summaries) == 1

    s = summaries[0]
    assert s["student_id"] in ["S021", "s021", "021", "S21"] or s["name"] == "sam"

    params = [n["parameter"] for n in s["needs_improvement"]]
    # sample_student_1.csv has attendance 89 -> should be flagged
    assert "attendance" in params
    assert s["overall_risk"] == "low"