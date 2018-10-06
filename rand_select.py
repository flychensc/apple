"""
机选，
从以往几期结果里随机抽选号码
"""
import random

from lottery import get_history


def _rand_select_list(results):
    pools = {}
    for result in results:
        for idx, value in enumerate(result):
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
            if not isinstance(sequence, list):
                sequence = [sequence]
            pools.setdefault(position, (list(), len(sequence)))
            pools[position][0].extend(sequence)

    result = {}
    for position, (sequence, size) in pools.items():
        random.shuffle(sequence)
        result.setdefault(position, list())
        result[position] = random.choices(sequence, k=size)

    return result

def rand_select(code, count=30):
    _select_func = {
        '七星彩': _rand_select_list,
        '大乐透': _rand_select_dict,
        '排列五': _rand_select_list,
        '排列三': _rand_select_list,
        '双色球': _rand_select_dict,
        '七乐彩': _rand_select_dict,
        '3D': _rand_select_list,
    }
    # get history
    historys = get_history(code, count)
    results = [history['result'] for history in historys]

    return _select_func[code](results)


if __name__ == "__main__":
    codes = ['双色球', '七乐彩', '3D', '大乐透', '排列三', '排列五', '七星彩']
    for code in codes:
        print(code)
        one = rand_select(code)
        print(one)
