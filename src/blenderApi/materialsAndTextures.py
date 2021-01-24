import bpy


def getCurrentMaterialTextures(material_name, material_textures):
    print("do stuff")


def getSpecificMaterialTextures():


def applyTexturesForEachMaterial(textures_list):
    for material in bpy.data.materials:
        material_textures =  getSpecificMaterialTextures()
        getCurrentMaterialTextures(material.name, material_textures)