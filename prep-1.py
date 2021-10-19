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

# Requires web browser
result = app.acquire_token_interactive(scopes=config['scope'])			
print(result)
