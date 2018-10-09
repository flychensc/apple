"""
绘制相似度
"""
import dash
import dash_html_components as html
import dash_core_components as dcc

from lottery import get_history, similar, iter_history

codes = ['双色球', '七乐彩', '3D', '大乐透', '排列三', '排列五', '七星彩']
count = 30

datas = []
for c in codes:
    print('Get %s data...' % c)
    try:
        his = get_history(c, count*2)
    except AttributeError:
        print('Fail to get history')
        continue
    sim = []
    date = []

    def _collecter(code, latest, past):
        sim.append(similar(latest['result'], [one['result'] for one in past])*100)
        date.append(latest['date'])

    iter_history(c, _collecter)

    data={'type':'line', 'name':c}
    data['x'] = date
    data['y'] = sim

    datas.append(data)

app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(children='相似度对比'),

    html.Div(children='''
        最近%d期
    ''' % count),

    dcc.Graph(
        id='exp-value-graph',
        figure={
            'data':datas,
            'layout':{
                'title':'相似度'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
