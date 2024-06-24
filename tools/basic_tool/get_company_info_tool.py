from tools.basic_function.get_company_info import GetCompanyInfo
from tools.basic_function.search_company_name import SearchCompanyName


class GetCompanyInfoTool:
    def __init__(self):
        self.tool_name = 'get_company_info_tool'
        self.get_company_info = GetCompanyInfo()
        self.search_company_name = SearchCompanyName()

    def get_glm_tool_dict(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.tool_name,
                "description": '根据公司名称获得该公司所有基本和注册信息，可以传入多个公司名称，返回一个列表',
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company_name_list": {
                            "description": '一个公司名称的列表',
                            "type": "list"
                        },
                    },
                    "required": ["company_name_list"]
                },
            }
        }

    def run(self, company_name_list: list):
        if 'Items' in company_name_list:
            company_name_list = company_name_list['Items']
        info_list = []
        for company_name in company_name_list:
            info = self.get_company_info.get_company_info_and_register(company_name=company_name)
            if info == {}:
                company_name_tmp = self.search_company_name.search_company_name_by_info(key='公司简称', value=company_name)
                if company_name_tmp == []:
                    company_name_tmp = self.search_company_name.search_company_name_by_info(key='英文名称',
                                                                                            value=company_name)
                if company_name_tmp:
                    info = self.get_company_info.get_company_info_and_register(company_name=company_name_tmp[0]['公司名称'])
            if info != {}:
                info_list.append(info)
        if info_list == []:
            return '公司名不存在，请根据问题提取正确的公司名'

        return info_list
