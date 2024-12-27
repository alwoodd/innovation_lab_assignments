from config_editor.classes import *
from config_editor.functions import *
from innovation_lab_assignments.classes import Config

def main():
    config = Config.get_instance()
    config.load_config()

    app_widget_store = AppWidgetStore.get_instance()

    main_window = Tk()
    main_window.title("Config Editor")
    # TODO icon
    # main_window.iconbitmap()
    app_widget_store.add_widget(main_window, AppWidgetId.MAIN_WINDOW)

    day_frame = ttk.Frame(main_window, padding=20)  # , relief=RIDGE)
    day_frame.grid()

    # main_window.rowconfigure(index=[0,1], weight=1)
    main_window.columnconfigure(index=0, weight=1)

    mock_sheets_dict_list = [{'sheet': {'activities':
        [
            {'activity': 'Athletics', 'cap': 'no cap'},
            {'activity': 'Genius Grant', 'cap': 8},
            {'activity': 'Serving Seniors', 'cap': 14},
            {'activity': 'Cricut Crafts', 'cap': 8},
            {'activity': 'STUCO', 'cap': 'no cap'},
            {'activity': 'Baseball/Softball', 'cap': 'no cap'},
            {'activity': 'Dungeons & Dragons', 'cap': 'no cap'},
            {'activity': 'Math Tutoring', 'cap': 'no cap'},
            {'activity': 'Table Tennis/Ping Pong', 'cap': 8}],
        'day': 'Monday'}},
        {'sheet': {'activities':
            [
                {'activity': 'Athletics', 'cap': 'no cap'},
                {'activity': 'Genius Grant', 'cap': 8},
                {'activity': 'Woodshop', 'cap': 8},
                {'activity': 'Chess', 'cap': 'no cap'},
                {'activity': 'Praise Team', 'cap': 'no cap'},
                {'activity': 'Baseball/Softball Training', 'cap': 25},
                {'activity': 'Robotics', 'cap': 'no cap'},
                {'activity': 'Basketball Training', 'cap': 25},
                {'activity': 'Morning Announcements', 'cap': 4},
                {'activity': 'Masterclass', 'cap': 'no cap'}],
            'day': 'Tuesday'}}
    ]
    activity_widget_manager = ActivityWidgetsManager.get_instance()
    activity_widget_manager.init(mock_sheets_dict_list)

    ttk.Label(day_frame, text="Select Day:").grid(row=0, column=0, padx=5)
    days = activity_widget_manager.get_all_days()
    day_combo = ttk.Combobox(day_frame, values=days)
    day_combo.grid(row=0, column=1)
    day_combo.bind("<<ComboboxSelected>>", on_combo_select)
    day_combo.set(days[0])  # Select the first item in the list.
    app_widget_store.add_widget(day_combo, AppWidgetId.DAY_COMBO)

    activities_frame = ttk.Frame(main_window, padding=20)
    activities_frame.grid(sticky=W + E)  # row=1, column=0
    activities_frame.columnconfigure(index=0, weight=1)
    # activities_frame.rowconfigure(index=[0,1,2,3], weight=1)
    app_widget_store.add_widget(activities_frame, AppWidgetId.ACTIVITIES_FRAME)

    ttk.Label(activities_frame, text="Cap:").grid(row=0, column=1, sticky=W, padx=activity_widget_pad_x)

    build_activity_rows(activities_frame, day_combo.get())

    add_activity_frame = ttk.Frame(main_window)
    add_activity_frame.grid(sticky=W + E)
    ttk.Button(add_activity_frame, text="+Add Activity", command=on_click_add).pack(pady=5)

    save_exit_frame = ttk.Frame(main_window, padding=(10, 10))  # , relief=RIDGE)
    save_exit_frame.grid(sticky=W + E)
    save_exit_frame.columnconfigure(index=0, weight=1)

    ttk.Button(save_exit_frame, text="Save", command=on_click_save).grid(row=0, column=0, padx=20, sticky=W)
    ttk.Button(save_exit_frame, text="Exit", command=on_click_exit).grid(row=0, column=1, padx=20, sticky=W)

    main_window.mainloop()
