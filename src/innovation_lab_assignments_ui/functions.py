from tkinter import Tk
from typing import Optional
import json
from innovation_lab_assignments_ui.classes import RunConfig

_run_config_instance: Optional[RunConfig] = None
_main_window: Optional[Tk] = None

INNOVATION_LAB_ASSIGNMENTS_CONFIG_FILE = "innovation_lab_assignments.json"

def _get_full_config_file_path():
    from innovation_lab_assignments.classes import Config
    from innovation_lab_assignments.functions import prepend_project_root_if_required
    full_path = prepend_project_root_if_required(INNOVATION_LAB_ASSIGNMENTS_CONFIG_FILE,
                                                 Config.get_instance().project_root)
    return full_path

def get_saved_run_config() ->RunConfig:
    global _run_config_instance
    from pathlib import Path
    from json import JSONDecodeError

    if _run_config_instance is not None:
        return _run_config_instance

    # Open and read INNOVATION_LAB_ASSIGNMENTS_CONFIG_FILE if it exists.
    config_file_content = {}
    full_path = _get_full_config_file_path()

    if Path(full_path).exists():
        try:
            with open(full_path) as input_file:
                config_file_content = json.load(input_file)
        except JSONDecodeError:
            # We found the file, but its contents are malformed.
            pass

    _run_config_instance = RunConfig(config_file_content)
    return _run_config_instance

def save_run_config():
    global _run_config_instance
    if _run_config_instance is not None:
        full_path = _get_full_config_file_path()

        with open(full_path, "w") as output_file:
            # noinspection PyTypeChecker
            json.dump(_run_config_instance.to_dict(), output_file, indent=2)

def get_main_window() ->Tk:
    global _main_window

    if _main_window is None:
        _main_window = Tk()

    return _main_window

