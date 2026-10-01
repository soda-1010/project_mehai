from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AnalysisRequest:
    request_type: str
    user_id: Optional[str] = None
    ai_tool: Optional[str] = None
    text: Optional[str] = None
    image_path: Optional[str] = None


@dataclass
class ToolEvidence:
    tool_name: str
    status: str
    data: Dict[str, Any] = field(default_factory=dict)
    findings: List[str] = field(default_factory=list)


@dataclass
class RiskAssessment:
    score: int
    level: str
    factors: List[str] = field(default_factory=list)
    components: Dict[str, int] = field(default_factory=dict)


@dataclass
class PolicyDecision:
    action: str
    reason: str
    requires_confirmation: bool = False


@dataclass
class SecurityEvent:
    request: AnalysisRequest
    evidence: List[ToolEvidence]
    risk: RiskAssessment
    decision: PolicyDecision