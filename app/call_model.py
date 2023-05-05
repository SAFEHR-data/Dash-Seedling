#  Copyright (c) University College London Hospitals NHS Foundation Trust
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
from azure.identity import DefaultAzureCredential
import requests
import adal
from azure.keyvault.secrets import SecretClient

def call_model(app_to_call_id, payload):
    """
    Only works in hosting, until local auth flow is implemented
    EXAMPLE USAGE: call_model('los-predictor', '{"csn": 12345}')
    """
    
    tenant_id = os.environ["TENANT_ID"]
    key_vault_uri = os.environ["KEY_VAULT_URI"]
    environment = os.environ["ENVIRONMENT"]

    app_uri = f'webapp-{app_to_call_id}-uclh-flowehr-{environment}'
    app_id_key = f'{app_uri}-client-id'
    app_secret_key = f'{app_uri}-client-secret'

    # get a token for KV using default cred - this will only work in hosted as dev accounts don't have access to the KV, 
    # but should use an interactive login for the developer instead. 
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)
    app_id = client.get_secret(app_id_key).value
    app_secret = client.get_secret(app_secret_key).value

    authority_url = f'https://login.microsoftonline.com/{tenant_id}'
    context = adal.AuthenticationContext(authority_url)
    token = context.acquire_token_with_client_credentials(app_id, app_id, app_secret)

    headers = {
        'Authorization': 'Bearer ' + token["accessToken"],
        'Content-Type': 'application/json'
    }

    response = requests.post(
        url=f'https://{app_uri}.azurewebsites.net/run', 
        headers=headers,
        data=payload)

    return response.json()

