from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import os

# Copernicus credentials
COPERNICUS_ID = os.environ.get('COPERNICUS_ID')
COPERNICUS_SECRET = os.environ.get('COPERNICUS_SECRET')

# Create a session
client = BackendApplicationClient(client_id=COPERNICUS_ID)
oauth = OAuth2Session(client=client)

# Get token for the session
token = oauth.fetch_token(token_url='https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token',
                          client_secret=COPERNICUS_SECRET)

# All requests using this session will have an access token automatically added
data = {
    "bbox": [13, 45, 14, 46],
    "datetime": "2019-12-10T00:00:00Z/2019-12-10T23:59:59Z",
    "collections": ["sentinel-1-grd"],
    "limit": 5,
}
url = "https://sh.dataspace.copernicus.eu/api/v1/catalog/1.0.0/search"
resp = oauth.post(url, json=data)
print(resp.content)
print(f"{resp.status_code}: {resp.reason}")