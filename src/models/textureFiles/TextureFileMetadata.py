from src.constants.TextureMap import TextureMap
from src.models.FileMetadata import FileMetadata


class TextureFileMetadata:
    def __init__(
            self,
            scene_name: str,
            material_name: str,
            texture_map: TextureMap,
            file_metadata: FileMetadata = None
    ):
        self.scene_name = scene_name
        self.material_name = material_name
        self.texture_map = texture_map
        self.file_metadata = file_metadata
