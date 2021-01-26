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
    name = {'七星彩':'04', '大乐透':'85', '排列五':'350133', '排列三':'35'}
    if _type not in name:
        raise ValueError

    payload = {'gameNo': name[_type], 'provinceId':'0'}

    if count:
        payload["pageSize"] = count
    else:
        payload["pageSize"] = 30

    """
GET https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=04&provinceId=0&pageSize=30&isVerify=1&pageNo=1 HTTP/1.1
Host: webapi.sporttery.cn
Connection: keep-alive
Accept: application/json, text/javascript, */*; q=0.01
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.50
Origin: https://static.sporttery.cn
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://static.sporttery.cn/
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
    """
    url = 'https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry'
    r = requests.get(url=url, params=payload)
    result = r.json()

    historys = []
    if result['errorCode'] == '0':
        for data in result['value']['list']:
            history = {'date': data['lotteryDrawTime']}
            if _type == '大乐透':
                num_result = [int(i) for i in data['lotteryDrawResult'].split()]
                red = num_result[:-2]
                blue = num_result[-2:]
                history['result'] = {'red': red, 'blue': blue}
            else:
                history['result'] = [int(i) for i in data['lotteryDrawResult'].split()]
            history['total'] = int(int(data['totalSaleAmount'].replace(",",""))/2)
            history['grades'] = []
            for prizeLevel in data['prizeLevelList']:
                grade = {}

                grade['num'] = int(prizeLevel['stakeCount'].replace(",",""))
                grade['money'] = int(float(prizeLevel['stakeAmount'].replace(",","")))

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
