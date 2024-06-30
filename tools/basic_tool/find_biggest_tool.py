from tools.basic_function.get_company_info import GetCompanyInfo
from tools.basic_function.search_company_name import SearchCompanyName
from utils.utils import convert_to_number, convert_from_number


class FindBiggestTool:
    def __init__(self):
        self.tool_name = 'find_biggest_tool'

    def get_glm_tool_dict(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.tool_name,
                "description": '找最大的工具：根据融资信息的参股比例或者投资金额字段找最大的融资信息。',
                "parameters": {
                    "type": "object",
                    "properties": {
                        "key_name": {
                            "description": '用于找最大的字段名，参股比例或投资金额',
                            "type": "str",
                            "enum": ["参股比例", "投资金额"]
                        },
                    },
                },
            }
        }

    def run(self, key_name: str, value: int, info_dict: dict) -> dict:

        info_list = info_dict['子公司信息']
        def custom_sort(data):
            if data[key_name]:
                return -convert_to_number(data[key_name])
            return 0

        info_list = sorted(info_list, key=custom_sort)

        res_list = []
        if info_list:
            for info in info_list:
                if convert_to_number(info[key_name]) == convert_to_number(info_list[0][key_name]):
                    res_list.append(info)
                else:
                    break

        info_dict['子公司数量'] = len(res_list)
        info_dict['子公司信息'] = []
        total_amount = 0
        for item in res_list:
            if item['投资金额']:
                total_amount += convert_to_number(item['投资金额'])
        info_dict['总投资金额'] = convert_from_number(total_amount)
        return info_dict

