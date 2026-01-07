import pytest


def test_get_student_feedback_fallback(monkeypatch):
    from backend.ml.gemini_client import get_student_feedback

    # No Gemini available in test env, use fallback messages
    assert "Needs focused improvement" in get_student_feedback("A", 0.9)
    assert "Progressing" in get_student_feedback("B", 0.4)
    assert "Doing well" in get_student_feedback("C", 0.1)


def test_rank_students_by_need_fallback():
    from backend.ml.gemini_client import rank_students_by_need

    summaries = [
        {"name": "Alice", "overall_risk": "low"},
        {"name": "Bob", "overall_risk": "high"},
        {"name": "Cara", "overall_risk": "medium"},
    ]

    out = rank_students_by_need(summaries)
    assert "Priority for support" in out
    assert "Bob" in out
