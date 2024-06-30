from utils.utils import convert_to_number, convert_from_number


class ScreeningTool:
    def __init__(self):
        self.tool_name = 'screening_tool'

    def get_glm_tool_dict(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.tool_name,
                "description": '筛选工具：根据融资信息的参股比例、投资金额字段进行筛选。',
                "parameters": {
                    "type": "object",
                    "properties": {
                        "key_name": {
                            "description": '用于筛选的字段名，参股比例或投资金额',
                            "type": "str",
                            "enum": ["参股比例", "投资金额"]
                        },
                        "value": {
                            "description": '筛选条件的阈值',
                            "type": "float"
                        }
                    },
                    "required": ["key_name", "value"]
                },
            }
        }

    def run(self, key_name: str, value: float, info_dict: dict) -> dict:
        info_list = info_dict['子公司信息']

        res_list = []
        for info in info_list:
            if info[key_name]:
                if convert_to_number(info[key_name]) > value:
                    res_list.append(info)

        info_dict['子公司数量'] = len(res_list)
        info_dict['子公司信息'] = res_list
        total_amount = 0
        for item in res_list:
            if item['投资金额']:
                total_amount += convert_to_number(item['投资金额'])
        info_dict['总投资金额'] = convert_from_number(total_amount)
        return info_dict

