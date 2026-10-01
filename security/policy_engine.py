from models.schemas import PolicyDecision, RiskAssessment


class PolicyEngine:
    """
    Converts a risk assessment into a security policy decision.

    The Policy Engine is responsible for deciding what MehAI
    should do after the Risk Engine calculates the risk.

    Risk levels:
        LOW      -> ALLOW
        MEDIUM   -> WARN
        HIGH     -> CONFIRM
        CRITICAL -> BLOCK
    """

    def __init__(self):
        self.name = "MehAI Policy Engine"

        self.policies = {
            "low": {
                "action": "ALLOW",
                "requires_confirmation": False,
                "reason": "Risk is within the allowed range."
            },

            "medium": {
                "action": "WARN",
                "requires_confirmation": False,
                "reason": (
                    "Moderate risk detected. "
                    "The user should review the warning."
                )
            },

            "high": {
                "action": "CONFIRM",
                "requires_confirmation": True,
                "reason": (
                    "High risk detected. "
                    "User confirmation is required."
                )
            },

            "critical": {
                "action": "BLOCK",
                "requires_confirmation": False,
                "reason": (
                    "Critical risk detected. "
                    "The operation is blocked."
                )
            }
        }

    def decide(self, risk: RiskAssessment):

        if not isinstance(risk, RiskAssessment):
            return PolicyDecision(
                action="BLOCK",
                reason="Invalid risk assessment.",
                requires_confirmation=False
            )

        policy = self.policies.get(risk.level)

        if policy is None:
            return PolicyDecision(
                action="BLOCK",
                reason=(
                    f"Unknown risk level '{risk.level}'. "
                    "Operation blocked for safety."
                ),
                requires_confirmation=False
            )

        return PolicyDecision(
            action=policy["action"],
            reason=policy["reason"],
            requires_confirmation=policy[
                "requires_confirmation"
            ]
        )

    def get_policy(self, risk_level):
        """
        Returns the policy configuration for a risk level.
        """

        if not isinstance(risk_level, str):
            return None

        return self.policies.get(
            risk_level.lower()
        )