# To run:
# F:\Programs\Blender2.91\blender --background --python src/main.py

# python -m pip install requests
import bpy
import sys, zipfile, os

from typing import List, Tuple


# region Local & Third Party modules setup
from src.constants.FileExtensions import FileExtensions


def registerModulesDirectories(module_path_list: List[str]):
    for module_path in module_path_list:
        if module_path not in sys.path:
            sys.path.append(module_path)


blenderDir = os.path.dirname(bpy.data.filepath)
srcDir = os.path.dirname(os.path.realpath(__file__))
registerModulesDirectories([blenderDir, srcDir])

from src.utils import ioUtils
from src.constants import paths
from src.utils.ioUtils import createDirectory, getZipNameInMemory
from src.validation import errorMessages
from src.models.DirectoryContext import DirectoryContext
from src.models.FileMetadata import FileMetadata

print("Hello Headless BLENDER")

#################################################################################


# get file location
url_list_file_path = input(
    "Please enter file absolute location (Exmp. D:\\myfiles\\fbx_list.txt)."
    "\nOr press ENTER to read form demo file in resources.\n"
)
if not bool(url_list_file_path.strip()):
    url_list_file_path = os.path.join(paths.resources_dir_path, 'demo_urls.txt')

#################################################################################

# read urls from file
fbx_model_url_list = ioUtils.getLinesListFromFile(url_list_file_path)

#################################################################################
# download fbx models

# with a session, we get keep alive
# session = httpUtils.getSession()
# print("open session")
#
# for file_number, zip_file_url in enumerate(fbx_model_url_list, start=1):
#     print(f"iteration: {file_number}")
#
#     response = session.get(zip_file_url)
#     print(f"...Downloading file {file_number} from ===> {zip_file_url}")
#
#     if not response.ok:
#         print(f"Sorry, could not download file from url: {zip_file_url}")
#         session.close()
#         continue
#
#     # read zip file binary:
#     print("reading zip from response")
#     response_content_binary = io.BytesIO(response.content)

zip_obj = zipfile.ZipFile(paths.resources_dir_path + '\\woodenBall.zip', 'r')

# Create a ZipFile Object and load sample.zip in it
# with zipfile.ZipFile(response_content_binary) as zip_obj:
# region
# TODO: refactor with FileManager and FileMetadata
# TODO: OPTIONAL: checks refactor into try with decorators

# Validation if zip valid
# if not validationChecks.checkIsZipValid(zip_obj): continue

dir_name_to_extract = getZipNameInMemory(zip_obj)
# if not bool(dir_name_to_extract): continue
path_to_extract = os.path.join(paths.downloads_dir_path, dir_name_to_extract)

# Get files metadata form zip in memory:
zip_dir_context = DirectoryContext(path_to_extract, zip_obj)

# region ####### Blender actions: ########
# TODO: 1) iterate through all .fbx files
fbx_files: Tuple[FileMetadata] = zip_dir_context.getFilesByExtension(FileExtensions.FBX)

if fbx_files:
    createDirectory(path_to_extract)
    print(f"exporting to disk into: {path_to_extract}")
    zip_obj.extractall(path_to_extract)
else:
    print(errorMessages.archive_missing_fbx_file)
    # continue

# TODO: 2) create scene with SceneManager

for fbx in fbx_files:
    print(fbx)

# TODO: 3) Apply textures on each Material

# TODO: 4) Reset mesh to origin (identity transform)

# TODO: 5) Reexport .fbx and textures respectively

# endregion

# blender_obj = blenderApi.getActiveObjectInScene()

# Check if has any material: (If an object doesn't have a material, it can be ignored.)
# validation.checkIfHasMaterial(blender_obj)

# TODO:
# for each request pass a chain
#
