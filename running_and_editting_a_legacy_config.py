import requests
import json
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://10.36.78.213/ixsuitestore"
apikey = "54278a98db384bd0a46911c9d19e5fc1"
session_id = "1"
headers = {
 'content-type': 'application/json; charset=us-ascii',
 'X-Api-Key': apikey
 }

def wait_for_operation(response):
    while True:
        state = response.json()["state"]
        if state == "IN_PROGRESS":
            operation_url = response.json()["url"]
            url = base_url + operation_url
            time.sleep(0.5)
            response = requests.request('GET', url, headers=headers,verify=False)
        elif response.json()["state"] == "SUCCESS":
            break
        else:
            print("Operation returned state {c} code and \r\n{b}".format(c=state, b=response.json()))
            exit()
        return


# Running passed-in [legacy shown here] config
config = {
    "runList": [ "samples/testsuite/sleeptest"],
    "parameterSets": [{
            "path": "samples",
            "parameters" : [
                {
                "name" :"seconds",
                "value" : 10
                 }
                ]
            }]
    }

url = base_url + '/api/v1/sessions/' + session_id + '/suitestore/config/operations/start'

print("Starting run")
response = requests.request('POST', url, headers=headers, data=json.dumps(config), verify=False)

# Wait for the start operation to return SUCCESS
wait_for_operation(response)
print("Run started")

# Wait for the run to finish
result_url = response.json()['result']
url = base_url + result_url

while True:
    response = requests.request('GET', url, headers=headers, verify=False)
    result = response.json()['runState']
    if result == 'done':
        break
    time.sleep(0.5)

print("Run finished")


# Getting entire configuration hierarchy using Select API
url = base_url + '/api/v1/sessions/' + session_id + '/suitestore/operations/select'
body = {
    "selects": [
        {
        "from": "/sessions/" + session_id + "/suitestore/config",
        "properties": ["*"],
        "children": [
            {
            "child": ".*",
            "properties": ["*"],
            "filters": []
            }
        ],
        "inlines": []
        }
    ]
    }
response = requests.request('POST', url, headers=headers, data=json.dumps(body),verify=False)

# Wait for the select operation to return SUCCESS
wait_for_operation(response)

parameter_url = response.json()['result'][0]['parameterSets'][0]['parameters'][0]['href']
url = base_url + parameter_url
body = {
    "name" :"seconds",
    "value" : 5
    }
print("Changing parameter value")
response = requests.request('PATCH', url, headers=headers, data=json.dumps(body),
verify=False)


# Running existing config
url = base_url + '/api/v1/sessions/' + session_id + '/suitestore/config/operations/start'
print("Starting run")
response = requests.request('POST', url, headers=headers, verify=False)

# Wait for the start operation to return SUCCESS
wait_for_operation(response)
print("Run started")

# Wait for the run to finish
result_url = response.json()['result']
url = base_url + result_url

while True:
    response = requests.request('GET', url, headers=headers, verify=False)
    result = response.json()['runState']
    if result == 'done':
        break
    time.sleep(0.5)

print("Run finished")