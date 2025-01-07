from tkinter import *
from tkinter import ttk
from my_utilities import init_log
import logging
from innovation_lab_assignments_ui.event_handlers import *
from innovation_lab_assignments_ui.functions import *
from innovation_lab_assignments.functions import prepend_project_root_if_required
from innovation_lab_assignments.classes import Config

log_file_name = "innovation_lab_assignment_ui.log"

def main():
    project_root = Config.get_instance().project_root
    init_log(prepend_project_root_if_required(log_file_name, project_root), logging_level=logging.DEBUG, truncate_log=True)

    main_window = get_main_window()
    main_window.title("Innovation Lab Assignments")
    icon_image_file = prepend_project_root_if_required("innovation lab icon.png", project_root)
    icon = PhotoImage(file=icon_image_file)
    main_window.wm_iconphoto(True, icon)
    main_window.grid_rowconfigure([0,2], weight=1, minsize=50)
    main_window.grid_columnconfigure([1], weight=1, minsize=8)

    run_config = get_saved_run_config()

    ttk.Label(main_window, text="CSV file with form responses").grid(row=0, column=0, padx=5)
    ttk.Label(main_window, textvariable=run_config.input_csv, background="white", padding=(0, 0, 10, 0)).grid(row=0, column=1, padx=5, sticky=E+W)
    ttk.Button(main_window, text="Open CSV", command=on_click_open_CSV).grid(row=0, column=2, padx=5, sticky=E)

    ttk.Label(main_window, text="Output folder").grid(row=1, column=0, padx=5, sticky=E)
    ttk.Label(main_window, textvariable=run_config.output_dir, background="white").grid(row=1, column=1, padx=5, sticky=E+W)
    ttk.Button(main_window, text="Open Folder", command=on_click_open_folder).grid(row=1, column=2, padx=5, sticky=E)

    ttk.Label(main_window, text="Config file").grid(row=2, column=0, padx=5, sticky=E)
    ttk.Label(main_window, textvariable=run_config.daily_activities_config_file, background="white").grid(row=2, column=1, padx=5, sticky=E+W)
    ttk.Button(main_window, text="Open Config", command=on_click_open_config).grid(row=2, column=2, padx=5, sticky=E)

    ttk.Button(main_window, text="Go", command=on_click_go).grid(row=3, column=1, sticky=S, pady=7, padx=12)

    main_window.mainloop()