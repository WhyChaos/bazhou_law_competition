from tools.basic_function.get_company_info import GetCompanyInfo
from tools.basic_function.search_company_name import SearchCompanyName


class GetMotherCompanyNameTool:
    def __init__(self):
        self.tool_name = 'get_mother_company_name_tool'
        self.get_company_info = GetCompanyInfo()
        self.search_company_name = SearchCompanyName()
        self.name_to_display = {
            '关联上市公司股票代码': '母公司股票代码',
            '关联上市公司股票简称': '母公司股票简称',
            '关联上市公司全称': '母公司全称',
            '上市公司关系': '关系',
            '上市公司参股比例': '参股比例',
            '上市公司投资金额': '投资金额',
            '公司名称': '子公司名称',
        }

    def get_glm_tool_dict(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.tool_name,
                "description": "找母公司的工具：根据子公司名称获得母公司名称和融资信息，可传入多个子公司名称。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sub_company_name_list": {
                            "description": "一个或多个子公司名称，一个列表",
                            "type": "list"
                        },
                    },
                    "required": ["sub_company_name_list"]
                },
            }
        }

    def run(self, sub_company_name_list) -> list:
        if 'Items' in sub_company_name_list:
            sub_company_name_list = sub_company_name_list['Items']
        res_list = []
        for sub_company_name in sub_company_name_list:
            res_list.append(self.get_mother_company_name_dict(sub_company_name=sub_company_name))

        return res_list

    def get_mother_company_name_dict(self, sub_company_name: str):
        mother_company_name_info = self.get_company_info.get_mother_company_info(sub_company_name=sub_company_name)
        if isinstance(mother_company_name_info, str):
            tmp = self.search_company_name.search_company_name_by_info('公司简称', sub_company_name)
            if len(tmp) == 0:
                tmp = self.search_company_name.search_company_name_by_info('英文名称', sub_company_name)
            if len(tmp) > 0:
                mother_company_name_info = self.get_company_info.get_mother_company_info(sub_company_name=tmp[0]['公司名称'])
        if isinstance(mother_company_name_info, str):
            return mother_company_name_info

        info = {}
        for key, value in self.name_to_display.items():
            info[value] = mother_company_name_info[key]

        return info
