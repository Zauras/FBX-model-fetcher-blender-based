import io, os

from typing import Tuple, List

from src.constants import paths
from src.constants.ImportActionType import ImportActionType
from src.constants.TextureMapType import TextureMapType
from src.textureFiles.constants import default_separator_value, default_texture_filename_pattern, \
    texture_file_type_identifier, file_name_identifier, material_identifier, texture_map_identifier
from src.utils.httpUtils import downloadContentFromUrlList
from src.utils.ioUtils import extractZipsInDirectoryToMemory, getLinesListFromFile


class UiManager:
    @staticmethod
    def getZipFilesAsBinary() -> List[io.BytesIO]:
        import_action_type = UiManager.__askImportActionType()

        if import_action_type.upper() == ImportActionType.Download.value:
            url_list_file_path = UiManager.__askUrlListSource()

            fbx_model_url_list = getLinesListFromFile(url_list_file_path)
            return downloadContentFromUrlList(fbx_model_url_list)

        elif import_action_type.upper() == ImportActionType.Import.value:
            return extractZipsInDirectoryToMemory(paths.imports_dir_path)

        else:
            return UiManager.getZipFilesAsBinary()

    @staticmethod
    def getTextureFilePattern() -> Tuple[str, str]:
        texture_filename_pattern, separator_value = UiManager.__askTextureFileNamePatten()

        if not bool(texture_filename_pattern.strip()):
            texture_filename_pattern = default_texture_filename_pattern

        if not bool(separator_value.strip()):
            separator_value = default_separator_value

        return texture_filename_pattern, separator_value

    @staticmethod
    def shoutExportFinished():
        print(
            "\n\n################# Exporting finished ###############################"
            "\nPlease inspect processed files in: "
            f"\n    {paths.exports_dir_path}"
        )

    @staticmethod
    def hintTextureMapTypeIdentifiers():
        print("Valid Texture Map identifiers are:")
        print("Identifier - Texture Map")
        for texture_map in TextureMapType:
            print(f"{texture_map.value} - {texture_map.name}")

    @staticmethod
    def __askImportActionType() -> str:
        import_action_type = input(
            "\n################# Choose import type ###############################"
            "\nPlease enter how you want to import files."
            "\nPossible answers: "
            "\n   D - for download from url list"
            f"\n   I - for import from {paths.imports_dir_path}"
            "\nAnswer: "
        )
        return import_action_type

    @staticmethod
    def __askUrlListSource() -> str:
        url_list_file_path = input(
            "\n################# Choose url list source #############################"
            "\nPlease enter file absolute location (Exmp. D:\\myfiles\\fbx_list.txt)."
            "\nOr press ENTER to read form demo file in resources.\n"
            "\nUrls source: "
            "\n"
        )
        if not bool(url_list_file_path.strip()):
            return UiManager.__askUrlListSource()

        return url_list_file_path

    @staticmethod
    def __askTextureFileNamePatten() -> Tuple[str, str]:
        texture_filename_pattern = input(
            "\n################# Choose texture file name pattern ###################"
            "\nPlease enter texture file name pattern"
            f"\nOr press ENTER to use default pattern: {default_texture_filename_pattern}\n"
            "\nValid pattern identifiers: "
            f"\n   {texture_file_type_identifier} - texture file identifier"
            f"\n   {file_name_identifier} - scene file name identifier"
            f"\n   {material_identifier} - material name identifier"
            f"\n   {texture_map_identifier} - texture map type identifier"
            "\n\nTexture file name pattern: "
        )
        separator_value = input(
            f"\nConfirm custom separator or press ENTER and use default: \'{default_separator_value}\'"
            "\n"
        )
        return texture_filename_pattern, separator_value
