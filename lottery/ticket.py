import requests

headers = {
    'Accept': 'application/json',
    'Referer': 'http://www.cwl.gov.cn/kjxx/',
}

jkdz = "http://www.cwl.gov.cn/cwl_admin/"
url = jkdz + "kjxx/findDrawNotice"
name = ['3d', 'ssq', 'qlc']

payload = {'name': 'ssq', "issueCount":'30'}

r = requests.get(url=url, params=payload, headers=headers)

print(r.json())
