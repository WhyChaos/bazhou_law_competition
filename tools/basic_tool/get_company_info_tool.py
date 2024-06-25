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
                "description": '查公司信息的工具：根据公司名称获得该公司所有基本和注册信息，可以传入多个公司名称，返回一个列表',
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company_name_list": {
                            "description": '一个公司名称的列表',
                            "type": "list"
                        },
                        "key_name_list":{
                            "description": '公司信息的字段名称列表',
                            "type": "list",
                            "enum": list(set(self.search_company_name.info_key)),
                        }
                    },
                    "required": ["company_name_list"]
                },
            }
        }

    def run(self, company_name_list: list, key_name_list: list=[]):
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

        if key_name_list:
            if 'Items' in key_name_list:
                key_name_list = key_name_list['Items']

            # 判断是否有不存在的关键字
            flag=False
            for key_name in key_name_list:
                if key_name not in self.search_company_name.info_key:
                    flag=True
            # 如果有不存在的，全部返回
            if flag:
                return info_list

            value_list = []
            key_name_list = list(set(key_name_list + ['公司名称']))
            for info in info_list:
                item = {}
                for key in key_name_list:
                    item[key] = info[key]
                value_list.append(item)

            info_list = value_list

        return info_list
