from tools.basic_function.get_legal_document import GetLegalDocument
from tools.basic_function.search_case_num import SearchCaseNum
class LegalDocumentInfo:
    def __init__(self):
        self.tool_name = 'legal_document_info'
        self.get_legal_document = GetLegalDocument()
        self.search_case_num_by_legal_document = SearchCaseNum()

    def get_glm_tool_dict(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.tool_name,
                "description": "根据法律文书信息字段是某个值时，查询所有满足条件的法律文书信息和数量",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "key": {
                            "description": "法律文书信息字段名称",
                            "enum": self.get_legal_document.legal_document_key,
                            "type": "string"
                        },
                        "value": {
                            "description": "法律文书信息字段具体的值",
                            "type": "string"
                        },
                    },
                    "required": ["key", "value"]
                },
            }
        }

    def run(self, key: str, value: str):
        case_num_list = self.search_case_num_by_legal_document.search_case_num_by_legal_document(key=key, value=value)
        if isinstance(case_num_list, str):
            return case_num_list
        info_list = []
        if case_num_list:
            for case_num_dict in case_num_list:
                info_list.append(self.get_legal_document.get_legal_document(case_num=case_num_dict['案号']))
        info = {}
        info['案件数量'] = len(case_num_list)
        info['案件信息'] = info_list
        return info
