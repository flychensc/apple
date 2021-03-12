"""
排列五的概率输出
"""

from lottery import get_history
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc


CODE = '排列五'
MIN = 1

COUNT = 200

def _calc_prob(num, datas):
    """
    计算num在datas里的概率
    e.g.:
        num = 1
        data = [[2,3],[1,7],[3,6]]
        retunr 1/3
    """
    count = datas.count(num)
    # count/len(datas)
    return round(count/len(datas)*100)

def calc_loc(historys, loc):
    """
    {
        0: [0.16, 0.16, 0.15, ...],
        1: [0.16, 0.16, 0.22, ...],
        ...
        9: [0.16, 0.16, 0.02, ...],
    }
    """
    history_numbers = [history['result'][loc-1] for history in historys]
    result = dict()
    for num in range(0,10): #0-9
        # result.setdefault(num, [])
        prob_list = list()
        size = len(history_numbers)
        while size >= MIN:
            prob_list.append(_calc_prob(num, history_numbers[:size]))
            size -= 1
        result[num] = prob_list
    return result


def gen_xls(historys):
    with pd.ExcelWriter('排列五.xlsx') as writer:
        for loc in range(1,5+1):
            cols1 = ["近%d期" % i for i in range(len(historys), MIN-1, -1)]
            data1 = calc_loc(historys, loc)
            df1 = pd.DataFrame.from_dict(data1, orient='index', columns=cols1)
            df1.to_excel(writer, sheet_name=f"第{loc}位")


def gen_html(historys):
    children = [
        html.H1(children='排列五分析'),

        html.Div(children='数学期望值趋势'),
    ]
    for loc in range(1,5+1):
        cols = ["近%d期" % i for i in range(len(historys), MIN-1, -1)]
        datas = []
        for k,v in calc_loc(historys, loc).items():
            data={'type':'line', 'name':k}
            data['x'] = cols
            data['y'] = v

            datas.append(data)

        children.append(dcc.Graph(
                id=f'{loc}-exp-val-graph',
                figure={
                    'data':datas,
                    'layout':{
                        'title':f'第{loc}位趋势'
                    }
                }
            ))

    app = dash.Dash()
    app.layout = html.Div(children=children)

    app.run_server(debug=True)


if __name__ == '__main__':
    historys = get_history(CODE, COUNT)
    #gen_xls(historys)
    gen_html(historys)
