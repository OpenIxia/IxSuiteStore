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


# Getting current run results
url = base_url + '/api/v1/sessions/' + session_id + '/suitestore/currentRun'
response = requests.request('GET', url, headers=headers, verify=False)
content = response.json()
print("The most recent run had a total of {t} scripts, of which {p} passed, \
 {f} failed and {u} did not run".format(t=content['totalCount'],\
 p=content['passCount'],f=content['failCount'], u=content['pendingCount']))


# Getting current run suites
url = base_url + '/api/v1/sessions/' + session_id + '/suitestore/currentRun/suites'
response = requests.request('GET', url, headers=headers, verify=False)
content = response.json()
suites = [s['displayName'] for s in content]
print("The following suites were executed in the most recent run: {s}".format(s=','.join(suites)))