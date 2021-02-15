"""
大乐透的概率输出
"""

from lottery import get_history
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc


CODE = '大乐透'
COUNT = 250
MIN = 50

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
        while size >= MIN:
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
        while size >= MIN:
            prob_list.append(_calc_prob(num, blues[:size]))
            size -= 1
        result[num] = prob_list
    return result


def gen_xls(historys):
    cols = ["近%d期" % i for i in range(len(historys), MIN-1, -1)]

    data1 = calc_red(historys)
    df1 = pd.DataFrame.from_dict(data1, orient='index', columns=cols)

    data2 = calc_blue(historys)
    df2 = pd.DataFrame.from_dict(data2, orient='index', columns=cols)

    with pd.ExcelWriter('大乐透.xlsx') as writer:
        df1.to_excel(writer, sheet_name="红球")
        df2.to_excel(writer, sheet_name="蓝球")


def gen_html(historys):
    cols = ["近%d期" % i for i in range(len(historys), MIN-1, -1)]

    datas1 = []
    for k,v in calc_red(historys).items():
        data={'type':'line', 'name':k}
        data['x'] = cols
        data['y'] = v

        datas1.append(data)

    datas2 = []
    for k,v in calc_blue(historys).items():
        data={'type':'line', 'name':k}
        data['x'] = cols
        data['y'] = v

        datas2.append(data)

    app = dash.Dash()
    app.layout = html.Div(children=[
        html.H1(children='大乐透数学期望分析'),

        html.Div(children='''
                近%d+%d期数据
            ''' % (COUNT, MIN)),

        dcc.Graph(
                id='red-exp-val-graph',
                figure={
                    'data':datas1,
                    'layout':{
                        'title':'红球趋势'
                    }
                }
            ),

        dcc.Graph(
                id='blue-exp-val-graph',
                figure={
                    'data':datas2,
                    'layout':{
                        'title':'蓝球趋势'
                    }
                }
            ),
    ])

    app.run_server(debug=True)


if __name__ == '__main__':
    historys = get_history(CODE, COUNT + MIN)
    #gen_xls(historys)
    gen_html(historys)
