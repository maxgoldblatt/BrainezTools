import bpy

"""Defines Custom Camera Preset w/ limits & paserpout enabled. Can Access via Shift A > Add Menu > Brainez Camera"""

def create_custom_cam(self, context):
    """Creates Custom Camera with passepartout presets @ Viewport location"""
    
    # Creates Camera. Implement while loop to create a proper name & ensure no override of data. May be redundant but it works.
    cam_name_number = 0
    while True:
        try:
            cam_data = bpy.data.cameras.new(f"Camera{cam_name_number}")
            cam_obj = bpy.data.objects.new(f"Camera{cam_name_number}", cam_data)
            bpy.context.scene.collection.objects.link(cam_obj)
            break
        except:
            cam_name_number += 1
    
    # Set Camera as active camera
    bpy.context.scene.camera = cam_obj

    # Set Passerpout
    cam_obj.data.show_passepartout = True
    cam_obj.data.passepartout_alpha = 1.0

    # Show Limits
    cam_obj.data.show_limits = True

    # Make Active
    bpy.ops.object.select_all(action='DESELECT')
    cam_obj.select_set(True)
    bpy.context.view_layer.objects.active = cam_obj
    
    # Activate and align viewport camera
    bpy.ops.view3d.camera_to_view()


class OBJECT_OT_AddCustomCam(bpy.types.Operator):
    """Class for Creating Custom Camera w/ Passapout enabled and @ current location"""
    bl_idname = "object.add_custom_camera"
    bl_label = "Brainez Camera"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add a Camera at the Current View Angle with Passerpaout" #tooltip


    def execute(self, context):
        create_custom_cam(self, context)
        return {'FINISHED'}

 
# Registration
def add_camera_button(self, context):
    self.layout.operator(
        OBJECT_OT_AddCustomCam.bl_idname,
        text="Brainez Camera",
        icon='VIEW_CAMERA')


def register():
    bpy.utils.register_class(OBJECT_OT_AddCustomCam)
    bpy.types.VIEW3D_MT_add.append(add_camera_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_AddCustomCam)
    bpy.types.VIEW3D_MT_add.remove(add_camera_button)