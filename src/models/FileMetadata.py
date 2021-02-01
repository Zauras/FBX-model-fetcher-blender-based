import os
from pathlib import Path
from typing import List, Union


class FileMetadata:
    # region static
    @staticmethod
    def __getPathObj(file_path) -> Path: return Path(file_path)

    @staticmethod
    def __getDirPath(file_path: str) -> str: return os.path.dirname(file_path)

    @staticmethod
    def __getFileName(path_ob: Path) -> str: return path_ob.stem

    @staticmethod
    def __getFileBase(path_ob: Path) -> str: return path_ob.name

    @staticmethod
    def __getFileExtension(path_ob: Path) -> str: return path_ob.suffix

    # endregion static

    # region properties
    @property
    def file_path(self) -> str: return self.__file_path  # C:/dir/filename.txt

    @property
    def dir_path(self) -> str: return self.__dir_path  # C:/dir

    @property
    def file_base(self) -> str: return self.__file_base  # filename.txt

    @property
    def file_name(self) -> str: return self.__file_name  # filename

    @property
    def extension(self) -> str: return self.__extension  # .txt

    # endregion properties

    # region constructors
    def __init__(self, dir_path: str, file_entry: Union[Path, str]):
        if type(file_entry) is str: file_entry = Path(file_entry)

        self.__dir_path = dir_path
        self.__file_base = FileMetadata.__getFileBase(file_entry)
        self.__file_name = FileMetadata.__getFileName(file_entry)
        self.__extension = FileMetadata.__getFileExtension(file_entry)
        self.__file_path = os.path.join(dir_path, self.file_base)


def getFilesFromDirByExtension(dir_path: str, extensions: List[str]):
    dir_files = Path(dir_path).iterdir()
    x = [file_entry for file_entry in dir_files if file_entry.suffix in extensions]
    return [FileMetadata("d", file_entry) for file_entry in x]
