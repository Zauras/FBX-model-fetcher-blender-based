# FBX-model-fetcher-blender-based
CLI app to fetch fbx models and apply material with textures, based on headless blender client.

Execute script with headless Blender:
  Run in CLI: [path to blender executable] --backgroun --python src/main.py
  (Example: F:\Programs\Blender2.91\blender --background --python src/main.py)

Funcionality:
  * import FBX files to process:
    > import .zip files to ~./resources/imports
    OR
    >  give path to .txt file which contains urls to download .zip's
    
  * Texture file pattern can be customized through CLI guide in process
  * Applies Base Color, Normal and Opacity textures to materials depending on texture file pattern
  * Resets mesh objects identity without changing geometry
  * Exports .fbx and textures to ~./exports

Prerequisites:
  *  >=Blender 2.8
  
Tested on Windows 10 with Blender 2.9

