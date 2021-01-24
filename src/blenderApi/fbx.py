import bpy


def loadFbxScene(path_to_fbx_file):
    bpy.ops.import_scene.fbx(filepath=path_to_fbx_file)


def importFbxWithTextures(path_to_fbx, textures_list):
    loadFbxScene(path_to_fbx)
    applyTexturesForEachMaterial()