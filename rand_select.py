"""
机选，
从以往count期结果里，随机times次抽选号码，选择相似度最低的那份
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
        result.setdefault(position, list())
        if size != 1:
            result[position] = random.choices(sequence, k=size)
        else:
            result[position] = random.choice(sequence)

    return result

def rand_select(code, count=30, times=10):
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
    # only result
    results = [history['result'] for history in historys]
    # random selection
    similarity_degree = 1
    selected = None
    for _i in range(times):
        r = _select_func[code](results)
        s = similar(r, results)
        if s < similarity_degree:
            selected = r
            similarity_degree = s
    return (selected, similarity_degree)


if __name__ == "__main__":
    codes = ['双色球', '七乐彩', '3D', '大乐透', '排列三', '排列五', '七星彩']
    for code in codes:
        one = rand_select(code)
        print("{0}\r\n  {1}\r\n  {2:.2f}%\r\n".format(code, one[0], one[1]*100))
