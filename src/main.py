# To run:
# F:\Programs\Blender2.91\blender --background --python src/main.py

# python -m pip install requests
import sys, io, os, zipfile

from typing import List


# region Local & Third Party modules setup ########################################

def registerModulesDirectories(module_path_list: List[str]):
    for module_path in module_path_list:
        if module_path not in sys.path:
            sys.path.append(module_path)


import bpy

blenderDir = os.path.dirname(bpy.data.filepath)
srcDir = os.path.dirname(os.path.realpath(__file__))
registerModulesDirectories([blenderDir, srcDir])

# endregion ######################################################################
# region Internal Imports ########################################################

from src.blenderApi.blenderApi import processFbxFilesWithBlender
from src.constants import paths
from src.utils.ioUtils import getLinesListFromFile, createDirectory, extractZipFile
from src.utils.httpUtils import downloadContentFromUrlList
from src.utils.validation import errorMessages
from src.utils.validation.validationChecks import isZipFile
from src.models.textureFiles.TextureFilesManager import TextureFilesManager, default_texture_filename_pattern, \
    texture_file_type_identifier, texture_map_identifier, material_identifier, file_name_identifier, \
    default_separator_value

# endregion ######################################################################
# region Info gathering from user ################################################

binary_files_to_process: List[io.BytesIO] = []

# TODO: ask user: download or read from resources/import
import_action_type = input(
    "\n################# Choose import type ###############################"
    "\nPlease enter how you want to import files."
    "\nPossible answers: "
    "\n   D - for download from url list"
    f"\n   I - for import from {paths.imports_dir_path}"
    "\nAnswer: "
)

# TODO: downloads -> ask .txt file with urls
if import_action_type == 'D':
    url_list_file_path = input(
        "\n################# Choose url list source ###############################"
        "\nPlease enter file absolute location (Exmp. D:\\myfiles\\fbx_list.txt)."
        "\nOr press ENTER to read form demo file in resources.\n"
        "\nUrls source: "
        "\n"
    )

    if not bool(url_list_file_path.strip()):
        url_list_file_path = os.path.join(paths.resources_dir_path, 'demo_urls.txt')

    fbx_model_url_list = getLinesListFromFile(url_list_file_path)
    binary_files_to_process = downloadContentFromUrlList(fbx_model_url_list)

elif import_action_type == 'I':
    # TODO: read all .zip files in imports dir dir
    path_to_imports = paths.imports_dir_path
    import_files = [f for f in os.listdir(path_to_imports) if os.path.isfile(os.path.join(path_to_imports, f))]
    print(import_files)

    # TODO: extract each to memory as binary
    binary_files = []
    for file in import_files:
        file_path = os.path.join(path_to_imports, file)
        print(zipfile.is_zipfile(file_path))

        if zipfile.is_zipfile(file_path):
            with open(file_path, 'rb') as binary_stream:
                binary_file = io.BytesIO(binary_stream.read())
                binary_files.append(binary_file)

    binary_files_to_process = binary_files

# TODO: asks texture file identifiers pattern
texture_filename_pattern = input(
    "\n################# Choose texture file name pattern ########################"
    "\nPlease enter texture file name pattern"
    f"\nOr press ENTER to use default pattern: {default_texture_filename_pattern}\n"
    "\nValid pattern identifiers: "
    f"\n   {texture_file_type_identifier} - texture file identifier"
    f"\n   {file_name_identifier} - scene file name identifier"
    f"\n   {material_identifier} - material name identifier"
    f"\n   {texture_map_identifier} - texture map type identifier"
    "\n\nTexture file name pattern: "
)
if not bool(texture_filename_pattern.strip()):
    texture_filename_pattern = default_texture_filename_pattern

separator_value = input(
    f"\nConfirm custom separator or press ENTER and use default: \'{default_separator_value}\'"
)
if not bool(separator_value.strip()):
    separator_value = default_separator_value

# endregion ######################################################################
# region Info gathering from user ################################################


# endregion ######################################################################
# Execute actions ################################################################

texture_files_manager = TextureFilesManager(
    filename_pattern=texture_filename_pattern,
    separator_value=separator_value
)


def processAndExportFbxFiles(binary_files: List[io.BytesIO]):
    for binary_file in binary_files:
        with zipfile.ZipFile(binary_file) as zip_obj:
            extraction_data = extractZipFile(zip_obj)
            if not extraction_data: continue
            zip_dir_context, fbx_files, path_to_extract = extraction_data

            if fbx_files:
                createDirectory(path_to_extract)
                print(f"Exporting to disk into: {path_to_extract}")
                zip_obj.extractall(path_to_extract)
            else:
                print(errorMessages.archive_missing_fbx_file)
                continue

            processFbxFilesWithBlender(fbx_files, zip_dir_context, texture_files_manager)


print("\n################# Processing imported FBX files ######################")

processAndExportFbxFiles(binary_files_to_process)

print(
    "\nExporting finished."
    "\nPlease inspect processed files in: "
    f"\n    {paths.exports_dir_path}"
)

# endregion ######################################################################
