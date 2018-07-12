import requests


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
    return r.json()

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
    return r.text

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
