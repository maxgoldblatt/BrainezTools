bl_info = {
    "name": "BrainezTools",
    "author": "Max Goldblatt",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Brainez Tools",
    "description": "Collection of tools for Blender intended to speed up various 3D workflows. Created by Brainez Visuals / Max Goldblatt",
    "category": "Material"
}

import bpy


from . import BrainezCam
from . import IDMaskManger


# Register / Unregister
def register():
    BrainezCam.register()
    IDMaskManger.register()

def unregister():
    BrainezCam.unregister()
    IDMaskManger.unregister()

if __name__ == "__main__":
    register()