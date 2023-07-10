import math
import numpy as np

EARTH_CIRC = 40075

def image_info(image):
    if type(image) != np.array:
      image = np.array(image)
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