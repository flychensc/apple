"""
expected_value 计算彩票期望值
"""


def _expected_value(his_one):
    return sum([grade['money']*(grade['num']/his_one['total']) for grade in his_one['grades']])

def expected_value(history):
    if type(history) is list:
        return [(one['date'], _expected_value(one)) for one in history]
    else:
        return [(history['date'], _expected_value(history))]


if __name__ == "__main__":
    from ticket import get_history

    data = get_history('3D', count=10)
    exp = expected_value(data)
    print(exp)
