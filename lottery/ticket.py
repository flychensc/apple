"""
用法：
print(get_history('双色球', count=1))

输出格式大致如下，差异在result部分，要么为dict，要么为list
[
    {
        'date': datetime.date(2018, 7, 12),
        'result': {
            'red': [4,7,13,20,29,33],
            'blue': 3
        },
        'grades': [
            {'num': 6,       'money': 8230212},
            {'num': 128,     'money': 189270},
            {'num': 1015,    'money': 3000},
            {'num': 56290,   'money': 200},
            {'num': 1090402, 'money': 10},
            {'num': 7457743, 'money': 5},
            {'num': 0,       'money': 0}
        ]
    }
]
"""
import requests
import datetime

from bs4 import BeautifulSoup


_str2date = lambda s,f: datetime.datetime.strptime(s, f).date()

def _get_cwl_history(_type, count=30):
    name = {'3D':'3d', '双色球':'ssq', '七乐彩':'qlc'}
    if _type not in name:
        raise ValueError

    payload = {'name': name[_type]}

    if count:
        payload["issueCount"] = count
    else:
        payload["issueCount"] = 30

    jkdz = "http://www.cwl.gov.cn/cwl_admin/"
    url = jkdz + "kjxx/findDrawNotice"

    headers = {
        'Accept': 'application/json',
        'Referer': 'http://www.cwl.gov.cn/kjxx/',
    }

    r = requests.get(url=url, params=payload, headers=headers)

    historys = []
    for one in r.json()['result']:
        history = {'date': _str2date(one['date'][:10], '%Y-%m-%d')}

        if name[_type] == 'ssq':
            red = [int(r) for r in one['red'].split(',')]
            blue = int(one['blue'])
            history['result'] = {'red': red, 'blue': blue}
        elif  name[_type] == 'qlc':
            red = [int(r) for r in one['red'].split(',')]
            blue = int(one['blue'])
            history['result'] = {'red': red, 'blue': blue}
        elif  name[_type] == '3d':
            red = [int(r) for r in one['red'].split(',')]
            history['result'] = red

        history['total'] = int(int(one['sales'])/2)

        history['grades'] = []
        for prizegrade in one['prizegrades']:
            grade = {}
            try:
                grade['num'] = int(prizegrade['typenum'])
            except ValueError:
                grade['num'] = 0

            try:
                grade['money'] = int(prizegrade['typemoney'])

                if name[_type] == '3d' and grade['num'] !=0:
                    grade['money'] = int(grade['money']/grade['num'])

            except ValueError:
                grade['money'] = 0

            history['grades'].append(grade)

        historys.append(history)

    return historys

def _get_lottery_history(_type, count=30):
    name = {'七星彩':'qxc', '大乐透':'dlt', '排列五':'plw', '排列三':'pls'}
    if _type not in name:
        raise ValueError

    payload = {'_ltype': name[_type], 'page':'false', 'startTerm':'', 'endTerm':''}

    if count:
        payload["termNum"] = count
    else:
        payload["termNum"] = 30

    url = 'http://www.lottery.gov.cn/historykj/history.jspx'
    r = requests.get(url=url, params=payload)

    soup = BeautifulSoup(r.text, 'lxml')
    result = soup.find('div', 'result')

    historys = []
    for one in result.find_all('tr'):
        datas = one.find_all('td')
        if datas is None or len(datas) < 3:
            continue

        history = {'date': _str2date(datas[-1].text, '%Y-%m-%d')}

        if name[_type] == 'qxc':
            history['result'] = [int(i) for i in datas[1].text]
            grades_start = 2
            grades_end = -4
            sales = -3
        elif  name[_type] == 'dlt':
            red = [int(r.text) for r in datas[1:6]]
            blue = [int(b.text) for b in datas[6:8]]
            history['result'] = {'red': red, 'blue': blue}
            grades_start = 8
            grades_end = -4
            sales = -3
        elif  name[_type] == 'plw':
            history['result'] = [int(i) for i in datas[1].text.split()]
            grades_start = 2
            grades_end = -4
            sales = -3
        elif  name[_type] == 'pls':
            history['result'] = [int(i) for i in datas[1].text.split()]
            grades_start = 2
            grades_end = -3
            sales = -2

        history['total'] = int(int(datas[sales].text.replace(',',''))/2)

        history['grades'] = []
        for idx in range(grades_start, grades_start+len(datas[grades_start:grades_end]), 2):
            grade = {}

            grade['num'] = int(datas[idx].text.replace(',',''))
            grade['money'] = int(float(datas[idx+1].text.replace(',','')))

            history['grades'].append(grade)

        historys.append(history)
    return historys

def get_history(_type, count=30):
    if _type in ['双色球', '七乐彩', '3D']:
        return _get_cwl_history(_type, count)
    elif _type in ['大乐透', '排列三', '排列五', '七星彩']:
        return _get_lottery_history(_type, count)
    else:
        raise ValueError


if __name__ == "__main__":
    data = get_history('双色球', count=1)
    print(data)
