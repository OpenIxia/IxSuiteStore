import requests
import json
import os
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://10.36.78.213/ixsuitestore"
apikey = "54278a98db384bd0a46911c9d19e5fc1"
session_id = "1"

local_file_path = '/tmp/samples.ssm'
ssm_name = os.path.basename(local_file_path)
ssm_file = {'upload_file': open(local_file_path, 'rb')}


# Upload module to IxSuitestore VM
upload_url = base_url + '/api/v1/sessions/0/suitestore/files?filename=' + ssm_name
headers = {'content-type': 'application/octet-stream'}
requests.request('POST', upload_url, headers=headers, files=ssm_file, verify=False)


# Install module
headers['content-type'] = 'application/json; charset=us-ascii'
install_url = base_url + '/api/v1/sessions/0/suitestore/settings/operations/installModule'
body = { "filename": ssm_name }
response = requests.request('POST', install_url, headers=headers,
data=json.dumps(body), verify=False)


# Operation is async, check for success
while True:
    if 'state' not in response.json().keys():
        print('Async operation response is:\r\n{r}'.format(r=response.json()))
        break

    state = response.json()["state"]
    url = response.json()["url"]
    if state == "SUCCESS":
        print("Install completed successfully")
        break
    elif state == "IN_PROGRESS":
        time.sleep(3)
        url = base_url + url
        response = requests.request('GET', url, headers=headers, verify=False)
        continue
    else:
        print(response)
