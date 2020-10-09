import configparser
import os
from os import path

from gltf_auto_export.defaults import default_config
from gltf_auto_export.utility import report


def find_config_file(project_file_name, current_path):
    normalized = os.path.normpath(current_path)
    parts = normalized.split(os.sep)
    accumulator = ""
    parts[0] = parts[0] + os.sep
    for part in parts:
        accumulator = os.path.join(accumulator, part)
        if os.path.exists(path.join(accumulator, project_file_name)):
            return True

    return False


def load_config(config_file):
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
    except Exception as e:
        print(e)
        return None

    return config


def prepare_config(config):
    gltf_config = config["gltf"] or {}
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
