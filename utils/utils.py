def convert_to_number(amount_str):
    # 定义单位及其对应的数值
    units = {
        '千': 10 ** 3,
        '万': 10 ** 4,
        '亿': 10 ** 8,
    }

    # 初始化结果为0
    number = 1.0

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