from tools.basic_tools.get_company_info import GetCompanyInfo
from tools.basic_tools.search_company_name_by_info import SearchCompanyNameByInfo


class CompanyInfo:
    def __init__(self):
        self.tool_name = 'company_info'
        self.get_company_info = GetCompanyInfo()
        self.search_company_name_by_info = SearchCompanyNameByInfo()

    def get_glm_tool_dict(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.tool_name,
                "description": "根据公司名称查公司信息，名称可以是全称、简称、英文。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company_name_list": {
                            "description": "需要查询的公司列表，注意不要遗漏公司，也可以只有一个公司。",
                            "type": "list"
                        },
                    },
                    "required": ["company_name_list"]
                },
            }
        }

    def get_company_list_info(self, company_name_list: list) -> list:
        info_list = []
        for company_name in company_name_list:
            info = self.get_company_info.get_company_info_and_register_and_sub(company_name)
            if info == {}:
                origin_company_name = self.search_company_name_by_info.search_company_name_by_info(key='公司简称',
                                                                                                   value=company_name)
                if len(origin_company_name) == 1:
                    origin_company_name = origin_company_name[0]['公司名称']
                    info = self.get_company_info.get_company_info_and_register_and_sub(origin_company_name)
            if info == {}:
                origin_company_name = self.search_company_name_by_info.search_company_name_by_info(key='英文名称',
                                                                                                   value=company_name)
                if len(origin_company_name) == 1:
                    origin_company_name = origin_company_name[0]['公司名称']
                    info = self.get_company_info.get_company_info_and_register_and_sub(origin_company_name)

            info_list.append(info)

        return info_list
