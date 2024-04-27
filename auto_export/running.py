import subprocess
from os import path

import bpy
from bpy.app.handlers import persistent

from auto_export.exporting import prepare_scene, export_model
from auto_export.types import Config
from auto_export.utility import get_blend_dir, get_blend_filename, debug_print
from .configuration import try_load_config_relative


def launch_blender(filepath):
    blender_executable = bpy.app.binary_path
    this_script = path.join(path.dirname(path.realpath(__file__)), '__main__.py')
    command = [blender_executable, filepath, '--background', '--python', this_script]
    print(" ".join(command))
    subprocess.call(command)


def export_using_config(config: Config):
    export_dir = config.output_dir
    name = get_blend_filename()
    if config.folder_per_model:
        export_dir = path.join(export_dir, name)

    export_objects = prepare_scene(config)
    if export_objects:
        export_model(export_dir, name, config, export_objects)
    else:
        print("No objects to export")

    # Used to save a sample of the blend file containing every export workaround
    if config.debug_blend:
        bpy.ops.wm.save_as_mainfile(filepath=config.debug_blend)
        print("Saved debug blend file at ")


def running_main():
    config = try_load_config_relative()
    if config is None:
        return

    export_using_config(config)


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


if __name__ == '__main__':
    print("Running from command line")
    running_main()
