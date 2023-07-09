
from utils import es_rgb, es_veg
from copernicus import CopernicusAPI
import numpy as np
import cv2

def image_info(image):
    print(f"Loaded image is {image.shape}, {image.dtype}, {image.shape[0]*image.shape[1]*image.shape[2]*image.itemsize}")
    print(f"Num uniques {len(np.unique(image))}")

api = CopernicusAPI()

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
                        "from": "2023-06-10T00:00:00Z",
                        "to": "2023-07-10T00:00:00Z",
                    }
                },
            }
        ],
    },
    "output": {
        "width": 2000,
        "height": 2000,
    },
    "evalscript": es_rgb,
}


resp = api.request(request)
np_array = np.frombuffer(resp.content, np.uint8)
image = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
image_info(image)


request["evalscript"] = es_veg
resp = api.request(request)
np_array = np.frombuffer(resp.content, np.uint8)
veg_image = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
image_info(veg_image)

cv2.imshow("ok", image)
cv2.imshow("ok2", veg_image)
cv2.waitKey(-1)