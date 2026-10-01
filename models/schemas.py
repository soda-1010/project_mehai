from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AnalysisRequest:
    """
    Standard input received by the MehAI orchestration layer.
    """

    request_type: str
    user_id: Optional[str] = None
    ai_tool: Optional[str] = None
    text: Optional[str] = None
    image_path: Optional[str] = None


@dataclass
class ToolEvidence:
    """
    Standard result produced by an analysis tool.
    """

    tool_name: str
    status: str
    data: Dict[str, Any] = field(default_factory=dict)
    findings: List[str] = field(default_factory=list)


@dataclass
class RiskAssessment:
    """
    Standard output of the Risk Engine.
    """

    score: int
    level: str
    factors: List[str] = field(default_factory=list)


@dataclass
class PolicyDecision:
    """
    Final security action determined by the Policy Engine.
    """

    action: str
    reason: str
    requires_confirmation: bool = False


@dataclass
class SecurityEvent:
    """
    Structured security event produced after an analysis.
    """

    request: AnalysisRequest
    evidence: List[ToolEvidence]
    risk: RiskAssessment
    decision: PolicyDecision