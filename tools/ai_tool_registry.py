class AIToolRegistry:
    """
    Maintains information about AI tools that can be assessed
    by the MehAI risk engine.
    """

    def __init__(self):
        self.name = "AI Tool Registry"

        self.tools = {
            "chatgpt": {
                "name": "ChatGPT",
                "approved": True,
                "base_risk": 10
            },
            "unknown_ai": {
                "name": "Unknown AI Tool",
                "approved": False,
                "base_risk": 40
            }
        }

    def get_tool(self, tool_id):
        """
        Retrieve information about an AI tool.
        """

        if not tool_id:
            return {
                "status": "error",
                "message": "No AI tool identifier was provided."
            }

        tool = self.tools.get(tool_id.lower())

        if tool is None:
            return {
                "status": "success",
                "tool_id": tool_id,
                "name": tool_id,
                "approved": False,
                "base_risk": 50
            }

        return {
            "status": "success",
            "tool_id": tool_id,
            **tool
        }

    def list_tools(self):
        """
        Return the currently registered AI tools.
        """

        return self.tools