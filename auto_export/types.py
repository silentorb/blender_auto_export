from typing import NamedTuple


class Config(NamedTuple):
    output_format: str
    output_dir: str
    folder_per_model: bool = False
    file_per_object: bool = False
    shape_bounds: bool = False
    save_debug_blend: bool = False
    exporter_config: dict = {}
