from tkinter.messagebox import askyesno
from tkinter.filedialog import askopenfilename
from config_editor.functions import *
from config_editor.classes import *
from innovation_lab_assignments.classes import Config

def on_check_no_cap(row_key):
    activity_widget_row: [ActivityWidgetRow] = ActivityWidgetRowManager.get_instance().get_row(row_key)
    checkbutton_variable = activity_widget_row.no_cap_widget.cget("variable")
    is_checked: str = (AppWidgetStore.get_instance().get_widget(AppWidgetId.MAIN_WINDOW)
                       .globalgetvar(checkbutton_variable))

    # is_checked is 1 when changing from not checked to checked, and
    # 0 when changing from checked to not checked
    if is_checked == "1":
        activity_widget_row.cap_widget.configure(state="disabled")
    else:
        activity_widget_row.cap_widget.configure(state="normal")


def on_click_remove(row_key):
    """
    Remove both the ActivityWidgetRow and ActivityWidget for the passed row_key,
    using their respective Manager classes.
    Args:
        row_key (int): row number
    """
    activity_widget_row_manager = ActivityWidgetRowManager.get_instance()
    activity_widget_row = activity_widget_row_manager.get_row(row_key)
    activity_name = activity_widget_row.get_activity_name()
    day = activity_widget_row.day
    ActivityWidgetsManager.get_instance().remove_activity_for_day(activity_name, day)

    activity_widget_row_manager.remove_row(row_key)

def on_click_save():
    new_sheets_list = ActivityWidgetsManager.get_instance().make_sheets_list()
    config = Config.get_instance()
    config.set_sheets(new_sheets_list)
    config.save_config()

def on_click_exit():
    ok_exit = True
    if ActivityWidgetsManager.get_instance().is_widgets_changed():
        ok_exit = askyesno("Unsaved changes", message="Exit without saving?")

    if ok_exit:
        AppWidgetStore.get_instance().get_widget(AppWidgetId.MAIN_WINDOW).destroy()

def on_click_add():
    """
    Create and add both an ActivityWidgetRow and ActivityWidget
    using their respective Manager classes.
    """
    app_widget_store = AppWidgetStore.get_instance()
    day = app_widget_store.get_widget(AppWidgetId.DAY_COMBO).get()
    new_activity = ActivityWidgetsManager.get_instance().create_new_activity_for_day(day)
    create_row_widgets_for(new_activity, app_widget_store.get_widget(AppWidgetId.ACTIVITIES_FRAME), day)

def on_combo_select(event):
    day_combo = event.widget
    activities_frame = AppWidgetStore.get_instance().get_widget(AppWidgetId.ACTIVITIES_FRAME)
    build_activity_rows(activities_frame, day_combo.get())

def on_click_load():
    filename = askopenfilename(
        title="Configuration File",
        filetypes=[
            ("JSON Files", "*.json"),
            ("All Files", "*.*")
        ],
        defaultextension="json")

    if filename != "":
        save_config_filename(filename)
        load_widget_data(filename)