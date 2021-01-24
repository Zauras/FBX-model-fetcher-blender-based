import os, zipfile
from typing import AnyStr

from src.validation import errorMessages


def joinPath(base_path, *paths) -> AnyStr:
    return os.path.join(base_path, paths)


def tryGetFbxFilenamesFromZip(zip_obj) -> list:
    # Get list of files names in zip
    file_names_in_zip = zip_obj.namelist()

    # for file_name in file_names_in_zip:
    fbx_file_names = [f for f in file_names_in_zip if f.endswith('.fbx')]

    if not bool(fbx_file_names):
        print(errorMessages.archive_missing_fbx_file)

    return fbx_file_names


def extractZipToMemory(input_zip):
    # read zip content to memory
    input_zip = zipfile.ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}


def getImageFilesFromDir(dir_path):
    extensions = [".jpg", ".png"]
    return [filename for filename in os.listdir(dir_path) if os.path.splitext(filename)[1] in extensions]


def getLinesListFromFile(file_path):
    return [line.strip() for line in open(file_path, 'r')]
