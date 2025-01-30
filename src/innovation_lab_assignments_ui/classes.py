from tkinter import StringVar
from typing import override


class RunConfig:
    """
    Members are StringVars that hold all the config values,
    and are bound to their respective Labels.
    """
    def __init__(self, config_content_dict: dict):
        self.input_csv = StringVar()
        self.output_dir = StringVar()
        self.daily_activities_config_file = StringVar()

        self.input_csv.set(self._empty_if_none(config_content_dict.get("input_csv")))
        self.output_dir.set(self._empty_if_none(config_content_dict.get("output_dir")))
        self.daily_activities_config_file.set(self._empty_if_none(config_content_dict.get("daily_activities_config_file")))

    @staticmethod
    def _empty_if_none(value: str):
        return "" if value is None else value

    def to_dict(self) ->dict:
        """
        Returns: dict: Suitable for saving to a .json file.
        """
        return {
            "input_csv": self.input_csv.get(),
            "output_dir": self.output_dir.get(),
            "daily_activities_config_file": self.daily_activities_config_file.get()
        }

    def is_valid(self) ->bool:
        """
        Returns: bool: False if any of the StringVar members have "", otherwise True
        :return:
        :rtype:
        """
        return False if self.input_csv.get() == "" or self.output_dir.get() == "" or self.daily_activities_config_file.get() == "" else True