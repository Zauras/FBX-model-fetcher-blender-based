import bpy

from typing import List

from src.blenderApi.managers.BlenderFileManager import BlenderFileManager
from src.blenderApi.managers.MaterialShaderGraphManager import MaterialShaderGraphManager
from src.models.DirectoryContext import DirectoryContext
from src.models.FileMetadata import FileMetadata
from src.textureFiles.TextureFileMetadata import TextureFileMetadata
from src.textureFiles.TextureFilesManager import TextureFilesManager
from src.utils.validation import errorMessages


class SceneManager:
    @staticmethod
    def importScene(
            scene_file_path: str,
    ):
        SceneManager.__removeAllObjectsInScene()
        BlenderFileManager.importSceneFile(scene_file_path)

    @staticmethod
    def __removeAllObjectsInScene():
        for obj in bpy.data.objects:
            bpy.data.objects.remove(obj)

    @staticmethod
    def __deselectAllObjectsInScene():
        for obj in bpy.context.selected_objects:
            obj.select_set(False)

    @staticmethod
    def __applyCurrentTransformAsOriginToAllMeshObjects():
        SceneManager.__deselectAllObjectsInScene()

        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                obj.select_set(True)
                bpy.ops.object.transform_apply(location=True, scale=True, rotation=True)
                obj.select_set(False)

    def __init__(
            self,
            scene_file: FileMetadata = None,
            texture_file_name_pattern_context: TextureFilesManager = None
    ):
        self.file_manager = BlenderFileManager(texture_file_name_pattern_context)
        scene_file and self.importScene(scene_file.file_path)

    def processAndExportImportedFile(
            self,
            textures_dir_context: DirectoryContext,
            path_to_export_scene_file: str,  # C:/workspace/exports/MyScene/my_scene.fbx
            path_to_export_textures: str  # C:/workspace/exports/MyScene/textures
    ):
        self.__applySceneTexturesOnExistingMaterials(textures_dir_context, path_to_export_textures)
        SceneManager.__applyCurrentTransformAsOriginToAllMeshObjects()
        BlenderFileManager.exportSceneFile(path_to_export_scene_file)

    def __applySceneTexturesOnExistingMaterials(
            self,
            textures_dir_context: DirectoryContext,
            path_to_export_textures: str
    ):
        new_textures_files: List[TextureFileMetadata] = self.file_manager.importSceneTextures(textures_dir_context)

        if not bool(bpy.data.materials):
            print(errorMessages.no_material)
            return

        for material in bpy.data.materials:
            material_textures = BlenderFileManager.getMaterialTextureFiles(material, new_textures_files)
            exported_material_textures = TextureFilesManager.exportTextureFiles(path_to_export_textures,
                                                                                material_textures)
            material_shader_manager = MaterialShaderGraphManager(material)
            material_shader_manager.cleanlyApplyTextures(exported_material_textures)
