import atlite
from atlite.gis import ExclusionContainer
import xarray as xr
import paths

def excluder(type):
    # Exclude land use per solar/wind
             
    # Source: https://egis.environment.gov.za/sa_national_land_cover_datasets
    # Download "South African National Land Cover (SANLC), 2018" Level 1 and 2 with info
    # Download tif: https://egis.environment.gov.za/data_egis/data_download/current
    # Classification: https://sfiler.environment.gov.za:8443/ssf/s/readFile/folderEntry/40903/8afbc1c77a484088017a4dddf3f3003f/1624802400000/last/SA_NLC_2020%20_Accuracy_Assessment_Report.zip

    # Must use INCLUDED because the geojson has bigger area than the CORINE tif.
    # Land-cover classes INCLUDED for solar areas:
    INCLUDED_SOLAR = [7,8,9,10,11,12,13,25,26,27,28,43,44,45,46,72,73]
    # Land-cover classes INCLUDED for wind energy areas:
    INCLUDED_WIND_NON_OCEAN = [7,8,11,12,26,27,30,31,38,40,42,43,44,45,46,70,71,72,73]
    INCLUDED_WIND_OCEAN = [16]
    
    CORINE = paths.input_path / 'geo/sanlc_western_cape.tif'

    exclusion = {
        'solar': {
            'codes': INCLUDED_SOLAR,
            'invert': True
        },
        'onwind': {
            'codes': INCLUDED_WIND_NON_OCEAN,
            'invert': True
        },
        'offwind': {
            'codes': INCLUDED_WIND_OCEAN,
            'invert': True
        }
    }

    exclcont = ExclusionContainer()

    exclcont.add_raster(CORINE, codes=exclusion[type]['codes'], invert=exclusion[type]['invert'], crs="EPSG:4326")

    return exclcont

def availability_matrix(cutout, selection, type):
    type_excluder = excluder(type)
    return cutout.availabilitymatrix(selection, type_excluder)

def capacity_factor(cutout, selection, type, model, matrix_path):

    wind_turbine = paths.library_path / 'windturbine' / model

    if (matrix_path).is_file():
        avail = xr.open_dataarray(matrix_path)
    else:
        avail = availability_matrix(cutout, selection, type)

    avail_matrix = avail.stack(spatial=["y", "x"])

    match type:
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