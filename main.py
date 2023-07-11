
import os
from PIL import Image 
from io import BytesIO
from utils import image_info
from utils import BoxCalc
from eval_scripts import es_rgb, es_veg, es_rgb_cl
from copernicus import CopernicusAPI, CopernicusReq

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
        request_c = CopernicusReq(box_coords, time, OUTPUT_SIZE_PX, es_rgb, "rgb")
        request_v = CopernicusReq(box_coords, time, OUTPUT_SIZE_PX, es_veg, "veg")
        requests.append(request_c)
        requests.append(request_v)

for i, request in enumerate(requests):
    # Get
    print(f"Getting {request.months[0]}.{request.years[0]}")
    resp = api.request(request.get_request(), True)
    # Decode
    image = Image.open(BytesIO(resp.content))
    # Save
    filename = f"{request.years[0]}_{request.months[0]}_{request.name[0]}.png"
    image.save(os.path.join("imgs", filename))