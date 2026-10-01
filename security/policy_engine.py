from models.schemas import PolicyDecision, RiskAssessment


class PolicyEngine:
    """
    Converts a risk assessment into a security action.
    """

    def __init__(self):
        self.name = "MehAI Policy Engine"

    def decide(self, risk):
        if risk.level == "low":

            return PolicyDecision(
                action="ALLOW",
                reason="Risk is within the allowed range."
            )

        if risk.level == "medium":

            return PolicyDecision(
                action="WARN",
                reason=(
                    "Moderate risk detected. "
                    "The user should review the warning."
                )
            )

        if risk.level == "high":

            return PolicyDecision(
                action="CONFIRM",
                reason=(
                    "High risk detected. "
                    "User confirmation is required."
                ),
                requires_confirmation=True
            )

        return PolicyDecision(
            action="BLOCK",
            reason=(
                "Critical risk detected. "
                "The operation is blocked."
            )
        )