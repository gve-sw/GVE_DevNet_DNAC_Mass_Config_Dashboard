"""
Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from requests.auth import HTTPBasicAuth
import requests
import urllib3
import json

urllib3.disable_warnings()


def dnac_get_Authorization_Token(dnac):
	"""
	Intent-based Authentication API call
	The token obtained using this API is required to be set as value to the X-Auth-Token HTTP Header
	for all API calls to Cisco DNA Center.
	:param: dnac
	:return: Token STRING
	"""
	url = 'https://{}/dna/system/api/v1/auth/token'.format(dnac['dnac_host'])
	# Make the POST Request
	resp = requests.post(url, auth=HTTPBasicAuth(dnac['dnac_username'], dnac['dnac_password']), verify=False)

	# Validate Response
	if 'error' in resp.json():
		print('ERROR: Failed to retrieve Access Token!')
		print('REASON: {}'.format(resp.json()['error']))
		result = ""
	else:
		result = resp.json()['Token']
	return result


def dnac_get_Available_Templates(dnac):
	"""
	List the DNA-Center configuration templates available
	:param: dnac - DNA-Center configuration, set during user session
	:return:
	"""
	url = "https://{}/dna/intent/api/v1/template-programmer/template".format(dnac['dnac_host'])
	headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json',
		'x-auth-token': dnac['token'],
	}
	body = None

	response = requests.get(url, headers=headers, verify=False)
	if response.status_code == 200:
		return response.json()
	else:
		return []


def dnac_get_Available_Projects(dnac):
	"""
	List the DNA-Center configuration templates available
	:param: dnac - DNA-Center configuration, set during user session
	:return:
	"""
	url = "https://{}/dna/intent/api/v1/template-programmer/project".format(dnac['dnac_host'])
	headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json',
		'x-auth-token': dnac['token'],
	}
	body = None

	response = requests.get(url, headers=headers, verify=False)
	if response.status_code == 200:
		return response.json()
	else:
		return []


def dnac_get_Template(dnac):
	"""
	List the DNA-Center configuration templates available
	:param: dnac - DNA-Center configuration, set during user session
	:return:
	"""
	url = "https://{}/dna/intent/api/v1/template-programmer/template/{}".format(dnac['dnac_host'], dnac['selectedTemplate'])

	headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json',
		'X-auth-token': dnac['token'],
	}
	body = None

	response = requests.request("GET", url, headers=headers, verify=False)
	if response.status_code == 200:
		return response.json()
	else:
		return {}


def dnac_deploy_Template(dnac, device, template_Id, params, doForce):
	"""

	"""
	url = "https://{}/dna/intent/api/v1/template-programmer/template/deploy".format(dnac['dnac_host'])
	headers = {
		'Content-Type: application/json',
		'Accept: application/json'
	}
	body = {
		"templateId": template_Id,
		"forcePushTemplate" : doForce,
		"targetInfo": [
		 {

			"id": device,
			"type": "MANAGED_DEVICE_IP",
			"params": params
			}
		 ]
    }

	response = requests.request("GET", url, headers=headers, data=body, verify=False)
	print(response)


def dnac_get_Site_Topology(dnac):
	"""
	List the DNA-Center configuration templates available
	:param: dnac - DNA-Center configuration, set during user session
	:return:
	"""
	url = "https://{}/dna/intent/api/v1/topology/site-topology".format(dnac['dnac_host'])

	headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json',
		'X-auth-token': dnac['token'],
	}
	body = None

	response = requests.request("GET", url, headers=headers, verify=False)
	if response.status_code == 200:
		return response.json()
	else:
		return {}


def dnac_get_Site_Membership(dnac, siteId):
	"""
	List the DNA-Center configuration templates available
	:param: dnac - DNA-Center configuration, set during user session
	:return:
	"""
	url = "https://{}/dna/intent/api/v1/membership/{}".format(dnac['dnac_host'], siteId)

	headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json',
		'X-auth-token': dnac['token'],
	}
	body = None

	response = requests.request("GET", url, headers=headers, verify=False)
	if response.status_code == 200:
		return response.json()
	else:
		return {}


def dnac_get_DNAC_Network_Devices(dnac):
	"""
	List the DNA-Center configuration templates available
	:param: dnac - DNA-Center configuration, set during user session
	:return:
	"""
	url = "https://{}/dna/intent/api/v1/network-device".format(dnac['dnac_host'])

	headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json',
		'X-auth-token': dnac['token'],
	}
	body = None

	response = requests.request("GET", url, headers=headers, verify=False)
	if response.status_code == 200:
		return response.json()
	else:
		return {}
