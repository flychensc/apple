"""
绘制期望值
"""
import dash
import dash_html_components as html
import dash_core_components as dcc

from lottery import get_history, expected_value

codes = ['双色球', '七乐彩', '3D', '大乐透', '排列三', '排列五', '七星彩']
count = 20

datas = []
for c in codes:
    print('Get %s data...' % c)
    try:
        his = get_history(c, count)
    except AttributeError:
        print('Fail to get history')
        continue
    exp = expected_value(his)

    data={'type':'line', 'name':c}
    data['x'] = [d for (d, e) in exp]
    data['y'] = [e for (d, e) in exp]

    datas.append(data)

app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(children='期望值对比'),

    html.Div(children='''
        最近%d期
    ''' % count),

    dcc.Graph(
        id='exp-value-graph',
        figure={
            'data':datas,
            'layout':{
                'title':'期望值'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
