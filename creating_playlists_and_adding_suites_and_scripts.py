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


# Add sleep script to Playlist 1
url = base_url + '/api/v1/sessions/' + str(session_id) + '/suitestore/config/playLists/1/runList'
body = { "path" : "samples/testsuite/sleeptest" }
response = requests.request('POST', url, headers=headers, data=json.dumps(body), verify=False)
print(response)


# Add entire tcl85suite suite to Playlist 1
url = base_url + '/api/v1/sessions/' + str(session_id) + '/suitestore/config/playLists/1/runList'
body = { "path" : "samples/tcl85suite" }
response = requests.request('POST', url, headers=headers, data=json.dumps(body), verify=False)
print(response)


# Set tcl85suite suite to run in parallel with sleep script
url = base_url + '/api/v1/sessions/' + str(session_id) + '/suitestore/config/playLists/1/runList/2'
body = { "startWithPrevious" : True}
response = requests.request('PATCH', url, headers=headers, data=json.dumps(body), verify=False)
print(response)


# Get required parameters for entire playlist
url = base_url + '/api/v1/sessions/' + str(session_id) + '/suitestore/config/playLists/1/operations/getrequiredparameters'
body = { }
response = requests.request('POST', url, headers=headers, data=json.dumps(body), verify=False)
print(response)


# Set global parameters and sleep test parameter
url = base_url + '/api/v1/sessions/' + str(session_id) + '/suitestore/config/playLists/1/operations/setParameterMap'
body = {
    {
        "arg2": [
            {
                "runPath": "/globalParameters/samples",
                "parameters": [
                    {
                    "name": "otherparam",
                    "value": "EXAMPLE"
                    }
                ]
            },
            {
                "runPath": "runList/1",
                "parameters": [
                    {
                    "name": "seconds",
                    "value": 5
                    }
                ]
            }
        ]
    }
}
response = requests.request('POST', url, headers=headers, data=json.dumps(body), verify=False)
print(response)


# Set parameter for script in suite tcl85suite
url = base_url + '/api/v1/sessions/' + str(session_id) + '/suitestore/config/playLists/1/operations/setParameterMap'
body = {
    {
        "arg2": [
            {
                "runPath": "runList/2/children/1",
                "parameters": [
                    {
                    "name": "seconds",
                    "value": 6
                    }
                ]
            }
        ]
    }
}

response = requests.request('POST', url, headers=headers, data=json.dumps(body), verify=False)
print(response)
