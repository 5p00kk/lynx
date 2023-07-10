
from utils import es_rgb, es_veg, es_rgb_cl, gen_request
from copernicus import CopernicusAPI
import numpy as np
import cv2
import math
from utils import latd_to_km, km_to_latd, lond_to_km, km_to_lond

def image_info(image):
    print(f"Loaded image is {image.shape}, {image.dtype}, {image.shape[0]*image.shape[1]*image.shape[2]*image.itemsize}")
    print(f"Num uniques {len(np.unique(image))}")

api = CopernicusAPI()

# Prepare request
pt = (16.931992, 52.409538)
box_size = (0.73, 0.44)
coords = [pt[0]-box_size[0]/2, pt[1]-box_size[1]/2, pt[0]+box_size[0]/2, pt[1]+box_size[1]/2]

time = ("2023-06-10T00:00:00Z", "2023-07-10T00:00:00Z")
requests = [gen_request(coords, time, es_rgb), gen_request(coords, time, es_veg)]

for i, request in enumerate(requests):
    resp = api.request(request)
    np_array = np.frombuffer(resp.content, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
    image_info(image)
    cv2.imshow(f"req {i}", image)
    cv2.waitKey(5)
cv2.waitKey(-1)