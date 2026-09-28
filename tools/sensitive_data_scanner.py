import re


class SensitiveDataScanner:
    """
    Detects potentially sensitive information in text.

    The initial implementation uses regular expressions.
    Presidio, spaCy, and custom recognizers can be integrated
    as the detection engine is expanded.
    """

    def __init__(self):
        self.name = "Sensitive Data Scanner"

        self.patterns = {
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",

            "phone": r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",

            "api_key": (
                r"\b(?:api[_-]?key|apikey|secret[_-]?key)"
                r"\s*[:=]\s*[A-Za-z0-9_\-]{8,}\b"
            )
        }

    def scan(self, text):
        """
        Scan text for configured sensitive-data patterns.

        Parameters:
            text (str): Text to analyze.

        Returns:
            dict: Structured detection result.
        """

        if not isinstance(text, str):
            return {
                "status": "error",
                "tool": self.name,
                "message": "Input must be text."
            }

        if not text.strip():
            return {
                "status": "error",
                "tool": self.name,
                "message": "No text was provided."
            }

        detections = []

        for data_type, pattern in self.patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)

            if matches:
                detections.append({
                    "type": data_type,
                    "count": len(matches)
                })

        return {
            "status": "success",
            "tool": self.name,
            "sensitive_data_found": len(detections) > 0,
            "detections": detections
        }