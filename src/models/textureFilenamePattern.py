# region CONSTANTS
file_type_identifier = 'T'
filename_identifier = 'FILE'
material_identifier = 'MAT'
texture_map_identifier = "MAP"
# endregion

# region DEFAULT VALUES
default_separator_value = '_'

default_identifier_list = [
    file_type_identifier,
    filename_identifier,
    material_identifier,
    texture_map_identifier
]
default_texture_filename_pattern = default_separator_value.join(default_identifier_list)


# endregion


class TextureFilePattern:
    def __init__(
            self,
            filename,
            filename_pattern,
            separator_value=default_separator_value,
    ):
        identifier_list = filter(
            lambda identifier: isinstance(identifier, str) and bool(identifier.strip()),
            [
                file_type_identifier,
                filename_identifier,
                material_identifier,
                texture_map_identifier
            ]
        )

        filename_pattern_parts = set(filename_pattern.split(separator_value))
        ordered_identifiers = [x for x in filename_pattern_parts if x in identifier_list]
        identifiers_values = set(filename.split(separator_value))

        self.identifiers_dictionary = dict(zip(ordered_identifiers, identifiers_values))

    def getFileType(self): return self.identifiers_dictionary[file_type_identifier]

    def getModelFileName(self): return self.identifiers_dictionary[filename_identifier]

    def getMaterialName(self): return self.identifiers_dictionary[material_identifier]

    def getTextureMapType(self): return self.identifiers_dictionary[texture_map_identifier]
