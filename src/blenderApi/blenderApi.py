import os

from src.blenderApi.SceneManager import SceneManager
from src.constants import paths
from src.utils.ioUtils import createDirectory


def processFbxFilesWithBlender(fbx_files, zip_dir_context):
    for fbx in fbx_files:
        dir_to_extract_processed_files = os.path.join(paths.exports_dir_path, fbx.file_name)
        createDirectory(dir_to_extract_processed_files)

        path_for_processed_fbx_textures = os.path.join(dir_to_extract_processed_files, 'textures')
        createDirectory(path_for_processed_fbx_textures)

        path_for_processed_fbx_file = os.path.join(dir_to_extract_processed_files, fbx.file_base)

        scene_manager = SceneManager(fbx)
        scene_manager.processAndExportImportedFile(
            zip_dir_context,
            path_for_processed_fbx_file,
            path_for_processed_fbx_textures
        )
