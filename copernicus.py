import os
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

# Copernicus credentials
COPERNICUS_ID = os.environ.get('COPERNICUS_ID')
COPERNICUS_SECRET = os.environ.get('COPERNICUS_SECRET')

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


class CopernicusReq():
    def __init__(self, coords, dates, output_size, es) -> None:
        self.dates = dates
        self.coords = coords
        self.output_size = output_size
        self.es = es
    
    def get_request(self):
        return CopernicusReq.gen_request(self.coords, self.dates, self.output_size, self.es)
    
    @staticmethod
    def gen_request(coords, time, size, es):
        request = {
            "input": {
                "bounds": {
                    "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"},
                    "bbox": coords,
                },
                "data": [
                    {
                        "type": "sentinel-2-l2a",
                        "dataFilter": {
                            "timeRange": {"from": time[0], "to": time[1]},
                            "mosaickingOrder": "leastCC",
                        },
                    }
                ],
            },
            "output": {"width": size, "height": size,},
            "evalscript": es,
        }
        return request

    @property
    def years(self):
        return [int(date_str[0:4]) for date_str in self.dates]
    @property
    def months(self):
        return [int(date_str[5:7]) for date_str in self.dates]
    @property
    def days(self):
        return [int(date_str[8:10]) for date_str in self.dates]