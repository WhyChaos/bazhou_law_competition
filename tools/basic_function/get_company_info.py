from tools.basic_function.base_function import BaseFunction
from tools.basic_function.search_company_name import SearchCompanyName

class GetCompanyInfo(BaseFunction):
    def __init__(self):
        super(GetCompanyInfo, self).__init__()
        self.search_company_name = SearchCompanyName()


    def get_company_info(self, company_name: str) -> dict:
        data = self.post_request(api='get_company_info', data={"company_name": company_name})
        if data is None or data == []:
            company_name = company_name.replace('(','（').replace(')','）')
            data = self.post_request(api='get_company_info', data={"company_name": company_name})
        if data is None or data == []:
            company_name = company_name.replace('（', '(').replace('）', ')')
            data = self.post_request(api='get_company_info', data={"company_name": company_name})
        if data is None or data == []:
            data = {}
        return data

    def get_company_register(self, company_name: str) -> dict:
        data = self.post_request(api='get_company_register', data={"company_name": company_name})
        if data is None or data == []:
            company_name = company_name.replace('(','（').replace(')','）')
            data = self.post_request(api='get_company_register', data={"company_name": company_name})
        if data is None or data == []:
            company_name = company_name.replace('（', '(').replace('）', ')')
            data = self.post_request(api='get_company_register', data={"company_name": company_name})
        if data is None or data == []:
            data = {}
        return data

    def get_sub_company_info(self, company_name: str) -> dict:
        data = self.post_request(api='get_sub_company_info', data={"company_name": company_name})
        if data is None or data == []:
            company_name = company_name.replace('(','（').replace(')','）')
            data = self.post_request(api='get_sub_company_info', data={"company_name": company_name})
        if data is None or data == []:
            company_name = company_name.replace('（', '(').replace('）', ')')
            data = self.post_request(api='get_sub_company_info', data={"company_name": company_name})
        if data is None or data == []:
            data = {}
        return data

    def get_mother_company_info(self, sub_company_name: str):
        data = self.get_sub_company_info(company_name=sub_company_name)
        if data:
            return data
        return '该公司名称不存在，请根据用户输入提取正确的公司名称'

    def get_company_sub(self, company_name: str) -> dict:
        data = self.get_sub_company_info(company_name)
        return data

    def get_company_info_and_register(self, company_name: str) -> dict:
        data = self.get_company_info(company_name)
        data = data | self.get_company_register(company_name)
        return data

    def get_company_info_and_register_and_sub(self, company_name: str) -> dict:
        data = self.get_company_info(company_name)
        data = data | self.get_company_register(company_name)
        data = data | self.get_sub_company_info(company_name)
        return data

    def get_company_info_and_register_and_sub_and_son(self, company_name: str) -> dict:
        data = self.get_company_info(company_name)
        data = data | self.get_company_register(company_name)
        data = data | self.get_sub_company_info(company_name)

        sub_list = self.search_company_name.search_company_name_by_sub(key='关联上市公司全称', value=company_name)
        sub_detail_list = []
        for sub in sub_list:
            sub_detail_list.append(self.get_company_sub(company_name=sub['公司名称']))

        data['旗下公司数量'] = len(sub_detail_list)
        data['旗下公司'] = sub_detail_list

        return data



    # def get_company_list_info_and_register(self, company_name_list: list) -> dict:
    #     list_a_data = {}
    #     for company_name in company_name_list:
    #         list_a_data[company_name] = self.get_company_info_and_register(company_name)
    #     return list_a_data









