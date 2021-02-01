# region CONSTANTS
from enum import Enum

albedo_map_identifier = "BC"
normal_map_identifier = "N"
opacity_map_identifier = "O"


# endregion

class TextureMapType(Enum):
    Base_Color = albedo_map_identifier
    Normal = normal_map_identifier
    Opacity = opacity_map_identifier
