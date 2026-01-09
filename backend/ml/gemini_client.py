import os

# -------------------------------
# Try loading Gemini
# -------------------------------
USE_GEMINI = False
model = None

try:
    import google.generativeai as genai

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    # Use a VALID model (from your ListModels output)
    model = genai.GenerativeModel("models/gemini-pro-latest")
    USE_GEMINI = True
    print("✅ Gemini enabled")

except Exception as e:
    print("⚠️ Gemini disabled, using fallback:", e)
    USE_GEMINI = False


# -------------------------------
# MAIN FUNCTION
# -------------------------------
def generate_explanation(student_data, risk):
    """
    IF Gemini works → Gemini explanation
    ELSE → Rule-based fallback explanation
    """

    # ===============================
    # ✅ FALLBACK (ALWAYS SAFE)
    # ===============================
    explanation = []
    positive_factors = []
    risk_factors = []
    suggested_actions = []

    # Marks
    if student_data["marks"] >= 60:
        positive_factors.append("Academic performance is satisfactory.")
    else:
        risk_factors.append("Low academic performance detected.")
        suggested_actions.append("Provide additional academic support.")

    # Assignments
    if student_data["assignments"] >= 70:
        positive_factors.append("Assignments are completed regularly.")
    else:
        risk_factors.append("Incomplete assignments affect understanding.")
        suggested_actions.append("Monitor and guide assignment completion.")

    # Attendance
    if student_data["attendance"] >= 75:
        positive_factors.append("Good attendance record.")
    else:
        risk_factors.append("Low attendance impacts learning continuity.")
        suggested_actions.append("Encourage consistent class attendance.")

    # Behavior
    if student_data["behavior"] >= 6:
        positive_factors.append("Positive classroom behavior.")
    else:
        risk_factors.append("Behavioral issues may reduce focus.")
        suggested_actions.append("Provide mentoring or counseling.")

    explanation.append(
        f"The student is classified as {risk} risk based on overall performance indicators."
    )

    fallback_response = {
        "success": True,
        "explanation": explanation,
        "positive_factors": positive_factors,
        "risk_factors": risk_factors,
        "suggested_actions": suggested_actions,
        "confidence": 65,
        "source": "fallback"
    }

    # ===============================
    # 🤖 TRY GEMINI (OPTIONAL)
    # ===============================
    if USE_GEMINI:
        try:
            prompt = f"""
You are an AI assistant helping teachers.

Student Data:
Attendance: {student_data['attendance']}%
Marks: {student_data['marks']}%
Assignments: {student_data['assignments']}%
Behavior: {student_data['behavior']}/10
Risk Level: {risk}

Explain clearly in simple language.
"""

            response = model.generate_content(prompt)
            text = response.text.strip()

            return {
                "success": True,
                "explanation": [text],
                "positive_factors": positive_factors,
                "risk_factors": risk_factors,
                "suggested_actions": suggested_actions,
                "confidence": 80,
                "source": "gemini"
            }

        except Exception as e:
            print("⚠️ Gemini failed, fallback used:", e)

    # ===============================
    # ✅ FINAL RETURN (SAFE)
    # ===============================
    return fallback_response
