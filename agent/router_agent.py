
from agent.base_agent import BaseAgent


class RouterAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def run(self, query):
        messages = []
        messages.append({
            "role": "system",
            "content": '''你是一位问题分类的专家，你的任务是根据用户给出的query，将其分为开放的问题和依赖数据库的问题。
数据库的表有公司信息表、融资信息表、法律文书表。
一定只输出0或1，不要有其他内容。
0表示开放的问题，1表示依赖数据库的问题'''
        })
        messages.append({
            "role": "user",
            "content": query
        })
        response = self.client.chat.completions.create(
            model=self.model_type,
            messages=messages,
            temperature=self.temperature,
            top_p=self.top_p
        )
        return response.choices[0].message.content
