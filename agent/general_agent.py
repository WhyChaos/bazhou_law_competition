
from agent.base_agent import BaseAgent


class GeneralAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def run(self, query):
        messages = []
        messages.append({
            "role": "system",
            "content": '你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。'
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
