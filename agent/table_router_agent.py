
from agent.base_agent import BaseAgent
from utils.schema import database_schema


class TableRouterAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def run(self, query):
        messages = []
        messages.append({
            "role": "system",
            "content": '你是一个好助手，你的任务是根据用户给出的问题，告诉用户回答这个问题需要哪张表。' +
            database_schema + '\n公司信息表用0表示，子公司融资信息表用1表示，法院判决书表用1表示。\n' +
            '只输出0或1或2，不要输出其他内容。'
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
            table_type = response.choices[0].message.content
            print(f'{query}-----{table_type}')
            if table_type == '0' or table_type == '1' or table_type == '2':
                break
            count += 1
            if count > 5:
                break
        if table_type not in ['0', '1', '2']:
            return '2'
        return table_type
