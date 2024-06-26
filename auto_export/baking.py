import bpy
import os.path


def create_image(image_name, image_path, length):
    image = bpy.data.images.new(image_name, length, length)
    print(image_path)
    image.filepath_raw = image_path
    image.file_format = 'PNG'
    return image


def create_texture_node(material, image):
    node = material.node_tree.nodes.new('ShaderNodeTexImage')
    node.image = image
    return node


def set_active_object(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)


def select_material_node(material, node):
    node.select = True
    material.node_tree.nodes.active = node


def bake_texture(original, image):
    print(f"Baking texture for {original.name}")
    for obj in bpy.data.objects:
        if obj.hide_get():
            obj.hide_set(True)
    original.hide_set(False)
    set_active_object(original)

    for material in original.data.materials:
        node = create_texture_node(material, image)
        select_material_node(material, node)

    bpy.context.scene.cycles.bake_type = 'DIFFUSE'
    bpy.ops.wm.save_as_mainfile(filepath="e:/bake-debug.blend")
    bpy.ops.object.bake(type='DIFFUSE', save_mode='EXTERNAL')
    print('Bake finished')


# Returns true if the material has a custom property named 'bake', regardless of the property value.
def should_bake(material):
    return 'bake' in material


# Not currently used but might come in handy down the road
def get_bake_materials():
    return [m for m in bpy.data.materials if should_bake(m)]


def get_bake_object_material(obj):
    if obj.type == 'MESH' and 'no-export' not in obj:
        for material in obj.data.materials:
            if should_bake(material):
                return material

    return None


# Returns all materials that have a custom property named 'bake'.  It doesn't matter what
# the property value is.
def get_bake_object_material_pairs():
    result = []
    for obj in bpy.data.objects:
        material = get_bake_object_material(obj)
        if material:
            result.append((obj, material))

    return result


def prune_graph_for_texture(obj, material, image):
    tree = material.node_tree
    nodes = tree.nodes
    nodes.clear()

    texture_node = create_texture_node(material, image)
    emission_node = material.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
    tree.links.new(texture_node.outputs[0], emission_node.inputs[0])

    # Delete other materials
    obj.data.materials.clear()
    obj.data.materials.append(material)

    # Reassign all polygons to the one remaining object material.
    # This is redundant for any polygons already assigned to the remaining material,
    # But should be as performant if not more so than filtering would take.
    for polygon in obj.data.polygons:
        polygon.material_index = 0


def bake_object_material(image_directory, obj, material):
    image_path = os.path.join(image_directory, material.name + '.png')
    print(f"image_path: {image_path}")
    length = int(round(float(material['size']))) if 'size' in material else 1024
    image = create_image(material.name, image_path, length)
    bake_texture(obj, image)
    image.save()
    prune_graph_for_texture(obj, material, image)


def bake_all(image_directory):
    bake_pairs = get_bake_object_material_pairs()
    for obj, material in bake_pairs:
        bake_object_material(image_directory, obj, material)
