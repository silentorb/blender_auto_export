import bpy


# This file contains functions used to workaround bugs in Blender and the glTF Exporter.
# If any of those bugs are fixed then the equivalent workaround functions will be obsolete.

# This function is used to work around a bug in the glTF Exporter.
def add_keyframe_if_missing(curves, obj_name, property_name, values):
    data_path = "pose.bones["" + obj_name + ""]." + property_name
    for curve in curves:
        if curve.data_path == data_path:
            return

    for i, value in enumerate(values):
        curve = curves.new(data_path, i, obj_name)
        curve.keyframe_points.insert(0, value)


# This function is used to ensure animation markers are exported
def prepare_animations():
    for action in bpy.data.actions:
        markers = []
        for marker in action.pose_markers:
            markers.append({"name": marker.name, "frame": marker.frame})

        if len(markers) > 0:
            action["markers"] = markers


# The GLTF exporter will skip meshes with ngon topology but won"t provide any information about the
# mesh that was skipped, such as its name.  Running this function first provides
# a better workflow for handling topology problems
def check_topology(objs):
    for obj in objs:
        if obj.type == "MESH":
            try:
                obj.data.calc_tangents()
            except:
                print("ERROR: Object " + obj.name + " has faces with more than 4 sides")
