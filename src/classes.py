import argparse
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
    def __init__(self, student_dict: dict):
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
        self.timestamp = datetime.strptime(student_dict["Timestamp"], "%m/%d/%Y %H:%M:%S")

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
    '''
    Parses the command line args, then stores them as an instance of Config.
    '''
    input_file = "input_file"
    output_dir = "output_dir"
    config_filename = "c"

    def _log_me(self):
        logging.info(Config.input_file + ":" + self.input_file)
        logging.info(Config.output_dir + ":" + self.output_dir)
        logging.info(Config.config_filename + ":" + self.config_json)

    @staticmethod
    def parse_cmd_line_args():
        '''
        Static method that sets up and uses argparse to get expected config info.
        Returns:
             Config: instance of Config
        '''
        arg_parser = argparse.ArgumentParser(prog="innovation_lab_assignments",
                                             description="Reads in CSV file of Google Form responses, and writes out a CSV file for every day and activity configured in daily_activities_config.json.")
        arg_parser.add_argument(Config.input_file, metavar="<input file>", help="Name of CSV file with form responses")
        arg_parser.add_argument(Config.output_dir, metavar="<output directory>",
                                help="Directory that the assignment_<day>.csv files are written.")
        arg_parser.add_argument("-" + Config.config_filename, help="Configuration file. Defaults to daily_activities_config.json.",
                                default="daily_activities_config.json",
                                metavar="JSON file")
        args_namespace = arg_parser.parse_args()
        args_dict = vars(args_namespace) #Convert to dict
        instance = Config(args_dict)
        instance._log_me()
        return instance

    def __init__(self, args_dict: dict):
        '''
        Initialize Config
        Args:
            args_dict (dict): dict with expected arg values
        '''
        self.input_file = args_dict[Config.input_file]
        self.output_dir = args_dict[Config.output_dir]
        self.config_json = args_dict[Config.config_filename]