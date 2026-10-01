from agent.router import RequestRouter

from tools.sensitive_data_scanner import SensitiveDataScanner
from tools.ai_tool_registry import AIToolRegistry
from tools.image_analyzer import ImageAnalyzer

from security.risk_engine import RiskEngine
from security.policy_engine import PolicyEngine
from security.security_logger import SecurityLogger

from models.schemas import AnalysisRequest, ToolEvidence


class MehAIAgent:
    """
    Core orchestration layer of MehAI.

    The agent:
    1. Understands the user's request.
    2. Routes the request to the appropriate tools.
    3. Collects tool evidence.
    4. Sends the evidence to the Risk Engine.
    5. Sends the risk assessment to the Policy Engine.
    6. Logs the resulting security event.
    """

    def __init__(self):
        self.name = "MehAI"
        self.version = "0.1.0"

        
        self.router = RequestRouter()

        
        self.sensitive_data_scanner = SensitiveDataScanner()
        self.ai_tool_registry = AIToolRegistry()
        self.image_analyzer = ImageAnalyzer()

        
        self.risk_engine = RiskEngine()
        self.policy_engine = PolicyEngine()

        
        self.security_logger = SecurityLogger()

    def process_request(
        self,
        user_request,
        text_to_scan=None,
        ai_tool=None,
        image_path=None
    ):
        """
        Main entry point for the MehAI agent.
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
                    "message": "Please enter the text you want me to scan."
                }

            return self._analyze_sensitive_data(
                user_request,
                text_to_scan
            )

        

        if intent == "ai_usage_analysis":

            if text_to_scan is None:
                return {
                    "status": "input_required",
                    "intent": intent,
                    "message": "Please enter the content you want to share."
                }

            return self._analyze_ai_usage(
                user_request,
                text_to_scan,
                ai_tool
            )

        

        if intent == "image_analysis":

            if image_path is None:
                return {
                    "status": "input_required",
                    "intent": intent,
                    "message": "Please provide the image path."
                }

            return self._analyze_image(
                user_request,
                image_path
            )

       

        return self._create_response(
            user_request,
            intent
        )

    

    def _analyze_sensitive_data(
        self,
        user_request,
        text_to_scan
    ):

        result = self.sensitive_data_scanner.scan(
            text_to_scan
        )

        if result["status"] == "error":
            return {
                "status": "error",
                "intent": "sensitive_data_analysis",
                "message": result["message"]
            }

        evidence = ToolEvidence(
            tool_name="Sensitive Data Scanner",
            status=result["status"],
            data={
                "detections": result["detections"],
                "sensitive_data_found":
                    result["sensitive_data_found"]
            }
        )

        risk = self.risk_engine.assess(
            [evidence]
        )

        decision = self.policy_engine.decide(
            risk
        )

        request = AnalysisRequest(
            request_type="sensitive_data_analysis",
            text=text_to_scan
        )

        event = {
            "request": request,
            "evidence": [evidence],
            "risk": risk,
            "decision": decision
        }

        log_record = self.security_logger.log(
            event
        )

        return {
            "status": "success",
            "intent": "sensitive_data_analysis",
            "message": self._format_security_response(
                risk,
                decision
            ),
            "detections": result["detections"],
            "risk": risk,
            "decision": decision,
            "log": log_record
        }

    

    def _analyze_ai_usage(
        self,
        user_request,
        text_to_scan,
        ai_tool
    ):

        if not ai_tool:
            ai_tool = self._extract_ai_tool(
                user_request
            )

        if not ai_tool:
            return {
                "status": "input_required",
                "intent": "ai_usage_analysis",
                "message": (
                    "Please specify the AI tool you want "
                    "to use, for example: ChatGPT."
                )
            }

        
        registry_result = self.ai_tool_registry.get_tool(
            ai_tool
        )

        
        scanner_result = self.sensitive_data_scanner.scan(
            text_to_scan
        )

        if scanner_result["status"] == "error":
            return {
                "status": "error",
                "intent": "ai_usage_analysis",
                "message": scanner_result["message"]
            }

        registry_evidence = ToolEvidence(
            tool_name="AI Tool Registry",
            status=registry_result["status"],
            data={
                "tool_id": registry_result["tool_id"],
                "name": registry_result["name"],
                "approved": registry_result["approved"],
                "base_risk": registry_result["base_risk"]
            }
        )

        sensitive_evidence = ToolEvidence(
            tool_name="Sensitive Data Scanner",
            status=scanner_result["status"],
            data={
                "detections": scanner_result["detections"],
                "sensitive_data_found":
                    scanner_result["sensitive_data_found"]
            }
        )

        evidence = [
            registry_evidence,
            sensitive_evidence
        ]

        
        risk = self.risk_engine.assess(
            evidence
        )

        
        decision = self.policy_engine.decide(
            risk
        )

        request = AnalysisRequest(
            request_type="ai_usage_analysis",
            ai_tool=ai_tool,
            text=text_to_scan
        )

        event = {
            "request": request,
            "evidence": evidence,
            "risk": risk,
            "decision": decision
        }

        log_record = self.security_logger.log(
            event
        )

        return {
            "status": "success",
            "intent": "ai_usage_analysis",
            "ai_tool": registry_result["name"],
            "approved": registry_result["approved"],
            "detections": scanner_result["detections"],
            "risk": risk,
            "decision": decision,
            "message": self._format_security_response(
                risk,
                decision
            ),
            "log": log_record
        }

    

    def _analyze_image(
        self,
        user_request,
        image_path
    ):

        result = self.image_analyzer.analyze(
            image_path
        )

        evidence = ToolEvidence(
            tool_name="Deepfake Analysis Tool",
            status=result["status"],
            data=result
        )

       

        if result["status"] != "success":
            return {
                "status": result["status"],
                "intent": "image_analysis",
                "message": result["message"],
                "evidence": evidence
            }

        risk = self.risk_engine.assess(
            [evidence]
        )

        decision = self.policy_engine.decide(
            risk
        )

        return {
            "status": "success",
            "intent": "image_analysis",
            "risk": risk,
            "decision": decision,
            "message": self._format_security_response(
                risk,
                decision
            )
        }

   

    def _extract_ai_tool(self, request):

        request_lower = request.lower()

        known_tools = [
            "chatgpt",
            "unknown_ai"
        ]

        for tool in known_tools:
            if tool in request_lower:
                return tool

        return None

    

    def _format_security_response(
        self,
        risk,
        decision
    ):

        return (
            f"Risk Level: {risk.level.upper()}\n"
            f"Risk Score: {risk.score}/100\n"
            f"Action: {decision.action}\n"
            f"Reason: {decision.reason}"
        )

    def _create_response(
        self,
        user_request,
        intent
    ):

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
                "I could not identify the security task "
                "in your request."
            )
        }

    def _help_message(self):

        return (
            "I am MehAI, an AI security agent.\n\n"
            "I can currently handle:\n"
            "- Sensitive-data analysis\n"
            "- AI-usage risk assessment\n"
            "- AI tool approval checking\n"
            "- Image analysis requests\n"
            "- Risk scoring and security policy decisions"
        )