import bpy

from src.models.textureFiles.importModelProcessContext import ImportModelProcessContext


def getCurrentMaterialTextures(material_name, material_textures):
    print("do stuff")


def getSpecificMaterialTextures(process_context: ImportModelProcessContext, material_name, textures_list):


def applyTexturesForEachMaterial(process_context: ImportModelProcessContext, textures_list, texture_filename_pattern):
    # each material in the scene
    for material in bpy.data.materials:
        material_textures = getSpecificMaterialTextures(process_context, material.name, textures_list)
        getCurrentMaterialTextures(material.name, material_textures)
