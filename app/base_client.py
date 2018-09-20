# External libraries
import requests, requests.auth
import json, os

# Load environment vars
import dotenv
path = dotenv.find_dotenv('.env')
dotenv.load_dotenv(dotenv_path=path)

# Settings
base_url = os.getenv("ALPHA_BASE_URL")
api_user = os.getenv("ALPHA_USERNAME")
api_pass = os.getenv("ALPHA_PASSWORD")

# Main method
def request(module, method, params):
    url = '%s/api/2/sync/%s/%s' % (base_url, module, method)
    auth = requests.auth.HTTPBasicAuth(api_user, api_pass)
    r = requests.post(url, json=params, auth=auth)
    return r.json()
