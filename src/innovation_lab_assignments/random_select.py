import random
from innovation_lab_assignments.classes import *

_current_time = datetime.now() #datetime(month=11, day=29, year=2024, hour=12, minute=0, second=0)

def _calculate_weight_using_timestamp(input_timestamp: datetime):
    """
    Calculate difference between current_time and input_timestamp in seconds,
    then return the reciprocal. Earlier input_timestamps will have smaller reciprocals.
    Args:
        input_timestamp (datetime): datetime to subtract from current_time
    Returns:
        float:
    """
    time_diff_seconds = (_current_time - input_timestamp).total_seconds()
    # Add 1 to prevent division by zero, however unlikely.
    return max(1 / (time_diff_seconds + 1), 0)

def _add_activity_weight(activity: Activity, student_with_weight_tuple):
    """
    This function is unconditionally called to conditionally add an additional weight.
    Args:
        activity (Activity): activity to be considered.
        student_with_weight_tuple (tuple): tuple from randomize_students()
    Returns:
        float: activity_weight
    """
    activity_weight = student_with_weight_tuple[1] #Initialize returned activity weight to current weight.
    # If the passed activity is in the match-case below,
    # perform whatever action is needed to calculate a new activity_weight.
    match activity.name:
        case "Athletics":
            activity_weight = _athletics_weight(student_with_weight_tuple)
        # Any future activity weights can be added as additional cases.
        #case "Robotics":
        #    activity_weight = _robotics_weight()

    return activity_weight

def _athletics_weight(student_tuple):
    """
    If the passed student is in_athletics, add more weight to their weight.
    Args:
        student_tuple (tuple)
    Returns:
        float: adjusted_weight
    """
    student, weight = student_tuple
    adjusted_weight = weight
    if student.in_athletics:
        weight_factor_key = "athletics"
        weight_factor: float = Config.get_instance().get_weight_factor(weight_factor_key)
        if weight_factor is None:
            logging.error(f"Weight factor for {weight_factor_key} is None. Check {Config.get_instance().config_json_name}.")
        else:
            adjusted_weight = weight + weight_factor

    return adjusted_weight

def randomize_students(student_candidates: [Student], activity: Activity) -> [Student]:
    """
    Randomize the passed students.
    Args:
        student_candidates ([Student])
        activity (Activity)
    Returns:
        [Student]: List of randomized students.
    """
    # Create a list of tuples using each student and their calculated weights. Each tuple is a student and weight.
    students_with_weights = [(student, _calculate_weight_using_timestamp(student.timestamp)) for student in student_candidates]

    students_with_weights = [(student_tuple[0], _add_activity_weight(activity, student_tuple)) for student_tuple in students_with_weights]

    # Multiply each weight by a random value.
    students_with_weights = [(student, weight * random.random()) for student, weight in students_with_weights]

    # Sort the tuples by weights.
    # sorted() returns a new list (of above tuples in this case). The key is the weight part of the tuple.
    sorted_students = sorted(students_with_weights, key=lambda student_tuple: student_tuple[1])
    # Iterate sorted_students, with the student going to student, and the weight going to weight (which is ignored)
    # during each iteration.
    # Finally, create a list of just students (not the student tuples) using each student via list comprehension.
    sorted_students = [student for student, ignored_weight in sorted_students]

    # Randomize the sorted list
    #random.shuffle(sorted_students)

    return sorted_students