from typing import List, Union, Tuple
from functional import seq

from src.constants.TextureMap import TextureMap
from src.models.DirectoryContext import DirectoryContext
from src.models.FileMetadata import FileMetadata
from src.models.textureFiles.TextureFileMetadata import TextureFileMetadata
from src.constants.FileExtensions import FileExtensions

# region CONSTANTS

VALID_TEXTURE_FILE_FORMATS = (FileExtensions.JPG, FileExtensions.PNG)

file_type_identifier = 'T'
file_name_identifier = 'FILE'
material_identifier = 'MAT'
texture_map_identifier = "MAP"

# endregion

# region DEFAULT VALUES
default_separator_value = '_'

TEXTURE_IDENTIFIERS = [
    file_type_identifier,
    file_name_identifier,
    material_identifier,
    texture_map_identifier
]
default_texture_filename_pattern = default_separator_value.join(TEXTURE_IDENTIFIERS)


# endregion


class TextureFilesManager:
    def __init__(
            self,
            filename_pattern: str = default_texture_filename_pattern,
            separator_value: str = default_separator_value,
    ):
        self.filename_pattern = filename_pattern
        self.separator_value = separator_value
        self.pattern_identifiers = tuple((seq(set(self.filename_pattern.split(self.separator_value)))
                                          .map(lambda identifier: identifier.strip())
                                          .filter(lambda identifier: identifier in TEXTURE_IDENTIFIERS)
                                          ))
        self.file_type_identifier_index = self.pattern_identifiers.index(file_type_identifier)
        self.file_name_identifier_index = self.pattern_identifiers.index(file_name_identifier)
        self.material_identifier_index = self.pattern_identifiers.index(material_identifier)
        self.texture_map_identifier_index = self.pattern_identifiers.index(texture_map_identifier)

    def getTextureFilesForDir(self, dir_context: DirectoryContext) -> List[TextureFileMetadata]:
        image_files: Tuple[FileMetadata] = dir_context.getFilesByExtension(VALID_TEXTURE_FILE_FORMATS)
        return seq([self.__getTextureMetadata(file_metadata) for file_metadata in image_files])\
            .filter(lambda file: bool(file))

    def __getTextureMetadata(self, file_metadata: FileMetadata) -> Union[TextureFileMetadata, None]:
        file_name_parts = file_metadata.file_name.split(self.separator_value)

        # TODO: separate validation checkers:
        is_valid_texture_file_name = self.__validateTextureFileName(file_name_parts)

        return TextureFileMetadata(
            scene_name=file_name_parts[self.file_name_identifier_index],
            material_name=file_name_parts[self.material_identifier_index],
            texture_map=TextureMap[file_name_parts[self.texture_map_identifier_index]],
            file_metadata=file_metadata
        ) if is_valid_texture_file_name else None

    def __validateTextureFileName(self, file_name_parts) -> bool:
        if len(file_name_parts) != len(self.pattern_identifiers):
            print("Incorrect texture file name format")
            return False
        if file_name_parts[self.file_type_identifier_index] != file_type_identifier:
            print("Missing or incorrect place of Texture identifier in file name")
            return False
        if file_name_parts[self.texture_map_identifier_index] not in file_type_identifier:
            print("File name does not contain correct or has misplaced Texture Map identifier")
            # TODO: separate as help hint utils function:
            print("Valid Texture Map identifiers are:")
            print("Identifier - Texture Map")
            for texture_map in TextureMap:
                print(f"\'{texture_map.value}\' - {texture_map.name}")
            return False
        return True
