def build_gemini_prompt(student, risk):
    return f"""
You are an AI assistant helping school teachers understand student performance.

Student Data:
- Attendance: {student['attendance']}%
- Marks: {student['marks']}%
- Assignment Completion: {student['assignments']}%
- Behavior Score: {student['behavior']}/10

Predicted Risk Level: {risk}

Explain this result clearly for a teacher.

Rules:
- Do NOT use technical or machine learning terms
- Use simple, professional language
- Be supportive and honest

Return ONLY valid JSON in this format:

{{
  "explanation": ["bullet points"],
  "positive_factors": ["strengths"],
  "risk_factors": ["weaknesses"],
  "suggested_actions": ["teacher actions"],
  "confidence": number between 0 and 100
}}
"""
