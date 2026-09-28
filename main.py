
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

            text_to_scan = input("Text: ")

            response = agent.process_request(
                user_request,
                text_to_scan
            )

        display_response(response)


if __name__ == "__main__":
    main()