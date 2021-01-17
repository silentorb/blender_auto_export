# Blender Auto Export

A Blender plugin for automating exporting models

## Overview

* Any time a Blender file is saved, this plugin checks if the .blend file has any parent directory with a `blender_export.json` file
* If a `blender_export.json` file is found, any configuration is loaded from it and a glTF file is exported
* The `blender_export.json` file can be empty
* Exporting is performed using the standard [Blender glTF Exporter](https://github.com/KhronosGroup/glTF-Blender-IO)

## Configuration

### Defaults

* By default the target export directory is the location of the .blend file

### Sample

### Object Filtering

You can prevent objects from being exported by either:

* Adding a custom property to an object with a property name of `no-export`
    * The property value doesn't matter
* Disabling rendering visibility for the object
    * Rendering visibility is used instead of scene visibility to support exporting hidden objects
