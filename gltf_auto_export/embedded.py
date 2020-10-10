import bpy

# This function can be called within an autorun .blend Python script as an alternative to using the plugin
from gltf_auto_export.running import try_export_gltf_persistent, try_export_gltf


def register_gltf_auto_export_once():
    if try_export_gltf_persistent not in bpy.app.handlers.save_pre and try_export_gltf not in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.append(try_export_gltf)
