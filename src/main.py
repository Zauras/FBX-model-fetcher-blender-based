# Your team needs to automate the processing of FBX models.
# Write a tool, which performs the following operations on each:

# 1. Attach textures to any existing materials on mesh objects contained within. If an object doesn't have a material, it can be ignored. It's fine for a material not to have any textures.
#  - Texture files may be .png or .jpg
#  - The texture filename patterns and material properties to connect them to:
#    - Filename 'T_{fbxfilename}_{materialname}_BC' should be used as a Diffuse or Albedo map
#    - Filename 'T_{fbxfilename}_{materialname}_N' should be used as a Normal map
#    - Filename 'T_{fbxfilename}_{materialname}_O' should be used as an Opacity map
#  - Bonus points if the texture filename patterns can be configured

# 2. Reset the transforms of any mesh objects to origin (identity transform) without moving their geometry. Meshes are never animated, and they are never parented or bound to other objects. Any other object types should be ignored.

# 3. Reexport the FBX file and copy only the used textures to output. FBX settings are not important. Textures should be put in a subdirectory named 'textures', relative to the output FBX file.


# Input:

# List of download URLs in a text file. Each download is a single zip archive.
# Contents of each zip file: a single .fbx file and multiple .png or .jpg files for textures. All contained files are in a flat directory structure.

# Not all inputs are valid. The following edge cases need to be handled by reporting or logging them as errors:
#  - Input archive has no FBX file
#  - FBX file has no materials

# Problems with a single input item should never stop the entire batch process. User intervention should not be required during processing of a batch.


# Expected output:

# FBX files and their textures exported to a configurable location in the file system. 
# Each zip file should result in one output directory (named according to zip file) at target location.


# Other notes:

# You can choose to implement the solution using any of the following: Blender, 3dsmax, Maya, or FBX SDK.
# We prefer the solution to be written in Python or C++.

# Use of any additional technologies is up to you, but have in mind that the primary purpose of this assignment is to evaluate your coding skills.

# The interface is up to you, e.g. it can be a GUI or CLI, and it can be a standalone application or a scripted tool. Choose what you think is the appropriate solution.


# To run:  
# .\blender --background --python 2.91\scripts\addons\my_custom_fbx_processor\main.py

#python -m pip install requests
import requests, zipfile, io, os

print("Hello BLENDER")

with open('P4Output.txt', 'w') as f:
    f.write("test")

