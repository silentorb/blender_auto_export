import os
from os import path

import bpy

from .configuration import try_load_config
from .utility import debug_print
from .workarounds import deselect_all, check_topology, prepare_animations


def get_export_objects():
    result = []
    for obj in bpy.context.scene.objects:
        if not obj.hide_render and "no-export" not in obj:
            result.append(obj)
    return result


def prepare_scene():
    deselect_all()
    export_objects = get_export_objects()
    if os.environ.get("CHECK_TOPOLOGY", None):
        check_topology(export_objects)

    prepare_animations()

    has_objects = len(export_objects) > 0
    if has_objects:
        deselect_all()

    return has_objects


def get_blend_filename():
    filepath = bpy.data.filepath
    return path.splitext(path.basename(filepath))[0]


def export_gltf(filepath, gltf_config):
    bpy.ops.export_scene.gltf(
        **gltf_config,
        filepath=filepath
    )


def try_export_gltf(_, __):
    blend_dir = path.dirname(bpy.data.filepath)
    name = get_blend_filename()

    debug_print("Checking glTF export")

    config = try_load_config(blend_dir)
    if config is None:
        return

    export_dir = config.get("export_dir") or blend_dir
    export_file = path.join(export_dir, name)

    print("Exporting ", export_file)

    if prepare_scene():
        export_gltf(export_file, config["gltf"])
        print("Exported ", export_file)
    else:
        print("No objects to export")


def bulk_export(dir):
    print("Coming soon...")
