import bpy


def doesObjContainsMaterials(blender_obj) -> bool:
    return not len(blender_obj.data.materials) == 0


# def applyTexturesForEachObjInScene(texture_list):
#     for obj in bpy.data.objects:
#         if doesObjContainsMaterials(obj):
#             getCurrentMaterialTextures(material_name, texture_list)


def getAllObjectsInScene():
    for obj in bpy.data.objects:
        print(obj.name)
        try:
            print("removed material from " + obj.name)
        except:
            print(obj.name + " does not have materials.")


def loadImageToBlender(path_to_img):
    return bpy.data.images.load(path_to_img)


def getActiveObjectInScene():
    return bpy.context.scene.objects.active

    # Apply .png/.jpg to nodes

    # TODO: check if has png/jpg files with pattern

    # Texture maps identifiers
    # TODO use enums:
    albedo_map_identifier = "BC"
    normal_map_identifier = "N"
    opacity_map_identifier = "O"

    texture_identifier = 'T'
    fbx_filename = ''
    material_name = ''
    texture_map_identifier = albedo_map_identifier

    texture_pattern = f"{texture_identifier}_{fbx_filename}_{material_name}_TMI"

    image_filenames = getImageFilesFromDir(downloads_dir_path)

    # TODO: load textures for each material of fbx file:

    # if fnmatch.fnmatch(file,
    #         f"{texture_identifier}"
    #         f"_*_*_"
    #         f"[{albedo_map_identifier}, {normal_map_identifier}, {opacity_map_identifier}]"
    # ):

    # Map principal shader with imported nodes

    # Export only .fbx with material and used textures

# Contents of each zip file: a single .fbx file and multiple .png or .jpg files for textures.
# All contained files are in a flat directory structure.
