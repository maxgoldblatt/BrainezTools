import bpy

"""Defines Panel & ID Mask Manager Functions"""

# Define a PropertyGroup to hold object references
class ObjectReference(bpy.types.PropertyGroup):
    obj: bpy.props.PointerProperty(type=bpy.types.Object)  # Reference to the actual object

# Group property
class ObjectGroup(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Group Name", default="New Group", description="Name of the group")
    objects: bpy.props.CollectionProperty(type=ObjectReference)  # Store references to objects using ObjectReference

#Main Panel for ID Mask
class VIEW3D_PT_ObjectGroupsPanel(bpy.types.Panel):
    bl_label = "ID Mask Manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BrainezTools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Check if object_groups exists
        if not hasattr(scene, "object_groups"):
            return  # Prevent errors if the property is missing

        # Groups List
        row = layout.row()
        row.template_list("UI_UL_list", "object_groups", scene, "object_groups", scene, "object_groups_index")

        col = row.column(align=True)
        col.operator("object_group.add_group", text="", icon="ADD")
        col.operator("object_group.remove_group", text="", icon="REMOVE")

        # Group Name
        if scene.object_groups:
            group = scene.object_groups[scene.object_groups_index]
            layout.prop(group, "name", text="")

            # Grouped objects
            box = layout.box()
            box.label(text="Objects in Group:")
            for obj_ref in group.objects:
                row = box.row()
                row.label(text=obj_ref.obj.name)
                op = row.operator("object_group.remove_object", text="", icon="X")
                op.object_name = obj_ref.obj.name

            layout.operator("object_group.add_object", text="Add Selected Object")

            # ID Mask Controls for the Selected Group
            layout.separator()
            layout.label(text="ID Mask Controls:")

            row = layout.row()
            row.operator("idmask.apply_pass_index", icon='ADD', text="Apply Pass Index")
            row = layout.row()
            row.operator("idmask.reset_pass_index", icon='REMOVE', text="Reset Pass Index")
            layout.prop(scene, "id_mask_num", text="ID Mask Value")

# Operator to add a new group
class OBJECT_OT_AddGroup(bpy.types.Operator):
    bl_idname = "object_group.add_group"
    bl_label = "Add Object Group"
    bl_description = "Add a new group for objects"

    def execute(self, context):
        group = context.scene.object_groups.add()
        group.name = f"Group {len(context.scene.object_groups)}"
        context.scene.object_groups_index = len(context.scene.object_groups) - 1
        return {'FINISHED'}

# Operator to remove a group
class OBJECT_OT_RemoveGroup(bpy.types.Operator):
    bl_idname = "object_group.remove_group"
    bl_label = "Remove Object Group"
    bl_description = "Remove the selected group"

    def execute(self, context):
        scene = context.scene
        if scene.object_groups:
            index = scene.object_groups_index
            scene.object_groups.remove(index)
            scene.object_groups_index = max(0, index - 1)
        return {'FINISHED'}

# Operator to add an object to a group
class OBJECT_OT_AddObjectToGroup(bpy.types.Operator):
    bl_idname = "object_group.add_object"
    bl_label = "Add Object to Group"
    bl_description = "Add the selected object to the current group"

    def execute(self, context):
        scene = context.scene
        if scene.object_groups and context.object:
            group = scene.object_groups[scene.object_groups_index]
            obj = context.object
            # Create a new ObjectReference for the selected object and add it to the group
            for obj in context.selected_objects:
                obj_ref = group.objects.add()
                obj_ref.obj = obj
        return {'FINISHED'}

# Operator to remove an object from a group
class OBJECT_OT_RemoveObjectFromGroup(bpy.types.Operator):
    bl_idname = "object_group.remove_object"
    bl_label = "Remove Object from Group"
    bl_description = "Remove an object from the current group"

    object_name: bpy.props.StringProperty()

    def execute(self, context):
        scene = context.scene
        if scene.object_groups:
            group = scene.object_groups[scene.object_groups_index]
            for i, obj_ref in enumerate(group.objects):
                if obj_ref.obj.name == self.object_name:
                    group.objects.remove(i)
                    break
        return {'FINISHED'}

#ID Mask Functions
def reset_id_mask(group):
    """Resets the ID_MASK for objects in the given group"""
    for obj_ref in group.objects:
        obj = obj_ref.obj
        if obj.type in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'}:
            obj.pass_index = 0
            print(f"Changed {obj} ID Mask to: {0}")
        else:
            print(f"Did not change {obj} ID Mask. Invalid object.")
            
def apply_id_mask(group, id_mask_value):
    """Applies the ID_MASK to objects in the given group"""
    for obj_ref in group.objects:
        obj = obj_ref.obj
        if obj.type in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'}:
            obj.pass_index = id_mask_value
            print(f"Changed {obj} ID Mask to: {id_mask_value}")
        else:
            print(f"Did not change {obj} ID Mask. Invalid object.")

#Creating ID Mask Operator Classes
class ID_MASK_APPLY(bpy.types.Operator):
    """Applies the current ID MASK VALUE to the selected group of objects"""
    bl_idname = "idmask.apply_pass_index"
    bl_label = "Apply Pass Index"

    def execute(self, context):
        scene = context.scene
        if scene.object_groups:
            group = scene.object_groups[scene.object_groups_index]
            apply_id_mask(group, scene.id_mask_num)
        return {'FINISHED'}

class ID_MASK_RESET_PASS(bpy.types.Operator):
    """Resets the ID Mask Value for the selected group"""
    bl_idname = "idmask.reset_pass_index"
    bl_label = "Reset Pass Index"

    def execute(self, context):
        scene = context.scene
        if scene.object_groups:
            group = scene.object_groups[scene.object_groups_index]
            reset_id_mask(group)
        return {'FINISHED'}

#Property registration function
def register_properties():
    bpy.types.Scene.object_groups = bpy.props.CollectionProperty(type=ObjectGroup)
    bpy.types.Scene.object_groups_index = bpy.props.IntProperty()

def unregister_properties():
    del bpy.types.Scene.object_groups
    del bpy.types.Scene.object_groups_index

# List to store all classes
classes = [
    ObjectReference,
    ObjectGroup,
    VIEW3D_PT_ObjectGroupsPanel,
    OBJECT_OT_AddGroup,
    OBJECT_OT_RemoveGroup,
    OBJECT_OT_AddObjectToGroup,
    OBJECT_OT_RemoveObjectFromGroup,
    ID_MASK_APPLY,
    ID_MASK_RESET_PASS
]

#Register & Unregister Classes
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    register_properties()

    bpy.types.Scene.id_mask_num = bpy.props.IntProperty(
        name="My Integer",
        description="An adjustable integer",
        default=10,
        min=1,
        max=100,
    )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    unregister_properties()
    del bpy.types.Scene.id_mask_num