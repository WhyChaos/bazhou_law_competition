from tools.basic_function.base_function import BaseFunction


class SearchCompanyName(BaseFunction):
    def __init__(self):
        super(SearchCompanyName, self).__init__()


    def search_company_name_by_info(self, key: str, value: str) -> list:
        data = self.post_request(api='search_company_name_by_info', data={"key": key, "value": value})
        if isinstance(data, dict):
            data = [data]
        if data is None:
            data = []
        return data

    def search_company_name_by_register(self, key: str, value: str) -> list:
        data = self.post_request(api='search_company_name_by_register', data={"key": key, "value": value})
        if isinstance(data, dict):
            data = [data]
        if data is None:
            data = []

        return data

    def search_company_name_by_sub(self, key: str, value: str) -> list:
        data = self.post_request(api='search_company_name_by_sub_info', data={"key": key, "value": value})
        if isinstance(data, dict):
            data = [data]
        if data is None:
            data = []
        return data

    def get_sub_company_company(self, mother_company_name: str):
        data = self.search_company_name_by_sub('关联上市公司全称', mother_company_name)
        if data == []:
            data = self.search_company_name_by_sub('关联上市公司股票简称', mother_company_name)
        if data == []:
            tmp = self.search_company_name_by_info('公司简称', mother_company_name)
            if len(tmp) == 0:
                tmp = self.search_company_name_by_info('英文名称', mother_company_name)
            if len(tmp) > 0:
                data = self.search_company_name_by_sub('关联上市公司全称', tmp[0]['公司名称'])
        if data != []:
            return data

        return '公司名称不存在，请根据用户输入提取出正确的公司名称'



    # def search_company_name_by_sub_wapper(self, key: str, value: str):
    #     if key not in self.sub_key:
    #         return f'不存在{key}这个字段名，请根据用户的内容中找出正确的字段名。'
    #     list_a_data = []
    #     list_a_data = self.search_company_name_by_sub(key, value)
    #
    #     if list_a_data == [] and (key == '关联上市公司股票简称' or key == '关联上市公司全称'):
    #         list_a_data = self.search_company_name_by_sub('关联上市公司股票简称', value)
    #         if list_a_data == []:
    #             list_a_data = self.search_company_name_by_sub('关联上市公司全称', value)
    #         if list_a_data == []:
    #             tmp = self.search_company_name_by_info('公司简称', value)
    #             if len(tmp) == 0:
    #                 tmp = self.search_company_name_by_info('英文名称', value)
    #             if len(tmp) > 0:
    #                 list_a_data = self.search_company_name_by_sub('关联上市公司全称', tmp[0]['公司名称'])
    #
    #     if list_a_data == [] and key == '公司名称':
    #         if list_a_data == []:
    #             list_a_data = self.search_company_name_by_info('英文名称', value)
    #         if list_a_data == []:
    #             list_a_data = self.search_company_name_by_info('公司简称', value)
    #
    #     if list_a_data == []:
    #         return f'字段名或字段值提供错误，请根据用户的内容中找出正确的字段名和字段值。'
    #     return list_a_data
    #
    # def search_company_name_by_info_and_register(self, key: str, value: str):
    #     if key not in self.info_key:
    #         return f'不存在{key}这个字段名，请根据用户的内容中找出正确的字段名。'
    #     list_a_data = []
    #     if key in self.info_key:
    #         list_a_data = self.search_company_name_by_info(key, value)
    #         if list_a_data == []:
    #             list_a_data = self.search_company_name_by_register(key, value)
    #         if list_a_data == [] and (key == '公司名称' or key == '公司简称' or key == '英文名称'):
    #             list_a_data = self.search_company_name_by_info('公司名称', value)
    #             if list_a_data == []:
    #                 list_a_data = self.search_company_name_by_info('英文名称', value)
    #             if list_a_data == []:
    #                 list_a_data = self.search_company_name_by_info('公司简称', value)
    #
    #
    #     if list_a_data == []:
    #         return f'字段名或字段值提供错误，请根据用户的内容中找出正确的字段名和字段值。'
    #     return list_a_data

