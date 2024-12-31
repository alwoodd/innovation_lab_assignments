import csv
from pathlib import PurePath

from innovation_lab_assignments.classes import *
import logging

def read_input_records(filename) ->[dict]:
    """
    Read input records from a CSV file.
    Args:
        filename (str): CSV file name
    Returns: [dict]
    """
    input_records = []

    try:
        with open(filename, "r") as input_file:
            csv_reader = csv.DictReader(input_file)
            stripped_fieldnames = []
            #Iterate reader's fieldnames and strip off leading and trailing spaces.
            for fieldname in csv_reader.fieldnames:
                stripped_fieldnames.append(fieldname.strip())
            csv_reader.fieldnames = stripped_fieldnames

            input_records = [input_record for input_record in csv_reader]
    except FileNotFoundError:
        logging.error("Input records with filename " + filename + " not found")

    return input_records

def students_with_activity_choice(students, activity_choice, day, priority) -> [Student]:
    """
    Creates list of students who have activity_choice for the passed day, at the passed priority,
    and is_available_for_day().
    Args:
        students ([Student]): students to be evaluated.
        activity_choice (Activity): activity to be considered.
        day (str): day to be considered.
        priority (int) priority to be considered.
    Returns:
        [Student]: List of students for passed in activity.
    """
    student_candidates: list[Student] = []

    def choice_filter(choice):
        """
        Inner Filter Function for filter() call below.
        Return True if the passed choice's priority is the priority passed into the outer function,
        and the choice's name is the activity choice name passed into the outer function.
        """
        return True if choice.priority == priority and choice.name == activity_choice.name else False

    for student in students:
        if student.is_available_for_day(day):
            # Filter all the student's choices for the day to just the passed in activity choice.
            # This filtered list may be empty (len == 0).
            all_student_choices = getattr(student, day + "_choices")
            student_day_choices = list(filter(choice_filter, all_student_choices))
            # If this student chose this activity, append to student_candidates.
            if len(student_day_choices) > 0:
                student_candidates.append(student)

    return student_candidates

def mark_students_selected_for_day(student_candidates, day, priority):
    """
    Call set_selection_priority_for_day() for every student candidate.
    """
    for student in student_candidates:
        student.set_selection_priority_for_day(priority, day)

def activities_to_rows(activities, dict_row_manager):
    """
    For all the passed activities, for each of their respective students,
    populate each of the activity's students using the passed dict_row_manager.
    Args:
          activities ([Activity])
          dict_row_manager (DictRowManager): Instance of DictRowManager
    """
    for activity in activities:
        students: [Student] = activity.students
        for i in range(0, len(students)):
            row_dict = dict_row_manager.get_row(i)
            row_dict[activity.name] = students[i].first_name + " " + students[i].last_name

def write_output_sheet(sheet_rec: SheetRec, output_dir: str):
    """
    Write passed sheet_rec to a csv file named "assignment_<day>".
    For example, if sheet_rec.day is Monday, the file name will be
    assignment_Monday.csv.
    Args:
        sheet_rec ([SheetRec])
        output_dir (str): Directory name to prepend to file name.
    """
    csv_name = output_dir + "/assignment_" + sheet_rec.day + ".csv"
    activity_field_names = [activity.name for activity in sheet_rec.activities]

    dict_row_manager = DictRowManager(activity_field_names)
    activities_to_rows(sheet_rec.activities, dict_row_manager)

    with open(csv_name, "w", newline="") as csv_file:
        # Ignore PyCharm's goofy 'Expected type SupportsWrite[str]'. The code works fine as-is.
        # noinspection PyTypeChecker
        csv_writer = csv.DictWriter(csv_file, activity_field_names)
        csv_writer.writeheader()
        csv_writer.writerows(dict_row_manager.get_all_rows())

def debug_log_randomized_students(students: [Student], day, activity):
    logging.debug("Randomized students for " + day + ", " + activity + ":")
    for student in students:
        logging.debug(student.first_name + ", " + student.last_name + "\t" + str(student.timestamp))

def prepend_project_root_if_required(filename: str, project_root: str) -> str:
    """
    If filename does not have the full path name, prepend project_root to it.
    Args:
        filename (str): filename to check.
    Returns:
        str: filename that already had a path, or filename with project_root for its path.
    """
    if not PurePath(filename).is_absolute():#os.path.isabs(filename):
        filename = str(PurePath(project_root).joinpath(filename))
        #filename = project_root + "\\" + filename

    return filename