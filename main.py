from agent.agent import MehAIAgent


def display_banner():
    print()
    print("========================================")
    print("          MEHAI SECURITY AGENT")
    print("========================================")
    print("Version: 0.1.0")
    print("Type 'help' for available commands.")
    print("Type 'exit' to close MehAI.")
    print("========================================")


def display_response(response):
    print()
    print("MehAI:")

    if response["status"] == "error":
        print("Error:", response["message"])
        return

    print(response["message"])

    if "intent" in response:
        print("Intent:", response["intent"])

    if "ai_tool" in response:
        print("AI Tool:", response["ai_tool"])

    if "approved" in response:
        print("Approved:", response["approved"])

    if "detections" in response:
        print("Detections:", response["detections"])

    if "risk" in response:
        risk = response["risk"]

        print()
        print("Risk Factors:")

        for factor in risk.factors:
            print("-", factor)

    if "decision" in response:
        decision = response["decision"]

        print("Decision:", decision.action)


def main():
    agent = MehAIAgent()

    display_banner()

    while True:
        print()
        user_request = input("You: ").strip()

        if user_request.lower() in ["exit", "quit"]:
            print()
            print("MehAI: Session ended.")
            break

        response = agent.process_request(user_request)

        if response["status"] == "input_required":

            print()
            print("MehAI:", response["message"])

            if response["intent"] == "ai_usage_analysis":

                ai_tool = input("AI Tool: ").strip()

                text_to_scan = input(
                    "Content to share: "
                ).strip()

                response = agent.process_request(
                    user_request,
                    text_to_scan=text_to_scan,
                    ai_tool=ai_tool
                )

            else:

                text_to_scan = input("Text: ")

                response = agent.process_request(
                    user_request,
                    text_to_scan=text_to_scan
                )

        display_response(response)


if __name__ == "__main__":
    main()