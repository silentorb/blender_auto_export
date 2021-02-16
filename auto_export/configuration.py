import json
import os
from os import path

from auto_export.gltf.defaults import default_configs
from .utility import report, get_blend_dir


def find_config_file(project_file_name, starting_path):
    normalized = os.path.normpath(starting_path)
    parts = normalized.split(os.sep)
    current_path = starting_path
    for i in range(len(parts) - 1):
        config_file = path.join(current_path, project_file_name)
        print(config_file)
        if os.path.exists(config_file):
            return config_file

        current_path = path.dirname(current_path)

    return None


def load_config(config_file):
    try:
        with open(config_file) as file:
            data = json.load(file)
    except Exception as e:
        print(e)
        return None

    return data


def prepare_config(config, config_file):
    format = config.get("format", "gltf")
    local_config = config.get('exporter_config', {})
    if format == "fbx" and "object_types" in local_config:
        local_config["object_types"] = set(local_config["object_types"])

    return {
        "file_per_object": False,
        **config,
        "exporter_config": {
            **default_configs().get(format, {}),
            **local_config
        },
        'config_file': config_file
    }


def try_load_config(blend_dir):
    config_file = find_config_file("blender_export.json", blend_dir)
    if config_file is None:
        return None

    config = load_config(config_file)
    if config is None:
        report(f"Could not load auto export configuration \"{config_file}\"", "ERROR")
        return None

    return prepare_config(config, config_file)


def try_load_config_relative():
    return try_load_config(get_blend_dir())
