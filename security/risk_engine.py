from models.schemas import RiskAssessment


class RiskEngine:
    """
    Deterministic risk assessment engine for MehAI.

    The engine separates risk into three major components:

    1. Tool Risk
       Risk associated with the AI tool being used.

    2. Data Risk
       Risk associated with sensitive information detected
       in the content being shared.

    3. Context Risk
       Additional risk created by combinations of conditions,
       such as sending personal data to an unapproved AI tool.

    The final score is capped at 100.
    """

    TOOL_RISK_APPROVED = 10
    TOOL_RISK_UNAPPROVED = 40
    TOOL_RISK_UNKNOWN = 50

    DATA_RISK_PERSONAL = 15
    DATA_RISK_CREDENTIAL = 40
    DATA_RISK_OTHER = 10

    CONTEXT_RISK_UNAPPROVED_PERSONAL = 10
    CONTEXT_RISK_UNAPPROVED_CREDENTIAL = 20

    def __init__(self):
        self.name = "MehAI Risk Engine"

    def assess(self, evidence):

        tool_risk = 0
        data_risk = 0
        context_risk = 0

        factors = []

        tool_approved = None
        personal_data_found = False
        credential_found = False

        for item in evidence:

            if item.tool_name == "AI Tool Registry":

                risk = self._evaluate_ai_tool(
                    item,
                    factors
                )

                tool_risk += risk

                tool_approved = item.data.get(
                    "approved"
                )

            elif item.tool_name == "Sensitive Data Scanner":

                risk, has_personal, has_credential = (
                    self._evaluate_sensitive_data(
                        item,
                        factors
                    )
                )

                data_risk += risk

                if has_personal:
                    personal_data_found = True

                if has_credential:
                    credential_found = True

            elif item.tool_name == "Deepfake Analysis Tool":

                risk = self._evaluate_deepfake(
                    item,
                    factors
                )

                data_risk += risk

        # --------------------------------
        # Context / combination risk
        # --------------------------------

        if tool_approved is False and personal_data_found:

            context_risk += (
                self.CONTEXT_RISK_UNAPPROVED_PERSONAL
            )

            factors.append(
                "Personal data is being shared with "
                "an unapproved AI tool."
            )

        if tool_approved is False and credential_found:

            context_risk += (
                self.CONTEXT_RISK_UNAPPROVED_CREDENTIAL
            )

            factors.append(
                "Credential data is being shared with "
                "an unapproved AI tool."
            )

        # --------------------------------
        # Final score
        # --------------------------------

        score = (
            tool_risk
            + data_risk
            + context_risk
        )

        score = min(score, 100)

        level = self._get_risk_level(score)

        components = {
            "tool_risk": tool_risk,
            "data_risk": data_risk,
            "context_risk": context_risk
        }

        return RiskAssessment(
            score=score,
            level=level,
            factors=factors,
            components=components
        )

    # ====================================
    # AI TOOL RISK
    # ====================================

    def _evaluate_ai_tool(
        self,
        evidence,
        factors
    ):

        approved = evidence.data.get(
            "approved"
        )

        base_risk = evidence.data.get(
            "base_risk"
        )

        if approved is True:

            factors.append(
                "AI tool is approved."
            )

            return base_risk or self.TOOL_RISK_APPROVED

        if approved is False:

            factors.append(
                "AI tool is not approved."
            )

            return base_risk or self.TOOL_RISK_UNAPPROVED

        factors.append(
            "AI tool approval status is unknown."
        )

        return self.TOOL_RISK_UNKNOWN

    # ====================================
    # SENSITIVE DATA RISK
    # ====================================

    def _evaluate_sensitive_data(
        self,
        evidence,
        factors
    ):

        detections = evidence.data.get(
            "detections",
            []
        )

        risk = 0

        personal_data_found = False
        credential_found = False

        for detection in detections:

            data_type = detection.get(
                "type"
            )

            count = detection.get(
                "count",
                0
            )

            if data_type in [
                "email",
                "phone"
            ]:

                risk += self.DATA_RISK_PERSONAL

                personal_data_found = True

                factors.append(
                    f"Sensitive {data_type} detected "
                    f"({count})."
                )

            elif data_type in [
                "api_key",
                "password",
                "credential",
                "secret"
            ]:

                risk += self.DATA_RISK_CREDENTIAL

                credential_found = True

                factors.append(
                    f"Credential or secret detected "
                    f"({count})."
                )

            else:

                risk += self.DATA_RISK_OTHER

                factors.append(
                    f"Sensitive data detected: "
                    f"{data_type} ({count})."
                )

        return (
            risk,
            personal_data_found,
            credential_found
        )

    # ====================================
    # DEEPFAKE RISK
    # ====================================

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

        factors.append(
            "No manipulated image finding reported."
        )

        return 0

    # ====================================
    # RISK LEVEL
    # ====================================

    def _get_risk_level(self, score):

        if score <= 25:
            return "low"

        if score <= 50:
            return "medium"

        if score <= 75:
            return "high"

        return "critical"