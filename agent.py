from zhipuai import ZhipuAI
import json
import os
from dotenv import load_dotenv

from tools import tools_handler
import sqlite3


class Agent:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('glm_api_key')
        self.client = ZhipuAI(api_key=api_key)
        self.model_type = 'glm-4'
        self.tools_handler = tools_handler.ToolsHandler()
        self.tools = self.tools_handler.get_glm_tools_list()

        self.law_conn = sqlite3.connect('law.db')
        self.law_glm_run_table_name = 'law_glm_run_table'

    def run(self, question):
        messages = []
        glm_run_record = ''
        answer = ''
        messages.append({
            "role": "system",
            "content": "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。"
        })
        messages.append({
            "role": "user",
            "content": question
        })
        while True:
            response = self.client.chat.completions.create(
                model=self.model_type,  # 填写需要调用的模型名称
                messages=messages,
                tools=self.tools,
            )
            if response.choices[0].message.tool_calls is None:
                answer = response.choices[0].message.content
                glm_run_record += f'finish_reason:{response.choices[0].finish_reason};content:{response.choices[0].message.content}\n'
                break
            messages.append(response.choices[0].message.model_dump())
            tool_call = response.choices[0].message.tool_calls[0]
            args = tool_call.function.arguments
            function_result = self.tools_handler.call_function(function_name=tool_call.function.name,
                                                               args_dict=json.loads(args))
            messages.append({
                "role": "tool",
                "content": f"{json.dumps(function_result, ensure_ascii=False)}",
                "tool_call_id": tool_call.id
            })
            glm_run_record += (f'finish_reason:{response.choices[0].finish_reason};' +
                               f'tool_name:{response.choices[0].message.tool_calls[0].function.name};' +
                               f'tool_arguments:{response.choices[0].message.tool_calls[0].function.arguments};' +
                               f'tool_result:{json.dumps(function_result, ensure_ascii=False)}\n')

            print(response.choices[0].message)

        try:
            self.insert_glm_run(question, glm_run_record)
        except Exception as e:
            print('记录失败')
        return answer

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
        '''.format(self.law_glm_run_table_name))
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
        '''.format(self.law_glm_run_table_name), (question, glm_resp))
        # 提交事务
        self.law_conn.commit()
        # 关闭游标
        cur.close()
