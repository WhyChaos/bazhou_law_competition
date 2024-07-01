import json

from tools.basic_tool.get_sub_company_info_tool import GetSubCompanyInfoTool
from tools.basic_tool.get_mother_company_name_tool import GetMotherCompanyNameTool
from utils.utils import convert_from_number

tmp = convert_from_number(123200330000)
print(tmp)
#

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


def convert_to_number(amount_str):
    if amount_str is None:
        return 0
    # 定义单位及其对应的数值
    units = {
        '千': 10 ** 3,
        '万': 10 ** 4,
        '亿': 10 ** 8,
    }

    # 初始化结果为0
    number = 1

    # 遍历单位
    for unit, multiplier in units.items():
        if unit in amount_str:
            # 找到单位所在的位置
            position = amount_str.find(unit)
            # 将单位前面的部分转换为浮点数，并乘以相应的倍数
            number *= multiplier
            # 移除已处理的部分
            amount_str = amount_str[:position] + amount_str[position + len(unit):]

    # 如果剩下的部分是数字，将其转换并加到结果中
    if amount_str:
        number *= float(amount_str)

    return number




def json_all():
    file_path = 'list_a_data/question_backup.jsonl'
    file_path_tmp = 'list_a_data/question_with_table_type.jsonl'
    data = read_jsonl(file_path)
    data_tmp = read_jsonl(file_path_tmp)
    for idx, item in enumerate(data):
        print('id', item['id'])
        if data[idx]['question'] != data_tmp[idx]['question']:
            print('错误1')
            break
        if data_tmp[idx]['type'] != '0' and data_tmp[idx]['type'] != '1':
            print('错误2')
            break
        if data_tmp[idx]['type'] == '0' and data_tmp[idx]['table_type'] != '100':
            print('错误3')
            break
        if data_tmp[idx]['type'] == '1' and data_tmp[idx]['table_type'] not in ['0', '1', '2']:
            print('错误4')
            break

def test_tool():
    tmp = GetMotherCompanyNameTool()
    info = tmp.run(sub_company_name='Jiangsu Yida Chemical Co., Ltd.')

    # tmp = GetSubCompanyInfoTool()
    # info = tmp.run(mother_company_name='恒宇信通航空装备(北京)股份有限公司')

    #
    print(info)


def test():
    file_path_answer = 'list_a_data/submission/5_submission.jsonl'
    file_path_question = 'list_a_data/question_with_table_type.jsonl'
    answer = read_jsonl(file_path_answer)
    question = read_jsonl(file_path_question)
    answer_dict = {}
    for item in answer:
        answer_dict[item['id']] = item
    question_dict = {}
    for item in question:
        question_dict[item['id']] = item

    for key, value in question_dict.items():
        print('id: ',key)
        if value['table_type'] == '0' and key not in answer_dict:
            print('错误', key)
            break
        if value['table_type'] == '0' and answer_dict[key]['question'] != value['question']:
            print('question错误', key)
            break

def merge():
    origin_answer = read_jsonl('list_a_data/submission/5_submission.jsonl')
    new_answer = read_jsonl('list_a_data/company_info_answer.jsonl')

    question_with_table_type = read_jsonl('list_a_data/question_with_table_type.jsonl')

    origin_answer_dict = {}
    for item in origin_answer:
        origin_answer_dict[item['id']] = item
    new_answer_dict = {}
    for item in new_answer:
        new_answer_dict[item['id']] = item

    for idx in range(230):
        table_type = question_with_table_type[idx]['table_type']
        item = origin_answer[idx]
        if table_type == '0':
            print('id:', idx)
            if item['id'] != idx or idx != question_with_table_type[idx]['id']:
                print('错误1')
                break
            if item['question'] != new_answer_dict[idx]['question']:
                print('错误2')
                break
            item['answer'] = new_answer_dict[idx]['answer']

        append_to_jsonl('list_a_data/submission/6_submission.jsonl', item)

# merge()
# test()
# test_tool()




