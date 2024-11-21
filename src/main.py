from functions import *
from random_select import random_select_students
from my_utilities import init_log

input_filename = "C:/temp/Q1 2024 Innovation Lab Selections DRAFT (Responses) - Form Responses 1.csv"
log_file_name = "C:/temp/innovation_lab_assignment.log"
config_filename = "C:/Users/dalwo/PycharmProjects/innovation_lab_assignments/daily_activities_config.json"
output_dir = "C:/temp/"

'''
***************************************************************************************
'''
init_log(log_file_name)

input_records = read_input_records(input_filename)
logging.info("%i records to process", len(input_records))
students = create_students_list(input_records)

sheets_config = load_output_config(config_filename)
logging.info("Config file contents:\n" + str(sheets_config))
sheet_recs = create_sheets_list(sheets_config.get("sheets"))

for sheet_rec in sheet_recs:
    for activity in sheet_rec.activities:
        # For each activity, iterate up to priority 3.
        for priority in range(1, 4):
            # If activity cap has not yet been reached...
            if len(activity.students) < activity.cap:
                # Get all students who want this activity at the current priority.
                student_candidates = students_with_activity_choice(students, activity, sheet_rec.day.lower(), priority)
                # If the number of student candidates exceeds the activity's remaining cap,
                # random_select_students() from the candidates, then select from that list up to the remaining cap value,
                # starting with beginning of the list.
                remaining_cap = activity.cap - len(activity.students)
                if len(student_candidates) > remaining_cap:
                    student_candidates = random_select_students(student_candidates)
                    student_candidates = student_candidates[0: remaining_cap]

                activity.students.extend(student_candidates)
            else:
                # Else activity cap has been reached.
                break #for priority loop

'''
Output a sheet CSV for every sheet_rec.
'''
for sheet_rec in sheet_recs:
    write_output_sheet(sheet_rec, output_dir)

print("done")