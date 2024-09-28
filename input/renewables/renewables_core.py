import atlite
import paths
import xarray as xr

from excluder import excluder

def availability_matrix(cutout, selection, energy_type):
    type_excluder = excluder(energy_type)
    return cutout.availabilitymatrix(selection, type_excluder)

def capacity_factor(cutout, selection, energy_type, generator, weather_geo, section, weather_start, weather_end):

    geo = section if section is not None else weather_geo

    wind_turbine = paths.renewables_root / 'windturbines_core' / generator
    matrix_path = paths.renewables / f"availability-matrix-{energy_type},geography={geo},start={weather_start},end={weather_end}.nc"

    if (matrix_path).is_file():
        avail = xr.open_dataarray(matrix_path)
    else:
        avail = availability_matrix(cutout, selection, energy_type)

    avail_matrix = avail.stack(spatial=["y", "x"])

    match energy_type:
        case 'solar':
            return cutout.pv(
                matrix=avail_matrix,
                panel=atlite.solarpanels.CdTe,
                orientation="latitude_optimal",
                index=selection.index,
                per_unit =True,
            )
        case 'onwind':
            return cutout.wind(
                matrix=avail_matrix,
                turbine = atlite.resource.get_windturbineconfig(wind_turbine),
                index=selection.index,
                per_unit =True,
            )

        case 'offwind':
            return cutout.wind(
                matrix=avail_matrix,
                turbine = atlite.resource.get_windturbineconfig(wind_turbine),
                index=selection.index,
                per_unit =True,
            )
        case _:
            print("Unknown energy type (solar, onwind, offwind)")
            return

def store_availability_matrix(cutout, selection, energy_type, weather_geo, section, weather_start, weather_end):

    geo = section if section is not None else weather_geo
    matrix_path = paths.renewables / f"availability-matrix-{energy_type},geography={geo},start={weather_start},end={weather_end}.nc"

    if not matrix_path.is_file():
        avail_matrix = availability_matrix(cutout, selection, energy_type)
        avail_matrix.to_netcdf(matrix_path)

def store_capacity_factor(cutout, selection, energy_type, model, weather_geo, section, weather_start, weather_end):

    geo = section if section is not None else weather_geo
    capfac_path = paths.renewables / f"capacity-factor-{energy_type},geography={geo},start={weather_start},end={weather_end}.nc"

    if not capfac_path.is_file():
        capfac = capacity_factor(cutout, selection, energy_type, model, weather_geo, section, weather_start, weather_end)
        capfac.to_netcdf(capfac_path)