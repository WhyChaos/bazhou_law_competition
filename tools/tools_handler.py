from tools.get_company_info import GetCompanyInfo
from tools.search_company_name_by_info import SearchCompanyNameByInfo
from tools.search_case_num_by_legal_document import SearchCaseNumByLegalDocument


class ToolsHandler:
    def __init__(self):
        self.tool_list=[GetCompanyInfo(), SearchCompanyNameByInfo(), SearchCaseNumByLegalDocument()]

    def get_glm_tools_list(self):
        return [tool.get_glm_tool_dict for tool in self.tool_list]

    def call_function(self, function_name: str, *args, **kwargs):
        pass

