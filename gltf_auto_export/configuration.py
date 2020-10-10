import configparser
import os
from os import path

from .defaults import default_config
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
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
    except Exception as e:
        print(e)
        return None

    return config._sections


def prepare_config(config):
    gltf_config = config.get("gltf") or {}
    return {
        "gltf": {
            **default_config(),
            **gltf_config
        }
    }


def try_load_config(blend_dir):
    config_file = find_config_file("blender_gltf_export.ini", blend_dir)
    if config_file is None:
        return None

    config = load_config(config_file)
    if config is None:
        report(f"Could not load glTF export configuration \"{config_file}\"", "ERROR")
        return None

    return prepare_config(config)


def try_load_config_relative():
    return try_load_config(get_blend_dir())
