import requests
from dotenv import load_dotenv
import os
import time
import sqlite3
import json


class BaseFunction(object):
    def __init__(self):
        load_dotenv()
        self.base_url = 'https://comm.chatglm.cn/law_api/'
        self.token = os.getenv('token')
        self.info_key = [
            '公司名称', '公司简称', '英文名称', '关联证券', '公司代码', '曾用简称', '所属市场', '所属行业', '上市日期',
            '法人代表', '总经理', '董秘', '邮政编码', '注册地址', '办公地址', '联系电话', '传真', '官方网址',
            '电子邮箱', '入选指数', '主营业务', '经营范围', '机构简介', '每股面值', '首发价格', '首发募资净额', '首发主承销商',
            '登记状态', '统一社会信用代码', '注册资本', '成立日期', '省份', '城市', '区县', '注册号',
            '组织机构代码', '参保人数', '企业类型', '曾用名'
        ]
        self.sub_key = [
            '关联上市公司股票代码', '关联上市公司股票简称', '关联上市公司全称', '上市公司关系', '上市公司参股比例',
            '上市公司投资金额', '公司名称'
        ]
        self.legal_document_key = [
            '标题', '案号', '文书类型', '原告', '被告', '原告律师', '被告律师', '案由', '审理法条依据', '涉案金额',
            '判决结果', '胜诉方', '文件名'
        ]
        self.law_conn = sqlite3.connect('law.db')
        self.law_api_table_name = 'law_api_table'

    def post_request(self, api: str, data: dict):
        query_result = self.query_law_api(api_name=api, data=self.json_dumps(data))
        if query_result:
            resp_data = self.json_loads(query_result[0][3])
        else:
            url = self.base_url + api
            headers = {
                'Authorization': 'Bearer ' + self.token,
                'Content-Type': 'application/json'
            }
            response = requests.post(url, headers=headers, json=data)

            while response.status_code != 200:
                response = requests.post(url, headers=headers, json=data)
                print(f'api: {api}, status: {response.status_code}, list_a_data: {data}')
                time.sleep(2)

            resp_data = response.json()
            try:
                self.insert_law_api(api_name=api, data=self.json_dumps(data), resp_data=self.json_dumps(resp_data))
            except Exception as e:
                print(f'插入失败,api: {api}, error: {e}, list_a_data: {data}, resp_data: {resp_data}')

        if isinstance(resp_data, str):
            resp_data = None

        print(resp_data)
        return resp_data


    def create_table_if_not_exists(self):
        # 创建一个游标对象
        cur = self.law_conn.cursor()
        # 创建表（如果不存在）
        cur.execute('''
            CREATE TABLE IF NOT EXISTS {} (
                id INTEGER PRIMARY KEY,
                api_name TEXT NOT NULL,
                list_a_data TEXT NOT NULL,
                resp_data TEXT NOT NULL,
                UNIQUE(api_name, list_a_data)
            )
        '''.format(self.law_api_table_name))
        # 提交事务
        self.law_conn.commit()
        # 关闭游标
        cur.close()

    def insert_law_api(self, api_name: str, data: str, resp_data: str):
        # 先创建表（如果不存在）
        self.create_table_if_not_exists()
        # 创建一个游标对象
        cur = self.law_conn.cursor()
        # 插入数据
        cur.execute('''
            INSERT INTO {} (api_name, list_a_data, resp_data)
            VALUES (?, ?, ?)
        '''.format(self.law_api_table_name), (api_name, data, resp_data))
        # 提交事务
        self.law_conn.commit()
        # 关闭游标
        cur.close()

    def query_law_api(self, api_name: str, data: str):
        # 先创建表（如果不存在）
        self.create_table_if_not_exists()
        # 创建一个游标对象
        cur = self.law_conn.cursor()
        # 查询数据
        cur.execute('''
            SELECT * FROM {}
            WHERE api_name = ?
            AND list_a_data = ?
        '''.format(self.law_api_table_name), (api_name, data))
        rows = cur.fetchall()
        # 关闭游标
        cur.close()
        return rows

    def json_dumps(self, data):
        json_str = json.dumps(data, ensure_ascii=False)
        return json_str

    def json_loads(self, data: str):
        return json.loads(data)


