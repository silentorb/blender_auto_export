import os
import bpy
from os import path


def debug_print(message):
    if os.environ.get("DEBUG_GLTF_AUTO_EXPORT", None):
        print(message)


# Since Blender error reporting functionality is tied to Operators, create an Operator
class ErrorDisplay(bpy.types.Operator):
    bl_idname = "wm.error_display"
    bl_label = "Reports an Error"

    severity: bpy.props.StringProperty()
    message: bpy.props.StringProperty()

    def execute(self, context):
        self.report({self.severity}, self.message)  # A lot of work to get to this line of code
        return {"FINISHED"}


def report(message, severity="INFO"):
    try:
        bpy.utils.register_class(ErrorDisplay)
        bpy.ops.wm.error_display("EXEC_DEFAULT", message=message, severity=severity)
        bpy.utils.unregister_class(ErrorDisplay)
    except Exception as e:
        print(e)


def get_blend_dir():
    return path.dirname(bpy.data.filepath)


def get_blend_filename():
    filepath = bpy.data.filepath
    return path.splitext(path.basename(filepath))[0]


def deselect_objects(objects):
    bpy.context.view_layer.objects.active = None
    for obj in objects:
        obj.select_set(False)


# The Blender operator to select/deselect has a bug with needing to get the proper context based on mouse hovering :(
def deselect_all():
    deselect_objects(bpy.data.objects)
