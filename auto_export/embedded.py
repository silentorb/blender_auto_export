import bpy

# This function can be called within an autorun .blend Python script as an alternative to using the plugin
from auto_export.running import try_export_persistent, try_export


def register_auto_export_once():
    if try_export_persistent not in bpy.app.handlers.save_pre and try_export not in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.append(try_export)
