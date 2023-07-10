
from utils import es_rgb, es_veg, es_rgb_cl, image_info, gen_request
from copernicus import CopernicusAPI
import numpy as np
import cv2
from utils import BoxCalc

RESOLUTION_KM = 0.01 # 10m
OUTPUT_SIZE_PX = 512 # px
CENTER = (16.931992, 52.409538) # lon, lat poznan

api = CopernicusAPI()
box_cal = BoxCalc(OUTPUT_SIZE_PX, RESOLUTION_KM)
print(box_cal)

# Calculate box coordinates (WGS84)
box_coords = box_cal.get_box(CENTER)

# Prepare requests
time = ("2023-06-10T00:00:00Z", "2023-07-10T00:00:00Z")
requests = [gen_request(box_coords, time, OUTPUT_SIZE_PX, es_rgb), gen_request(box_coords, time, OUTPUT_SIZE_PX, es_veg)]

for i, request in enumerate(requests):
    resp = api.request(request)
    np_array = np.frombuffer(resp.content, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
    image_info(image)
    cv2.imshow(f"req {i}", image)
    cv2.waitKey(5)
cv2.waitKey(-1)