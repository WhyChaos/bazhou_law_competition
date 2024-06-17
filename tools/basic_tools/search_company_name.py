from tools.basic_tools.base import Base


class SearchCompanyName(Base):
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

    def search_company_name_by_info_and_register_and_sub(self, key: str, value: str):
        if key not in self.info_key and key not in self.register_key and key not in self.sub_key:
            return f'不存在{key}这个字段名，请根据用户的内容中找出正确的字段名。'

        data = []
        if key in self.info_key:
            data = self.search_company_name_by_info(key, value)
        if data == [] and key in self.register_key:
            data = self.search_company_name_by_register(key, value)
        if data == [] and key in self.sub_key:
            data = self.search_company_name_by_sub(key, value)
        if key == '公司名称':
            key = '公司简称'
            if data == [] and key in self.info_key:
                data = self.search_company_name_by_info(key, value)
            if data == [] and key in self.register_key:
                data = self.search_company_name_by_register(key, value)
            if data == [] and key in self.sub_key:
                data = self.search_company_name_by_sub(key, value)
        if data == []:
            return f'字段名或字段值提供错误，请根据用户的内容中找出正确的字段名或字段值。'
        return data
