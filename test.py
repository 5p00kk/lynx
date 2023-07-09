from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from utils import COPERNICUS_ID, COPERNICUS_SECRET
import json
import numpy as np
import cv2

# Create a session
client = BackendApplicationClient(client_id=COPERNICUS_ID)
oauth = OAuth2Session(client=client)

# Get token for the session
token = oauth.fetch_token(token_url='https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token',
                          client_secret=COPERNICUS_SECRET)


evalscript = """
//VERSION=3
function setup() {
  return {
    input: ["B02", "B03", "B04"],
    output: {
      bands: 3,
      sampleType: "AUTO", // default value - scales the output values from [0,1] to [0,255].
    },
  }
}

function evaluatePixel(sample) {
  return [2.5*sample.B04, 2.5*sample.B03, 2.5*sample.B02]
}
"""

request = {
    "input": {
        "bounds": {
            "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"},
            "bbox": [
                13.322174072265625,
                45.85080395917834,
                14.05963134765625,
                46.29191774991382,
            ],
        },
        "data": [
            {
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {
                        "from": "2020-06-12T00:00:00Z",
                        "to": "2020-07-13T00:00:00Z",
                    }
                },
            }
        ],
    },
    "output": {
        "width": 512,
        "height": 512,
    },
    "evalscript": evalscript,
}

url = "https://sh.dataspace.copernicus.eu/api/v1/process"
resp = oauth.post(url, json=request)

print(f"{resp.status_code}: {resp.reason}")
print(f"Returned data is of type = {type(resp.content)} and length {len(resp.content)}.")

with open("my_file.png", "wb") as f:
    f.write(resp.content)

image = cv2.imread("my_file.png")

print(f"Loaded image is {image.shape}, {image.dtype}, {image.shape[0]*image.shape[1]*image.shape[2]*image.itemsize}")
print(f"{np.unique(image)}")

cv2.imshow("ok", image)
cv2.waitKey(-1)
