from innovation_lab_assignments.classes import Config
from config_editor.event_handlers import *

def main():
    app_widget_store = AppWidgetStore.get_instance()

    main_window = Tk()
    main_window.title("Config Editor")
    # TODO icon
    # main_window.iconbitmap()
    app_widget_store.add_widget(main_window, AppWidgetId.MAIN_WINDOW)

    day_frame = ttk.Frame(main_window, padding=20)#, relief=RIDGE)
    day_frame.grid(row=0, column=0, sticky=W+E)

    ttk.Button(day_frame, text="Load Config", command=on_click_load).grid(row=0, column=0, padx=15, sticky=W)

    ttk.Label(day_frame, text="Select Day:").grid(row=0, column=1, padx=5)
    #days = activity_widget_manager.get_all_days()
    day_combo = ttk.Combobox(day_frame, state="disabled")
    day_combo.grid(row=0, column=2)
    day_combo.bind("<<ComboboxSelected>>", on_combo_select)
    #day_combo.set(days[0])  # Select the first item in the list.
    app_widget_store.add_widget(day_combo, AppWidgetId.DAY_COMBO)

    activities_frame = ttk.Frame(main_window, padding=20)
    activities_frame.grid(sticky=W + E)  # row=1, column=0
    activities_frame.columnconfigure(index=0, weight=1)
    # activities_frame.rowconfigure(index=[0,1,2,3], weight=1)
    app_widget_store.add_widget(activities_frame, AppWidgetId.ACTIVITIES_FRAME)

    ttk.Label(activities_frame, text="Cap:").grid(row=0, column=1, sticky=W, padx=activity_widget_pad_x)

    add_activity_frame = ttk.Frame(main_window)
    add_activity_frame.grid(sticky=W + E)
    add_activity_button = ttk.Button(add_activity_frame, text="+Add Activity", command=on_click_add, state="disabled")
    add_activity_button.pack(pady=5)
    app_widget_store.add_widget(add_activity_button, AppWidgetId.ADD_ACTIVITY_BUTTON)

    save_exit_frame = ttk.Frame(main_window, padding=(10, 10))  # , relief=RIDGE)
    save_exit_frame.grid(sticky=W + E)
    save_exit_frame.columnconfigure(index=0, weight=1)

    save_button = ttk.Button(save_exit_frame, text="Save", command=on_click_save, state="disabled")
    save_button.grid(row=0, column=0, padx=20, sticky=W)
    ttk.Button(save_exit_frame, text="Exit", command=on_click_exit).grid(row=0, column=1, padx=20, sticky=W)
    app_widget_store.add_widget(save_button, AppWidgetId.SAVE_BUTTON)

    config_file_name = get_saved_config_filename()
    if config_file_name == "":
        on_click_load()
    else:
        load_widget_data(config_file_name)

    main_window.mainloop()
