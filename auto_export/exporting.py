import os
from os import path

import bpy

from auto_export.gltf.workarounds import check_topology
from auto_export.utility import deselect_all, deselect_objects
from .shapes import preprocess_bounds_shape
from baking import bake_all, prune_graph_for_texture
from .types import Config


def get_export_objects():
    result = []
    for obj in bpy.context.scene.objects:
        if not obj.hide_render and "no-export" not in obj:
            result.append(obj)
    return result


def select_objects(objs):
    for obj in objs:
        obj.select_set(True)


def prepare_scene(config: Config):
    export_objects = get_export_objects()

    if os.environ.get("CHECK_TOPOLOGY", None):
        check_topology(export_objects)

    # prepare_animations()

    if config.shape_bounds:
        for obj in bpy.context.scene.objects:
            preprocess_bounds_shape(obj)

    if export_objects:
        deselect_all()
        select_objects(export_objects)

    return export_objects


def get_root_objects(objects):
    return [obj for obj in objects if not obj.parent]


def get_export_file_extension(config):
    if "extension" in config:
        return config["extension"]

    extension_map = {
        "gltf": "",
        "fbx": ".fbx"
    }

    return extension_map.get(config["output_format"], "")


def export_prepared_model(exporter, exporter_config, filepath):
    exporter(
        **exporter_config,
        filepath=filepath
    )
    print("Exported ", filepath)


def set_export_object_visibility(objs):
    for obj in objs:
        if obj.hide_get():
            obj.hide_set(False)
        obj.select_set(True)


def export_model(export_dir, name, config: Config, objects):
    root_objects = get_root_objects(objects)
    exporter_config = config.exporter_config
    os.makedirs(export_dir, exist_ok=True)
    export_scene = bpy.ops.export_scene
    exporter = getattr(export_scene, config.output_format)
    extension = get_export_file_extension(config)
    if config.file_per_object:
        for obj in root_objects:
            deselect_objects(root_objects)
            obj.hide_set(False)
            obj.select_set(True)
            filename = name if len(root_objects) == 1 else obj.name
            filepath = path.join(export_dir, filename + extension)
            export_prepared_model(exporter, exporter_config, filepath)
    else:
        set_export_object_visibility(objects)

        filepath = path.join(export_dir, name + extension)
        export_prepared_model(exporter, exporter_config, filepath)
        print(len(objects))
