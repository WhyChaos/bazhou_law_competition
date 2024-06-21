from tools.basic_tools.get_company_info import GetCompanyInfo
from tools.basic_tools.search_company_name import SearchCompanyName


class CompanyInfo:
    def __init__(self):
        self.tool_name = 'company_info'
        self.get_company_info = GetCompanyInfo()
        self.search_company_name_by_info = SearchCompanyName()

    def get_glm_tool_dict(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.tool_name,
                "description": "查公司信息。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "key": {
                            "description": "公司信息中的字段名，从如下中选择：" + "、".join(
                                self.search_company_name_by_info.info_key) + '、' + "、".join(
                                self.search_company_name_by_info.register_key) + '、' + "、".join(
                                self.search_company_name_by_info.sub_key) + '。',
                            "type": "string"
                        },
                        "value": {
                            "description": "公司信息中的对应的字段值。",
                            "type": "string"
                        },
                    },
                    "required": ["key", "value"]
                },
            }
        }

    def run(self, key: str, value: str):
        info_list = []
        company_name_list = self.search_company_name_by_info.search_company_name_by_info_and_register_and_sub(key=key, value=value)
        if isinstance(company_name_list, str):
            return company_name_list
        if len(company_name_list) == 1:
            info = self.get_company_info.get_company_info_and_register_and_sub_and_sub_list(company_name_list[0]['公司名称'])
        else:
            info = {}
            info['公司数量'] = len(company_name_list)
            info['公司列表'] = company_name_list
        return info

    # def run_tmp(self, company_name_list: list) -> list:
    #     info_list = []
    #     for company_name in company_name_list:
    #         info = self.get_company_info.get_company_info_and_register_and_sub(company_name)
    #         if info == {}:
    #             origin_company_name = self.search_company_name_by_info.search_company_name_by_info(key='公司简称',
    #                                                                                                value=company_name)
    #             if len(origin_company_name) == 1:
    #                 origin_company_name = origin_company_name[0]['公司名称']
    #                 info = self.get_company_info.get_company_info_and_register_and_sub(origin_company_name)
    #         if info == {}:
    #             origin_company_name = self.search_company_name_by_info.search_company_name_by_info(key='英文名称',
    #                                                                                                value=company_name)
    #             if len(origin_company_name) == 1:
    #                 origin_company_name = origin_company_name[0]['公司名称']
    #                 info = self.get_company_info.get_company_info_and_register_and_sub(origin_company_name)
    #
    #         info_list.append(info)
    #
    #     return info_list
