import os
from dotenv import load_dotenv

# Optional - use official google generative AI SDK when available
# pip install google-generativeai
try:
    import google.generativeai as genai
except Exception:
    genai = None

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = os.getenv("GEMINI_ENDPOINT", None)

if genai and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception:
        # some versions use different config methods; ignore and rely on env
        pass


def get_student_feedback(name: str, risk_score: float, model_name: str = "gemini-pro") -> str:
    """Return a short 1-2 line motivating feedback for a single student.

    Falls back to a simple heuristic message if Gemini isn't available.
    """
    prompt = f"""
You are an education mentor.
A student named {name} has a performance risk score of {risk_score}.

Score Meaning:
0–0.3  = Low risk
0.3–0.6 = Medium risk
0.6–1.0 = High risk

In 1–2 lines:
- say whether the student needs improvement urgently or not
- keep tone positive & motivating
Return only the short text.
"""

    # Use SDK when available
    if genai:
        try:
            model = genai.GenerativeModel(model_name)
            resp = model.generate_content(prompt)
            # Newer SDKs may return structured objects; attempt to extract
            if hasattr(resp, "text"):
                return resp.text.strip()
            # resp may be a dict
            if isinstance(resp, dict):
                # attempt common keys
                return resp.get("output", resp.get("text", "")).strip()
        except Exception:
            pass

    # Heuristic fallback
    if risk_score >= 0.6:
        return f"Needs focused improvement soon; set short-term goals and provide targeted practice."
    elif risk_score >= 0.3:
        return f"Progressing but could benefit from consistent practice and monitoring."
    else:
        return f"Doing well — keep building consistency and challenge opportunities."


def rank_students_by_need(summaries: list, model_name: str = "gemini-pro") -> str:
    """Ask Gemini to rank students by who needs improvement first and give a short rationale.

    Returns plain text summary. Falls back to a simple heuristic ranking.
    """
    prompt = (
        "Here is student performance risk data:\n\n" + str(summaries) +
        "\n\nRank students by who needs improvement first. Explain briefly in 2-3 lines. Return only text."
    )

    if genai:
        try:
            model = genai.GenerativeModel(model_name)
            resp = model.generate_content(prompt)
            if hasattr(resp, "text"):
                return resp.text.strip()
            if isinstance(resp, dict):
                return resp.get("output", resp.get("text", "")).strip()
        except Exception:
            pass

    # Fallback: sort by overall_risk (high > medium > low) and return top 3 names
    def risk_value(r):
        mapping = {"high": 3, "medium": 2, "low": 1}
        return mapping.get(r.get("overall_risk", "medium"), 2)

    sorted_students = sorted(summaries, key=risk_value, reverse=True)
    top = sorted_students[:3]
    names = [s.get("name") for s in top]
    return f"Priority for support: {', '.join(names)}. Focus on targeted practice and engagement strategies."