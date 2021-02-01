import bpy

from typing import List

from src.models.DirectoryContext import DirectoryContext
from src.models.textureFiles.TextureFileMetadata import TextureFileMetadata
from src.models.textureFiles.TextureFilesManager import TextureFilesManager
from src.constants.FileExtensions import FileExtensions


class BlenderFileManager:
    @staticmethod
    def getMaterialTextureFiles(material, textures_files):
        material_textures_list = [texture_metadata for texture_metadata in textures_files
                                  if texture_metadata.material_name == material.name]
        return material_textures_list

    @staticmethod
    def importSceneFile(scene_file_path: str, file_type=FileExtensions.FBX):
        file_import_by_type_switcher = {
            FileExtensions.FBX: BlenderFileManager.__importFbx(scene_file_path),
        }
        file_import_by_type_switcher.get(file_type, "Invalid file type to import")

    @staticmethod
    def exportSceneFile(path_to_export_scene_file: str, file_type=FileExtensions.FBX, use_selection=False):
        file_export_by_type_switcher = {
            FileExtensions.FBX: BlenderFileManager.__exportFbx(path_to_export_scene_file, use_selection),
        }
        file_export_by_type_switcher.get(file_type, "Invalid file type to export")

    @staticmethod
    def __importFbx(path_to_fbx_file):
        bpy.ops.import_scene.fbx(filepath=path_to_fbx_file)

    @staticmethod
    def __exportFbx(path_to_fbx_file, use_selection=False):
        bpy.ops.export_scene.fbx(filepath=path_to_fbx_file, use_selection=use_selection)

    def __init__(
            self,
            texture_file_pattern_context: TextureFilesManager = None,
    ):
        self.texture_file_pattern_context = texture_file_pattern_context if bool(texture_file_pattern_context) \
            else TextureFilesManager()
        self.scene_textures: List[TextureFileMetadata] = []

    def importSceneTextures(self, dir_context: DirectoryContext) -> List[TextureFileMetadata]:
        texture_files = self.texture_file_pattern_context.getTextureFilesForDir(dir_context)
        self.scene_textures += texture_files
        return texture_files
