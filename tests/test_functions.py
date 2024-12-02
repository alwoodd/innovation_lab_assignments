from unittest import TestCase
from functions import *

class FunctionTests(TestCase):
    def test_eliminate_students_already_selected(self):
        # We don't care if all test students have the same dict. We only care about their student_id values.
        student_dict = {'I am currently participating in at least one LHS sport.': 'No',
                        'I understand that disciplinary issues could result in not receiving credit for Innovation Lab.': "I understand",
                        'I understand that my participation and effort in the selections I have made will determine if I am able to stay in each offering.': "I understand",
                        'Monday First Choice': 'College Essays', 'Monday Second Choice': 'Serving Seniors',
                        'Monday Third Choice': 'SAT/ACT Prep',
                        'Tuesday First Choice': 'Classic Vehicle Restoration', 'Tuesday Second Choice': 'Graphic Signs',
                        'Tuesday Third Choice': 'Robotics',
                        'Wednesday First Choice': 'Praise Team', 'Wednesday Second Choice': 'Serving Seniors',
                        'Wednesday Third Choice': 'Science Fair',
                        'Thursday First Choice': 'Morning Announcements', 'Thursday Second Choice': 'Robotics',
                        'Thursday Third Choice': 'Athletics',
                        'Timestamp': '10/28/2024 17:50:32',
                        'Type your first name': 'Scott', 'Type your last name': 'Mitchell'}

        # Our existing students have ids 0 - 4.
        existing_activity_students = []
        for student_id in range(5):
            existing_activity_students.append(Student(student_dict, student_id))

        # Generate candidates with ids 5 - 9.
        student_candidates = []
        for student_id in range(5,10):
            student_candidates.append(Student(student_dict, student_id))

        # Add a candidate with id 1. This student_id is already in existing_activity_students.
        student_candidates.append(Student(student_dict, 1))
        # Now we have 6 students in student_candidates.

        # remove_students_already_selected() should return a list with only student_ids 5 - 9,
        # as student_id 1 is already in existing_activity_students.
        revised_student_list = remove_students_already_selected(existing_activity_students, student_candidates)
        self.assertEqual(len(revised_student_list), 5)