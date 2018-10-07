"""
机选，
从以往count期结果里，随机k个抽选号码，随机选择一份
"""
import random

from lottery import get_history, similar


def _rand_select_list(results):
    pools = {}
    for result in results:
        for idx, value in enumerate(result):
            # 【排列】按位区分，放入历史每位的数据
            pools.setdefault(idx, list())
            pools[idx].append(value)

    result = []
    for sequence in pools.values():
        random.shuffle(sequence)
        result.append(random.choice(sequence))

    return result

def _rand_select_dict(results):
    pools = {}

    for result in results:
        for position, sequence in result.items():
            if type(sequence) is not list:
                sequence = [sequence]
            # 【组合】按颜色区分，放入历史每个颜色的数据，以及数量
            pools.setdefault(position, (list(), len(sequence)))
            pools[position][0].extend(sequence)

    result = {}
    for position, (sequence, size) in pools.items():
        random.shuffle(sequence)
        if size != 1:
            while 1:
                result[position] = random.choices(sequence, k=size)
                if len(result[position]) == len(set(result[position])):
                    break
        else:
            result[position] = random.choice(sequence)

    return result

def rand_select(code, count=30, k=10):
    _select_func = {
        '七星彩': _rand_select_list,
        '大乐透': _rand_select_dict,
        '排列五': _rand_select_list,
        '排列三': _rand_select_list,
        '双色球': _rand_select_dict,
        '七乐彩': _rand_select_dict,
        '3D': _rand_select_list,
    }
    _ref_range = {
        '七星彩': (5, 14),
        '大乐透': (12, 18),
        '排列五': (6, 12),
        '排列三': (4, 16),
        '双色球': (12, 20),
        '七乐彩': (16, 24),
        '3D': (5, 15),
    }
    # get history
    historys = get_history(code, count)
    # only result
    results = [history['result'] for history in historys]
    # random selection
    (s_min, s_max) = _ref_range[code]
    rs = []
    while 1:
        r = _select_func[code](results)
        s = similar(r, results)
        if s_min < s*100 < s_max:
            rs.append((r, s))
        if len(rs) == k:
            break
    return random.choice(rs)

if __name__ == "__main__":
    codes = ['双色球', '七乐彩', '3D', '大乐透', '排列三', '排列五', '七星彩']
    for code in codes:
        one = rand_select(code)
        print("{0}\r\n  {1}\r\n  {2:.2f}%\r\n".format(code, one[0], one[1]*100))
