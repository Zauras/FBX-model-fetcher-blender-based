import os, zipfile, io
import pathlib

from shutil import copy
from typing import Tuple, List

from src.constants import paths
from src.constants.FileExtensions import FileExtensions
from src.models.DirectoryContext import DirectoryContext
from src.models.FileMetadata import FileMetadata
from src.utils.validation.errorMessages import failed_extract_zip


def extractZipFile(zip_obj: zipfile.ZipFile):
    try:
        dir_name_to_extract = getZipNameInMemory(zip_obj)

        path_to_extract = os.path.join(paths.downloads_dir_path, dir_name_to_extract)
        print(f"Extracting zip to: {path_to_extract}")

        # Get files metadata form zip in memory:
        zip_dir_context = DirectoryContext(path_to_extract, zip_obj)
        fbx_files: Tuple[FileMetadata] = zip_dir_context.getFilesByExtension(FileExtensions.FBX)

        return zip_dir_context, fbx_files, path_to_extract

    except:
        print(failed_extract_zip)
        return False


def extractZipToMemory(input_zip):
    # read zip content to memory
    input_zip = zipfile.ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}


def getLinesListFromFile(file_path):
    return [line.strip() for line in open(file_path, 'r')]


def getZipNameInMemory(zipfile_obj: zipfile.ZipFile):
    files_in_zip = zipfile_obj.namelist()
    if len(files_in_zip) == 0: return None
    zip_name = zipfile_obj.filename if bool(zipfile_obj.filename) else 'nameless_file.zip'

    return pathlib.Path(zip_name).stem


def createDirectory(dir_path: str) -> bool:
    try:
        os.mkdir(dir_path)
    except OSError:
        print(f"Creation of the directory {dir_path} failed")
        return False
    else:
        print(f"Successfully created the directory {dir_path}")
        return True


def exportFile(source_file: FileMetadata, destination_path: str) -> FileMetadata:
    copy(source_file.file_path, destination_path)
    return FileMetadata(destination_path, source_file.file_base)


def extractZipsInDirectoryToMemory(directory_path):
    dir_files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

    binary_files: List[io.BytesIO] = []
    for file in dir_files:
        file_path = os.path.join(directory_path, file)
        print(zipfile.is_zipfile(file_path))

        if zipfile.is_zipfile(file_path):
            with open(file_path, 'rb') as binary_stream:
                binary_file = io.BytesIO(binary_stream.read())
                binary_files.append(binary_file)

    return binary_files
