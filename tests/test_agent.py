from agent.agent import MehAIAgent



def test_approved_ai_public_content():

    agent = MehAIAgent()

    response = agent.process_request(
        "Can I send this to ChatGPT?",
        text_to_scan="Hello, please summarize this public information.",
        ai_tool="chatgpt"
    )

    assert response["status"] == "success"
    assert response["intent"] == "ai_usage_analysis"
    assert response["approved"] is True

    assert response["risk"].level == "low"
    assert response["risk"].score == 10

    assert response["risk"].components["tool_risk"] == 10
    assert response["risk"].components["data_risk"] == 0
    assert response["risk"].components["context_risk"] == 0

    assert response["decision"].action == "ALLOW"




def test_approved_ai_sensitive_content():

    agent = MehAIAgent()

    response = agent.process_request(
        "Can I send this to ChatGPT?",
        text_to_scan=(
            "My email is test@example.com "
            "and my phone is 9876543210."
        ),
        ai_tool="chatgpt"
    )

    assert response["status"] == "success"
    assert response["approved"] is True

    assert len(response["detections"]) == 2

    assert response["risk"].level == "medium"
    assert response["risk"].score == 40

    assert response["risk"].components["tool_risk"] == 10
    assert response["risk"].components["data_risk"] == 30
    assert response["risk"].components["context_risk"] == 0

    assert response["decision"].action == "WARN"




def test_unapproved_ai_public_content():

    agent = MehAIAgent()

    response = agent.process_request(
        "Can I send this to an AI?",
        text_to_scan="Hello, please summarize this public information.",
        ai_tool="grok"
    )

    assert response["status"] == "success"
    assert response["approved"] is False
    assert response["detections"] == []

    assert response["risk"].level == "medium"
    assert response["risk"].score == 50

    assert response["risk"].components["tool_risk"] == 50
    assert response["risk"].components["data_risk"] == 0
    assert response["risk"].components["context_risk"] == 0

    assert response["decision"].action == "WARN"




def test_unapproved_ai_sensitive_content():

    agent = MehAIAgent()

    response = agent.process_request(
        "Can I send this to an AI?",
        text_to_scan=(
            "My email is test@example.com "
            "and my phone is 9876543210."
        ),
        ai_tool="grok"
    )

    assert response["status"] == "success"
    assert response["approved"] is False

    assert len(response["detections"]) == 2

    # Risk calculation:
    # Unknown/unapproved AI tool = 50
    # Email + phone = 30
    # Unapproved tool + personal data context = 10
    # Total = 90

    assert response["risk"].level == "critical"
    assert response["risk"].score == 90

    assert response["risk"].components["tool_risk"] == 50
    assert response["risk"].components["data_risk"] == 30
    assert response["risk"].components["context_risk"] == 10

    assert response["decision"].action == "BLOCK"




def test_policy_engine_low_risk():

    agent = MehAIAgent()

    response = agent.process_request(
        "Can I send this to ChatGPT?",
        text_to_scan="Public information.",
        ai_tool="chatgpt"
    )

    decision = response["decision"]

    assert decision.action == "ALLOW"
    assert decision.requires_confirmation is False



def test_policy_engine_medium_risk():

    agent = MehAIAgent()

    response = agent.process_request(
        "Can I send this to ChatGPT?",
        text_to_scan=(
            "My email is test@example.com "
            "and my phone is 9876543210."
        ),
        ai_tool="chatgpt"
    )

    decision = response["decision"]

    assert decision.action == "WARN"
    assert decision.requires_confirmation is False



def test_policy_engine_critical_risk():

    agent = MehAIAgent()

    response = agent.process_request(
        "Can I send this to an AI?",
        text_to_scan=(
            "My email is test@example.com "
            "and my phone is 9876543210."
        ),
        ai_tool="grok"
    )

    decision = response["decision"]

    assert decision.action == "BLOCK"
    assert decision.requires_confirmation is False