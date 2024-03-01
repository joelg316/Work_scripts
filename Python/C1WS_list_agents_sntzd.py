from __future__ import print_function
import sys, warnings
import deepsecurity
from deepsecurity.rest import ApiException
from pprint import pprint
import inspect

# Setup
if not sys.warnoptions:
	warnings.simplefilter("ignore")
configuration = deepsecurity.Configuration()
configuration.host = 'https://cloudone.trendmicro.com/api'

# Authentication
configuration.api_key['api-secret-key'] = ''
# Initialization
# Set Any Required Values
api_instance = deepsecurity.ComputersApi(deepsecurity.ApiClient(configuration))
api_version = 'v1'
expand_options = deepsecurity.Expand()
expand_options.add(expand_options.all)
expand = expand_options.list()
overrides = False

try:
	api_response = api_instance.list_computers(api_version, expand=expand, overrides=overrides).to_dict()

	with open(r"C:\Users\joelg\OneDrive - TrendMicro\Documents\PycharmProjects\C1WS_list_agents\output.csv", "w") as f:

		pprint(api_response['computers'][0])
		f.write(str(api_response['computers'][0]))

		pprint("hostname, agent_version, last_agent_communication")
		f.write("hostname, agent_version, last_agent_communication")

		for k, i in enumerate(api_response['computers']):

			pprint(str(k) + ": " + i['host_name'] + ", " + i['agent_version'] + ", " + str(i['last_agent_communication']))
			f.write(str(pprint(k + ": " + i['host_name'] + ", " + i['agent_version'] + ", " + str(i['last_agent_communication']))))

	#print(type(api_response))
	#getattr(api_response, 'host_name')
	#print(inspect.getfile(api_response.__class__))
except ApiException as e:
	print("An exception occurred when calling ComputersApi.list_computers: %s\n" % e)

