import requests
import json

url_base = 'https://api.xdr.trendmicro.com'
url_path = '/v2.0/xdr/oat/detections'
token = ''

query_params = { 'end': '1632093072',
  'size': '50',
  'start': '1631833872'}
headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json;charset=utf-8'}

r = requests.get(url_base + url_path, params=query_params, headers=headers)

print(r.status_code)
if 'application/json' in r.headers.get('Content-Type', ''):
    print(json.dumps(r.json(), indent=4))
else:
    print(r.text)