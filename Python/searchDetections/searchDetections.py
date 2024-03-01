import requests
import json

token = ''

url_base = 'https://api.xdr.trendmicro.com'
url_path = '/v2.0/xdr/search/detections'
query_params = {}
headers = {'Authorization': 'Bearer ' + token , 'Content-Type': 'application/json;charset=utf-8'}


def searchDetections():
    body = '''
    {
        "offset": 0,
        "limit": 10,
        "startTime": "2021-10-26T00:00:00Z",
        "endTime": "2021-10-29T00:00:00Z",
        "query": "eventName:MALWARE_DETECTION"
    }
    '''

    r = requests.post(url_base + url_path, params=query_params, headers=headers, data=body)

    print(r.status_code)
    if 'application/json' in r.headers.get('Content-Type', ''):
        print(json.dumps(r.json(), indent=4))
    else:
        print(r.text)

if __name__ == "__main__":
    searchDetections()