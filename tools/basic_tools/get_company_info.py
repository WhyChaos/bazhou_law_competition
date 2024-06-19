from tools.basic_tools.base import Base
from tools.basic_tools.search_company_name import SearchCompanyName

class GetCompanyInfo(Base):
    def __init__(self):
        super(GetCompanyInfo, self).__init__()
        self.search_company_name = SearchCompanyName()


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

    def get_company_info_and_register_and_sub_and_sub_list(self, company_name: str) -> dict:
        data = self.get_company_info_and_register_and_sub(company_name)
        sub_list = self.search_company_name.search_company_name_by_sub(key='关联上市公司全称', value=company_name)
        sub_info_list = []
        for sub in sub_list:
            sub_info_list.append(self.get_sub_company_info(company_name=sub['公司名称']))
        data['旗下公司数量'] = len(sub_list)
        data['旗下公司'] = [{'子公司名称':sub['公司名称'], '参股比例': sub['上市公司参股比例'], '投资金额': sub['上市公司投资金额'], '关系': sub['上市公司关系']} for sub in sub_info_list]
        return data

    # def get_company_list_info_and_register(self, company_name_list: list) -> dict:
    #     data = {}
    #     for company_name in company_name_list:
    #         data[company_name] = self.get_company_info_and_register(company_name)
    #     return data









