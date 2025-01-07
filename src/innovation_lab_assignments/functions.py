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
            if csv_reader.fieldnames is not None:
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
            all_student_choices = getattr(student, day.lower() + "_choices")
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

def activities_to_rows(activities, dict_row_manager: DictRowManager):
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

def build_days_dict_row_manager(students: [Student], days)-> DictRowManager:
    """
    Create and return a DictRowManager whose keys are days, and rows are
    student that is still available for a given day.
    Args:
        students ([Student]): Students to be considered.
        days ([str]): days to check for available students.
    Returns:
        DictRowManager
    """
    dict_row_manager = DictRowManager(days)

    for day in days:
        i = 0
        for student in students:
            if student.is_available_for_day(day):
                row_dict = dict_row_manager.get_row(i)
                row_dict[day] = student.first_name + " " + student.last_name
                i += 1

    return dict_row_manager

def write_require_manual_assignment(students: [Student], days, output_dir:str):
    """
    Write a CSV with students that are still available for each day.
    Args:
         students ([Student]): Students to be considered.
         days ([str]): CSV headings
         output_dir (str): Directory name to prepend to csv name.
    """
    csv_name = output_dir + "/require_manual_assignment.csv"
    dict_row_manager = build_days_dict_row_manager(students, days)

    with open(csv_name, "w", newline="") as csv_file:
        # noinspection PyTypeChecker
        csv_writer = csv.DictWriter(csv_file, days)
        csv_writer.writeheader()
        csv_writer.writerows(dict_row_manager.get_all_rows())

def debug_log_unselected_students(students: [Student], day, priority):
    logging.debug("Students still unselected for " + day + " after assigning priority " + str(priority) + " activities:")
    for student in students:
        if student.is_available_for_day(day):
            logging.debug(student.first_name + " " + student.last_name)

def cap_student_candidates(students: [Student], remaining_cap, day, priority, activity) ->[Student]:
    """
    From a passed list of randomized students, returns a list of students no longer then the remaining_cap.
    Also logs all of the passed randomized students, indicating which survived by making the cut.
    Args:
        students ([Student]): Randomized students
        remaining_cap (int): How many of the students that make the cut
        day (str): day for logging
        priority (int): priority for logging
        activity (str): activity name for logging
    Returns:
        [Student] surviving_students
    """
    # Inner function to do the logging.
    def _debug_log_randomized_students():
        logging.debug("Randomized students for " + day + ", priority " + str(priority) + ", " + activity + " (* indicates selected students:)")
        for student, indicator in students_with_indicator:
            logging.debug(student.first_name + " " + student.last_name + indicator + "\t\t" + str(student.timestamp))

    # Create list of students plus an initially empty indicator.
    students_with_indicator = [[student, ""] for student in students]
    # Cap-off the students list.
    surviving_students = students[0: remaining_cap]

    # Update the indicator for the surviving students with an "*".
    for i in range(len(surviving_students)):
        students_with_indicator[i][1] = "*"

    _debug_log_randomized_students()

    return surviving_students

#TODO Change to NOT pass in project_root.
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

    return filename

def die():
    logging.error("Unable to continue")
    return 1

def main_loop():
    from innovation_lab_assignments.random_select import randomize_students
    from innovation_lab_assignments.classes import Config
    config = Config.get_instance()
    success = 0

    input_records_dict_list = read_input_records(config.input_file_name)
    logging.info("%i records to process", len(input_records_dict_list))
    if len(input_records_dict_list) == 0:
        return die()

    # Create a list of Student from input_records_dict_list. The student_id is generated using enumerate().
    students = [Student(student_dict, student_id) for student_id, student_dict in enumerate(input_records_dict_list, 1)]

    # Create a list of Sheet_Rec from sheets data in config.json_data.
    sheet_recs = [SheetRec(sheet_dict["sheet"]) for sheet_dict in config.get_sheets()]

    for sheet_rec in sheet_recs:
        for priority in range(1, 4):
            for activity in sheet_rec.activities:
                # If activity cap has not yet been reached...
                if len(activity.students) < activity.cap:
                    # Get all still-available students who want this activity at the current priority.
                    student_candidates = students_with_activity_choice(students, activity, sheet_rec.day, priority)
                    # If the number of student candidates exceeds the activity's remaining cap,
                    # randomize_students() using the candidates, then select from that list up to the remaining cap value,
                    # starting with beginning of the list.
                    remaining_cap = activity.cap - len(activity.students)
                    if len(student_candidates) > remaining_cap:
                        student_candidates = randomize_students(student_candidates, activity)
                        # Use only the first student through the remaining cap.
                        student_candidates = cap_student_candidates(student_candidates, remaining_cap, sheet_rec.day, priority, activity.name)

                    activity.students.extend(student_candidates)
                    mark_students_selected_for_day(student_candidates, sheet_rec.day, priority)

            debug_log_unselected_students(students, sheet_rec.day, priority)

    '''
    Output a sheet CSV for every sheet_rec.
    '''
    for sheet_rec in sheet_recs:
        write_output_sheet(sheet_rec, config.output_dir_name)

    '''
    Write CSV with students not selected for any activities by day.
    '''
    days = [sheet_rec.day for sheet_rec in sheet_recs ]
    write_require_manual_assignment(students, days, config.output_dir_name)

    return success
