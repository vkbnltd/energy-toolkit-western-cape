from atlite.gis import ExclusionContainer
import paths


def excluder(energy_type):

    # REPLACE with your logic for creating area exclusions per each renewable energy_type: solar, onwind, offwind

    exclcont = ExclusionContainer()

    exclcont.add_raster("REPLACE with your logic")

    return exclcont