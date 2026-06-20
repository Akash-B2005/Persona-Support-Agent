from src.generator import generate_response

response = generate_response(
    user_query="How do I reset my password?",
    persona="Frustrated User",
    retrieved_context="""
    Use the Forgot Password page.
    Enter your registered email.
    Check inbox for reset link.
    """
)

print(response)