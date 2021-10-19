import json
import requests
import pickle

# open privates
with open('private.json', 'r') as f:
	config = json.load(f)

# load token
with open('token', 'rb') as f:
	token = pickle.load(f)

# refresh token
params = { 'grant_type': 'refresh_token',
            'client_id': config['client_id'],
            'refresh_token': token['refresh_token'] }
response = requests.post('https://login.microsoftonline.com/consumers/oauth2/v2.0/token', data=params).json()
token['access_token'] = response['access_token']
token['refresh_token'] = response['refresh_token']  # replace access/refresh token

# save token
with open('token', 'wb') as f:
	pickle.dump(token, f)

# Calling graph API using the access token
query="https://graph.microsoft.com/v1.0/me"             # Query to retrieve user information
#query="https://graph.microsoft.com/v1.0/me/drive"      # Query to access onedrive

graph_data = requests.get(  # Use token to call downstream service
    query,
    headers={
        'Authorization': 'Bearer ' + token['access_token'],
        'Accept': 'application/json',
        'Content-Type': 'application/json'},
    stream=False
    ).json()

print("Graph API call result: %s" % json.dumps(graph_data, indent=2))
