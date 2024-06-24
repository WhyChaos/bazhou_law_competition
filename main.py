from agent import Agent
import json
import concurrent.futures

from datetime import datetime

class Game:
    def __init__(self):
        self.max_threads = 5
        self.question_file_path = 'data/one_question.jsonl'
        self.submission_file_path = f'data/submission_{self.get_current_time_string()}.jsonl'
        self.question_list = self.read_jsonl(self.question_file_path)

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
        with open(file_path, 'a', encoding='utf-8') as file:
            json_line = json.dumps(data, ensure_ascii=False)
            file.write(json_line + '\n')

    def run_one_question(self, question_dict:dict):
        print(f"目前ID:", question_dict['id'])
        agent = Agent()
        # answer = agent.run(question=question_dict['question'])
        answer_dict = {'id': question_dict['id'], 'question': question_dict['question'], 'answer': answer}
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

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(self.max_threads) as executor:
            # 提交任务到线程池
            futures = [executor.submit(self.run_one_question, question_dict) for question_dict in self.question_list]

            # # 等待所有任务完成并获取结果
            # for future in concurrent.futures.as_completed(futures):
            #     result = future.result()
            #     print(f'Result: {result}')
        self.sort()


if __name__ == '__main__':
    game = Game()
    # game.run()
    tmp = {"id": 124, "question": "简述侵犯著作权罪的客观行为。", "answer": "侵犯著作权罪的客观行为主要表现为未经著作权人许可，擅自复制、发行、出租、展览、表演、放映、广播、信息网络传播著作权人的作品，或者未经专利权人许可，擅自实施专利，或者未经商标权人许可，擅自使用商标，或者未经著作权人许可，擅自使用与著作权有关的权利，情节严重的行为。\n\n具体来说，这些客观行为包括：\n\n1. 未经著作权人许可，复制、发行、出租、展览、表演、放映、广播、信息网络传播著作权人的作品，包括文字作品、音乐作品、美术作品、视听作品、计算机软件等。\n\n2. 未经专利权人许可，实施专利，包括制造、使用、许诺销售、销售、进口专利产品，或者使用专利方法，或者使用、许诺销售、销售、进口依照该专利方法直接获得的 产品。\n\n3. 未经商标权人许可，使用商标，包括在同一种商品上使用与其注册商标相同的商标，或者在同一种商品上使用与其注册商标近似的商标，或者销售明知是他人的注册 商标标识。\n\n4. 未经著作权人许可，使用与著作权有关的权利，包括出版、表演、录音录像、播放、展览、发行、信息网络传播等。\n\n这些行为需达到情节严重的程度，如侵权时间长、范围广、获利大等，才能构成侵犯著作权罪。"}

    game.run_one_question(tmp)