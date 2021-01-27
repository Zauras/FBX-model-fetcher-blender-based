import os, zipfile
import pathlib


def extractZipToMemory(input_zip):
    # read zip content to memory
    input_zip = zipfile.ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}


def getLinesListFromFile(file_path):
    return [line.strip() for line in open(file_path, 'r')]


def getZipNameInMemory(zipfile_obj: zipfile.ZipFile):
    files_in_zip = zipfile_obj.namelist()
    if len(files_in_zip) == 0: return None
    zip_name = files_in_zip[0]
    return pathlib.Path(zip_name).stem


def createDirectory(dir_path: str) -> bool:
    try:
        os.mkdir(dir_path)
    except OSError:
        print("Creation of the directory %s failed" % dir_path)
        return False
    else:
        print("Successfully created the directory %s " % dir_path)
        return True
