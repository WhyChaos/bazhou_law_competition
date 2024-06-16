from tools.basic_tools.base import Base


class SearchSubCompanyNameByInfo(Base):
    def __init__(self):
        super(SearchSubCompanyNameByInfo, self).__init__()


    def search_sub_company_name_by_info(self, key: str, value: str) -> list:
        data = self.post_request(api='search_company_name_by_sub_info', data={"key": key, "value": value})
        if isinstance(data, dict):
            data = [data]

        return data

