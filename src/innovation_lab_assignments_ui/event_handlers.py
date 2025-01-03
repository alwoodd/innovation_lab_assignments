from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import showerror, showinfo

from innovation_lab_assignments_ui.functions import *

def on_click_open_CSV():
        filename = askopenfilename(title="CSV File", filetypes=[
            ("CSV Files", "*.csv"),
            ("All Files", "*.*")
        ], defaultextension="csv")

        if filename != "":
            run_config = get_saved_run_config()
            run_config.input_csv.set(filename)


def on_click_open_config():
    filename = askopenfilename(title="Configuration File", filetypes=[
        ("JSON Files", "*.json"),
        ("All Files", "*.*")
    ], defaultextension="json")

    if filename != "":
        run_config = get_saved_run_config()
        run_config.daily_activities_config_file.set(filename)


def on_click_go():
    from innovation_lab_assignments.functions import main_loop
    from innovation_lab_assignments.classes import Config
    save_run_config()

    run_config = get_saved_run_config()
    config = Config.get_instance()

    if not run_config.is_valid():
        showerror(message="A parameter is missing.")
    else:
        config.input_file_name = run_config.input_csv.get()
        config.output_dir_name = run_config.output_dir.get()
        config.load_config_with(run_config.daily_activities_config_file.get())

        return_code = main_loop()
        if return_code != 0:
            showerror(title="Failed", message="Run from the command line and look for errors.")
        else:
            showinfo(message="Done")
            get_main_window().destroy()

def on_click_open_folder():
    folder = askdirectory(title="Output Folder")

    if folder != "":
        run_config = get_saved_run_config()
        run_config.output_dir.set(folder)