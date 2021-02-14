"""
expected_value 计算彩票期望值
similar 计算相似度，【排列】判断对于位的数值相同与否。【组合】判断每个颜色相同的数值数量。
"""
from numpy import mean

from lottery import get_history


def _expected_value(his_one):
    """
    (每级获奖数量/销售数量)*每级奖金的汇总
    """
    return sum([grade['money']*(grade['num']/his_one['total']) for grade in his_one['grades']])

def expected_value(history):
    if type(history) is list:
        return [(one['date'], _expected_value(one)) for one in history]
    else:
        return [(history['date'], _expected_value(history))]

def _similar(data, sample):
    """
    data与sample匹配的位(个)数/总位(个)数
    """
    if type(sample) is list:
        matched = 0
        size = len(sample)
        for p in range(size):
            if data[p] == sample[p]:
                matched += 1
        return matched/size
    elif type(sample) is dict:
        matched = 0
        size = 0
        for k, v in sample.items():
            if type(v) is list:
                size += len(v)
                for d in data[k]:
                    if d in v:
                        matched += 1
            else:
                size += 1
                if v == data[k]:
                    matched += 1
        return matched/size

def similar(data, samples):
    if type(samples) is list:
        values = [_similar(data, sample) for sample in samples]
    else:
        values = [_similar(data, samples)]
    return round(mean(values), 4)

def _is_permutation_winning(my, result, count):
    """判断是否匹配(排列方式)
    my: 排列数1
    result: 排列数2
    count: 匹配的位数
    e.g.:
        my     = [9,9,8,5,6,3,8]
        result = [2,0,3,5,6,4,9]
        count  = 2
        return is True
    """
    s, e = 0, count #逐个切片
    while e <= len(result):
        if my[s:e] == result[s:e]:
            return True
        s += 1
        e += 1
    return False

def _is_combination_winning(my, result, count):
    """判断是否匹配(组合方式)
    my: 组合数1
    result: 组合数2
    count: 匹配的个数
    e.g.:
        my     = [1,3,8,15,16,23]
        result = [2,3,6,15,20,23]
        count  = 3
        return is True
    """
    check = set(result)
    for m in my:
        check.add(m)
    if (len(check) - len(result)) == (len(result) - count):
        return True
    return False

def is_winning(code, my, result):
    """判断是否中奖
    code: 彩票类别
    my: 投注号码
    result: 开奖结果
    e.g.:
        code   = '排列三'
        my     = [1,3,8]
        result = [1,8,2]
        return is False
    """
    if code in ['排列五', '排列三']:
        return my == result
    if code in ['七星彩']:
        if _is_permutation_winning(my, result, 7):
            return True
        if _is_permutation_winning(my, result, 6):
            return True
        if _is_permutation_winning(my, result, 5):
            return True
        if _is_permutation_winning(my, result, 4):
            return True
        if _is_permutation_winning(my, result, 3):
            return True
        if _is_permutation_winning(my, result, 2):
            return True
    if code in ['双色球']:
        if my['blue'] == result['blue'] and _is_combination_winning(my['red'], result['red'], 6):
            return True
        if _is_combination_winning(my['red'], result['red'], 6):
            return True
        if my['blue'] == result['blue'] and _is_combination_winning(my['red'], result['red'], 5):
            return True
        if my['blue'] == result['blue'] and _is_combination_winning(my['red'], result['red'], 4) or _is_combination_winning(my['red'], result['red'], 5):
            return True
        if my['blue'] == result['blue'] and _is_combination_winning(my['red'], result['red'], 3) or _is_combination_winning(my['red'], result['red'], 4):
            return True
        if my['blue'] == result['blue']:
            return True
    return False

def iter_history(code, handler, count=30, period=30):
    """判断是否中奖
    code: 彩票类别
    handler: 处理函数
    count: 每个待处理数据的数量
    period: 处理多长时间的数据
    e.g.:
        historys = [[1,2],[1,3],[2,3],[2,4],[3,5],[4,5]]
        count = 3, period = 2
        1st:
            latest = [1,2]
            past = [[1,3],[2,3],[2,4]]
        2nd:
            latest = [1,3]
            past = [[2,3],[2,4],[3,5]]
        3rd:
            latest = [2,3]
            past = [[2,4],[3,5],[4,5]]
    """
    history = get_history(code, count+period)
    assert(len(history) == (count+period))
    out = list()
    idx = 0
    while idx < period:
        latest = history[idx]
        past = history[idx+1:idx+1+count]
        idx += 1
        ret = handler(code, latest, past)
        if ret:
            out.append(ret)
    return out


if __name__ == "__main__":
    from ticket import get_history

    data = get_history('3D', count=10)
    exp = expected_value(data)
    print(exp)
