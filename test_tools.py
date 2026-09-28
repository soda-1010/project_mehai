from tools.image_analyzer import ImageAnalyzer
from tools.sensitive_data_scanner import SensitiveDataScanner
from tools.ai_tool_registry import AIToolRegistry


def main():
    print("Testing Deepfake Analysis Tool")
    image_tool = ImageAnalyzer()
    print(image_tool.analyze("test.jpg"))

    print()
    print("Testing Sensitive Data Scanner")
    scanner = SensitiveDataScanner()

    text = "My email is test@example.com and my phone is 9876543210."

    print(scanner.scan(text))

    print()
    print("Testing AI Tool Registry")
    registry = AIToolRegistry()

    print(registry.get_tool("chatgpt"))
    print(registry.get_tool("unknown_ai"))


if __name__ == "__main__":
    main()