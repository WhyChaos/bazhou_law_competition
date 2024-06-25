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
        call_tool_result = []
        idx = 0
        while idx < len(plan):
            item = plan[idx]
            messages.append({
                "role": "user",
                "content": item
            })
            function_result = None
            messages_backup = messages.copy()
            while True:
                tool_choice = self.choose_tool(item)

                if len(call_tool_result) > 0 and call_tool_result[-1] == tool_choice:
                    response = self.answer_without_before(item, tool_choice)
                else:
                    response = self.answer_with_before(messages, item, tool_choice)


                if response.choices[0].message.tool_calls is None:
                    continue
                # messages_tool.append(response.choices[0].message.model_dump())
                tool_call = response.choices[0].message.tool_calls[0]
                args = tool_call.function.arguments
                if tool_call.function.name == 'get_top_n_tool':
                    args_dict = json.loads(args) | {'info_list': tool_result[-1]}
                    function_result = self.tools_handler.call_function(function_name=tool_call.function.name,
                                                                   args_dict=args_dict)
                else: # 当调用查询公司信息的时候，可以和get_top_n_tool 一样，用确定的消息传递（tool_result）
                    function_result = self.tools_handler.call_function(function_name=tool_call.function.name,
                                                                       args_dict=json.loads(args))

                if isinstance(function_result,str):
                    messages.append(response.choices[0].message.model_dump())
                    messages.append({
                        "role": "tool",
                        'content': function_result,
                        "tool_call_id": tool_call.id
                    })
                else:
                    messages = messages_backup
                    messages.append({
                        "role": "tool",
                        'content': json.dumps(function_result, ensure_ascii=False)
                    })
                    idx += 1
                    tool_result.append(function_result)
                    call_tool_result.append(tool_choice)
                    break
                # messages_tool.append({
                #     "role": "tool",
                #     "content": f"{json.dumps(function_result, ensure_ascii=False)}",
                #     "tool_call_id": tool_call.id
                # })
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
                    top_p=self.top_p,
                    max_tokens=8192
                )
                answer = response.choices[0].message.content
                break
            except Exception as e:
                print('retry')

        return answer

    def answer_with_before(self, messages, item, tool_choice):
        response = self.client.chat.completions.create(
            model=self.model_type,  # 填写需要调用的模型名称
            messages=messages,
            tools=self.tools,
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=8192,
            tool_choice={"type": "function", "function": {"name": tool_choice}},
        )
        return response

    def answer_without_before(self, item, tool_choice):
        messages = []
        messages.append({
            "role": "system",
            "content": '你是一个乐于解答各种问题的助手，你的任务是调用工具准确回答问题。'
        })
        messages.append({
            "role": "user",
            "content": item
        })
        response = self.client.chat.completions.create(
            model=self.model_type,  # 填写需要调用的模型名称
            messages=messages,
            tools=self.tools,
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=8192,
            tool_choice={"type": "function", "function": {"name": tool_choice}},
        )
        return response


    def choose_tool(self, query):
        messages = []
        messages.append({
            "role": "system",
            "content": '''你是一个语义理解的助手，你的任务是根据用户的query,判断调用什么工具。
使用查公司信息的工具时，输出'get_company_info_tool',
使用找公司名称的工具时，输出'search_company_name_tool',
使用筛选工具时，输出'get_top_n_tool'。
不要输出其他内容。
'''.format()
        })
        messages.append({
            "role": "user",
            "content": 'query：' + query + '''
回答我get_company_info_tool或search_company_name_tool或get_top_n_tool'''
        })
        while True:
            response = self.client.chat.completions.create(
                model=self.model_type,  # 填写需要调用的模型名称
                messages=messages,
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=20
            )
            answer = response.choices[0].message.content
            if answer == 'get_company_info_tool':
                break
            if answer == 'search_company_name_tool':
                break
            if answer == 'get_top_n_tool':
                break
        return answer

