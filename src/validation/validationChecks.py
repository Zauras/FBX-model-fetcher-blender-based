import zipfile

from src import blenderApi
from src.main import zip_file_url
from src.validation import errorMessages


def checkIsZipValid(zip_obj):
    if zipfile.ZipFile.testzip(zip_obj):
        return True
    else:
        print(errorMessages.invalid_zip)
        return False


def checkIfHasMaterial(blender_obj) -> bool:
    has_material = blenderApi.doesObjContainsMaterials(blender_obj)
    if has_material:
        return True
    else:
        print(errorMessages.no_material)
        return False


def checkIsHttpResponseOk(response):
    if not response.ok:
        print(f"Sorry, could not download file from url: {zip_file_url}")
