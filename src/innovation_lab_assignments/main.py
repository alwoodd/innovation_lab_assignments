from innovation_lab_assignments.functions import *
from innovation_lab_assignments.random_select import randomize_students
from innovation_lab_assignments.classes import Config
from my_utilities import init_log
import logging

log_file_name = "innovation_lab_assignment.log"

def _die():
    logging.error("Unable to continue")

def main():
    config = Config.get_instance()
    init_log(prepend_project_root_if_required(log_file_name, config.project_root), logging_level=logging.DEBUG, truncate_log=True)

    config.parse_cmd_line_args()

    input_records_dict_list = read_input_records(config.input_file_name)
    logging.info("%i records to process", len(input_records_dict_list))
    if len(input_records_dict_list) == 0:
        return _die()
    # Create a list of Student from input_records_dict_list. The student_id generated using enumerate().
    students = [Student(student_dict, student_id) for student_id, student_dict in enumerate(input_records_dict_list, 1)]

    config.load_config()
    logging.info("Config file contents:\n" + str(config.json_data))
    if len(config.json_data) == 0:
        return _die()
    # Create a list of Sheet_Rec from sheets data in config.json_data.
    sheet_recs = [SheetRec(sheet_dict["sheet"]) for sheet_dict in config.get_sheets()]

    for sheet_rec in sheet_recs:
        for priority in range(1, 4):
            for activity in sheet_rec.activities:
                # If activity cap has not yet been reached...
                if len(activity.students) < activity.cap:
                    # Get all still-available students who want this activity at the current priority.
                    student_candidates = students_with_activity_choice(students, activity, sheet_rec.day.lower(), priority)
                    # If the number of student candidates exceeds the activity's remaining cap,
                    # randomize_students() using the candidates, then select from that list up to the remaining cap value,
                    # starting with beginning of the list.
                    remaining_cap = activity.cap - len(activity.students)
                    if len(student_candidates) > remaining_cap:
                        student_candidates = randomize_students(student_candidates, activity)
                        debug_log_randomized_students(student_candidates, sheet_rec.day, activity.name)
                        # Use only the first student through the remaining cap.
                        student_candidates = student_candidates[0: remaining_cap]

                    activity.students.extend(student_candidates)
                    mark_students_selected_for_day(student_candidates, sheet_rec.day.lower(), priority)

    '''
    Output a sheet CSV for every sheet_rec.
    '''
    for sheet_rec in sheet_recs:
        write_output_sheet(sheet_rec, config.output_dir_name)

    logging.info("Done")