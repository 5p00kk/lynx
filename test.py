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
    input: ["VH"],
    output: { id: "default", bands: 1 },
  }
}

function evaluatePixel(samples) {
  return [toDb(samples.VH)]
}

// visualizes decibels from -20 to 0

function toDb(linear) {
  // the following commented out lines are simplified below
  // var log = 10 * Math.log(linear) / Math.LN10
  // var val = Math.max(0, (log + 20) / 20)
  return Math.max(0, Math.log(linear) * 0.21714724095 + 1)
}
"""

request = {
    "input": {
        "bounds": {
            "bbox": [
                1360000,
                5121900,
                1370000,
                5131900,
            ],
            "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/3857"},
        },
        "data": [
            {
                "type": "sentinel-1-grd",
                "dataFilter": {
                    "timeRange": {
                        "from": "2019-02-02T00:00:00Z",
                        "to": "2019-04-02T23:59:59Z",
                    }
                },
                "processing": {"orthorectify": "true"},
            }
        ],
    },
    "output": {
        "width": 512,
        "height": 512,
        "responses": [
            {
                "identifier": "default",
                "format": {"type": "image/png"},
            }
        ],
    },
    "evalscript": evalscript,
}

url = "https://sh.dataspace.copernicus.eu/api/v1/process"
resp = oauth.post(url, json=request)

print(f"{resp.status_code}: {resp.reason}")


with open("my_file.png", "wb") as f:
    f.write(resp.content)

image = cv2.imread("my_file.png")
cv2.imshow("ok", image)
cv2.waitKey(-1)

#with open('output_file.json', 'w') as f:
#    json.dump(data_js, f, indent=4)

