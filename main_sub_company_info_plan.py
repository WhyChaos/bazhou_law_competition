from agent.sub_company_info.sub_company_info_plan_agent import SubCompanyInfoPlanAgent
import json
import concurrent.futures

from datetime import datetime
import threading

class Game:
    def __init__(self):
        self.max_threads = 5
        self.question_file_path = 'list_a_data/company_sub_question.jsonl'
        self.submission_file_path = f'list_a_data/submission_{self.get_current_time_string()}.jsonl'
        self.question_list = self.read_jsonl(self.question_file_path)
        self.lock = threading.Lock()

        # 获取当前时间并格式化
    def get_current_time_string(self):
        now = datetime.now()
        formatted_time = now.strftime("%Y_%m_%d_%H_%M")
        return formatted_time


    def read_jsonl(self, file_path):
        data = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                data.append(json.loads(line.strip()))
        return data

    def append_to_jsonl(self, file_path, data):
        with self.lock:
            with open(file_path, 'a', encoding='utf-8') as file:
                json_line = json.dumps(data, ensure_ascii=False)
                file.write(json_line + '\n')

    def run_one_question(self, question_dict:dict):
        print(f"目前ID:", question_dict['id'])
        agent = SubCompanyInfoPlanAgent()
        if question_dict['table_type'] == '1':
            plan = agent.run(question=question_dict['question'])
            answer_dict = {'id': question_dict['id'], 'table_type': question_dict['table_type'], 'question': question_dict['question'], 'plan': plan}
            self.append_to_jsonl(self.submission_file_path, answer_dict)
        return question_dict['id']

    def sort(self):
        answer_dict_list = self.read_jsonl(self.submission_file_path)
        def custom_sort(data):
            return data['id']

        answer_dict_list = sorted(answer_dict_list, key=custom_sort)
        with open(self.submission_file_path, 'w') as file:
            pass
        for answer_dict in answer_dict_list:
            self.append_to_jsonl(self.submission_file_path, answer_dict)

    def single_thread_run(self):
        for question_dict in self.question_list:
            self.run_one_question(question_dict)
        self.sort()

    def multi_thread_run(self):
        with concurrent.futures.ThreadPoolExecutor(self.max_threads) as executor:
            # 提交任务到线程池
            futures = [executor.submit(self.run_one_question, question_dict) for question_dict in self.question_list]
            # # 等待所有任务完成并获取结果
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                print(f'Result: {result}')
        # concurrent.futures.wait(futures)
        self.sort()


if __name__ == '__main__':
    game = Game()
    game.single_thread_run()