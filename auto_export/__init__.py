import bpy

from auto_export.running import try_export_persistent, running_main

bl_info = {
    "name": "Auto Export",
    "category": "Import-Export",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "author": "Christopher W. Johnson"
}


def register():
    if try_export_persistent not in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_post.append(try_export_persistent)


def unregister():
    if try_export_persistent in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_post.remove(try_export_persistent)
