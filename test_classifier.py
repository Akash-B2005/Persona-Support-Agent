from src.classifier import classify_persona

message = "Our API is returning 401 errors"

result = classify_persona(message)

print("\nResult:")
print(result)