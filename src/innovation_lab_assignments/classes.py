import logging
import sys
from datetime import datetime

class SheetRec:
    """
    Each instance is a sheet's (i.e., a day's) name and list of activities.
    Each activity has its own list of assigned students.

    Attributes:
        day (str): Sheet day
        activities (list[Activity]): The sheet's list of activities
    """
    def __init__(self, sheet_dict: dict):
        self.day = sheet_dict["day"]
        self.activities = self._create_activity_list(sheet_dict["activities"])

    @staticmethod
    def _create_activity_list(activities_dict_list):
        activities_list = []
        for activity_dict in activities_dict_list:
            activities_list.append((Activity(activity_dict)))

        return activities_list

class Activity:
    """
    Each instance is an activity for SheetRec.activities.

    Attributes:
        name (str): Activity name
        cap (int): Cap on number of students for activity.
        students (list[Student]): List of assigned Students.
    """
    def __init__(self, activity_dict: dict):
        self.name = activity_dict["activity"]
        self.cap = self._convert_cap_to_int(activity_dict["cap"])
        self.students = []

    def __str__(self):
        return f"name: {self.name}, cap: {self.cap}"

    @staticmethod
    def _convert_cap_to_int(cap_value: str) -> int:
        """
        If passed cap_value is a str, return sys.maxsize. Otherwise, just return cap_value.
        Args:
            cap_value (str): String to be converted to int
        Returns:
            int
        """
        numeric_cap = cap_value if type(cap_value) == int else sys.maxsize
        return numeric_cap

class Student:
    """
    Student.
    Attributes:
        timestamp (datetime): Time record was created
        first_name (str)
        last_name (str)
        in_athletics (bool)
        effort_agreement (bool)
        credit_agreement (bool)
        monday_choices ([Choice]): List of 3 choices
        tuesday_choices ([Choice]): List of 3 choices
        wednesday_choices ([Choice]): List of 3 choices
        thursday_choices ([Choice]): List of 3 choices
    """
    def __init__(self, student_dict: dict, student_id: int):
        self.student_id = student_id
        self.first_name = student_dict["Type your first name"]
        self.last_name = student_dict["Type your last name"]
        self.in_athletics = True if student_dict["I am currently participating in at least one LHS sport."] == "Yes" else False
        self.effort_agreement = True if student_dict["I understand that my participation and effort in the selections I have made will determine if I am able to stay in each offering."] == "I understand" else False
        self.credit_agreement = True if student_dict["I understand that disciplinary issues could result in not receiving credit for Innovation Lab."] == "I understand" else False
        self.monday_choices =   [Choice(student_dict["Monday First Choice"], 1),
                                 Choice(student_dict["Monday Second Choice"], 2),
                                 Choice(student_dict["Monday Third Choice"], 3)]
        self.tuesday_choices =  [Choice(student_dict["Tuesday First Choice"], 1),
                                 Choice(student_dict["Tuesday Second Choice"], 2),
                                 Choice(student_dict["Tuesday Third Choice"], 3),]
        self.wednesday_choices =[Choice(student_dict["Wednesday First Choice"], 1),
                                 Choice(student_dict["Wednesday Second Choice"], 2),
                                 Choice(student_dict["Wednesday Third Choice"], 3),]
        self.thursday_choices = [Choice(student_dict["Thursday First Choice"], 1),
                                 Choice(student_dict["Thursday Second Choice"], 2),
                                 Choice(student_dict["Thursday Third Choice"], 3),]
        self.day_selections = {"monday" : 0, "tuesday" : 0, "wednesday" : 0, "thursday" : 0}
        self.timestamp = datetime.strptime(student_dict["Timestamp"], "%m/%d/%Y %H:%M:%S")

    def __str__(self):
        day_selections = ""
        keys = self.day_selections.keys()
        for key in keys:
            day_selections += f" day: {key}, priority: {self.day_selections[key]}"
        return f"name: {self.first_name} {self.last_name}, in athletics? {self.in_athletics} {day_selections}"

    def set_selection_priority_for_day(self, priority, day):
        """
        Mark at which priority the passed day was selected.
        """
        self.day_selections[day] = priority

    def is_available_for_day(self, day):
        """
        Return True if the student has not yet been selected for the passed day.
        """
        return True if self.day_selections[day] == 0 else False

class Choice:
    '''
    An activity choice with priority
    Attributes:
        name (str): Choice's activity name
        priority (int): Priority of choice
    '''
    def __init__(self, name: str, priority: int):
        self.name = name
        self.priority = priority

    def __str__(self):
        return f"name: {self.name}, priority: {self.priority}"

class DictRowManager:
    '''
    Each instance manages a list rows, and creates rows as needed.
    Each row is a dict whose keys come from a list of field names pass in the constructor.
    '''
    def __init__(self, row_fields: [str]):
        self._row_fields = row_fields
        self._rows = []

    def _generate_row(self) -> dict:
        '''
        Create a dict using _row_fields as its keys.
        '''
        row_dict = dict.fromkeys(self._row_fields)
        return row_dict

    def get_row(self, index):
        '''
        Return the row at the passed index from the managed list of rows.
        If the row does not yet exist, first _generate_row(), add it to the list
        of rows.
        Args:
            index (int)
        Returns: [dict] Requested row as a dict
        '''
        if len(self._rows) <= index:
            row_dict = self._generate_row()
            self._rows.append(row_dict)

        return self._rows[index]

    def get_all_rows(self):
        '''
        Return the managed list of rows.
        '''
        return self._rows

class Config:
    """
    Exposes configurable items.
    This class is a singleton. Use Config.get_instance() to get the single instance.
    """
    _instance = None
    _is_initialize_allowed = False

    def __init__(self):
        """
        __init__() is only allowed to be run when _is_initialize_allowed.
        """
        if not Config._is_initialize_allowed:
            message = "Only one instance is allowed. Use 'create_instance'."
            logging.error(message)
            raise RuntimeError(message)
        Config._is_initialize_allowed = False #No more instantiations allowed.
        self.input_file_name: str = ""
        self.output_dir_name: str = ""
        self.config_json_name: str = ""
        self.project_root: str = ""
        self.json_data: dict = {}
        self.weight_factor_dict = None
        self._cmd_line_args_parsed = False

    @staticmethod
    def get_instance():
        """
        Return singleton instance. Instantiate first if needed.
        Returns:
            Config: instance of Config
        """
        if Config._instance is None:
            Config._is_initialize_allowed = True #The only allowed case of instantiation.
            Config._instance = Config()
        return Config._instance


    def _log_me(self):
        logging.info(Config.input_file_name + ":" + self.input_file_name)
        logging.info(Config.output_dir_name + ":" + self.output_dir_name)
        logging.info(Config.config_filename + ":" + self.config_json_name)

    # Dictionary keys for parse_cmd_line_args().
    input_file_name = "input_file"
    output_dir_name = "output_dir"
    config_filename = "c"
    def parse_cmd_line_args(self):
        import argparse
        """
        Set up and uses argparse to get expected config info.
        """
        arg_parser = argparse.ArgumentParser(prog="innovation_lab_assignments",
                                             description="Reads in CSV file of Google Form responses, and writes out a CSV file for every day and activity configured in daily_activities_config.json.")
        arg_parser.add_argument(Config.input_file_name, metavar="<input file>", help="Name of CSV file with form responses")
        arg_parser.add_argument(Config.output_dir_name, metavar="<output directory>",
                                help="Directory that the assignment_<day>.csv files are written.")
        arg_parser.add_argument("-" + Config.config_filename, help="Configuration file. Defaults to daily_activities_config.json.",
                                default="daily_activities_config.json",
                                metavar="JSON file")
        args_namespace = arg_parser.parse_args()
        args_dict = vars(args_namespace) #Convert to dict
        self.input_file_name = args_dict[Config.input_file_name]
        self.output_dir_name = args_dict[Config.output_dir_name]
        self.config_json_name = args_dict[Config.config_filename]

        self._cmd_line_args_parsed = True
        self._log_me()

    def load_config(self):
        from innovation_lab_assignments.functions import prepend_project_root_if_required
        from json import JSONDecodeError
        import json
        """
        Load sheets configuration from config_json_name JSON file into json_data.
        """
        if not self._cmd_line_args_parsed:
            message = "parse_cmd_line_args() must be called first."
            logging.error(message)
            raise RuntimeError(message)
        filename = prepend_project_root_if_required(self.config_json_name, self.project_root)

        try:
            with open(filename) as input_file:
                self.json_data = json.load(input_file)
        except FileNotFoundError:
            logging.error("JSON config file with filename " + filename + " not found")
        except JSONDecodeError:
            logging.error("JSON config file" + filename + " contains invalid JSON")

    def get_weight_factor(self, activity_name) -> float:
        """
        Return weight factor for the passed activity_name.
        The weight factors are found in json_data, loaded by load_config().
        Args:
            activity_name (str)
        Returns:
            float: weight factor
        """
        # Lazy-load weight_factor_dict.
        if self.weight_factor_dict is None:
            weight_factor_dict_list = self.json_data.get("activity_weight_factors")
            #                                       Normalize activity key to lower case.
            self.weight_factor_dict = {weight_factor_dict["activity"].lower() : weight_factor_dict["weight_factor"]
                                       for weight_factor_dict in weight_factor_dict_list}

        return self.weight_factor_dict.get(activity_name)