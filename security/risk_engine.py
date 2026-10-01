from models.schemas import RiskAssessment, ToolEvidence


class RiskEngine:
    """
    Calculates a deterministic security risk score
    from evidence produced by MehAI's analysis tools.
    """

    def __init__(self):
        self.name = "MehAI Risk Engine"

    def assess(self, evidence):
        score = 0
        factors = []

        for item in evidence:

            if item.tool_name == "AI Tool Registry":
                score += self._evaluate_ai_tool(
                    item,
                    factors
                )

            elif item.tool_name == "Sensitive Data Scanner":
                score += self._evaluate_sensitive_data(
                    item,
                    factors
                )

            elif item.tool_name == "Deepfake Analysis Tool":
                score += self._evaluate_deepfake(
                    item,
                    factors
                )

        score = min(score, 100)

        level = self._get_risk_level(score)

        return RiskAssessment(
            score=score,
            level=level,
            factors=factors
        )

    def _evaluate_ai_tool(self, evidence, factors):

        approved = evidence.data.get(
            "approved",
            False
        )

        base_risk = evidence.data.get(
            "base_risk",
            50
        )

        if not approved:
            factors.append(
                "AI tool is not approved."
            )

            return base_risk

        return base_risk

    def _evaluate_sensitive_data(
        self,
        evidence,
        factors
    ):

        detections = evidence.data.get(
            "detections",
            []
        )

        additional_risk = 0

        for detection in detections:

            data_type = detection.get("type")

            if data_type == "api_key":
                additional_risk += 40
                factors.append(
                    "API credential detected."
                )

            elif data_type in ["email", "phone"]:
                additional_risk += 15
                factors.append(
                    f"Sensitive {data_type} detected."
                )

            else:
                additional_risk += 10
                factors.append(
                    f"Sensitive data detected: {data_type}."
                )

        return additional_risk

    def _evaluate_deepfake(
        self,
        evidence,
        factors
    ):

        is_fake = evidence.data.get(
            "is_fake",
            False
        )

        if is_fake:
            factors.append(
                "Potential manipulated image detected."
            )

            return 50

        return 0

    def _get_risk_level(self, score):

        if score <= 25:
            return "low"

        if score <= 50:
            return "medium"

        if score <= 75:
            return "high"

        return "critical"