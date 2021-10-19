from msal import PublicClientApplication
import json
import requests
import pickle
import sys

# open privates
with open('private.json', 'r') as f:
	config = json.load(f)

app = PublicClientApplication(
    config['client_id'],
    authority=config['authority'],		# ?client_id=YOUR_TENANT_ID
)

assert len(sys.argv) == 2

code = sys.argv[1]

result = app.acquire_token_by_authorization_code(code, scopes=config['scope'], redirect_uri=config['redirect_uri'])
print(result)

# save token
with open('token', 'wb') as f:
	pickle.dump(result, f)
