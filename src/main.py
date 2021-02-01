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
from src.utils.ioUtils import createDirectory, extractZipFile
from src.utils.validation import errorMessages
from src.models.textureFiles.TextureFilesManager import TextureFilesManager
from src.ui.UiManager import UiManager

# endregion ######################################################################
# region Info gathering from user ################################################

binary_files_to_process: UiManager.getZipFilesAsBinary()
texture_filename_pattern, separator_value = UiManager.getTextureFilePattern()

# Execute actions ################################################################

texture_files_manager = TextureFilesManager(
    filename_pattern=texture_filename_pattern,
    separator_value=separator_value
)


def processAndExportFbxFiles(binary_files: List[io.BytesIO]):
    if not bool(binary_files_to_process):
        print("\nThere is no files to process")
        return

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
UiManager.shoutExportFinished()

# endregion ######################################################################
