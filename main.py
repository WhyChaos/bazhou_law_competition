from agent import Agent
import json

from datetime import datetime

# 获取当前时间并格式化
def get_current_time_string():
    now = datetime.now()
    formatted_time = now.strftime("%Y_%m_%d_%H_%M")
    return formatted_time


def read_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line.strip()))
    return data

def append_to_jsonl(file_path, data):
    with open(file_path, 'a', encoding='utf-8') as file:
        json_line = json.dumps(data, ensure_ascii=False)
        file.write(json_line + '\n')


def main():
    agent = Agent()
    question_file_path = 'data/question.jsonl'
    submission_file_path = f'data/submission_{get_current_time_string()}.jsonl'
    question_list = read_jsonl(question_file_path)

    for question_dict in question_list:
        print(f"目前ID:",question_dict['id'])
        answer = agent.run(question=question_dict['question'])
        answer_dict = {'id':question_dict['id'], 'question':question_dict['question'], 'answer': answer}
        append_to_jsonl(submission_file_path, answer_dict)


if __name__ == '__main__':
    main()