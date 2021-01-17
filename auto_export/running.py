import subprocess
from os import path

import bpy
from bpy.app.handlers import persistent

from auto_export.exporting import prepare_scene, export_model
from auto_export.utility import get_blend_dir, get_blend_filename, debug_print
from .configuration import try_load_config_relative


def launch_blender(filepath):
    blender_executable = bpy.app.binary_path
    this_script = path.join(path.dirname(path.realpath(__file__)), '__main__.py')
    command = [blender_executable, filepath, '--background', '--python', this_script]
    print(" ".join(command))
    subprocess.call(command)


def get_custom_output_dir(config):
    return path.abspath(path.join(path.dirname(config["config_file"]), config["output_dir"]))


def export_using_config(config):
    print('config', config)
    export_dir = get_custom_output_dir(config) if "output_dir" in config else get_blend_dir()
    name = get_blend_filename()
    if (config.get("folder_per_model", False)):
        export_dir = path.join(export_dir, name)

    export_objects = prepare_scene()
    if export_objects:
        export_model(export_dir, name, config, export_objects)
    else:
        print("No objects to export")


def try_export(_, __):
    print("Checking glTF export")

    config = try_load_config_relative()
    if config is None:
        return

    # Launch in a separate process so the active scene isn't modified by export preparation
    launch_blender(bpy.data.filepath)


@persistent
def try_export_persistent(_, __):
    try_export(_, __)


def bulk_export(dir):
    print("Coming soon...")


def running_main():
    config = try_load_config_relative()
    if config is None:
        return

    export_using_config(config)


if __name__ == '__main__':
    print("Running from command line")
    running_main()
