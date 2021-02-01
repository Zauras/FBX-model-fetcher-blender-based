from src.constants.FileExtensions import FileExtensions

# region CONSTANTS
VALID_TEXTURE_FILE_FORMATS = (FileExtensions.JPG, FileExtensions.PNG)

texture_file_type_identifier = 'T'
file_name_identifier = 'FILE'
material_identifier = 'MAT'
texture_map_identifier = "MAP"
# endregion

# region DEFAULT VALUES
default_separator_value = '_'

TEXTURE_IDENTIFIERS = [
    texture_file_type_identifier,
    file_name_identifier,
    material_identifier,
    texture_map_identifier
]
default_texture_filename_pattern = default_separator_value.join(TEXTURE_IDENTIFIERS)
# endregion
