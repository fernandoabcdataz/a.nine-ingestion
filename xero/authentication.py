from google.cloud import secretmanager
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from cachetools import TTLCache
from config import CONFIG

token_url = CONFIG['TOKEN_URL']
project_id = CONFIG['PROJECT_ID']
client_name = CONFIG['CLIENT_NAME']

def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"{CONFIG['SECRETS_PATH']}/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')

def get_client_credentials():
    client_id_secret_name = f"{project_id}-{client_name}-xero-client-id"
    client_secret_secret_name = f"{project_id}-{client_name}-xero-client-secret"
    
    CLIENT_ID = get_secret(client_id_secret_name)
    CLIENT_SECRET = get_secret(client_secret_secret_name)
    
    return CLIENT_ID, CLIENT_SECRET

token_cache = TTLCache(maxsize=1, ttl=3600)  # Cache token for 1 hour

def get_token():
    if 'token' in token_cache:
        return token_cache['token']
    
    CLIENT_ID, CLIENT_SECRET = get_client_credentials()
    
    client = BackendApplicationClient(client_id=CLIENT_ID)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=token_url, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    token_cache['token'] = token
    return token