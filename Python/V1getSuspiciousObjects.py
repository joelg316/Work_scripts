#! python3
# Reference: https://automation.trendmicro.com/xdr/api-v2#tag/Suspicious-Object-List/paths/~1v2.0~1xdr~1threatintel~1suspiciousObjects/get

import json
import requests

# Must get token from Vision One settings: Administration > User Accounts > select user
# > Change role to "Vision One Console and APIs" > copy authentication token and make sure it is not expired
token = ''

# These should not be modified unless Vision One URL changes
url_base = 'https://api.xdr.trendmicro.com'
url_path = '/v2.0/xdr/threatintel/suspiciousObjects'
query_params = {}
headers = {'Authorization': 'Bearer ' + token , 'Content-Type': 'application/json;charset=utf-8'}


def api_get_so():
    try:
        print("Querying Vision One suspicious objects")
        r = requests.get(url_base + url_path, params=query_params, headers=headers)
        print(r.status_code)
        if 'application/json' in r.headers.get('Content-Type', ''):
            print(json.dumps(r.json(), indent=4))
        else:
            print(r.text)
    except Exception as e:
        print("Could not get suspicious object list from Vision One\n" + e)

if __name__ == "__main__":
    api_get_so()