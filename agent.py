from zhipuai import ZhipuAI
import json
import os
import local_tools
from dotenv import load_dotenv

from tools import tools_handler


class Agent:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv('glm_api_key')
        self.client = ZhipuAI(api_key=api_key)
        self.tools = local_tools.tool_list
        self.model_type = 'glm-4'
        self.tools_handler = tools_handler.ToolsHandler()

    def run(self, question):
        messages = []
        messages.append({
            "role": "system",
            "content": "你是一个善于调用工具的助手，你的任务是为用户回答准确的答案。"
        })
        messages.append({
            "role": "user",
            "content": question
        })
        response = self.client.chat.completions.create(
            model=self.model_type,  # 填写需要调用的模型名称
            messages=messages,
            tools=self.tools,
        )
        while response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            args = tool_call.function.arguments
            function_result = self.tools_handler.call_function(function_name=tool_call.function.name, args=args)
            messages.append({
                "role": "tool",
                "content": f"{json.dumps(function_result)}",
                "tool_call_id": tool_call.id
            })
            response = self.client.chat.completions.create(
                model=self.model_type,
                messages=messages,
                tools=self.tools,
            )
            print(response.choices[0].message)
            messages.append(response.choices[0].message.model_dump())

        print(response.choices[0].message)

