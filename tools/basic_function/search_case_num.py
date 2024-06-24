from tools.basic_function.base_function import BaseFunction


class SearchCaseNum(BaseFunction):
    def __init__(self):
        super(SearchCaseNum, self).__init__()

    def search_case_num_by_legal_document(self, key: str, value: str):
        if key not in self.legal_document_key:
            return f'不存在{key}这个字段名，请根据用户的内容中找出正确的字段名。'
        if key == '案号':
            value = value.replace('（', '(').replace('）',')')


        data = self.post_request(api='search_case_num_by_legal_document', data={"key": key, "value": value})
        if isinstance(data, dict):
            data = [data]
        if data == []:
            return f'字段名或字段值提供错误，请根据用户的内容中找出正确的字段名或字段值。'

        return data

