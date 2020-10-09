import bpy

from gltf_auto_export import try_export_gltf_persistent
from gltf_auto_export.exporting import try_export_gltf


# This function can be called within an autorun .blend Python script as an alternative to using the plugin
def register_gltf_auto_export_once():
    if try_export_gltf_persistent not in bpy.app.handlers.save_pre and try_export_gltf not in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.append(try_export_gltf)
