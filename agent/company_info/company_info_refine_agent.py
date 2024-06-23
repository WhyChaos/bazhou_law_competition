from zhipuai import ZhipuAI
import json
from agent.base_agent import BaseAgent
import os

from tools.tools_handler.company_info_tools_handler import CompanyInfoToolsHandler


class CompanyInfoRefineAgent(BaseAgent):
    def __init__(self):
        super().__init__()


    def run(self, question):
        messages = []
        self.glm_run_record = 'company_info_refine_table\n'

        messages.append({
            "role": "user",
            "content": '''现在有三个工具如下：
查公司信息的工具：根据公司名称获得该公司所有基本和注册信息，可以传入多个公司名称，返回一个列表。
找公司名称的工具：根据公司某个基本信息字段是某个值时，查询所有满足条件的公司名称和数量。
筛选工具：根据公司关键字段取前n、top n等操作

根据问题，告诉我回答这个问题依次要调用哪些工具。

输出字符串的列表。

例子1:
问题：请帮我了解江苏金迪克生物技术股份有限公司所在的行业领域，并告知在该行业领域内总共有多少家企业？
输出：["调用查公司信息的工具：查询江苏金迪克生物技术股份有限公司的信息，找出公司所在的行业领域。", "调用找公司名称的工具：查询该行业领域的所有公司名称和数量。"]

例子2:
问题：能否列出计算机、通信和其他电子设备制造业注册资本排名前3位的公司，并提供它们的具体注册资本数额？
输出：["调用找公司名称的工具：查询计算机、通信和其他电子设备制造业的所有公司名称。", "调用查公司信息的工具：查询这些公司的信息，找出这些公司注册资本。", "调用筛选工具：筛选出注册资本最大的三家公司。"]

例子3:
问题：汉威科技的法人、注册地和电子邮箱分别是？
输出：["调用查公司信息的工具：查询汉威科技的公司信息，找出法人、注册地、电子邮箱。"]

例子4:
问题：请核对一下，注册编号为610000100085935，这个公司叫什么。
输出：["调用找公司名称的工具：通过注册编号为610000100085935查询公司名称。"]

问题：''' + question + '\n' +
'输出：'
        })
        while True:
            response = self.client.chat.completions.create(
                model=self.model_type,  # 填写需要调用的模型名称
                messages=messages,
                temperature=self.temperature,
                top_p=self.top_p
            )
            if response.choices[0].message.tool_calls is None:
                plan = response.choices[0].message.content
                self.glm_run_record += f'finish_reason:{response.choices[0].finish_reason};content:{response.choices[0].message.content}\n'
                try:
                    plan = json.loads(plan)
                    break
                except Exception as e:
                    print('Retry')
        return plan
