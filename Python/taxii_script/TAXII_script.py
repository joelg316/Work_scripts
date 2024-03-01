# Python script to poll stix json data from a TAXII 1.x server, then upload it to Vision One UDSO API
# Author: Joel Ginsberg
# Created Date: 9/25/21
# Reference:
# https://cabby.readthedocs.io/en/latest/user.html
# https://automation.trendmicro.com/xdr/api-v2#tag/Sandbox-Analysis/paths/~1v2.0~1xdr~1sandbox~1quota/get

from cabby import create_client
import json
import requests
import os
from pprint import pprint

# Modify the following values to fit your environment
# working_dir requires either forward slashes like C:/Users/joelg/ or double backslashes like C:\\Users\\joelg\\, either one works on Windows
working_dir = "C:/Users/joelg/"
# These files will be created by the script in the working directory
stix_file = "stix.json"
output_file = "output.json"

# Must get token from Vision One settings: Administration > User Accounts > select user
# > Change role to "Vision One Console and APIs" > copy authentication token and make sure it is not expired
token = ''

# These should not be modified unless Vision One URL changes
url_base = 'https://api.xdr.trendmicro.com'
url_path = '/v2.0/xdr/threatintel/suspiciousObjects'
query_params = {}
headers = {'Authorization': 'Bearer ' + token , 'Content-Type': 'application/json;charset=utf-8'}

def poll_taxii():
    '''Connect to TAXII 1.x server and poll their STIX 2.x data which should be in json format'''
    # Must configure TAXII server settings, for example:

    # taxii_host = "otx.alienvault.com"
    # taxii_discovery_path = '/taxii/discovery'
    # taxii_user = 'a59f9a82d94bbb1ecd4d84476c7de89714b9446aa383c3bbae9fcda3e43c99e2'
    # taxii_pw = 'none'
    # collection_name = 'user_AlienVault'
    # collections_url = 'https://otx.alienvault.com/taxii/collections'

    taxii_host = 'taxii-pilot.cisecurity.org'
    taxii_discovery_path = '/services/discovery-msisac'
    taxii_user = ''
    taxii_pw = ''
    collection_name = 'collection-msisac'
    collections_url = 'https://taxii-pilot.cisecurity.org/services/collection-management-msisac'

    try:
        client = create_client(
            taxii_host,
            use_https=True,
            discovery_path=taxii_discovery_path)

        # basic authentication
        client.set_auth(username=taxii_user, password=taxii_pw)

        services = client.discover_services()
        # Looking for collection management service URL which is used to get collections in next step
        # e.g: Service type=COLLECTION_MANAGEMENT, address=https://otx.alienvault.com/taxii/collections
        print("Available services:")
        for service in services:
            print('Service type={s.type}, address={s.address}'
                  .format(s=service))
            # Assign collection management URL for next step
            if service.type == "COLLECTION_MANAGEMENT":
                collections_url = service.address

        print("Collection management URL: " + collections_url)
    except Exception as e:
        print(e)
    try:
        collections = client.get_collections(
            uri=collections_url)
        print("\n")
        for collection in collections:
            print("Available collections: " + str(collection))
        content_blocks = client.poll(collection_name=collection_name, uri=collections_url)
    except Exception as e:
        print("Could not poll stix data\n" + str(e))

    try:
        with open(working_dir + stix_file, "wb") as f:
            for block in content_blocks:
                f.write(block.content)
        print("Stix data polled and written to file " + f.name)
    except Exception as e:
        print(e)


def parse_stix():
    '''Process raw stix data from poll_taxi() result into usable fields for API'''
    result = []
    # Confirm stix_file is not empty
    if os.stat(working_dir + stix_file).st_size != 0:
        try:
            with open(working_dir + stix_file, "r") as f1:
                print("Processing stix data input file " + f1.name)
                # Wrap json objects {} in an array [] because json.loads cannot read more than one json object
                # unless they're in an array
                data = json.loads("[" +
                    f1.read().replace("}\n{", "},\n{") +
                "]")

                for i in data:
                    name = (i["objects"][0]["name"])
                    # Splitting ipaddr to separate value from other text
                    ipaddr = (i["objects"][0]["pattern"]).split("'")
                    result.append((name, ipaddr[1]))

                # keep only unique entries
                result = list(dict.fromkeys(result))
                #print("\n\n" + str(result));
        except Exception as e:
            print(e)
        if result:
            try:
                with open (working_dir + output_file,"w") as f2:
                    f2.write(json.dumps(result))
                    print("Extracted the following values from stix data and wrote results to file: " + f2.name)
                    print(json.dumps(result))
                return json.dumps(result)
            except Exception as e:
                print(e)
        else:
            print("Could not parse data from stix file " + stix_file)
    else:
        print("Please confirm that data exists in input file: " + working_dir + stix_file)

def api_create_so():
    try:
        with open(working_dir + output_file, "r") as f:
            input = json.load(f)
            if input:
                print("Uploading data to Vision One suspicious objects")
                for i in input:
                    name = i[0]
                    value = i[1]

                    if name == "domain IOC":
                        type = "domain"
                    else:
                        type = "ip"

                    scanAction = "block"
                    print("Uploading: " + name, value + ", scan action: " + scanAction)
                    body = '''
                        {
                            "data": [
                                {
                                    "type": "''' + type + '''",
                                    "value": "''' + value + '''",
                                    "description": "TAXII ''' + name + '''",
                                    "scanAction": "''' + scanAction + '''",
                                    "riskLevel": "high",
                                    "expiredDay": "90"
                                }
                            ]
                        }
                        '''
                    r = requests.post(url_base + url_path, params=query_params, headers=headers, data=body)

                    print("Status code: " + str(r.status_code))
                    if 'application/json' in r.headers.get('Content-Type', ''):
                        print(json.dumps(r.json(), indent=4))
                    else:
                        print(r.text)

                    # Only show errors once instead of once per upload attempt
                    if r.status_code != 200:
                        break
                    else:
                        continue
            else:
                print("No data to upload to API")
    except Exception as e:
        print("Could not upload to API\n" + str(e))

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
        print("Could not get suspicious object list from Vision One\n" + str(e))


if __name__ == "__main__":
    poll_taxii()
    parse_stix()
    api_create_so()
    api_get_so()

