class RequestRouter:
    INTENTS = {
        "IMAGE_ANALYSIS": "image_analysis",
        "SENSITIVE_DATA_ANALYSIS": "sensitive_data_analysis",
        "AI_USAGE_ANALYSIS": "ai_usage_analysis",
        "GENERAL": "general",
        "UNKNOWN": "unknown"
    }

    def determine_intent(self, user_request):

        if not isinstance(user_request, str):
            return self.INTENTS["UNKNOWN"]

        request = user_request.strip().lower()

        if not request:
            return self.INTENTS["UNKNOWN"]

        

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

       
        ai_usage_keywords = [
            "shadow ai",
            "ai tool",
            "ai usage",
            "chatgpt",
            "use chatgpt",
            "use an ai",
            "send to ai",
            "send this to ai",
            "share with ai",
            "share this with ai",
            "ai application",
            "can i send this to",
            "can i use"
        ]

        if any(keyword in request for keyword in ai_usage_keywords):
            return self.INTENTS["AI_USAGE_ANALYSIS"]

        

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