import json
import os
from os import path
from typing import Optional

from auto_export.gltf.defaults import default_configs
from .types import Config
from .utility import report, get_blend_dir, get_blend_filename


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


def get_custom_output_dir(config_path: str, data: dict):
    initial_output_dir = data.get("output_dir", None)
    output_dir = path.abspath(path.join(path.dirname(config_path), initial_output_dir)) \
        if initial_output_dir else get_blend_dir()

    if data.get("folder_per_model", False):
        return path.join(output_dir, get_blend_filename())

    return output_dir


def prepare_config(data: dict, config_file) -> Config:
    args = dict(data)
    output_format = data.get("output_format", "gltf")
    local_config = data.get('exporter_config', {})
    if output_format == "fbx" and "object_types" in local_config:
        local_config["object_types"] = set(local_config["object_types"])

    args["output_format"] = output_format
    args["output_dir"] = get_custom_output_dir(config_file, data)
    args["exporter_config"] = {
        **default_configs().get(output_format, {}),
        **local_config
    }

    return Config(**args)


def try_load_config(blend_dir) -> Optional[Config]:
    config_file = find_config_file("blender_export.json", blend_dir)
    if config_file is None:
        return None

    raw_config = load_config(config_file)
    if raw_config is None:
        report(f"Could not load auto export configuration \"{config_file}\"", "ERROR")
        return None

    return prepare_config(raw_config, config_file)


def try_load_config_relative() -> Optional[Config]:
    return try_load_config(get_blend_dir())
