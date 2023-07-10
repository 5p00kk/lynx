
from utils import es_rgb, es_veg, es_rgb_cl, image_info, gen_request
from copernicus import CopernicusAPI, CopernicusReq
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
years = [year for year in range(2020,2024)]
months = [month for month in range(1,13)]
requests = []
for year in years:
    for month in months:
        from_d = f"{year}-{month:02d}-01T00:00:00Z"
        to_d = f"{year}-{month:02d}-28T00:00:00Z"
        time = (from_d, to_d)
        request = CopernicusReq(box_coords, time, OUTPUT_SIZE_PX, es_rgb)
        requests.append(request)

for i, request in enumerate(requests):
    # Get
    resp = api.request(request.get_request())
    # Decode
    np_array = np.frombuffer(resp.content, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
    # Save
    cv2.imwrite(f"{request.years[0]}_{request.months[0]}.png", image)

cv2.waitKey(-1)
