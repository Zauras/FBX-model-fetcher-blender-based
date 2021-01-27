import bpy




def importFbxWithTextures(path_to_fbx, textures_list):
    loadFbxScene(path_to_fbx)
    applyTexturesForEachMaterial()