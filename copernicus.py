from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from utils import COPERNICUS_ID, COPERNICUS_SECRET

class CopernicusAPI:
    def __init__(self) -> None:
        # Create a session
        self.client = BackendApplicationClient(client_id=COPERNICUS_ID)
        self.oauth = OAuth2Session(client=self.client)

        # Get token for the session
        self.token = self.oauth.fetch_token(token_url="https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
                                            client_secret=COPERNICUS_SECRET)

    def request(self, request):
        req_url = "https://sh.dataspace.copernicus.eu/api/v1/process"
        resp = self.oauth.post(req_url, json=request)
        print(f"{resp.status_code}: {resp.reason}")
        print(f"Returned data is of type = {type(resp.content)} and length {len(resp.content)}.")
        return resp