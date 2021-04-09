

# this script updates the 'device name'  of  multiple Meraki MX appliances listed in a csv

import requests
import json
from csv import reader
from getpass import getpass


print("script to change multiple  Meraki device names\n")

#prompt for api key & region Id
apikey= getpass('api key ?: ')
region= input('region Id ? ')


#function to perform the device name change
#calls a csv where  lives the network name, device serial & device name 


def namechange ( network_name, serial, new_device_name):
	#pass in variables to meraki url
	url = "https://api.meraki.com/api/v0/organizations/%s" % region + "/networks/%s" % network_name + "/devices/%s" % serial
	#pass variables into the payload
	payload='''{"name": "new_device_name"}'''
	py_dict = json.loads(payload)
	py_dict['name']= new_device_name
	payload = json.dumps(py_dict)
	headers = {
	'Accept': 'application/json',
	#api key entered secretely by user
	'X-Cisco-Meraki-API-Key': apikey,
	'Content-Type': 'application/json'
		}
	# this will be a PUT request	
	response = requests.request("PUT", url, headers=headers, data=payload)
	pretty_json = json.loads(response.text)
	#print updated output to user
	print(json.dumps(pretty_json, indent=2))
	return


#  parse data from csv and convert to a dictionary called meraki_dict
meraki_dict = {}
with open ("update_device_name_list.csv", "r") as csv_file:
	csv_content = reader(csv_file)
	devicelist = next(csv_content)	
	for conf in csv_content:
		for device in devicelist:
			if not device:
				continue			
			if device not in meraki_dict.keys():
				meraki_dict[device] = []
			n = devicelist.index(device)
			meraki_dict[device].append(conf[n])


# loop through csv and call the function for each column (device) that needs name changing

for device in meraki_dict.keys():
	network_name = device
	serial =  (meraki_dict[device][0])
	new_device_name = (meraki_dict[device][1])

#print to user before making change
	print(network_name)
	print(serial)
	print( " Device Name Will Be Changed To: " + (new_device_name))

#call function to change the device name
	namechange(network_name, serial, new_device_name)
