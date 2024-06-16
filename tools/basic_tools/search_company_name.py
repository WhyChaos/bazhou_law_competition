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

    def search_company_name_by_info_and_register_and_sub(self, key: str, value: str) -> list:
        data = self.search_company_name_by_info(key, value)
        if data == []:
            data = self.search_company_name_by_register(key, value)
        if data == []:
            data = self.search_company_name_by_sub(key, value)
        return data
