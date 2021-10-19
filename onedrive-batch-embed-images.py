import json
import requests
import pickle
import re

# open privates
with open('private.json', 'r') as f:
	config = json.load(f)

# load token
with open('token', 'rb') as f:
	token = pickle.load(f)

# refresh token
refresh_data = { 'grant_type': 'refresh_token',
            'client_id': config['client_id'],
            'refresh_token': token['refresh_token'] }
response = requests.post('https://login.microsoftonline.com/consumers/oauth2/v2.0/token', data=refresh_data).json()
token['access_token'] = response['access_token']
token['refresh_token'] = response['refresh_token']  # replace access/refresh token

# save token
with open('token', 'wb') as f:
	pickle.dump(token, f)


"""
[USER PARAMETERS]
Set folder path to batch embed, starting from root

example =>
	folder_path = '/Pictures/Me/'

"""
folder_path = '/사진/tester/' 		 # FILLME write here
sort_by_date_taken = True			# FILLME turn on/off


""""""""""""""
""""""""""""""
# code start
# refer https://docs.microsoft.com/en-us/onedrive/developer/rest-api/?view=odsp-graph-online
assert folder_path is not None

header = {
        'Authorization': 'Bearer ' + token['access_token'],
        'Accept': 'application/json',
        'Content-Type': 'application/json'
}
drivebaselink = "https://graph.microsoft.com/v1.0/me/drive/"

# get folder id
query = drivebaselink + "root:" + folder_path
folderdata = requests.get( query, headers=header, stream=False ).json()

folder_id = folderdata['id']
assert folder_id != None

# get file ids in folder
query = drivebaselink + f"items/{folder_id}/children"
childrendata = requests.get( query, headers=header, stream=False ).json()
children = childrendata['value']

result = []
image_count = 0
success_count = 0

if sort_by_date_taken:
	children = sorted(children, key = (lambda it: it['fileSystemInfo']['createdDateTime']) )

for item in children:
	if 'image' not in item.keys():	# the file must be a type of image
		continue
	image_count += 1
	itemid = item['id']
	query = drivebaselink + f"items/{itemid}/thumbnails"
	response = requests.get( query, headers=header).json()

	print(json.dumps(item))
	print("response: \n%s" % json.dumps(response, indent=2))

	if 'value' not in response.keys(): # failure
		print("embed failed for file id "+ itemid)
		continue

	# get filesize
	width = item['image']['width']
	height = item['image']['height']

	# You may modify which value to fetch
	largelink = response['value'][0]['large']['url']										# 800x800
	tmp = re.sub(pattern='\?width\=[0-9]+', repl=f'?width={width}', string=largelink)	
	originallink = re.sub(pattern='height=[0-9]+', repl=f'height={height}', string=tmp)		# original size

	result.append( (originallink, largelink) )
	success_count += 1

print("\n\nDone.")
print(f"{ success_count} images embeded out of {image_count} images in the folder\n")

# print(result)
output_filename = 'batch-embed-links.pickle'
with open(output_filename, 'wb') as f:
	pickle.dump(result, f)
