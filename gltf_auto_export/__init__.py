import bpy
from bpy.app.handlers import persistent

from .exporting import try_export_gltf

bl_info = {
    "name": "glTF Auto Export",
    "category": "Import-Export",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "author": "Christopher W. Johnson"
}


@persistent
def try_export_gltf_persistent(_, __):
    try_export_gltf(_, __)


def register():
    # Unregister debugging purposes to ensure fresh code is registered.
    # Should not have a significant performance hit.
    unregister()

    if try_export_gltf_persistent not in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.append(try_export_gltf_persistent)


def unregister():
    if try_export_gltf_persistent in bpy.app.handlers.save_pre:
        bpy.app.handlers.save_pre.remove(try_export_gltf_persistent)
