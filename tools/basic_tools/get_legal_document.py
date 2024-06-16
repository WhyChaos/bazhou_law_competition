from tools.basic_tools.base import Base


class GetLegalDocument(Base):
    def __init__(self):
        super(GetLegalDocument, self).__init__()
        self.tool_name = 'get_legal_document'


    def get_glm_tool_dict(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.tool_name,
                "description": "根据案号获得该案所有基本信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "case_num": {
                            "description": "案号",
                            "type": "string"
                        },
                    },
                    "required": ["case_num"]
                },
            }
        }

    def get_legal_document(self, case_num: str) -> list:
        data = self.post_request(api='get_legal_document', data={"case_num": case_num})
        if isinstance(data, dict):
            data = [data]

        return data
