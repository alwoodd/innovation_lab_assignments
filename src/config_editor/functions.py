import json
from pathlib import Path
from tkinter import ttk
from config_editor.classes import *
from innovation_lab_assignments.classes import Config

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
    from config_editor.event_handlers import on_check_no_cap, on_click_remove

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

def load_widget_data(filename):
    """
    Call Config.load_config_with() using passed filename, then
    load ActivityWidgetManager sheets using Config.get_sheets().
    Set the day_combo using ActivityWidgetManager.get_all_days().
    Call build_activity_rows()
    """
    activity_widget_manager = ActivityWidgetsManager.get_instance()
    config = Config.get_instance()

    config.load_config_with(filename)
    activity_widget_manager.load_sheets(config.get_sheets())

    days = activity_widget_manager.get_all_days()
    app_widget_store = AppWidgetStore.get_instance()
    day_combo = app_widget_store.get_widget(AppWidgetId.DAY_COMBO)
    day_combo.configure(values = days)
    day_combo.set(days[0])  # Select the first item in the list.

    build_activity_rows(AppWidgetStore.get_instance().get_widget(AppWidgetId.ACTIVITIES_FRAME), days[0])

    #Enable previously disabled widgets.
    day_combo.configure(state = "normal")
    app_widget_store.get_widget(AppWidgetId.SAVE_BUTTON).configure(state = "normal")
    app_widget_store.get_widget(AppWidgetId.ADD_ACTIVITY_BUTTON).configure(state="normal")

##########################################################################################
CONFIG_EDITOR_CONFIG_FILE = "config_editor.json"

def get_saved_config_filename() ->str:
    """
    Returns: str The name of the sheets json from CONFIG_EDITOR_CONFIG_FILE
    If CONFIG_EDITOR_CONFIG_FILE cannot be found, or the sheets json does
    not exist, "" is returned.
    Returns: str
    """
    from innovation_lab_assignments.functions import prepend_project_root_if_required
    from json import JSONDecodeError
    # Open and read CONFIG_EDITOR_CONFIG_FILE if it exists.
    config_file_name = "" #This is the file to use with Config.load_config_with().
    full_path = prepend_project_root_if_required(CONFIG_EDITOR_CONFIG_FILE,
                                                 Config.get_instance().project_root)
    if Path(full_path).exists():
        try:
            with open(full_path) as input_file:
                config_file_content = json.load(input_file)
        except JSONDecodeError:
            # We found the file, but its contents are malformed.
            return config_file_name

        config_file_name = config_file_content.get("config_file_name")
        if config_file_name is None or not Path(config_file_name).exists():
            config_file_name = ""

    return config_file_name

def save_config_filename(filename: str):
    """
    Save the passed filename into CONFIG_EDITOR_CONFIG_FILE
    Args: filename (str)
    """
    from innovation_lab_assignments.functions import prepend_project_root_if_required
    full_path = prepend_project_root_if_required(CONFIG_EDITOR_CONFIG_FILE,
                                                 Config.get_instance().project_root)
    config_file_content = {"config_file_name": filename}
    with open(full_path, mode="w") as out_file:
        # noinspection PyTypeChecker
        json.dump(config_file_content, out_file)