from tools.company_info import CompanyInfo
from tools.legal_document_info import LegalDocumentInfo


class ToolsHandler:
    def __init__(self):
        company_info = CompanyInfo()
        legal_document_info = LegalDocumentInfo()
        self.tool_list = [company_info, legal_document_info]

    def get_glm_tools_list(self) -> list:
        glm_tools_list = []
        glm_tools_list = [tool.get_glm_tool_dict() for tool in self.tool_list]
        glm_tools_list.append({
            "type": "web_search",
            "web_search": {
                "enable": True,
                # "search_query": "欧洲杯",
                "search_result": True,
                # "search_prompt": search_prompt
            }
        })
        return glm_tools_list

    def call_function(self, function_name: str, args_dict: dict):
        result = []
        for tool in self.tool_list:
            if function_name == tool.tool_name:
                result = tool.run(**args_dict)
                break

        return result
