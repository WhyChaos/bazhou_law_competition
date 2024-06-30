from tools.basic_function.get_company_info import GetCompanyInfo
from tools.basic_function.search_company_name import SearchCompanyName
from utils.utils import convert_to_number, convert_from_number


class GetSubCompanyInfoTool:
    def __init__(self):
        self.tool_name = 'get_sub_company_info_tool'
        self.get_company_info = GetCompanyInfo()
        self.search_company_name_by_info = SearchCompanyName()
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
                "description": "查子公司的工具：根据母公司名称获得总投资金额、所有子公司名称、数量和融资信息。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "mother_company_name": {
                            "description": "母公司名称",
                            "type": "string"
                        },
                    },
                    "required": ["mother_company_name"]
                },
            }
        }

    def run(self, mother_company_name: str):
        info_list = []
        sub_company_name_list = self.search_company_name_by_info.get_sub_company_company(mother_company_name=mother_company_name)
        if isinstance(sub_company_name_list, str):
            return sub_company_name_list
        for sub_company_name in sub_company_name_list:
            info_list.append(self.get_company_info.get_company_sub(company_name=sub_company_name['公司名称']))

        info = {}
        if info_list:
            info['母公司全称'] = info_list[0]['关联上市公司全称']
            info['母公司股票代码'] = info_list[0]['关联上市公司股票代码']
            info['母公司股票简称'] = info_list[0]['关联上市公司股票简称']
        info['子公司数量'] = len(info_list)
        info['子公司信息'] = []
        total_amount = 0
        for item in info_list:
            info['子公司信息'].append({
                '子公司名称': item['公司名称'],
                '关系': item['上市公司关系'],
                '参股比例': item['上市公司参股比例'],
                '投资金额': item['上市公司投资金额'],
            })
            total_amount += convert_to_number(item['上市公司投资金额'])
        info['总投资金额'] = convert_from_number(total_amount)
        return info

