from google import genai
from src.config import GEMINI_API_KEY

client = genai.Client(
    api_key=GEMINI_API_KEY
)

def generate_response(
    user_query,
    persona,
    retrieved_context
):

    if persona == "Technical Expert":

        persona_prompt = """
        You are a Senior Support Engineer.

        Provide:
        - Root Cause
        - Configuration Details
        - API Information
        - Troubleshooting Steps
        """

    elif persona == "Frustrated User":

        persona_prompt = """
        You are a Support Specialist.

        Be empathetic.

        Use simple language.

        Use bullet points.
        """

    else:

        persona_prompt = """
        You are a Client Relations Director.

        Be concise.

        Mention business impact.

        Mention expected timeline.
        """

    full_prompt = f"""
    {persona_prompt}

    Context:
    {retrieved_context}

    User Question:
    {user_query}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )

    return response.text