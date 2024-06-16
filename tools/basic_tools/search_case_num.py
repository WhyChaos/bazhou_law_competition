from tools.basic_tools.base import Base


class SearchCaseNum(Base):
    def __init__(self):
        super(SearchCaseNum, self).__init__()

    def search_case_num_by_legal_document(self, key: str, value: str) -> list:
        data = self.post_request(api='search_case_num_by_legal_document', data={"key": key, "value": value})
        if isinstance(data, dict):
            data = [data]

        return data

