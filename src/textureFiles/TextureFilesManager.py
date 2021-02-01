from typing import List, Union, Tuple

from src.constants.TextureMapType import TextureMapType
from src.models.DirectoryContext import DirectoryContext
from src.models.FileMetadata import FileMetadata
from src.ui.UiManager import UiManager
from src.utils.ioUtils import exportFile
from src.textureFiles.TextureFileMetadata import TextureFileMetadata
from src.textureFiles.constants import default_texture_filename_pattern, default_separator_value, \
    texture_file_type_identifier, file_name_identifier, material_identifier, texture_map_identifier, \
    TEXTURE_IDENTIFIERS, VALID_TEXTURE_FILE_FORMATS


class TextureFilesManager:
    @staticmethod
    def __cloneTextureMetadata(texture_file: TextureFileMetadata, new_file_metadata) -> TextureFileMetadata:
        return TextureFileMetadata(
            scene_name=texture_file.scene_name,
            material_name=texture_file.material_name,
            texture_map=texture_file.texture_map,
            file_metadata=new_file_metadata
        )

    @staticmethod
    def exportTextureFiles(
            path_to_export,
            texture_files: Tuple[TextureFileMetadata]
    ) -> Tuple[TextureFileMetadata]:
        exported_textures: List[TextureFileMetadata] = []

        for texture_file in texture_files:
            exported_file_metadata: FileMetadata = exportFile(texture_file.file_metadata, path_to_export)
            exported_texture_metadata = TextureFilesManager.__cloneTextureMetadata(texture_file, exported_file_metadata)
            exported_textures.append(exported_texture_metadata)

        return tuple(exported_textures)

    def __init__(
            self,
            filename_pattern: str = default_texture_filename_pattern,
            separator_value: str = default_separator_value,
    ):
        self.filename_pattern = filename_pattern
        self.separator_value = separator_value
        self.pattern_identifiers = self.__extractPatternIdentifiersFromPatternString()

        self.file_type_identifier_index = self.pattern_identifiers.index(texture_file_type_identifier)
        self.file_name_identifier_index = self.pattern_identifiers.index(file_name_identifier)
        self.material_identifier_index = self.pattern_identifiers.index(material_identifier)
        self.texture_map_identifier_index = self.pattern_identifiers.index(texture_map_identifier)

    def __extractPatternIdentifiersFromPatternString(self):
        filename_parts = self.filename_pattern.split(self.separator_value)
        filtered_filename_parts = [part.strip() for part in filename_parts if part in TEXTURE_IDENTIFIERS]
        unique_filename_parts = dict.fromkeys(filtered_filename_parts).keys()
        return tuple(unique_filename_parts)

    def getTextureFilesForDir(self, dir_context: DirectoryContext) -> List[TextureFileMetadata]:
        image_files: Tuple[FileMetadata] = dir_context.getFilesByExtension(VALID_TEXTURE_FILE_FORMATS)
        return [self.__getTextureMetadata(file_metadata) for file_metadata in image_files if bool(file_metadata)]

    def __getTextureMetadata(self, file_metadata: FileMetadata) -> Union[TextureFileMetadata, None]:
        file_name_parts = file_metadata.file_name.split(self.separator_value)
        is_valid_texture_file_name = self.__validateTextureFileName(file_name_parts)

        return TextureFileMetadata(
            scene_name=file_name_parts[self.file_name_identifier_index],
            material_name=file_name_parts[self.material_identifier_index],
            texture_map=TextureMapType(file_name_parts[self.texture_map_identifier_index]),
            file_metadata=file_metadata
        ) if is_valid_texture_file_name else None

    def __validateTextureFileName(self, file_name_parts) -> bool:
        if len(file_name_parts) != len(self.pattern_identifiers):
            print("Incorrect texture file name format")
            return False

        if file_name_parts[self.file_type_identifier_index] != texture_file_type_identifier:
            print("Missing or incorrect place of Texture identifier in file name")
            return False

        if file_name_parts[self.texture_map_identifier_index] \
                not in [texture_map_type.value for texture_map_type in TextureMapType]:
            print("File name does not contain correct or has misplaced Texture Map identifier")
            UiManager.hintTextureMapTypeIdentifiers()
            return False

        return True
