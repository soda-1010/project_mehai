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

    assert response["risk"].level == "critical"
    assert response["risk"].score == 80

    assert response["decision"].action == "BLOCK"