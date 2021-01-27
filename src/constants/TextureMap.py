# region CONSTANTS
from enum import Enum

albedo_map_identifier = "BC",
normal_map_identifier = "N",
opacity_map_identifier = "O"


# endregion

class TextureMap(Enum):
    ALBEDO = albedo_map_identifier
    NORMAL = normal_map_identifier
    OPACITY = opacity_map_identifier
