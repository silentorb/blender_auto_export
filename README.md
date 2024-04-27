# Blender Auto Export

A Blender plugin for automating model exporting.  Also provides enhanced export features.

## Overview

Any time a Blender file is saved, this plugin checks if the .blend file has any parent directory
with a `blender_export.json` file.

If a `blender_export.json` file is found, any configuration is loaded from it and a model file is exported.

The `blender_export.json` file can be empty.

Primarily supports glTF and FBX but is designed to support other exporters.

To provide enhanced export features, the scene is modified before exporting.

To prevent permanent modifications to the blend file, this addon launches a background Blender process which 
loads the blend file, modifies it, exports it, and then closes without saving the changes.

## Defaults

* By default, the target export directory is the location of the .blend file

## Sample `blender_export.json`
```json
{
  "output_format": "gltf",
  "output_dir": "../../output",
  "folder_per_model": true,
  "exporter_config": {
    "export_yup": false
  }
}
```
## Object filtering

You can prevent objects from being exported by either:

* Adding a custom property to an object with a property name of `no-export`
    * The property value doesn't matter
* Disabling rendering visibility for the object
    * Rendering visibility is used instead of scene visibility to support exporting hidden objects

## Texture baking

Blender Auto Export supports automatic texture baking.

Currently only diffuse texture baking is supported.

When a material contains a custom attribute of 'bake' (regardless of the value of the attribute),
the following operations will be performed on the object and that material:

1. A new diffuse texture image will be baked for the object, using all of the object's materials.
2. A PNG image file will be saved beside the object's exported model file.  The image file name will be the material name.
3. All other materials will be removed from the exported object, and the contents of the primary material will be replaced with a texture node referencing the saved image file. 
