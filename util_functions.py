import requests


def get_token(key_file):
    # 1. Get your keys at https://stepik.org/oauth2/applications/
    # (client type = confidential, authorization grant type = client credentials)3
    with open(key_file) as file:
        client_id = file.readline().strip()
        client_secret = file.readline().strip()

    # 2. Get a token
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    response = requests.post('https://stepik.org/oauth2/token/',
                             data={'grant_type': 'client_credentials'},
                             auth=auth)
    token = response.json().get('access_token', None)
    if not token:
        print('Unable to authorize with provided credentials')
        exit(1)
    return token
