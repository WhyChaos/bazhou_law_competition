from zhipuai import ZhipuAI
import json
from agent.base_agent import BaseAgent
import os

from tools.tools_handler.tools_handler import ToolsHandler

from tools.basic_tool.get_company_info_tool import GetCompanyInfoTool
from tools.basic_tool.search_company_name_tool import SearchCompanyNameTool
from tools.basic_tool.get_top_n_tool import GetTopNTool


class CompanyInfoAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.run_log_table = os.getenv('run_log_company_info')
        self.tools_handler = ToolsHandler([GetCompanyInfoTool, SearchCompanyNameTool, GetTopNTool])
        self.tools = self.tools_handler.get_glm_tools_list()


    def run(self, question, plan:list):
        messages = []

        messages.append({
            "role": "system",
            "content": '你是一个乐于解答各种问题的助手，你的任务是调用工具准确回答问题。'
        })
        tool_result = []
        for item in plan:
            messages.append({
                "role": "user",
                "content": item
            })
            messages_tool = messages.copy()
            function_result = None
            while True:
                response = self.client.chat.completions.create(
                    model=self.model_type,  # 填写需要调用的模型名称
                    messages=messages_tool,
                    tools=self.tools,
                    temperature=self.temperature,
                    top_p=self.top_p
                )
                if response.choices[0].message.tool_calls is None:
                    answer = response.choices[0].message.content
                    messages.append({
                        'role': 'assistant',
                        'content': answer
                    })
                    if function_result:
                        tool_result.append(function_result)
                    break
                messages_tool.append(response.choices[0].message.model_dump())
                tool_call = response.choices[0].message.tool_calls[0]
                args = tool_call.function.arguments
                if tool_call.function.name == 'get_top_n_tool':
                    args_dict = json.loads(args) | {'info_list': tool_result[-1]}
                    function_result = self.tools_handler.call_function(function_name=tool_call.function.name,
                                                                   args_dict=args_dict)
                else:
                    function_result = self.tools_handler.call_function(function_name=tool_call.function.name,
                                                                       args_dict=json.loads(args))
                messages_tool.append({
                    "role": "tool",
                    "content": f"{json.dumps(function_result, ensure_ascii=False)}",
                    "tool_call_id": tool_call.id
                })
        while True:
            try:
                messages.append({
                    "role": "user",
                    "content": "根据前面的内容回答这个问题：" + question
                })
                response = self.client.chat.completions.create(
                    model=self.model_type,  # 填写需要调用的模型名称
                    messages=messages,
                    temperature=self.temperature,
                    top_p=self.top_p
                )
                answer = response.choices[0].message.content
                break
            except Exception as e:
                print('retry')

        return answer

