import pandas as pd
import geopandas as gpd
import atlite
from shapely.ops import unary_union
from shapely.geometry import Polygon

from input.geo.geo_core import get_geo
import paths

def generate_cutout(weather_geo, sections, weather_start, weather_end):
        
    minx, miny, maxx, maxy = [] # REPLACE with function assigning bounds for cutout

    cutout_path = paths.weather /  f"cutout,geography={weather_geo},start={weather_start},end={weather_end}.nc"
    
    cutout = atlite.Cutout(
        path=cutout_path,
        module="era5",
        x=slice(minx, maxx),
        y=slice(miny, maxy),
        time=slice(weather_start,weather_end),
        dx=0.125,
        dy=0.125,
        dt="3h"
    )

    cutout.prepare(features=['influx', 'temperature', 'wind'])

    selections = {} # REPLACE with code creating the selections object using the sections input

    eez = None # REPLACE with code creating eez using gpd

    index = pd.to_datetime(cutout.coords['time'])

    return [cutout, selections, eez, index]