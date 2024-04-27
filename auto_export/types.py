from typing import NamedTuple, Optional


class Config(NamedTuple):
    output_format: str
    output_dir: str
    folder_per_model: bool = False
    file_per_object: bool = False
    shape_bounds: bool = False
    debug_blend: Optional[str] = None
    exporter_config: dict = {}
