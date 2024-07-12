class CompanyInfo(Base):
    __tablename__ = "company_info"
    公司名称 = Column(Text, primary_key=True, default='')
    公司简称 = Column(Text, default='')
    英文名称 = Column(Text, default='')
    关联证券 = Column(Text, default='')
    公司代码 = Column(Text, default='')
    曾用简称 = Column(Text, default='')
    所属市场 = Column(Text, default='')
    所属行业 = Column(Text, default='')
    成立日期 = Column(Text, default='')
    上市日期 = Column(Text, default='')
    法人代表 = Column(Text, default='')
    总经理 = Column(Text, default='')
    董秘 = Column(Text, default='')
    邮政编码 = Column(Text, default='')
    注册地址 = Column(Text, default='')
    办公地址 = Column(Text, default='')
    联系电话 = Column(Text, default='')
    传真 = Column(Text, default='')
    官方网址 = Column(Text, default='')
    电子邮箱 = Column(Text, default='')
    入选指数 = Column(Text, default='')
    主营业务 = Column(Text, default='')
    经营范围 = Column(Text, default='')
    机构简介 = Column(Text, default='')
    每股面值 = Column(Text, default='')
    首发价格 = Column(Text, default='')
    首发募资净额 = Column(Text, default='')
    首发主承销商 = Column(Text, default='')


class CompanyRegister(Base):
    __tablename__ = 'company_register'
    公司名称 = Column(Text, primary_key=True, default='')
    登记状态 = Column(Text, default='')
    统一社会信用代码 = Column(Text, default='')
    法定代表人 = Column(Text, default='')
    注册资本 = Column(Text, default='')
    成立日期 = Column(Text, default='')
    企业地址 = Column(Text, default='')
    联系电话 = Column(Text, default='')
    联系邮箱 = Column(Text, default='')
    注册号 = Column(Text, default='')
    组织机构代码 = Column(Text, default='')
    参保人数 = Column(Text, default='')
    行业一级 = Column(Text, default='')
    行业二级 = Column(Text, default='')
    行业三级 = Column(Text, default='')
    曾用名 = Column(Text, default='')
    企业简介 = Column(Text, default='')
    经营范围 = Column(Text, default='')


class SubCompanyInfo(Base):
    __tablename__ = 'sub_company_info'
    关联上市公司全称 = Column(Text, default='')
    上市公司关系 = Column(Text, default='')
    上市公司参股比例 = Column(Text, default='')
    上市公司投资金额 = Column(Text, default='')
    公司名称 = Column(Text, primary_key=True, default='')


class LegalDoc(Base):
    __tablename__ = 'legal_doc'
    关联公司 = Column(Text, default='')
    标题 = Column(Text, default='')
    案号 = Column(Text, default='', primary_key=True)
    文书类型 = Column(Text, default='')
    原告 = Column(Text, default='')
    被告 = Column(Text, default='')
    原告律师事务所 = Column(Text, default='')
    被告律师事务所 = Column(Text, default='')
    案由 = Column(Text, default='')
    涉案金额 = Column(Text, default='')
    判决结果 = Column(Text, default='')
    日期 = Column(Text, default='')
    文件名 = Column(Text, default='')


class CourtInfo(Base):
    __tablename__ = 'court_info'
    法院名称 = Column(Text, default='', primary_key=True)
    法院负责人 = Column(Text, default='')
    成立日期 = Column(Text, default='')
    法院地址 = Column(Text, default='')
    法院联系电话 = Column(Text, default='')
    法院官网 = Column(Text, default='')


class CourtCode(Base):
    __tablename__ = 'court_code'
    法院名称 = Column(Text, default='', primary_key=True)
    行政级别 = Column(Text, default='')
    法院级别 = Column(Text, default='')
    法院代字 = Column(Text, default='')
    区划代码 = Column(Text, default='')
    级别 = Column(Text, default='')


class LawfirmInfo(Base):
    __tablename__ = 'lawfirm_info'
    律师事务所名称 = Column(Text, default='', primary_key=True)
    律师事务所唯一编码 = Column(Text, default='')
    律师事务所负责人 = Column(Text, default='')
    事务所注册资本 = Column(Text, default='')
    事务所成立日期 = Column(Text, default='')
    律师事务所地址 = Column(Text, default='')
    通讯电话 = Column(Text, default='')
    通讯邮箱 = Column(Text, default='')
    律所登记机关 = Column(Text, default='')


class LawfirmLog(Base):
    __tablename__ = 'lawfirm_log'
    律师事务所名称 = Column(Text, default='', primary_key=True)
    业务量排名 = Column(Text, default='')
    服务已上市公司 = Column(Text, default='')
    报告期间所服务上市公司违规事件 = Column(Text, default='')
    报告期所服务上市公司接受立案调查 = Column(Text, default='')


class AddrInfo(Base):
    __tablename__ = 'addr_info'
    地址 = Column(Text, default='', primary_key=True)
    省份 = Column(Text, default='')
    城市 = Column(Text, default='')
    区县 = Column(Text, default='')


class AddrCode(Base):
    __tablename__ = 'addr_code'
    省份 = Column(Text, default='')
    城市 = Column(Text, default='')
    城市区划代码 = Column(Text, default='')
    区县 = Column(Text, default='')
    区县区划代码 = Column(Text, default='', primary_key=True)


class TempInfo(Base):
    __tablename__ = 'temp_info'
    日期 = Column(Text, default='', primary_key=True)
    省份 = Column(Text, default='', primary_key=True)
    城市 = Column(Text, default='')
    天气 = Column(Text, default='')
    最高温度 = Column(Text, default='')
    最低温度 = Column(Text, default='')
    湿度 = Column(Text, default='')


class LegalAbstract(Base):
    __tablename__ = 'legal_abstract'
    文件名 = Column(Text, default='')
    案号 = Column(Text, default='', primary_key=True)
    文本摘要 = Column(Text, default='')


class XzgxfInfo(Base):
    __tablename__ = 'xzgxf_info'
    限制高消费企业名称 = Column(Text, default='')
    案号 = Column(Text, default='', primary_key=True)
    法定代表人 = Column(Text, default='')
    申请人 = Column(Text, default='')
    涉案金额 = Column(Text, default='')
    执行法院 = Column(Text, default='')
    立案日期 = Column(Text, default='')
    限高发布日期 = Column(Text, default='')