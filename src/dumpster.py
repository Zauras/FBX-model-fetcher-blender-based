# Import FBX
#bpy.ops.import_scene.fbx(filepath=yourFBXfilePath)

# if no materials associated with it
[]

# if it does have a material then it will display something like
[('Material', bpy.data.materials["Material"])]

obj = bpy.context.scene.objects.active
if len(obj.data.materials) == 0:
    newMat = bpy.data.materials.new('newmaterial')
    obj.data.materials.append(newMat)

mat = bpy.context.object.active_material
objs = []
for obj in bpy.data.objects:
    for slot in obj.material_slots:
        if slot.material == mat:
            objs.append(obj)

# Loads image from disk (1st line) or uses an image loaded (or generated) previously (2nd line).
myImg = bpy.data.images.load('C:/path/to/the/image.jpg')
myImg = bpy.data.images['image name.jpg']

# Sets the texture type to image
bpy.context.active_object.material_slots['Material'].material.texture_slots['Tex'].texture.type = 'IMAGE'
# Assigns the image to the texture
bpy.context.active_object.material_slots['Material'].material.texture_slots['Tex'].texture.image = myImg

# Similar to material_slot.material, there is a texture_slot.texture
# (I'm assuming Blender internal from the texture_slots.add in q)

mat = bpy.data.materials['Material']
tex = bpy.data.textures.new("SomeName", 'IMAGE')
slot = mat.texture_slots.add()
slot.texture = tex
# A simple example using Cycles can be found here https://blender.stackexchange.com/a/14115/15543


# for i, o in enumerate(bsdf.inputs):
# ...     i, o.name
# ...
# (0, 'Base Color')
# (1, 'Subsurface')
# (2, 'Subsurface Radius')
# (3, 'Subsurface Color')
# (4, 'Metallic')
# (5, 'Specular')
# (6, 'Specular Tint')
# (7, 'Roughness')
# (8, 'Anisotropic')
# (9, 'Anisotropic Rotation')
# (10, 'Sheen')
# (11, 'Sheen Tint')
# (12, 'Clearcoat')
# (13, 'Clearcoat Roughness')
# (14, 'IOR')
# (15, 'Transmission')
# (16, 'Transmission Roughness')
# (17, 'Emission')
# (18, 'Alpha')
# (19, 'Normal')
# (20, 'Clearcoat Normal')
# (21, 'Tangent')


#Script to add material, add vertex colour node, link it to base color of bsdf.

newmat = bpy.data.materials.new("VertCol")
newmat.use_nodes = True
node_tree = newmat.node_tree
nodes = node_tree.nodes

bsdf = nodes.get("Principled BSDF")
'''
# alternatively

output, bsdf = nodes
'''


assert(bsdf) # make sure it exists to continue

vcol = nodes.new(type="ShaderNodeVertexColor")
vcol.layer_name = "VColor" # the vertex color layer name

# make links

node_tree.links.new(vcol.outputs[0], bsdf.inputs[0])


# Good example: https://github.com/jbaicoianu/blender-scripts/blob/master/build-material-library.py