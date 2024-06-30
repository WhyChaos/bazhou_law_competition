from utils.utils import convert_to_number


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

    def run(self, key_name: str, value: float, info_list) -> list:
        if '子公司信息' in info_list:
            info_list = info_list['子公司信息']

        res_list = []
        for info in info_list:
            if info[key_name]:
                if convert_to_number(info[key_name]) > value:
                    res_list.append(info)

        return res_list

