
from agent.router import RequestRouter
from tools.sensitive_data_scanner import SensitiveDataScanner


class MehAIAgent:
    """
    Core orchestration layer for the MehAI system.

    The agent identifies the requested task and connects
    the request to the appropriate security tool.
    """

    def __init__(self):
        self.name = "MehAI"
        self.version = "0.1.0"

        self.router = RequestRouter()
        self.sensitive_data_scanner = SensitiveDataScanner()

    def process_request(self, user_request, text_to_scan=None):
        """
        Process a user request.

        For sensitive-data analysis, the text to scan is
        supplied separately after the intent is identified.
        """

        if not isinstance(user_request, str):
            return {
                "status": "error",
                "message": "The request must be text."
            }

        user_request = user_request.strip()

        if not user_request:
            return {
                "status": "error",
                "message": "Please enter a request."
            }

        intent = self.router.determine_intent(user_request)

        if intent == "sensitive_data_analysis":

            if text_to_scan is None:
                return {
                    "status": "input_required",
                    "intent": intent,
                    "message": (
                        "Please enter the text you want "
                        "me to scan."
                    )
                }

            return self._analyze_sensitive_data(text_to_scan)

        return self._create_response(
            user_request,
            intent
        )

    def _analyze_sensitive_data(self, text_to_scan):
        """
        Send text to the Sensitive Data Scanner
        and format the result for the user.
        """

        result = self.sensitive_data_scanner.scan(text_to_scan)

        if result["status"] == "error":
            return {
                "status": "error",
                "intent": "sensitive_data_analysis",
                "message": result["message"]
            }

        if not result["sensitive_data_found"]:
            return {
                "status": "success",
                "intent": "sensitive_data_analysis",
                "message": (
                    "No sensitive data was detected."
                ),
                "detections": []
            }

        detection_messages = []

        for detection in result["detections"]:
            data_type = detection["type"]
            count = detection["count"]

            detection_messages.append(
                f"- {data_type}: {count}"
            )

        message = (
            "Sensitive data detected:\n"
            + "\n".join(detection_messages)
        )

        return {
            "status": "success",
            "intent": "sensitive_data_analysis",
            "message": message,
            "detections": result["detections"]
        }

    def _create_response(self, user_request, intent):
        """
        Create an agent response based on the detected intent.
        """

        if intent == "image_analysis":
            return {
                "status": "success",
                "intent": intent,
                "message": (
                    "I identified this as an image-analysis request. "
                    "The Deepfake Analysis Tool will handle this task "
                    "when it is connected."
                )
            }

        if intent == "ai_usage_analysis":
            return {
                "status": "success",
                "intent": intent,
                "message": (
                    "I identified this as an AI-usage risk request. "
                    "The AI Tool Registry and Risk Engine will handle "
                    "this task when they are connected."
                )
            }

        if intent == "general":
            return {
                "status": "success",
                "intent": intent,
                "message": self._help_message()
            }

        return {
            "status": "success",
            "intent": "unknown",
            "message": (
                "I could not identify the security task in your "
                "request. Try asking me to analyze an image, "
                "check sensitive data, or assess AI usage."
            )
        }

    def _help_message(self):
        """
        Return the capabilities currently available in Phase 1.
        """

        return (
            "I am MehAI, an AI security agent. "
            "I can identify requests related to image/deepfake "
            "analysis, sensitive-data analysis, and AI-usage "
            "risk assessment. Sensitive-data scanning is "
            "currently connected."
        )