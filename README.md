# Microsoft Graph API Guide for Personal Live Account

## Introduction

Guidance and useful tools for **PERSONAL** Microsoft Graph API use (applied only for personal live account).

## Functionalities

- Basic personal authentication guide (i.e. retrieving token)
- **(onedrive-batch-embed-images.py)** Batch embed all images in a single folder, at once.
- To be added...

## Requirements

`pip3 install msal`

## Preparation
1. Register application in Azure ADD
   - https://github.com/AzureAD/microsoft-authentication-library-for-python
   - https://developer.microsoft.com/en-us/onedrive

   1. In `secrets` tab, make secrets. Leave memo of id and value somewhere else.
   2. In `authorization` tab, Add platform for `mobile and desktop application`. Check `https://login.microsoftonline.com/common/oauth2/nativeclient` as redirection URI.
   3. In `API permissions` tab, add some permissions, especially `Files.XXX` and `Sites.XXX`.

2. Write `private.json` by referring `private.json.template`.
	- `authority` : tenant ID
	- `client_id` : client ID
	- `secret_id` : secret ID
	- `secret`    : secret value

3. Execute authentication script in order.
   1. `python3 prep-1.py`
      When browser pops up, modify the link as follows, and then press `Enter` : 
      ```   
         'redirect_uri=http%3a%2f%2flocalhostXXXXXX' ====> 'redirect_uri=https://login.microsoftonline.com/common/oauth2/nativeclient'
      ```
      And then grant application access permission in the brower.
   2. `python3 prep-2.py`
      Open the displayed link. The address bar will contain one address, which has `code=` in its string. It is formatted as follows : `M.R3_BAY.7b37ad1a-22de-87ff-7c06-XXXXXXXXXX` (ignore # at the very end).
   3. `python3 prep-3.py CODE`
      Here, the `CODE` is the output code(`M.R3_BAY_~~~~~`) of step 2. If token is retrieved right, the token contents will be displayed and the pickled token object will be saved as file named `token`. Keep that file carefully.

4. Try running `example-api-request.py`. You can change the query link and fetch various data.

## Reference

- https://docs.microsoft.com/en-us/onedrive/developer/rest-api/?view=odsp-graph-online
- https://newbedev.com/download-files-from-personal-onedrive-using-python
- https://github.com/AzureAD/microsoft-authentication-library-for-python/blob/dev/sample/confidential_client_secret_sample.py

## License

MIT