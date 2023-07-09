import os

# Copernicus credentials
COPERNICUS_ID = os.environ.get('COPERNICUS_ID')
COPERNICUS_SECRET = os.environ.get('COPERNICUS_SECRET')

es_rgb = """
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

es_veg = """
//VERSION=3
function setup() {
  return {
    input: ["B05", "B06", "B07"],
    output: {
      bands: 3,
      sampleType: "AUTO", // default value - scales the output values from [0,1] to [0,255].
    },
  }
}

function evaluatePixel(sample) {
  return [sample.B05, sample.B06, sample.B07]
}
"""

def gen_request(coords, time, es):
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
                    },
                }
            ],
        },
        "output": {"width": 512, "height": 512,},
        "evalscript": es,
    }
    return request