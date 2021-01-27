import os
import zipfile
from enum import Enum
from typing import List, Union, Callable, Tuple, Iterable

from ..constants import paths
from .FileMetadata import FileMetadata


class DirectoryContext:
    # @staticmethod
    # def getFilesMetadataFromZip(dir_name_to_extract: str, zip_obj: zipfile.ZipFile) -> FolderMetadata:
    #     path_to_extract = os.path.join(paths.downloads_dir_path, dir_name_to_extract)
    #     files_in_zip = zip_obj.namelist()  # ["filename.txt"]
    #     return FolderMetadata(path_to_extract, files_in_zip)

    def __init__(self, dir_name_to_extract: str, zip_obj: zipfile.ZipFile):
        path_to_extract = os.path.join(paths.downloads_dir_path, dir_name_to_extract)
        files_in_zip = zip_obj.namelist()  # ["filename.txt"]
        self.__initFileTuple(path_to_extract, files_in_zip)

    # region API:

    def getFilesByExtension(self, extension: Union[str, Iterable[str], Iterable[Enum]]) -> Tuple[FileMetadata]:
        if isinstance(extension, str):
            return self.getFilesByAssertFunc(lambda file_metadata: file_metadata.extension == extension)
        else:
            return self.getFilesByAssertFunc(lambda file_metadata: file_metadata.extension in extension)

    def hasFileWithExtension(self, extension: str):
        return any(file for file in self.files_metadata_tuple if file.extension == extension)

    def getFilesByAssertFunc(self, assert_func: Callable[[FileMetadata], bool]) -> Tuple[FileMetadata]:
        return tuple([file for file in self.files_metadata_tuple if assert_func(file)])

    # endregion

    # region PRIVATE:

    def __initFileTuple(self, dir_path: str, file_bases_list: List[str]):
        self.files_metadata_tuple = tuple([FileMetadata(dir_path, file_base) for file_base in file_bases_list])

    # endregion
