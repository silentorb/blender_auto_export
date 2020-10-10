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
    bpy.utils.register_class(ErrorDisplay)
    bpy.ops.wm.error_display("EXEC_DEFAULT", message=message, severity=severity)
    bpy.utils.unregister_class(ErrorDisplay)


def get_blend_dir():
    return path.dirname(bpy.data.filepath)


def get_blend_filename():
    filepath = bpy.data.filepath
    return path.splitext(path.basename(filepath))[0]
