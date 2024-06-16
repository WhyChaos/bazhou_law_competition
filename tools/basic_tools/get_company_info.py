from tools.basic_tools.base import Base


class GetCompanyInfo(Base):
    def __init__(self):
        super(GetCompanyInfo, self).__init__()
        self.tool_name = 'get_company_info'

    def get_glm_tool_dict(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.tool_name,
                "description": "根据公司名称获得该公司所有信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "company_name_list": {
                            "description": "需要查询的公司名称列表，注意不要遗漏公司，也可以只有一个公司",
                            "type": "list"
                        },
                    },
                    "required": ["company_name_list"]
                },
            }
        }

    def get_company_info(self, company_name: str) -> dict:
        data = self.post_request(api='get_company_info', data={"company_name": company_name})
        if data is None:
            data = {}
        return data

    def get_company_register(self, company_name: str) -> dict:
        data = self.post_request(api='get_company_register', data={"company_name": company_name})
        if data is None:
            data = {}
        return data

    def get_company_info_and_register(self, company_name: str) -> dict:
        data = self.get_company_info(company_name)
        data = data | self.get_company_register(company_name)
        return data

    def get_company_list_info_and_register(self, company_name_list: list) -> dict:
        data = {}
        for company_name in company_name_list:
            data[company_name] = self.get_company_info_and_register(company_name)
        return data







