from google.cloud import secretmanager
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from cachetools import TTLCache
import os
from config import TOKEN_URL

def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')

CLIENT_ID = get_secret('xero-client-id')
CLIENT_SECRET = get_secret('xero-client-secret')

token_cache = TTLCache(maxsize=1, ttl=3600)  # Cache token for 1 hour

def get_token():
    if 'token' in token_cache:
        return token_cache['token']
    client = BackendApplicationClient(client_id=CLIENT_ID)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=TOKEN_URL, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    token_cache['token'] = token
    return token