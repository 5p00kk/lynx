import os
import math
import numpy as np

# Copernicus credentials
COPERNICUS_ID = os.environ.get('COPERNICUS_ID')
COPERNICUS_SECRET = os.environ.get('COPERNICUS_SECRET')

EARTH_CIRC = 40075

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

es_rgb_cl = """
//VERSION=3
function setup() {
  return {
    input: ["B02", "B03", "B04", "SCL"],
    output: {
      bands: 3,
      sampleType: "AUTO", // default value - scales the output values from [0,1] to [0,255].
    },
  }
}

function evaluatePixel(sample) {
  if ([8, 9, 10].includes(sample.SCL)) {
    return [1, 0, 0]
  } else {
    return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02]
  }
}
"""


def image_info(image):
    print(f"Loaded image is {image.shape}, {image.dtype}, {image.shape[0]*image.shape[1]*image.shape[2]*image.itemsize}")
    print(f"Num uniques {len(np.unique(image))}")

class BoxCalc:
    def __init__(self, output_size, data_resolution) -> None:
        self.resolution = data_resolution
        self.output_size_px = output_size
        self.output_size_km = output_size*data_resolution
        self.coords = (0,0)

    def get_box(self, center_pt):
        lat_d = BoxCalc.km_to_latd(self.output_size_km)
        lon_d = BoxCalc.km_to_lond(self.output_size_km, center_pt[1])
        self.coords = [center_pt[0]-lon_d/2, center_pt[1]-lat_d/2, center_pt[0]+lon_d/2, center_pt[1]+lat_d/2]
        return self.coords
    
    @staticmethod
    def latd_to_km(lat_d):
        km = lat_d*(EARTH_CIRC/360)
        return km
    
    @staticmethod
    def km_to_latd(km):
        lat_d = km*(360/EARTH_CIRC)
        return lat_d
    
    @staticmethod
    def lond_to_km(lon_d, lat):
        km = math.cos(math.radians(lat))*lon_d*(EARTH_CIRC/360)
        return km
    
    @staticmethod
    def km_to_lond(km, lat):
        lon_d = (1/math.cos(math.radians(lat)))*(360/EARTH_CIRC)*km
        return lon_d

    def __repr__(self) -> str:
        return f"BoxCalc [km]{self.resolution}, [km]{self.output_size_km}x{self.output_size_km} [px]{self.output_size_px}x{self.output_size_px}"