import subprocess
from os import path

import bpy
from bpy.app.handlers import persistent

from gltf_auto_export.exporting import prepare_scene, export_gltf
from gltf_auto_export.utility import get_blend_dir, get_blend_filename, debug_print
from .configuration import try_load_config_relative


def launch_blender(filepath):
    blender_executable = bpy.app.binary_path
    this_script = path.join(path.dirname(path.realpath(__file__)), '__main__.py')
    command = [blender_executable, filepath, '--background', '--python', this_script]
    print(" ".join(command))
    subprocess.call(command)


def export_gltf_using_config(config):
    export_dir = config.get("export_dir") or get_blend_dir()
    name = get_blend_filename()

    export_objects = prepare_scene()
    if export_objects:
        export_gltf(export_dir, name, config["gltf"], export_objects)
    else:
        print("No objects to export")


def try_export_gltf(_, __):
    print("Checking glTF export")

    config = try_load_config_relative()
    if config is None:
        return

    # Launch in a separate process so the active scene isn't modified by export preparation
    launch_blender(bpy.data.filepath)


@persistent
def try_export_gltf_persistent(_, __):
    try_export_gltf(_, __)


def bulk_export(dir):
    print("Coming soon...")


def running_main():
    config = try_load_config_relative()
    if config is None:
        return

    export_gltf_using_config(config)


if __name__ == '__main__':
    print("Running from command line")
    running_main()
