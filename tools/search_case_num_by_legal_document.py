from tools.base import Base


class SearchCaseNumByLegalDocument(Base):
    def __init__(self):
        super(SearchCaseNumByLegalDocument, self).__init__()
        self.tool_name = 'search_case_num_by_legal_document'



    def get_glm_tool_dict(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.tool_name,
                "description": "根据法律文书某个字段是某个值来查询具体的案号",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "key": {
                            "description": "法律文书字段名",
                            "type": "string"
                        },
                        "value": {
                            "description": "法律文书字典值",
                            "type": "string"
                        },
                    },
                    "required": ["key", "value"]
                },
            }
        }

    def search_case_num_by_legal_document(self, key: str, value: str) -> list:
        data = self.post_request(api='search_case_num_by_legal_document', data={"key": key, "value": value})
        if isinstance(data, dict):
            data = [data]

        return data

