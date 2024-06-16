from tools.basic_tools.base import Base


class GetSubCompanyInfo(Base):
    def __init__(self):
        super(GetSubCompanyInfo, self).__init__()

    def get_company_sub_info(self, company_name: str) -> dict:
        data = self.post_request(api='get_sub_company_info', data={"company_name": company_name})
        if data is None:
            data = {}
        return data





