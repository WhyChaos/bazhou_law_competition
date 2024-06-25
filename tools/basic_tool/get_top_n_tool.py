from tools.basic_function.get_company_info import GetCompanyInfo
from tools.basic_function.search_company_name import SearchCompanyName


class GetTopNTool:
    def __init__(self):
        self.tool_name = 'get_top_n_tool'

    def get_glm_tool_dict(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.tool_name,
                "description": '筛选工具：根据某数字类型字段取最大的几个，比如top几、前几、最大的几个，字段如注册资本',
                "parameters": {
                    "type": "object",
                    "properties": {
                        "key_name": {
                            "description": '涉及的字段名，字符串类型',
                            "type": "str"
                        },
                        "num": {
                            "description": '取前几的个数，整型',
                            "type": "int"
                        }
                    },
                    "required": ["key_name", "int"]
                },
            }
        }

    def run(self, key_name: str, num: int, info_list: list) -> list:
        def custom_sort(data):
            return -float(data[key_name])

        info_list = sorted(info_list, key=custom_sort)
        if len(info_list) > num:
            info_list = info_list[:num]
        return info_list

