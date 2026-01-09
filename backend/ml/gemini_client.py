import os
import json
import google.generativeai as genai

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = None
try:
 model = genai.GenerativeModel("models/gemini-flash-latest")



except Exception as e:
    print("Gemini init failed:", e)


def generate_explanation(prompt):
    # ✅ SAFE fallback (never breaks UI)
    fallback = {
        "explanation": [
            "The student's risk level is determined using attendance, marks, assignments, and behavior."
        ],
        "positive_factors": [
            "The student shows strengths in some academic or engagement areas."
        ],
        "risk_factors": [
            "Some performance indicators are below the expected level."
        ],
        "suggested_actions": [
            "Provide personalized academic guidance.",
            "Monitor progress regularly.",
            "Engage parents if needed."
        ],
        "confidence": 65
    }

    if model is None:
        return fallback

    try:
        response = model.generate_content(prompt)

        text = response.text.strip()

        # 🔐 Extract JSON safely
        start = text.find("{")
        end = text.rfind("}") + 1

        if start == -1 or end == -1:
            return fallback

        return json.loads(text[start:end])

    except Exception as e:
        print("Gemini generation failed:", e)
        return fallback
