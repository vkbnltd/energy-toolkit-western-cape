import pandas as pd
import geopandas as gpd
import atlite

import paths
from input.weather.cutout import generate_cutout

def store_weather(geo, sections, weather_start, weather_end):
    cutout_path = paths.weather / f"cutout,geography={geo},start={weather_start},end={weather_end}.nc"
    index_path = paths.weather / f"index,geography={geo},start={weather_start},end={weather_end}.nc"

    cutout, selections, eez, index = generate_cutout(geo, sections, weather_start, weather_end)

    index.to_series().to_csv(index_path)

    for key, selection in selections.items():
        selection_path = paths.weather / f"selection,geography={key},start={weather_start},end={weather_end}.shp"

        if not selection_path.is_file():
            selection.to_file(selection_path)

def load_weather(geo, section, weather_start, weather_end):
    cutout_path = paths.weather / f"cutout,geography={geo},start={weather_start},end={weather_end}.nc"

    section_key = None if section is None else (section if not isinstance(section, list) else "-".join(section))
    geo_key = section_key if section_key is not None else geo

    selection_path = paths.weather / f"selection,geography={geo_key},start={weather_start},end={weather_end}.shp"

    cutout = atlite.Cutout(cutout_path)#, chunks={"time": 1, "x": 1024, "y": 1024})
    selection = gpd.read_file(selection_path)#, chunks={"time": 1, "x": 1024, "y": 1024})
    index = pd.to_datetime(cutout.coords['time'])

    return cutout, selection, index
