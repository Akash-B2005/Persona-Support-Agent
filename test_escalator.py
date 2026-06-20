from src.escalator import check_escalation

result = check_escalation(
    user_query="Refund my money now",
    persona="Frustrated User",
    confidence=0.91
)

print(result)