bl_info = {
    "name": "Brainez Toolkit & ID Mask Manager",
    "blender": (4, 0, 1),
    "category": "3D View",
    "version": (1, 0, 0),
    "description": "Set of tools created by Brainez Visuals | Max Goldblatt. Includes ID Mask Manager, VALORANT Weapon Shader Creator, & VALORANT Character Shader Creator.",
}

import bpy

def new_charmat():
    """Creates new material on the selected object and selected material slot"""
    global charshader
    global principled_bsdf_node
    # New material
    charshader = bpy.data.materials.new(name="Valorant_Character_Shader")
    charshader.use_nodes = True
    principled_bsdf_node = charshader.node_tree.nodes["Principled BSDF"]
    
    #Apply Material
    obj = bpy.context.active_object
    # Ensure the object has material slots
    if obj.material_slots:
        # Assign the new material to the active material slot
        obj.material_slots[obj.active_material_index].material = charshader
    else:
        # Add a new material slot and assign the new material if no slots exist
        obj.data.materials.append(charshader)
    return charshader
    return principled_bsdf_node

# Global variables to hold nodes
normal_map_node = None
color_ramp_ao = None
color_ramp_emit = None
AEM_seperate = None

def add_normal_map():
    """Adds Valorant Normal Map setup to material"""
    global normal_map_node  # Declare it as global to modify the global variable
    node_location_x_step = 200
    current_node_location_x = -node_location_x_step - 800
    y_location = -600

    # Create Normal Map Node
    normal_map_node = charshader.node_tree.nodes.new(type="ShaderNodeNormalMap")
    normal_map_node.location.x = current_node_location_x
    current_node_location_x -= node_location_x_step
    normal_map_node.location.y = y_location

    # Create CombineRGB Node
    combine_RGB_Node = charshader.node_tree.nodes.new(type="ShaderNodeCombineRGB")
    combine_RGB_Node.location.x = current_node_location_x
    current_node_location_x -= node_location_x_step
    combine_RGB_Node.location.y = y_location

    # Create Invert Node
    invert_Node = charshader.node_tree.nodes.new(type="ShaderNodeInvert")
    invert_Node.location.x = current_node_location_x
    current_node_location_x -= node_location_x_step
    invert_Node.location.y = y_location

    # Create SeparateRGB Node
    separate_RGB_Node = charshader.node_tree.nodes.new(type="ShaderNodeSeparateRGB")
    separate_RGB_Node.location.x = current_node_location_x
    current_node_location_x -= node_location_x_step
    separate_RGB_Node.location.y = y_location - 25

    # Create Image Texture
    image_tex = charshader.node_tree.nodes.new(type="ShaderNodeTexImage")
    image_tex.location.x = current_node_location_x - 300
    image_tex.location.y = y_location
    image_tex.label = "Normal"
    
    #############################################################################
    
    # LINKS
    # Link R SeparateRGB node to R CombineRGB Node
    charshader.node_tree.links.new(separate_RGB_Node.outputs["R"],
                                    combine_RGB_Node.inputs["R"])
    # Link G SeparateRGB node to Invert Node
    charshader.node_tree.links.new(separate_RGB_Node.outputs["G"],
                                    invert_Node.inputs["Color"])
    # Link Invert Node to G CombineRGB Node
    charshader.node_tree.links.new(invert_Node.outputs["Color"],
                                   combine_RGB_Node.inputs["G"])
    # Link B SeparateRGB node to B CombineRGB Node
    charshader.node_tree.links.new(separate_RGB_Node.outputs["B"],
                                    combine_RGB_Node.inputs["B"])
    # Link CombineRGB Node to Normal Map
    charshader.node_tree.links.new(combine_RGB_Node.outputs["Image"],
                                    normal_map_node.inputs["Color"])
    # Link Normal to Normal
    charshader.node_tree.links.new(normal_map_node.outputs["Normal"],
                                   principled_bsdf_node.inputs["Normal"])
    # Link Image Node to Separate RGB
    charshader.node_tree.links.new(image_tex.outputs["Color"],
                                   separate_RGB_Node.inputs["Image"])

def mrae_splitter():
    """Creates MRAE Texture setup"""
    global color_ramp_ao
    global color_ramp_emit
    node_location_x_step = 200
    current_node_location_x = -node_location_x_step - 900
    y_location = 200

    # Create Color Ramp, Emit Mask
    color_ramp_emit = charshader.node_tree.nodes.new(type="ShaderNodeValToRGB")
    color_ramp_emit.label = "Emit Mask"
    color_ramp_emit.color_ramp.elements[0].position = 0.55
    color_ramp_emit.color_ramp.elements[1].position = 0.659091
    color_ramp_emit.location.x = current_node_location_x - 100
    color_ramp_emit.location.y = y_location - 50

    # Create Color Ramp, AO Mask
    color_ramp_ao = charshader.node_tree.nodes.new(type="ShaderNodeValToRGB")
    color_ramp_ao.label = "AO Mask"
    color_ramp_ao.color_ramp.elements[0].position = 0.286364
    color_ramp_ao.color_ramp.elements[1].position = 0.555
    color_ramp_ao.location.x = current_node_location_x - 100
    current_node_location_x -= node_location_x_step + 100
    color_ramp_ao.location.y = y_location + 250

    # Create SeparateRGB
    separate_RGB_Node = charshader.node_tree.nodes.new(type="ShaderNodeSeparateRGB")
    separate_RGB_Node.location.x = current_node_location_x
    current_node_location_x -= node_location_x_step
    separate_RGB_Node.location.y = y_location

    # Create Gamma Node
    #gamma_node = charshader.node_tree.nodes.new(type="ShaderNodeGamma")
    #gamma_node.location.x = current_node_location_x
    #current_node_location_x -= node_location_x_step
    #gamma_node.location.y = y_location
    #gamma_node.inputs[1].default_value = 0.450

    # Create Image Tex
    image_tex = charshader.node_tree.nodes.new(type="ShaderNodeTexImage")
    image_tex.location.x = current_node_location_x - 300
    image_tex.location.y = y_location
    image_tex.label = "MRAE"
    
    #############################################################################
    
    # LINKS
    # Link R to Metallic
    charshader.node_tree.links.new(separate_RGB_Node.outputs["R"],
                                   principled_bsdf_node.inputs[1])
    # Link G to Emit
    charshader.node_tree.links.new(separate_RGB_Node.outputs["G"],
                                   color_ramp_emit.inputs[0])
    # Link G to AO
    charshader.node_tree.links.new(separate_RGB_Node.outputs["G"],
                                   color_ramp_ao.inputs[0])
    # Link Blue to Rough
    charshader.node_tree.links.new(separate_RGB_Node.outputs["B"],
                                   principled_bsdf_node.inputs[2])
    # Links Gamma to SeparateRGB
    #charshader.node_tree.links.new(gamma_node.outputs["Color"],
                                   #separate_RGB_Node.inputs["Image"])
    # Link Image Tex to Gamma
    charshader.node_tree.links.new(image_tex.outputs["Color"],
                                   separate_RGB_Node.inputs["Image"])

def diffuse_tex():
    """Creates Normal and Emmision Setup"""
    global normal_map_node
    global color_ramp_ao
    global color_ramp_emit
    node_location_x_step = 200
    current_node_location_x = -node_location_x_step - 300
    y_location = 900

    # Create Highlights
    highlight_add = charshader.node_tree.nodes.new(type="ShaderNodeMixRGB")
    highlight_add.blend_type = "DODGE"
    highlight_add.label = "Add Highlights"
    highlight_add.inputs['Fac'].default_value = 1.0
    highlight_add.location.x = current_node_location_x
    highlight_add.location.y = y_location - 100
    current_node_location_x -= node_location_x_step

    # Create AO Multiply
    ao_mix = charshader.node_tree.nodes.new(type="ShaderNodeMixRGB")
    ao_mix.blend_type = "MULTIPLY"
    ao_mix.label = "AO_Mult"
    ao_mix.inputs['Fac'].default_value = 1.0
    ao_mix.use_clamp = 1
    ao_mix.location.x = current_node_location_x
    ao_mix.location.y = y_location
    current_node_location_x -= node_location_x_step

    # Create Image Tex
    image_tex = charshader.node_tree.nodes.new(type="ShaderNodeTexImage")
    image_tex.location.x = current_node_location_x - 1300
    image_tex.location.y = y_location + 300
    image_tex.label = "Diffuse"

    # Create Ambient Occlusion
    ao_node = charshader.node_tree.nodes.new(type="ShaderNodeAmbientOcclusion")
    ao_node.samples = 1
    ao_node.location.x = -1000
    ao_node.location.y = -350

    # Create Mix AO Node
    mix_aos = charshader.node_tree.nodes.new(type="ShaderNodeMixRGB")
    mix_aos.blend_type = "MULTIPLY"
    mix_aos.label = "Mix AOs"
    mix_aos.use_clamp = 1
    mix_aos.inputs['Fac'].default_value = 1.0
    mix_aos.location.x = -850
    mix_aos.location.y = -300

    # Create Gamma Node
    gamma_node = charshader.node_tree.nodes.new(type="ShaderNodeGamma")
    gamma_node.location.x = -700
    gamma_node.location.y = -200
    
    # Create Attribute Node
    col_attribute = charshader.node_tree.nodes.new(type="ShaderNodeVertexColor")
    col_attribute.location.x = -2100
    col_attribute.location.y = 700
    
    # Create Seperate Color Node
    separate_RGB_Node = charshader.node_tree.nodes.new(type="ShaderNodeSeparateRGB")
    separate_RGB_Node.location.x = -1800
    separate_RGB_Node.location.y = 700
    
    # Create Highlights Invert Node
    highlight_i = charshader.node_tree.nodes.new(type="ShaderNodeInvert")
    highlight_i.label = "Highlights"
    highlight_i.location.x = -1600
    highlight_i.location.y = 750
    
    # Create Emmision Multiply Node
    emit_mult = charshader.node_tree.nodes.new(type="ShaderNodeMixRGB")
    emit_mult.blend_type = "MULTIPLY"
    emit_mult.label = "Emission Mask"
    emit_mult.inputs['Fac'].default_value = 1.0
    emit_mult.location.x = -600
    emit_mult.location.y = 0
    
    # Create AO Strength
    ao_strength = charshader.node_tree.nodes.new(type="ShaderNodeValue")
    ao_strength.label = "AO Strength"
    ao_strength.location.x = -2100
    ao_strength.location.y = 900
    ao_strength.outputs[0].default_value = 0
    
    # Create Highlights Strength
    h_strength = charshader.node_tree.nodes.new(type="ShaderNodeValue")
    h_strength.label = "Highlights Strength"
    h_strength.location.x = -2100
    h_strength.location.y = 800
    h_strength.outputs[0].default_value = 0
    
    # Create Emmision Strength
    e_strength = charshader.node_tree.nodes.new(type="ShaderNodeValue")
    e_strength.label = "Emmission Strength"
    e_strength.location.x = -2100
    e_strength.location.y = 985
    e_strength.outputs[0].default_value = 0
    
    # Create Normal Strength
    n_strength = charshader.node_tree.nodes.new(type="ShaderNodeValue")
    n_strength.label = "Normal Strength"
    n_strength.location.x = -2100
    n_strength.location.y = 550
    n_strength.outputs[0].default_value = 1
    
    
    
    #############################################################################
    
    # Link Normal Map to AO
    if normal_map_node:  # Check if normal_map_node is available
        charshader.node_tree.links.new(normal_map_node.outputs["Normal"],
                                       ao_node.inputs["Normal"])

    # Link AO to Mix AOs
    charshader.node_tree.links.new(ao_node.outputs["Color"],
                                       mix_aos.inputs["Color2"])
    # Link AO_Mask to AOs
    if color_ramp_ao:  # Ensure color_ramp_ao is available
        charshader.node_tree.links.new(color_ramp_ao.outputs["Color"],
                                       mix_aos.inputs["Color1"])
                                       
    # Link MixAOs to Gamma Node
    charshader.node_tree.links.new(mix_aos.outputs["Color"],
                                      gamma_node.inputs["Color"])
                                       
    # Link Gamma to AO_mult
    charshader.node_tree.links.new(gamma_node.outputs["Color"],
                                       ao_mix.inputs["Color2"])
                                       
    # Link Diffuse to AO_mult
    charshader.node_tree.links.new(image_tex.outputs["Color"],
                                       ao_mix.inputs["Color1"])
                                       
    # Link Color Attribute to Seperate RGB
    charshader.node_tree.links.new(col_attribute.outputs["Color"],
                                       separate_RGB_Node.inputs["Image"])
    
    # Link Seperate RGB R to Highlights
    charshader.node_tree.links.new(separate_RGB_Node.outputs["R"],
                                       highlight_i.inputs["Color"])
    
    # Link Highlights Invert to Highlights Mix      
    charshader.node_tree.links.new(highlight_i.outputs["Color"],
                                    highlight_add.inputs["Color2"])
   
    # Link AO_Mix to Highlights Mix
    charshader.node_tree.links.new(ao_mix.outputs["Color"],
                                    highlight_add.inputs["Color1"])
    
    # Link Add Highlgihts to Principled BSDF                
    charshader.node_tree.links.new(highlight_add.outputs["Color"],
                                principled_bsdf_node.inputs[0])
                                
    # Link Emmission Mask to Emit Mult
    charshader.node_tree.links.new(color_ramp_emit.outputs["Color"],
                                       emit_mult.inputs["Color2"])   
                                       
    # Link Diffuse to Emit Mult
    charshader.node_tree.links.new(image_tex.outputs["Color"],
                                       emit_mult.inputs["Color1"])
    
    # Link Emit Mask to BSDF
    charshader.node_tree.links.new(emit_mult.outputs["Color"],
                                principled_bsdf_node.inputs[26])


    # Link AO Strength  
    charshader.node_tree.links.new(ao_strength.outputs["Value"],
                                ao_mix.inputs["Fac"])
    # Link Highlights Strength    
    charshader.node_tree.links.new(h_strength.outputs["Value"],
                                highlight_add.inputs["Fac"])
    # Link Emmission Strength
    charshader.node_tree.links.new(e_strength.outputs["Value"],
                                principled_bsdf_node.inputs[27])
    # Link Normal Strength  
    charshader.node_tree.links.new(n_strength.outputs["Value"],
                                normal_map_node.inputs["Strength"])

def new_weaponmat():
    global weaponshader
    global principled_bsdf_node
    # New material
    weaponshader = bpy.data.materials.new(name="Valorant_Weapon_Shader")
    weaponshader.use_nodes = True
    principled_bsdf_node = weaponshader.node_tree.nodes["Principled BSDF"]
    
    #Apply Material
    obj = bpy.context.active_object
    # Ensure the object has material slots
    if obj.material_slots:
        # Assign the new material to the active material slot
        obj.material_slots[obj.active_material_index].material = weaponshader
    else:
        # Add a new material slot and assign the new material if no slots exist
        obj.data.materials.append(weaponshader)
    return weaponshader
    return principled_bsdf_node

def add_weapon_normal_map():
    """Creates Normal Map Setup for Weapon Shader"""
    global normal_map_node  # Declare it as global to modify the global variable 
    node_location_x_step = 200
    current_node_location_x = -node_location_x_step - 100
    y_location = -100
    
    # Create Normal Map Node
    normal_map_node = weaponshader.node_tree.nodes.new(type="ShaderNodeNormalMap")
    normal_map_node.location.x = current_node_location_x
    current_node_location_x -= node_location_x_step
    normal_map_node.location.y = y_location
    
    # Create CombineRGB Node
    combine_RGB_Node = weaponshader.node_tree.nodes.new(type="ShaderNodeCombineRGB")
    combine_RGB_Node.location.x = current_node_location_x
    current_node_location_x -= node_location_x_step
    combine_RGB_Node.location.y = y_location

    # Create Invert Node
    invert_Node = weaponshader.node_tree.nodes.new(type="ShaderNodeInvert")
    invert_Node.location.x = current_node_location_x
    current_node_location_x -= node_location_x_step
    invert_Node.location.y = y_location

    # Create SeparateRGB Node
    separate_RGB_Node = weaponshader.node_tree.nodes.new(type="ShaderNodeSeparateRGB")
    separate_RGB_Node.location.x = current_node_location_x
    current_node_location_x -= node_location_x_step
    separate_RGB_Node.location.y = y_location - 25

    # Create Image Texture
    image_tex = weaponshader.node_tree.nodes.new(type="ShaderNodeTexImage")
    image_tex.location.x = current_node_location_x - 200
    image_tex.location.y = y_location
    image_tex.label = "Normal"

    #############################################################################
    
    # LINKS
    # Link R SeparateRGB node to R CombineRGB Node
    weaponshader.node_tree.links.new(separate_RGB_Node.outputs["R"],
                                    combine_RGB_Node.inputs["R"])
    # Link G SeparateRGB node to Invert Node
    weaponshader.node_tree.links.new(separate_RGB_Node.outputs["G"],
                                    invert_Node.inputs["Color"])
    # Link Invert Node to G CombineRGB Node
    weaponshader.node_tree.links.new(invert_Node.outputs["Color"],
                                   combine_RGB_Node.inputs["G"])
    # Link B SeparateRGB node to B CombineRGB Node
    weaponshader.node_tree.links.new(separate_RGB_Node.outputs["B"],
                                    combine_RGB_Node.inputs["B"])
    # Link CombineRGB Node to Normal Map
    weaponshader.node_tree.links.new(combine_RGB_Node.outputs["Image"],
                                    normal_map_node.inputs["Color"])
    # Link Normal to Normal
    weaponshader.node_tree.links.new(normal_map_node.outputs["Normal"],
                                   principled_bsdf_node.inputs["Normal"])
    # Link Image Node to Separate RGB
    weaponshader.node_tree.links.new(image_tex.outputs["Color"],
                                   separate_RGB_Node.inputs["Image"])

def MRS():
    """Creates MRS Tex Setup for Weapon Shader"""
    node_location_x_step = 200
    current_node_location_x = -node_location_x_step - 600
    y_location = 200
    
    #Creates Seperate RGB Node for MRS Shader
    separate_RGB_Node = weaponshader.node_tree.nodes.new(type="ShaderNodeSeparateRGB")
    separate_RGB_Node.location.x = current_node_location_x
    current_node_location_x -= node_location_x_step
    separate_RGB_Node.location.y = y_location - 25
    separate_RGB_Node.label = "MRS Seperation"
    
    
    #Creates Image Texture for MRS Texture
    image_tex = weaponshader.node_tree.nodes.new(type="ShaderNodeTexImage")
    image_tex.location.x = current_node_location_x - 200
    image_tex.location.y = y_location
    image_tex.label = "MRS Texture"
     
    
    #LINKS
    #Links R to Metallic
    weaponshader.node_tree.links.new(separate_RGB_Node.outputs["R"],
                                    principled_bsdf_node.inputs[1])
    #Links G to Roughness
    weaponshader.node_tree.links.new(separate_RGB_Node.outputs["G"],
                                    principled_bsdf_node.inputs[2])
    #Links B to Specular
    #Links B to Specular
    weaponshader.node_tree.links.new(separate_RGB_Node.outputs["B"],
                                    principled_bsdf_node.inputs[12])
                                    
    #Links Image Tex to Seperate RGB
    weaponshader.node_tree.links.new(image_tex.outputs["Color"],
                                    separate_RGB_Node.inputs[0])

def weaponDiffuse():
    """Creates AEM & Diffuse Setup for Weapon Shader"""
    global AEM_seperate
    global weapon_diffuse_tex
    node_location_x_step = 200
    current_node_location_x = -node_location_x_step - 100
    y_location = 400
    
    #Creates MIXRGB Node for the AEM AO and the Diffuse Texture
    ao_mult = weaponshader.node_tree.nodes.new(type="ShaderNodeMixRGB")
    ao_mult.blend_type = "MULTIPLY"
    ao_mult.label = "AO Mult"
    ao_mult.inputs['Fac'].default_value = 1.0
    ao_mult.location.x = current_node_location_x
    ao_mult.location.y = y_location
     
    #Creates SeperateRGB Node for the AEM texture
    AEM_seperate = weaponshader.node_tree.nodes.new(type="ShaderNodeSeparateRGB")
    AEM_seperate.location.x = current_node_location_x - 300
    current_node_location_x -=  node_location_x_step
    AEM_seperate.location.y = y_location - 50
    AEM_seperate.label = "AEM Seperation"
    
    
    #Creates AEM Texture Node
    aem_tex = weaponshader.node_tree.nodes.new(type="ShaderNodeTexImage")
    aem_tex.location.x = current_node_location_x - 500
    aem_tex.location.y = y_location
    aem_tex.label = "AEM Texture"
    
    #Creates DiffuseTexture Node
    weapon_diffuse_tex = weaponshader.node_tree.nodes.new(type="ShaderNodeTexImage")
    weapon_diffuse_tex.location.x = current_node_location_x - 500
    weapon_diffuse_tex.location.y = y_location + 220
    weapon_diffuse_tex.label = "Diffuse Texture"
    
    #AO Strength Node
    ao_strength = weaponshader.node_tree.nodes.new(type="ShaderNodeValue")
    ao_strength.location.x = current_node_location_x - 500
    ao_strength.location.y = y_location + 350
    ao_strength.label = "AO Strength"
    ao_strength.outputs[0].default_value = 1
    
    #LINKS
    #AEM tex to AEM Seperation
    weaponshader.node_tree.links.new(aem_tex.outputs["Color"],
                                    AEM_seperate.inputs[0])
    #AO Strength to AO Mult
    weaponshader.node_tree.links.new(ao_strength.outputs[0],
                                    ao_mult.inputs[0])
    #Diffuse Tex to AO Mult
    weaponshader.node_tree.links.new(weapon_diffuse_tex.outputs["Color"],
                                    ao_mult.inputs[1])
    #AEM Seperation to AO Mult
    weaponshader.node_tree.links.new(AEM_seperate.outputs[0],
                                    ao_mult.inputs[2])
    #AO Mult to BSDF
    weaponshader.node_tree.links.new(ao_mult.outputs[0],
                                    principled_bsdf_node.inputs[0])
    return AEM_seperate
    return weapon_diffuse_tex

def weaponEmit():
    """Creates Emmision Setup for Weapon Shader"""
    global AEM_seperate
    global weapon_diffuse_tex
    
    
    node_location_x_step = 200
    current_node_location_x = -node_location_x_step + 500
    y_location = 400
    
    #Creates Add Shader
    add_shader = weaponshader.node_tree.nodes.new(type="ShaderNodeAddShader")
    add_shader.location.x = current_node_location_x
    add_shader.location.y = 400
    
    #Creates Emmision Shader
    emit_shader = weaponshader.node_tree.nodes.new(type="ShaderNodeEmission")
    emit_shader.location.x = current_node_location_x - 200
    emit_shader.location.y = 400
    
    #Emit mix
    mix_shader =  weaponshader.node_tree.nodes.new(type="ShaderNodeMixRGB")
    mix_shader.blend_type = "MULTIPLY"
    mix_shader.inputs['Fac'].default_value = 1
    mix_shader.location.y = 600
    
    #Emit Strength
    emit_strength = weaponshader.node_tree.nodes.new(type="ShaderNodeValue")
    emit_strength.outputs[0].default_value = 0
    emit_strength.location.x = current_node_location_x - 1300
    emit_strength.location.y = 850
    emit_strength.label = "Emmision Strength"
    
    #Links
    #AEM G to Color1
    weaponshader.node_tree.links.new(AEM_seperate.outputs[1],
                                    mix_shader.inputs[1])
    #Link Diffuse Tex to Color2
    weaponshader.node_tree.links.new(weapon_diffuse_tex.outputs[0],
                                    mix_shader.inputs[2])
    #Link Color to Emmission Shader
    weaponshader.node_tree.links.new(mix_shader.outputs[0],
                                    emit_shader.inputs[0])
    #Link Strength to Emmission Strength
    weaponshader.node_tree.links.new(emit_strength.outputs[0],
                                    emit_shader.inputs[1])
    #Link BSDF to Add Shader
    weaponshader.node_tree.links.new(principled_bsdf_node.outputs[0],
                                    add_shader.inputs[1])
    #Link Emmission to Add Shader
    weaponshader.node_tree.links.new(emit_shader.outputs[0],
                                    add_shader.inputs[0])

def weaponShader():
    """Sequence of Functions to create the weapon shader"""
    new_weaponmat()
    add_weapon_normal_map()
    MRS()
    weaponDiffuse()
    weaponEmit()

def create_charShader():
    """Sequence of Functions to create the character shader"""
    new_charmat()
    add_normal_map()
    mrae_splitter()
    diffuse_tex()

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

#Main Panel for Shaders
class BVT_PT_Panel(bpy.types.Panel):
    bl_label = "Brainez VALORANT Tools"
    bl_idname = "VIEW3D_PT_id_mask"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BrainezTools'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("bvt.create_character_shader", text="Create Character Shader")
        row = layout.row()
        row.operator("bvt.create_weapon_shader", text="Create Weapon Shader")
        
#Operator to create character shader
class BVT_OT_CreateCharacterShader(bpy.types.Operator):
    """Creates Character Shader"""
    bl_idname = "bvt.create_character_shader"
    bl_label = "Create Character Shader"

    def execute(self, context):
        create_charShader()
        return {'FINISHED'}

#Opeartor to create weapon shader
class BVT_OT_CreateWeaponShader(bpy.types.Operator):
    """Creates Weapon Shader"""
    bl_idname = "bvt.create_weapon_shader"
    bl_label = "Create Weapon Shader"

    def execute(self, context):
        weaponShader()
        return {'FINISHED'}

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
    ID_MASK_RESET_PASS,
    BVT_PT_Panel,
    BVT_OT_CreateCharacterShader,
    BVT_OT_CreateWeaponShader,
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


if __name__ == "__main__":
    register()
