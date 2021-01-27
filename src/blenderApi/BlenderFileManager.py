import bpy

from typing import List

from src.models.DirectoryContext import DirectoryContext
from src.models.textureFiles.TextureFileMetadata import TextureFileMetadata
from src.models.textureFiles.TextureFilesManager import TextureFilesManager
from src.constants.FileExtensions import FileExtensions


class BlenderFileManager:
    def __init__(
            self,
            texture_file_pattern_context: TextureFilesManager = TextureFilesManager(),
    ):
        self.texture_file_pattern_context = texture_file_pattern_context
        self.scene_textures: List[TextureFileMetadata] = []

    @staticmethod
    def __loadFbxScene(path_to_fbx_file):
        bpy.ops.import_scene.fbx(filepath=path_to_fbx_file)

    @staticmethod
    def __getFileLoadSwitcher(scene_file_path):
        return {
            FileExtensions.FBX: BlenderFileManager.__loadFbxScene(scene_file_path),
        }

    def importSceneFile(self, scene_file_path: str, file_type=FileExtensions.FBX):
        file_load_switcher = self.__getFileLoadSwitcher(scene_file_path)
        file_load_switcher.get(file_type, "Invalid file type to import")

    def importTextures(self, dir_context: DirectoryContext):
        texture_files = self.texture_file_pattern_context.getTextureFilesForDir(dir_context)
        self.scene_textures += texture_files
        return texture_files
