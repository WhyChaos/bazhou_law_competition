from tools.basic_tools.base import Base

class GetCompanyInfo(Base):
    def __init__(self):
        super(GetCompanyInfo, self).__init__()
        self.tool_name = 'get_company_info'


    def get_company_info(self, company_name: str) -> dict:
        data = self.post_request(api='get_company_info', data={"company_name": company_name})
        if data is None or data == []:
            data = {}
        return data

    def get_company_register(self, company_name: str) -> dict:
        data = self.post_request(api='get_company_register', data={"company_name": company_name})
        if data is None or data == []:
            data = {}
        return data

    def get_sub_company_info(self, company_name: str) -> dict:
        data = self.post_request(api='get_sub_company_info', data={"company_name": company_name})
        if data is None or data == []:
            data = {}
        return data

    def get_company_info_and_register_and_sub(self, company_name: str) -> dict:
        data = self.get_company_info(company_name)
        data = data | self.get_company_register(company_name)
        data = data | self.get_sub_company_info(company_name)
        return data

    # def get_company_list_info_and_register(self, company_name_list: list) -> dict:
    #     data = {}
    #     for company_name in company_name_list:
    #         data[company_name] = self.get_company_info_and_register(company_name)
    #     return data









