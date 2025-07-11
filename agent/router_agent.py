
from agent.base_agent import BaseAgent


class RouterAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def run(self, query):
        messages = []
        messages.append({
            "role": "system",
            "content": '''你是一位问题分类的专家，你的任务是根据用户给出的query，将其分为开放的问题和依赖数据库的问题。
数据库的表有公司信息表、融资信息表、法院判决书表。
一定只输出0或1，不要有其他内容。
0表示开放的问题，1表示依赖数据库的问题'''
        })
        messages.append({
            "role": "user",
            "content": query
        })
        count = 0
        while True:
            response = self.client.chat.completions.create(
                model=self.model_type,
                messages=messages,
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=2
            )
            type = response.choices[0].message.content
            print(f'{query}-----{type}')
            if type == '0' or type == '1':
                break
            count += 1
            if count > 5:
                break
        return type
