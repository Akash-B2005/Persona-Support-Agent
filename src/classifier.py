import json
from google import genai
from src.config import GEMINI_API_KEY

client = genai.Client(
    api_key=GEMINI_API_KEY
)

def classify_persona(user_message):

    prompt = f"""
Classify the user into ONE category:

1. Technical Expert
2. Frustrated User
3. Business Executive

Return ONLY valid JSON.

Example:
{{
    "persona": "Technical Expert",
    "confidence": 0.92
}}

User Message:
{user_message}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw_text = response.text.strip()

        print("Gemini Response:")
        print(raw_text)

        # Remove markdown if Gemini returns it
        raw_text = raw_text.replace("```json", "")
        raw_text = raw_text.replace("```", "")
        raw_text = raw_text.strip()

        result = json.loads(raw_text)

        return result

    except Exception as e:

        print(f"Error: {e}")

        return {
            "persona": "Technical Expert",
            "confidence": 0.50
        }