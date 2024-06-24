


class ToolsHandler:
    def __init__(self, ToolList: list):
        self.tool_list = []
        for Tool in ToolList:
            self.tool_list.append(Tool())

    def get_glm_tools_list(self) -> list:
        return [tool.get_glm_tool_dict() for tool in self.tool_list]

    def call_function(self, function_name: str, args_dict: dict):
        result = []
        for tool in self.tool_list:
            if function_name == tool.tool_name:
                result = tool.run(**args_dict)
                break

        return result
