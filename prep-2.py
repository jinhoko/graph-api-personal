from msal import PublicClientApplication
import json
import requests
import pickle

# open privates
with open('private.json', 'r') as f:
	config = json.load(f)

app = PublicClientApplication(
    config['client_id'],
    authority=config['authority'],		# ?client_id=YOUR_TENANT_ID
)

result = app.get_authorization_request_url(scopes=config['scope'], redirect_uri=config['redirect_uri'])
print(result)