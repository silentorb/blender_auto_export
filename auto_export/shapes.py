import bpy
import mathutils


bounds_type_key = 'bounds'


def get_horizontal_radius(dimensions):
    return max(dimensions.x, dimensions.y) / 2


def is_vector_approximately_non_zero(position, min):
    return abs(position[0]) > min or abs(position[1]) > min or abs(position[2]) > min


def get_shape_offset(bound_box):
    center = sum((mathutils.Vector(b) for b in bound_box), mathutils.Vector()) / 8
    min = 0.03
    if is_vector_approximately_non_zero(center, 0.03):
        return center

    return None


def get_bounds_children(parent):
    return [obj for obj in bpy.data.objects if obj.parent == parent and bounds_type_key in obj]


def aggregate_child_bounds(obj):
    children = [preprocess_bounds_shape(child) for child in get_bounds_children(obj) ]
    return [c for c in children if c != None]


def preprocess_bounds_shape(obj):
    type = str(obj.get(bounds_type_key))
    if type is None:
        return None

    dimensions = obj.dimensions
    # print('shape ' + type)
    bounds = None
    if type == 'composite':
        bounds = {
            'type': 'composite',
            'children': aggregate_child_bounds(obj)
        }
    elif type == 'cylinder':
        bounds = {
            'type': 'cylinder',
            'radius': get_horizontal_radius(dimensions),
            'height': dimensions.z
        }
    elif type == 'mesh':
        bounds = {
            'type': 'mesh',
            'radius': get_horizontal_radius(dimensions),
            'height': dimensions.z
        }
    elif type == 'box':
        bounds = {
            'type': 'box',
            'dimensions': (dimensions.x, dimensions.y, dimensions.z)
        }

    if bounds:
        if type != 'mesh' and type != 'composite':
            offset = get_shape_offset(obj.bound_box)
            if is_vector_approximately_non_zero(obj.location, 0.01):
                if offset:
                    offset += obj.location
                else:
                    offset = obj.location
            if offset:
                bounds['offset'] = offset
        obj['bounds'] = bounds

    # print('shape end ' + type)

    return bounds

