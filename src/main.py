# To run:
# F:\Programs\Blender2.91\blender --background --python src/main.py

# python -m pip install requests
import zipfile, io, os

from src import blenderApi
from src.utils import ioUtils, httpUtils, paths
from src.validation import validation

print("Hello Headless BLENDER")

#################################################################################


# get file location
url_list_file_path = input(
    "Please enter file absolute location (Exmp. D:\\myfiles\fbx_list.txt)."
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
session = httpUtils.getSession()
print("open session")

for file_number, zip_file_url in enumerate(fbx_model_url_list, start=1):
    print(f"iteration: {file_number}")

    # not working properly
    # if not check_if_downloadable(zip_file_url):
    #     print(f"Sorry, but content is not downloadable from url: {zip_file_url}")
    #     continue

    # ignored, filename = zip_file_url.rsplit('/', 1)
    # print(f"filename: {filename}")

    response = session.get(zip_file_url)
    print(f"...Downloading file {file_number} from ===> {zip_file_url}")

    if not response.ok:
        print(f"Sorry, could not download file from url: {zip_file_url}")
        session.close()
        continue

    # read zip file binary:
    print("reading zip from response")
    response_content_binary = io.BytesIO(response.content)

    # Create a ZipFile Object and load sample.zip in it
    with zipfile.ZipFile(response_content_binary) as zip_obj:
        # TODO: checks refactor into try with decorators
        if validation.checkIsZipValid(zip_obj): continue

        fbx_file_names = ioUtils.tryGetFbxFilenamesFromZip(zip_obj)
        if not bool(fbx_file_names): continue

        fbx_file_names_without_extension = os.path.splitext(fbx_file_names[0])[0]
        path_to_extract = os.path.join(paths.downloads_dir_path, fbx_file_names_without_extension)
        # create folder for extraction:
        try:
            os.mkdir(path_to_extract)
        except OSError:
            print("Creation of the directory %s failed" % path_to_extract)
        else:
            print("Successfully created the directory %s " % path_to_extract)

        # Extract zip to disk:
        print(f"exporting to disk into: {path_to_extract}")
        zip_obj.extractall(path_to_extract)

        ####### Blender actions: ###############################################################

        blender_obj = blenderApi.getActiveObjectInScene()

        # Check if has any material: (If an object doesn't have a material, it can be ignored.)
        validation.checkIfHasMaterial(blender_obj)

# TODO:
# for each request pass a chain
#
