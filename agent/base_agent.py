from zhipuai import ZhipuAI
import os
from dotenv import load_dotenv
import sqlite3

class BaseAgent:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('glm_api_key')
        self.client = ZhipuAI(api_key=api_key)
        self.model_type = os.getenv('model_type')

        self.law_conn = sqlite3.connect(os.getenv('db_name'))
        self.run_log_table = os.getenv('run_log_table')

        self.temperature = 0.95
        self.top_p = 0.9

    def create_table_if_not_exists(self):
        # 创建一个游标对象
        cur = self.law_conn.cursor()
        # 创建表（如果不存在）
        cur.execute('''
            CREATE TABLE IF NOT EXISTS {} (
                id INTEGER PRIMARY KEY,
                question TEXT NOT NULL,
                glm_resp TEXT NOT NULL,
                timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        '''.format(self.run_log_table))
        # 提交事务
        self.law_conn.commit()
        # 关闭游标
        cur.close()

    def insert_glm_run(self, question: str, glm_resp: str):
        # 先创建表（如果不存在）
        self.create_table_if_not_exists()
        # 创建一个游标对象
        cur = self.law_conn.cursor()
        # 插入数据
        cur.execute('''
            INSERT INTO {} (question, glm_resp)
            VALUES (?, ?)
        '''.format(self.run_log_table), (question, glm_resp))
        # 提交事务
        self.law_conn.commit()
        # 关闭游标
        cur.close()
