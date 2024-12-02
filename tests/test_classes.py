import sys
from unittest import TestCase
from classes import *
import datetime

class ClassTests(TestCase):
    def test_Student_init(self):
        student_dict = {'I am currently participating in at least one LHS sport.': 'No',
                        'I understand that disciplinary issues could result in not receiving credit for Innovation Lab.': "I understand",
                        'I understand that my participation and effort in the selections I have made will determine if I am able to stay in each offering.': "I understand",
                        'Monday First Choice': 'College Essays', 'Monday Second Choice': 'Serving Seniors', 'Monday Third Choice': 'SAT/ACT Prep',
                        'Tuesday First Choice': 'Classic Vehicle Restoration', 'Tuesday Second Choice': 'Graphic Signs', 'Tuesday Third Choice': 'Robotics',
                        'Wednesday First Choice': 'Praise Team', 'Wednesday Second Choice': 'Serving Seniors', 'Wednesday Third Choice': 'Science Fair',
                        'Thursday First Choice': 'Morning Announcements', 'Thursday Second Choice': 'Robotics', 'Thursday Third Choice': 'Athletics',
                        'Timestamp': '10/28/2024 17:50:32',
                        'Type your first name': 'Scott', 'Type your last name': 'Mitchell'}
        # Create a student
        student: Student = Student(student_dict, 10)

        self.assertEqual(student.first_name, "Scott")
        self.assertEqual(student.last_name, "Mitchell")
        self.assertEqual(student.timestamp, datetime.datetime(2024, 10, 28, 17, 50, 32))
        self._test_student_choices(student.monday_choices, ["College Essays", "Serving Seniors", "SAT/ACT Prep"])
        self._test_student_choices(student.tuesday_choices, ["Classic Vehicle Restoration", "Graphic Signs", "Robotics"])
        self._test_student_choices(student.wednesday_choices, ["Praise Team", "Serving Seniors", "Science Fair"])
        self._test_student_choices(student.thursday_choices, ["Morning Announcements", "Robotics", "Athletics"])
        self.assertEqual(student.in_athletics, False)
        self.assertEqual(student.credit_agreement, True)
        self.assertEqual(student.effort_agreement, True)
        self.assertEqual(student.student_id, 10)

    def _test_student_choices(self, choices: [Choice], choice_names: [str]):
        choice_item = 0
        for choice in choices:
            self.assertEqual(choice.name, choice_names[choice_item])
            self.assertEqual(choice.priority, choice_item + 1)
            choice_item = choice_item + 1

    def test_SheetRec_init(self):
        sheet_dict =  {'day': 'Tuesday',
                          'activities':
                               [{'activity': 'Athletics', 'cap': 'no cap'},
                                {'activity': 'Genius Grant- TBD on if your grant is selected by Mr. Eickstead and Mrs. Rikard', 'cap': 8},
                                {'activity': 'Wood Working', 'cap': 8},
                                {'activity': 'Robotics', 'cap': 'no cap'},
                                {'activity': 'Graphic Signs', 'cap': 10},
                                {'activity': 'Praise Team', 'cap': 'no cap'},
                                {'activity': 'Classic Vehicle Restoration', 'cap': 8},
                                {'activity': 'Morning Announcements', 'cap': 4},
                                {'activity': 'Basketball Training', 'cap': 25}]
                       }

        # Create a Sheet_Rec
        sheet_rec = SheetRec(sheet_dict)

        self.assertEqual(sheet_rec.day, "Tuesday")
        data_dict_list = [{'activity': 'Athletics', 'cap': sys.maxsize},
                                {'activity': 'Genius Grant- TBD on if your grant is selected by Mr. Eickstead and Mrs. Rikard', 'cap': 8},
                                {'activity': 'Wood Working', 'cap': 8},
                                {'activity': 'Robotics', 'cap': sys.maxsize},
                                {'activity': 'Graphic Signs', 'cap': 10},
                                {'activity': 'Praise Team', 'cap': sys.maxsize},
                                {'activity': 'Classic Vehicle Restoration', 'cap': 8},
                                {'activity': 'Morning Announcements', 'cap': 4},
                                {'activity': 'Basketball Training', 'cap': 25}]
        self._test_sheet_activities(sheet_rec.activities, data_dict_list)

    def _test_sheet_activities(self, activities: [Activity], activity_data: [dict]):
        activity_item = 0
        for activity in activities:
            self.assertEqual(activity.name, activity_data[activity_item]["activity"])
            self.assertEqual(activity.cap, activity_data[activity_item]["cap"])
            activity_item = activity_item + 1

    def test_Activity_init(self):
        activity_dict = {"activity":"rowing", "cap" : 99}
        activity = Activity(activity_dict)
        self.assertEqual(activity.name, "rowing")
        self.assertEqual(activity.cap, 99)

    def test_Choice_init(self):
        choice = Choice("Monday Fourth Choice", 1)
        self.assertEqual(choice.name, "Monday Fourth Choice")
        self.assertEqual(choice.priority, 1)