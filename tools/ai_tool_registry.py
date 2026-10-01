class AIToolRegistry:
    """
    Registry of AI tools that MehAI can assess.

    Each tool contains:
    - name
    - approval status
    - base risk
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

        if not tool_id:
            return {
                "status": "error",
                "message": "No AI tool identifier was provided."
            }

        tool_id = tool_id.strip().lower()

        tool = self.tools.get(tool_id)

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
        return self.tools