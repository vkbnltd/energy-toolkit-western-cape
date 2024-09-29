import pandas as pd
import geopandas as gpd
import atlite
from shapely.ops import unary_union
from shapely.geometry import Polygon

from input.geo.geo_core import get_geo
import paths

def generate_cutout(weather_geo, sections, weather_start, weather_end):
    #Source: https://www.igismap.com/south-africa-shapefile-download-boundary-line-polygon/
    #country = gpd.read_file(f"{root_data_path}/geo/south_africa_Province_level_1.geojson")
    #KEY = 'shape1'
    #Source: https://cartographyvectors.com/map/1334-western-cape-south-africa

    country = gpd.read_file(paths.geo_root / 'western-cape-south-africa_1334.geojson')
    KEY = 'name'

    area = country.loc[country[KEY].isin([weather_geo])]

    minx, miny, maxx, maxy = area.total_bounds

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

    selections = gpd.GeoDataFrame(geometry=[unary_union(area.geometry)], crs=country.crs)

    eez = None # REPLACE with code creating eez using gpd

    index = pd.to_datetime(cutout.coords['time'])

    return [cutout, selections, eez, index]