import requests
import json
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username = 'admin'
password = 'admin'
base_url = "https://10.36.78.213/ixsuitestore"


# Retrieve API Key for user admin
headers = {'content-type': 'application/json; charset=us-ascii'}
body = { 'username' : username, 'password' : password }
url = base_url + '/api/v1/auth/session'
response = requests.request('POST', url, headers=headers, data=json.dumps(body),
verify=False)
apikey = response.json()['apiKey']


# Create and start a new session
headers['X-Api-Key'] = apikey

## - create the session
body = { 'applicationType': 'suitestore' }
url = base_url + '/api/v1/sessions'
response = requests.request('POST', url, headers=headers, data=json.dumps(body),
verify=False)
session_id = response.json()['id']

## - start the session
url = base_url + '/api/v1/sessions/' + str(session_id) + '/operations/start'
response = requests.request('POST', url, headers=headers, verify=False)
url = response.json()['url']

## - check start operation progress
url = response.json()[u'url']
while True:
    response = requests.request('GET', url, headers=headers, verify=False)
    state = response.json()["state"]
    if state == "SUCCESS":
        break
    elif state == "IN_PROGRESS":
        time.sleep(0.5)
        continue
    else:
        print("Failed to start session {s}. Status: {c}. Body:\r\n{b}".format(s=session_id,\
                c=state,b=response.json()))

print("Session {s} started successfully".format(s=session_id))
