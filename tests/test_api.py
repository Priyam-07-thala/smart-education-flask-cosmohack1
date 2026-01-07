import io
import os
from backend.app import app


def test_api_student_improvements_file_upload():
    client = app.test_client()
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_student_1.csv")
    with open(csv_path, "rb") as f:
        data = {"file": (f, "sample_student_1.csv")}
        resp = client.post("/api/student_improvements", data=data, content_type="multipart/form-data")

    assert resp.status_code == 200
    js = resp.get_json()
    assert isinstance(js, list) or isinstance(js, dict)
    payload = js[0] if isinstance(js, list) else js.get("summaries", [])[0]
    assert "needs_improvement" in payload


def test_api_student_feedback_flag(monkeypatch):
    # Patch the get_student_feedback helper to avoid network calls
    from backend.app import app

    def fake_feedback(name, score):
        return f"Fake feedback for {name} ({score})"

    monkeypatch.setattr("backend.ml.gemini_client.get_student_feedback", fake_feedback)

    client = app.test_client()
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_student_1.csv")
    with open(csv_path, "rb") as f:
        data = {"file": (f, "sample_student_1.csv")}
        resp = client.post("/api/student_improvements?feedback=1", data=data, content_type="multipart/form-data")

    assert resp.status_code == 200
    js = resp.get_json()
    # top-level dict with 'summaries'
    assert "summaries" in js
    assert "feedback" in js["summaries"][0]