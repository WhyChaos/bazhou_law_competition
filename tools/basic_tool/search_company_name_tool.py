from tools.basic_function.get_company_info import GetCompanyInfo
from tools.basic_function.search_company_name import SearchCompanyName


class SearchCompanyNameTool:
    def __init__(self):
        self.tool_name = 'search_company_name_tool'
        self.get_company_info = GetCompanyInfo()
        self.search_company_name_by_info = SearchCompanyName()

    def get_glm_tool_dict(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.tool_name,
                "description": "根据公司某个基本信息字段是某个值时，查询所有满足条件的公司名称和数量",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "key": {
                            "description": "公司信息的字段名称",
                            "enum": list(set(self.search_company_name_by_info.info_key) - set(['公司名称', '公司简称', '英文名称', '经营范围'])),
                            "type": "str"
                        },
                        "value": {
                            "description": "公司信息字段具体的值",
                            "type": "str"
                        },
                    },
                    "required": ["key", "value"]
                },
            }
        }

    def run(self, key: str, value: str):
        info = {}
        company_name_list = self.search_company_name_by_info.search_company_name_by_info_and_register(key=key,
                                                                                                      value=value)
        if isinstance(company_name_list, str):
            return company_name_list

        info['公司数量'] = len(company_name_list)
        info['公司名称'] = [company_name_dict['公司名称'] for company_name_dict in company_name_list]
        return info
