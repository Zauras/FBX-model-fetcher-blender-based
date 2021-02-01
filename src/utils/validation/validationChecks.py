import zipfile

from src.utils.validation import errorMessages


def isZipFile(path):
    return zipfile.ZipFile.testzip(path)


def checkIsZipValid(zip_obj):
    if zipfile.ZipFile.testzip(zip_obj):
        return True
    else:
        print(errorMessages.invalid_zip)
        return False


def checkIsHttpResponseOk(response, request_url: str):
    if not response.ok:
        print(f"Sorry, could not download file from url: {request_url}")
