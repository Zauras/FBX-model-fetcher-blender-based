from typing import Tuple

import bpy

from src.blenderApi.constants.ShaderNodes import ShaderNodeTypes, DEFAULT_PRINCIPAL_BSDF_NODE_NAME
from src.blenderApi.models.MaterialContext import MaterialContext
from src.constants.TextureMapType import TextureMapType
from src.models.Coordinates2D import Coordinates2D
from src.models.textureFiles.TextureFileMetadata import TextureFileMetadata


class MaterialShaderGraphManager:
    @staticmethod
    def getDefaultShaderNodeCoordinates(shader_node_type: ShaderNodeTypes):
        node_initialize_switcher = {
            ShaderNodeTypes.OutputMaterial: Coordinates2D(400.0, 0.0),
            ShaderNodeTypes.BsdfPrincipled: Coordinates2D(0.0, 0.0),
            ShaderNodeTypes.TextureImage: Coordinates2D(-200.0, -300.0),
            ShaderNodeTypes.NormalMap: Coordinates2D(-500.0, -250.0),
        }
        return node_initialize_switcher.get(shader_node_type, "Invalid shader node type")

    def __init__(
            self,
            material,
    ):
        material.use_nodes = True
        self.material_context = MaterialContext(material)
        self.node_principled_bsdf = self.__getNodeByName(DEFAULT_PRINCIPAL_BSDF_NODE_NAME)

    def __getNodeByName(self, node_name):
        return self.material_context.nodes.get(node_name)

    def __cleanMaterialsShaderGraph(self):
        material_nodes = self.material_context.nodes
        for shader_node in material_nodes:
            material_nodes.remove(shader_node)

    def reInitializeShaderGraphForMaterial(self):
        self.material_context.material.use_nodes = True

        self.__cleanMaterialsShaderGraph()

        node_material_output = self.addShaderNode(ShaderNodeTypes.OutputMaterial)
        self.node_principled_bsdf = self.addShaderNode(ShaderNodeTypes.BsdfPrincipled)

        self.__linkShaderNodes(node_material_output.inputs['Surface'], self.node_principled_bsdf.outputs['BSDF'])

    def __linkShaderNodes(self, node_input, node_output):
        self.material_context.node_links.new(node_input, node_output)

    def addShaderNode(self, shader_node_type: ShaderNodeTypes, coordinates_2d=None):
        shader_node = self.material_context.nodes.new(type=shader_node_type.value)

        if not coordinates_2d: coordinates_2d = self.getDefaultShaderNodeCoordinates(shader_node_type)
        shader_node.location = coordinates_2d.x, coordinates_2d.y
        return shader_node

    def addTextureByType(self, texture_map_type: TextureMapType, texture_image_path: str):
        texture_map_switcher = {
            TextureMapType.Base_Color: self.addBaseColorTexture(texture_image_path),
            TextureMapType.Normal: self.addNormalTexture(texture_image_path),
            TextureMapType.Opacity: self.addOpacityTexture(texture_image_path),
        }
        return texture_map_switcher.get(texture_map_type, "Invalid texture map type")

    def createImageTexture(self, texture_image_path: str):
        node_texture = self.addShaderNode(ShaderNodeTypes.TextureImage)
        node_texture.image = bpy.data.images.load(texture_image_path)
        return node_texture

    def addBaseColorTexture(self, texture_image_path: str):
        node_texture_image = self.createImageTexture(texture_image_path)

        self.__linkShaderNodes(
            self.node_principled_bsdf.inputs['Base Color'],
            node_texture_image.outputs['Color']
        )
        return node_texture_image

    def addOpacityTexture(self, texture_image_path: str):
        node_texture_image = self.createImageTexture(texture_image_path)

        self.__linkShaderNodes(self.node_principled_bsdf.inputs['Alpha'], node_texture_image.outputs['Color'])
        return node_texture_image

    def addNormalTexture(self, texture_image_path: str):
        node_texture_image = self.createImageTexture(texture_image_path)
        node_normal_map = self.addShaderNode(ShaderNodeTypes.NormalMap)

        self.__linkShaderNodes(self.node_principled_bsdf.inputs['Normal'], node_normal_map.outputs['Normal'])
        self.__linkShaderNodes(node_normal_map.inputs['Color'], node_texture_image.outputs['Color'])

        return node_texture_image

    def cleanlyApplyTextures(self, texture_files: Tuple[TextureFileMetadata]):
        self.reInitializeShaderGraphForMaterial()

        for texture_metadata in texture_files:
            texture_map_type = texture_metadata.texture_map
            texture_image_path = texture_metadata.file_metadata.file_path

            self.addTextureByType(texture_map_type, texture_image_path)
