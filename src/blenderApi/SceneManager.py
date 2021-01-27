import bpy

from src.blenderApi.BlenderFileManager import BlenderFileManager
from src.models.DirectoryContext import DirectoryContext
from src.models.textureFiles.TextureFilesManager import TextureFilesManager


class SceneManger:
    def __init__(
            self,
            texture_file_name_pattern_context: TextureFilesManager = None,
            scene_file_path: str = None
    ):
        self.file_manager = BlenderFileManager(texture_file_name_pattern_context)
        scene_file_path and self.importScene(scene_file_path)

    def importScene(
            self,
            scene_file_path: str,
    ):
        self.file_manager.importSceneFile(scene_file_path)

    def loadAndApplyTexturesOnExistingMaterials(self, textures_dir_context: DirectoryContext):
        new_textures_files = self.file_manager.importTextures(textures_dir_context)
        bpy.data.images['your_image.png'].pack()

        # TODO: creade

        # Create a material
        material = bpy.data.materials.new(name="Example_Material")
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        # Reuse the material output node that is created by default
        material_output = nodes.get("Material Output")

        # Create Image Texture node and load the displacement texture.
        # You need to add the actual path to the texture.
        displacement_tex = nodes.new("ShaderNodeTexImage")
        displacement_tex.image = bpy.data.images.load("/path/to/your/texture")
        displacement_tex.image.colorspace_settings.name = "Non-Color"

        # Create the Displacement node
        displacement = nodes.new("ShaderNodeDisplacement")

        # Create the Texture Coordinate node
        tex_coordinate = nodes.new("ShaderNodeTexCoord")

        # Connect the Texture Coordinate node to the displacement texture.
        # This uses the active UV map of the object.
        links.new(displacement_tex.inputs["Vector"], tex_coordinate.outputs["UV"])

        # Connect the displacement texture to the Displacement node
        links.new(displacement.inputs["Height"], displacement_tex.outputs["Color"])

        # Connect the Displacement node to the Material Output node
        links.new(material_output.inputs["Displacement"], displacement.outputs["Displacement"])

        # Get the active object
        active_obj = bpy.context.view_layer.objects.active

        # Check if the active object has a material slot, create one if it doesn't.
        # Assign the material to the first slot for the active object.
        if active_obj.material_slots:
            active_obj.material_slots[0].material = material
        else:
            active_obj.material_slots.append(material)
