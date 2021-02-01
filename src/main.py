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

# endregion ######################################################################
# region Info gathering from user ################################################
# TODO: ask user: download or read from resources/import
# TODO: downloads -> ask .txt file with urls
# TODO: asks texture file identifiers pattern

url_list_file_path = input(
    "Please enter file absolute location (Exmp. D:\\myfiles\\fbx_list.txt)."
    "\nOr press ENTER to read form demo file in resources.\n"
)
if not bool(url_list_file_path.strip()):
    url_list_file_path = os.path.join(paths.resources_dir_path, 'demo_urls.txt')

# endregion ######################################################################
# region Info gathering from user ################################################

fbx_model_url_list = getLinesListFromFile(url_list_file_path)


# endregion ######################################################################
# Execute actions ################################################################

# zip_obj = zipfile.ZipFile(paths.resources_dir_path + '\\woodenBall.zip', 'r')
def processAndExportFbxFiles(binary_files: List[io.BytesIO]):
    for binary_file in binary_files:
        with zipfile.ZipFile(binary_file) as zip_obj:
            extraction_data = extractZipFile(zip_obj)
            if not extraction_data: continue
            zip_dir_context, fbx_files, path_to_extract = extraction_data

            if fbx_files:
                createDirectory(path_to_extract)
                print(f"exporting to disk into: {path_to_extract}")
                zip_obj.extractall(path_to_extract)
            else:
                print(errorMessages.archive_missing_fbx_file)
                continue

            processFbxFilesWithBlender(fbx_files, zip_dir_context)


downloadedContent = downloadContentFromUrlList(fbx_model_url_list)
processAndExportFbxFiles(downloadedContent)

# endregion ######################################################################
