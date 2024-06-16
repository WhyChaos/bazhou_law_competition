from tools.basic_tools.base import Base


class GetLegalDocument(Base):
    def __init__(self):
        super(GetLegalDocument, self).__init__()

    def get_legal_document(self, case_num: str) -> dict:
        data = self.post_request(api='get_legal_document', data={"case_num": case_num})
        if data is None:
            data = {}
        return data
