from enum import Enum


DEFAULT_PRINCIPAL_BSDF_NODE_NAME = "Principled BSDF"


class ShaderNodeTypes(Enum):
    OutputMaterial = 'ShaderNodeOutputMaterial'
    BsdfPrincipled = 'ShaderNodeBsdfPrincipled'
    TextureImage = 'ShaderNodeTexImage'
    NormalMap = 'ShaderNodeNormalMap'
