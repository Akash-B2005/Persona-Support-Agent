def check_escalation(
    user_query,
    persona,
    confidence
):

    sensitive_keywords = [
        "billing",
        "refund",
        "legal",
        "account deletion"
    ]

    frustration_keywords = [
        "terrible",
        "worst",
        "frustrated",
        "angry",
        "nothing works"
    ]

    issue = "General Support"

    # Rule 1: Low Confidence
    if confidence < 0.45:

        return {
            "escalate": True,
            "persona": persona,
            "issue": issue,
            "confidence": confidence,
            "recommended_action":
            "Human Support Required"
        }

    # Rule 2: Sensitive Topics
    for keyword in sensitive_keywords:

        if keyword.lower() in user_query.lower():

            issue = keyword

            return {
                "escalate": True,
                "persona": persona,
                "issue": issue,
                "confidence": confidence,
                "recommended_action":
                "Human Support Required"
            }

    # Rule 3: Frustration Detection
    for keyword in frustration_keywords:

        if keyword.lower() in user_query.lower():

            issue = "Customer Frustration"

            return {
                "escalate": True,
                "persona": persona,
                "issue": issue,
                "confidence": confidence,
                "recommended_action":
                "Human Support Required"
            }

    return {
        "escalate": False
    }