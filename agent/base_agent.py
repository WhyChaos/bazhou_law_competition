from zhipuai import ZhipuAI
import os
from dotenv import load_dotenv

class BaseAgent:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('glm_api_key')
        self.client = ZhipuAI(api_key=api_key)
        self.model_type = os.getenv('model_type')

        self.law_conn = os.getenv('db_name')
        self.run_log_table = os.getenv('run_log_table')

        self.temperature = 0.95
        self.top_p = 0.9

