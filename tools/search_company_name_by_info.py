from tools.base import Base


class SearchCompanyNameByInfo(Base):
    def __init__(self):
        super(SearchCompanyNameByInfo, self).__init__()
        self.tool_name = 'search_company_name_by_info'

    def get_glm_tool_dict(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.tool_name,
                "description": "根据公司某一个信息来查询具体的公司名称，公司信息包括:关联证券、公司代码、所属市场、所属行业、上市日期、法人代表、总经理、董秘、邮政编码、注册地址、办公地址、联系电话、传真、官方网址、电子邮箱、入选指数、主营业务、经营范围、机构简介、每股面值、首发价格、首发募资净额、首发主承销商。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "key": {
                            "description": "公司信息名称",
                            "type": "string"
                        },
                        "value": {
                            "description": "公司信息值",
                            "type": "string"
                        },
                    },
                    "required": ["key", "value"]
                },
            }
        }

    def search_company_name_by_info(self, key: str, value: str) -> list:
        data = self.post_request(api='search_company_name_by_info', data={"key": key, "value": value})
        if isinstance(data, dict):
            data = [data]

        return data

    def search_company_name_by_register(self, key: str, value: str) -> list:
        data = self.post_request(api='search_company_name_by_register', data={"key": key, "value": value})
        if isinstance(data, dict):
            data = [data]

        return data
