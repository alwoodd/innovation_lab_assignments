from tkinter import ttk
from config_editor.event_handlers import *
from config_editor.classes import *

def build_activity_rows(activities_frame, day: str):
    """
    Iterate the activities for the passed day, and call create_row_widgets_for() for each of them.
    Args:
        activities_frame (Frame): The parent Frame for the created widgets.
        day (str): Activities for this day.
    """
    #Remove existing rows
    ActivityWidgetRowManager.get_instance().remove_all_rows()

    activities = ActivityWidgetsManager.get_instance().get_activity_widgets_for_day(day)

    for activity in activities:
        create_row_widgets_for(activity, activities_frame, day)

def create_row_widgets_for(activity: ActivityWidget, frame: ttk.Frame, day: str):
    """
    Create all the Widgets that correspond to the members of an ActivityWidget,
    then use ActivityWidgetRowManager.add_row() to add an ActivityWidgetRow for
    those Widgets.
    Args:
        activity (ActivityWidget): Input for creating widgets
        frame (ttk.Frame): Parent frame for created widgets
        day (str):
    """
    activity_widget_row_manager = ActivityWidgetRowManager.get_instance()
    row = activity_widget_row_manager.current_number_of_rows() + 1

    name_widget = ttk.Entry(frame, textvariable=activity.name_variable, width=30)
    cap_widget_state = "disabled" if activity.no_cap_boolean_variable.get() else "normal"
    cap_widget = ttk.Entry(frame, textvariable=activity.cap_variable, width=3,
                           state=cap_widget_state)
    no_cap_widget = ttk.Checkbutton(frame, text="No Cap", variable=activity.no_cap_boolean_variable,
                                    command=lambda r=row: on_check_no_cap(r))
    button_widget = ttk.Button(frame, text="Remove", command=lambda r=row: on_click_remove(r))

    activity_widget_row_manager.add_row(row, name_widget, cap_widget, no_cap_widget, button_widget, day)