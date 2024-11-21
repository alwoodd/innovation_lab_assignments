import random
from classes import *

_current_time = datetime.now()

def _calculate_weight_using_timestamp(input_timestamp: datetime):
    '''
    Calculate difference between current_time and input_timestamp in seconds,
    subtract a random offset, then returns that value.
    Args:
        input_timestamp (datetime): datetime to subtract from current_time
    Returns:
        float:
    '''
    time_diff_seconds = (_current_time - input_timestamp).total_seconds()
    # random_offset is a value between 0 and (time_diff_seconds * factor).
    random_offset = random.uniform(0, time_diff_seconds * .1)
    return time_diff_seconds - random_offset

def random_select_students(student_candidates: [Student]) -> [Student]:
    '''
    Randomize the passed students.
    Args:
        student_candidates ([Student])
    Returns:
        [Student]: List of randomized students.
    '''
    # Create a list of tuples using each student and their calculated weights. Each tuple is a student and weight.
    student_with_weights = [(student, _calculate_weight_using_timestamp(student.timestamp)) for student in student_candidates]

    # sorted() returns a new list (of above tuples in this case). The key is the weight part of the tuple.
    sorted_students = sorted(student_with_weights, key=lambda student_tuple: student_tuple[1], reverse=True)
    # Iterate sorted_students, with the student going to student, and the weight going to weight (which is ignored)
    # during each iteration.
    # Finally, create a list of just students (not the student tuples) using each student via list comprehension.
    sorted_students = [student for student, discarded_weight in sorted_students]

    # Randomize the sorted list
    #random.shuffle(sorted_students)

    return sorted_students