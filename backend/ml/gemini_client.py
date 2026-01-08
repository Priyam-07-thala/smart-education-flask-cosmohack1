import os
import json

try:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
except Exception as e:
    model = None
    print("Gemini init failed:", e)


def generate_explanation(prompt):
    # Fallback if Gemini is unavailable
    if model is None:
        return {
            "explanation": [
                "The student shows mixed academic and behavioral indicators."
            ],
            "positive_factors": [
                "Some performance metrics are within acceptable range."
            ],
            "risk_factors": [
                "Inconsistent attendance or marks increase overall risk."
            ],
            "suggested_actions": [
                "Monitor progress closely.",
                "Provide targeted academic support."
            ],
            "confidence": 65
        }

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        return json.loads(text)
    except Exception as e:
        print("Gemini generation failed:", e)
        return {
            "explanation": [
                "The risk level is based on attendance, marks, assignments, and behavior."
            ],
            "positive_factors": [
                "Student shows potential to improve with guidance."
            ],
            "risk_factors": [
                "Current performance trends indicate elevated risk."
            ],
            "suggested_actions": [
                "Schedule one-on-one mentoring.",
                "Engage parents if needed."
            ],
            "confidence": 60
        }
