import os
from os import path

import bpy

from .workarounds import deselect_all, check_topology, deselect_objects


def get_export_objects():
    result = []
    for obj in bpy.context.scene.objects:
        if not obj.hide_render and "no-export" not in obj:
            result.append(obj)
    return result


def select_objects(objs):
    for obj in objs:
        obj.select_set(True)


def prepare_scene():
    export_objects = get_export_objects()

    if os.environ.get("CHECK_TOPOLOGY", None):
        check_topology(export_objects)

    # prepare_animations()

    if export_objects:
        deselect_all()
        select_objects(export_objects)

    return export_objects


def get_root_objects(objects):
    return [obj for obj in objects if not obj.parent]


def export_gltf(export_dir, name, gltf_config, objects):
    root_objects = get_root_objects(objects)
    for obj in root_objects:
        deselect_objects(root_objects)
        obj.select_set(True)
        filename = name if len(root_objects) == 1 else obj.name
        filepath = path.join(export_dir, filename)
        bpy.ops.export_scene.gltf(
            **gltf_config,
            filepath=filepath
        )
        print("Exported ", filepath)
