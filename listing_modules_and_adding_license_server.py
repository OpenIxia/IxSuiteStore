import requests
import json
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


base_url = "https://10.36.78.213/ixsuitestore"
apikey = "54278a98db384bd0a46911c9d19e5fc1"
session_id = "1"
license_server = "10.36.78.2"
headers = {
    'content-type': 'application/json; charset=us-ascii',
    'X-Api-Key': apikey
 }


# Getting installed modules
url = base_url + '/api/v1/sessions/0/suitestore/modules'
response = requests.request('GET', url, headers=headers, verify=False)
module_names = [m['displayName'] for m in response.json()]
print("The following modules are installed:{m}.".format(m=','.join(module_names)))


# Getting required licenses for first module
module_id = response.json()[0]['id']
url = url + '/' + str(module_id) + '/licensing/licenses'
response = requests.request('GET', url, headers=headers, verify=False)
if response.json() == []:
    print("No licenses are required to run module {m}.".format(m=module_id))
else:
    licenses = [l['featureName'] for l in response.json()]
    print("The following licenses are required to run module {m}: {l}".format(\
        m=module_id, l=','.join(licenses)))


# Adding a license server
url = base_url + '/api/v1/sessions/0/suitestore/settings/licenseServers'
body = { "host": license_server }
response = requests.request('POST', url, headers=headers, data=json.dumps(body), verify=False)
if response.status_code == 201:
    print("Added license server {s}".format(s=license_server))
else:
    print("Failed to add license server. Status: {c}. Body:\r\n{b}".format(c=response.status_code, \
            b=response.json()))

