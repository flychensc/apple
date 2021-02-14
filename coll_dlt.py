"""
大乐透的概率输出
"""

from lottery import get_history
from pandas import DataFrame


def _calc_prob(num, datas):
    """
    计算num在datas里的概率
    e.g.:
        num = 1
        data = [[2,3],[1,7],[3,6]]
        retunr 1/3
    """
    match = 0
    for data in datas:
        if num in data:
            match += 1
    return match/len(datas)

def calc_red(historys):
    """
    {
        1: [0.16, 0.16, 0.15, ...],
        2: [0.16, 0.16, 0.22, ...],
        ...
        35: [0.16, 0.16, 0.02, ...],
    }
    """
    reds = [history['result']['red'] for history in historys]
    result = dict()
    for num in range(1,36): #35选5
        # result.setdefault(num, [])
        prob_list = list()
        size = len(reds)
        while size > 0:
            prob_list.append(_calc_prob(num, reds[:size]))
            size -= 1
        result[num] = prob_list
    return result


def calc_blue(historys):
    """
    {
        1: [0.16, 0.16, 0.15, ...],
        2: [0.16, 0.16, 0.22, ...],
        ...
        12: [0.16, 0.16, 0.3, ...],
    }
    """
    blues = [history['result']['blue'] for history in historys]
    result = dict()
    for num in range(1,13): #12选2
        # result.setdefault(num, [])
        prob_list = list()
        size = len(blues)
        while size > 0:
            prob_list.append(_calc_prob(num, blues[:size]))
            size -= 1
        result[num] = prob_list
    return result


if __name__ == '__main__':
    code = '大乐透'
    count = 250
    historys = get_history(code, count)
    data1 = calc_blue(historys)
    df1 = DataFrame.from_dict(data1, orient='index')
    df1.to_excel("大乐透.xls", sheet_name="蓝球")
    data2 = calc_red(historys)
    df2 = DataFrame.from_dict(data2, orient='index')
    df1.to_excel("大乐透.xls", sheet_name="红球")
