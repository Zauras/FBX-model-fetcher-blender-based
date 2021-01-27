# import TextureFilePattern from textureFilePattern
from src.models.textureFiles.TextureFilesManager import TextureFilePattern


class ImportModelProcessContext:
    def __init__(
            self,
            filename,
            filename_pattern,
            separator_value,
    ):
        self.filename = filename
        self.texture_file_pattern = TextureFilePattern(filename, filename_pattern, separator_value)
