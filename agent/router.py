class RequestRouter:
    """
    Determines the type of task requested by the user.
    """

    INTENTS = {
        "IMAGE_ANALYSIS": "image_analysis",
        "SENSITIVE_DATA_ANALYSIS": "sensitive_data_analysis",
        "AI_USAGE_ANALYSIS": "ai_usage_analysis",
        "GENERAL": "general",
        "UNKNOWN": "unknown"
    }

    def determine_intent(self, user_request):
        """
        Analyze a user request and return the most relevant intent.
        """

        if not isinstance(user_request, str):
            return self.INTENTS["UNKNOWN"]

        request = user_request.strip().lower()

        if not request:
            return self.INTENTS["UNKNOWN"]

        # Image and deepfake requests
        image_keywords = [
            "deepfake",
            "deep fake",
            "image analysis",
            "analyze image",
            "check image",
            "manipulated image",
            "fake image"
        ]

        if any(keyword in request for keyword in image_keywords):
            return self.INTENTS["IMAGE_ANALYSIS"]

        # Sensitive-data requests
        sensitive_keywords = [
            "sensitive data",
            "personal data",
            "private data",
            "confidential data",
            "personal information",
            "api key",
            "password",
            "credential",
            "email",
            "phone number"
        ]

        if any(keyword in request for keyword in sensitive_keywords):
            return self.INTENTS["SENSITIVE_DATA_ANALYSIS"]

        # AI usage / Shadow AI requests
        ai_usage_keywords = [
            "shadow ai",
            "ai tool",
            "ai usage",
            "use chatgpt",
            "use an ai",
            "send to ai",
            "share with ai",
            "ai application"
        ]

        if any(keyword in request for keyword in ai_usage_keywords):
            return self.INTENTS["AI_USAGE_ANALYSIS"]

        # General conversational requests
        general_keywords = [
            "hello",
            "hi",
            "hey",
            "help",
            "what can you do",
            "who are you"
        ]

        if any(keyword in request for keyword in general_keywords):
            return self.INTENTS["GENERAL"]

        return self.INTENTS["UNKNOWN"]