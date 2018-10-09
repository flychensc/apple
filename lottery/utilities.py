"""
expected_value 计算彩票期望值
similar 计算相似度，【排列】判断对于位的数值相同与否。【组合】判断每个颜色相同的数值数量。
"""
from numpy import mean

from lottery import get_history


def _expected_value(his_one):
    return sum([grade['money']*(grade['num']/his_one['total']) for grade in his_one['grades']])

def expected_value(history):
    if type(history) is list:
        return [(one['date'], _expected_value(one)) for one in history]
    else:
        return [(history['date'], _expected_value(history))]

def _similar(data, sample):
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

def iter_history(code, handler, count=30, period=30):
    history = get_history(code, count+period)
    out = list()
    idx = 0
    while idx < period:
        latest = history[idx]
        past = history[idx+1:idx+1+count]
        idx += 1
        out.append(handler(code, latest, past))
    return out


if __name__ == "__main__":
    from ticket import get_history

    data = get_history('3D', count=10)
    exp = expected_value(data)
    print(exp)
