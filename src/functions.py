import logging
import csv
import json
from json import JSONDecodeError
from classes import *

def read_input_records(filename):
    '''
    Read input records from a CSV file.
    Args:
        filename (str): CSV file name
    Returns: [dict]
    '''
    input_records = []

    try:
        with open(filename, "r") as input_file:
            csv_reader = csv.DictReader(input_file)
            stripped_fieldnames = []
            #Iterate reader's fieldnames and strip off leading and trailing spaces.
            for fieldname in csv_reader.fieldnames:
                stripped_fieldnames.append(fieldname.strip())
            csv_reader.fieldnames = stripped_fieldnames

            for input_record in csv_reader:
                input_records.append(input_record)
    except FileNotFoundError:
        logging.error("Input records with filename " + filename + " not found")

    return input_records

def load_output_config(filename):
    """
    Load sheets configuration from config_filename JSON file.
    Args:
        filename (str): JSON file name
    Returns:
        dict: content of config_file_name
    """
    json_data = {}
    try:
        with open(filename) as input_file:
            json_data = json.load(input_file)
    except FileNotFoundError:
        logging.error("JSON config file with filename " + filename + " not found")
    except JSONDecodeError:
        logging.error("JSON config file" + filename + " contains invalid JSON")

    return json_data

def create_sheets_list(sheets_dict: dict):
    '''
    Create a list of Sheet_Rec from passed dict.
    Args:
        sheets_dict (dict): sheets data as a dict (see load_output_config).
    Returns: list[Sheet_Rec]

    '''
    sheet_recs: list[SheetRec] = []
    for sheet_dict in sheets_dict:
        sheet_recs.append(SheetRec(sheet_dict["sheet"]))

    return sheet_recs

def create_students_list(students_dict_list: list) -> [Student]:
    students: list[Student] = []
    for student_dict in students_dict_list:
        students.append(Student(student_dict))

    return students

def students_with_activity_choice(students, activity_choice, day, priority) -> [Student]:
    '''
    Creates list of students who have activity_choice for the passed day, at the passed priority.
    Args:
        students ([Student]): students to be evaluated.
        activity_choice (Activity): activity to be considered.
        day (str): day to be considered.
        priority (int) priority to be considered.
    Returns:
        [Student]: List of students for passed in activity.
    '''
    student_candidates: list[Student] = []

    def choice_filter(choice):
        '''
        Inner Filter Function for filter() call below.
        Return True if the passed choice's priority is the priority passed into the outer function,
        and the choice's name is the activity choice name passed into the outer function.
        '''
        return True if choice.priority == priority and choice.name == activity_choice.name else False

    for student in students:
        # Filter all the student's choices for the day to just the passed in activity choice.
        # This filtered list may be empty (len == 0).
        all_student_choices = getattr(student, day + "_choices")
        student_day_choices = list(filter(choice_filter, all_student_choices))
        # If this student chose this activity, append to student_candidates.
        if len(student_day_choices) > 0:
            student_candidates.append(student)

    return student_candidates

def activities_to_rows(activities, dict_row_manager):
    '''
    For all the passed activities, for each of their respective students,
    populate each of the activity's students using the passed dict_row_manager.
    Args:
          activities ([Activity])
          dict_row_manager (DictRowManager): Instance of DictRowManager
    '''
    for activity in activities:
        students: [Student] = activity.students
        for i in range(0, len(students)):
            row_dict = dict_row_manager.get_row(i)
            row_dict[activity.name] = students[i].first_name + " " + students[i].last_name

def write_output_sheet(sheet_rec: SheetRec, output_dir: str):
    '''
    Write passed sheet_rec to a csv file named "assignment_<day>".
    For example, if sheet_rec.day is Monday, the file name will be
    assignment_Monday.csv.
    Args:
        sheet_rec ([SheetRec])
        output_dir (str): Directory name to prepend to file name.
    '''
    csv_name = output_dir + "assignment_" + sheet_rec.day + ".csv"
    activity_field_names = [activity.name for activity in sheet_rec.activities]

    dict_row_manager = DictRowManager(activity_field_names)
    activities_to_rows(sheet_rec.activities, dict_row_manager)

    with open(csv_name, "w", newline="") as csv_file:
        # Ignore PyCharm's goofy 'Expected type SupportsWrite[str]'. The code works fine as-is.
        # noinspection PyTypeChecker
        csv_writer = csv.DictWriter(csv_file, activity_field_names)
        csv_writer.writeheader()
        csv_writer.writerows(dict_row_manager.get_all_rows())