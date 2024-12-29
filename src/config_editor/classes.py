from innovation_lab_assignments.classes import Activity
from tkinter import *
import sys
import hashlib
from enum import Enum, auto

activity_widget_pad_x = 8

class ActivityWidget(Activity):
    """
    Extends Activity with tk.Variables
    Attributes:
        name_variable (StringVar): tk.Variable to bind to Widget
        cap_variable (IntVar): tk.Variable to bind to Widget
        no_cap_boolean_variable (BooleanVar): tk.Variable to bind to Widget

    """
    def __init__(self, activity_dict: dict):
        super().__init__(activity_dict)

        self.name_variable = StringVar(value=self.name)
        self.cap_variable = IntVar(value=self.cap)
        self.no_cap_boolean_variable = BooleanVar(value=False)

        self._set_checkbox()

    def _set_checkbox(self):
        """
        Sets cap_variable and no_cap_boolean_variable according to the self.cap value.
        """
        is_checked = True if self.cap == sys.maxsize else False
        self.no_cap_boolean_variable.set(is_checked)
        #Also initialize cap_variable to zero if is_checked.
        if is_checked:
            self.cap_variable.set(0)

    def __str__(self):
        return (
            f"name:{self.name},cap:{self.cap},name_variable:{self.name_variable.get()},"
            f"cap_variable:{self.cap_variable.get()},"
            f"no_cap_boolean_variable:{self.no_cap_boolean_variable.get()}"
        )

class ActivityWidgetsManager:
    """
    Singleton that manages all the ActivityWidgets for all days.
    get_activity_widgets_for_day(): Get all ActivityWidgets for a day
    make_sheets_list():
    get_all_days(): Get a list of days stored in this instance.
    remove_activity_for_day(): Remove passed ActivityWidget for the passed day.
    """
    _instance = None
    _is_initialize_allowed = False

    def __init__(self):
        """
        __init__() is only allowed to be run when _is_initialize_allowed.
        """
        if not ActivityWidgetsManager._is_initialize_allowed:
            message = "Only one instance is allowed. Use 'get_instance()'."
            raise RuntimeError(message)

        ActivityWidgetsManager._is_initialize_allowed = False
        self._activity_dict = {} #key: day, value: [ActivityWidget]
        self._initial_checksum = None

    def load_sheets(self, sheets_dict_list: [dict]):
        self._activity_dict.clear()
        for sheet_dict in sheets_dict_list:
            sheet_value = sheet_dict["sheet"]
            activity_widgets = self._create_activity_list(sheet_value["activities"])
            self._activity_dict[sheet_value["day"]] = activity_widgets

        self._initial_checksum = self._calculate_checksum()

    @staticmethod
    def _create_activity_list(activities_dict_list) ->[ActivityWidget]:
        activities_widget_list = []
        for activity_dict in activities_dict_list:
            activities_widget_list.append((ActivityWidget(activity_dict)))

        return activities_widget_list

    @staticmethod
    def get_instance():
        """
        Return singleton instance. Instantiate first if needed.
        Returns:
            ActivityWidgetsManager: instance of ActivityWidgetsManager
        """
        if ActivityWidgetsManager._instance is None:
            ActivityWidgetsManager._is_initialize_allowed = True #The only allowed case of instantiation.
            ActivityWidgetsManager._instance = ActivityWidgetsManager()
        return ActivityWidgetsManager._instance

    def _calculate_checksum(self) ->str:
        """
        Iterate all the ActivityWidgets in the _activity_dict, and concatenate
        all their __str__() into activities_str.
        Convert activities_str into a hash, then the hash to a checksum.
        Returns: str: checksum
        """
        activities_str = ""
        for day in iter(self._activity_dict):
            activities = self.get_activity_widgets_for_day(day)
            for activity in activities:
                activities_str += activity.__str__()

        hash_obj = hashlib.md5(activities_str.encode("utf-8"))
        checksum = hash_obj.hexdigest()
        return checksum

    def get_activity_widgets_for_day(self, day:str) ->[ActivityWidget]:
        """
        Args: day (str)
        Returns: [ActivityWidget] for the passed day.
        """
        activity_widgets = self._activity_dict[day]
        return activity_widgets

    def make_sheets_list(self) ->[dict]:
        """
        Convert all the managed ActivityWidgets into a list of dicts.
        This list can be used to replace the sheets value of the config file.
        Returns: [dict]
        """
        sheets_list = []
        for day in self._activity_dict.keys():
            activity_widgets = self.get_activity_widgets_for_day(day)
            activity_dict_list = []
            for activity_widget in activity_widgets:
                #If no_cap_boolean_variable is True, cap_value is sys.maxsize.
                #Otherwise, it is cap_variable.
                cap_value = sys.maxsize if activity_widget.no_cap_boolean_variable.get() else activity_widget.cap_variable.get()
                activity_dict_list.append({"activity": activity_widget.name_variable.get(),
                                           "cap": cap_value})

            sheets_list.append({"sheet":
                                    {"day": day,
                                        "activities": activity_dict_list
                                    }
                                })

        return sheets_list

    def get_all_days(self) ->[str]:
        """
        Return a list of managed days.
        Returns: [str]
        """
        dict_keys = self._activity_dict.keys()
        return list(dict_keys)

    def remove_activity_for_day(self, activity_name: str, day: str):
        """
        Remove ActivityWidget from manager for the passed activity name and day.
        Args:
            activity_name (str)
            day (str)
        """
        activity_widgets = self.get_activity_widgets_for_day(day)
        # Filter through activity_widgets and retrieve activity_widget with activity_name.
        widget_to_remove = next(activity_widget
                                for activity_widget in activity_widgets
                                    if activity_widget.name == activity_name)
        activity_widgets.remove(widget_to_remove)
        pass

    def create_new_activity_for_day(self, day: str) ->ActivityWidget:
        """
        Create an ActivityWidget with default values for the passed day.
        Args: day (str)
        Returns: ActivityWidget: new widget
        """
        new_activity = ActivityWidget({"activity": "TBD", "cap": "no cap"})
        current_activity_widgets: [ActivityWidget] = self.get_activity_widgets_for_day(day)
        current_activity_widgets.append(new_activity)
        return new_activity

    def is_widgets_changed(self) -> bool:
        """
        Compares the current checksum to the initial checksum.
        Returns: (bool) True checksums differ, else False.
        """
        is_changed = False
        #If _initial_checksum was never set, then assume not is_changed.
        if self._initial_checksum is not None:
            current_check_sum = self._calculate_checksum()
            is_changed = self._initial_checksum != current_check_sum

        return is_changed

###########################################################################

class ActivityWidgetRow:
    """
    Each instance is all the Widgets in a row on a grid.
    Attributes:
        name_widget (Widget)
        cap_widget (Widget)
        no_cap_widget (Widget)
        button_widget (Widget)
        day (str): Day this row is for.
    """
    def __init__(self, name_widget, cap_widget, no_cap_widget, button_widget, day):
        self.name_widget = name_widget
        self.cap_widget = cap_widget
        self.no_cap_widget = no_cap_widget
        self.button_widget = button_widget
        self.day = day

    def get_activity_name(self) ->str:
        return self.name_widget.get()

class ActivityWidgetRowManager:
    """
    Singleton that manages all the existing ActivityWidgetRows.
    New rows can be added with add_row()
    Existing rows can be retrieved with get_row(), and removed with remove_row().
    """
    _instance = None
    _is_initialize_allowed = False

    def __init__(self):
        """
        __init__() is only allowed to be run when _is_initialize_allowed.
        """
        if not ActivityWidgetRowManager._is_initialize_allowed:
            message = "Only one instance is allowed. Use 'get_instance()'."
            raise RuntimeError(message)

        ActivityWidgetRowManager._is_initialize_allowed = False
        self._activity_widget_row_dict = {}

    @staticmethod
    def get_instance():
        """
        Return singleton instance. Instantiate first if needed.
        Returns:
            ActivityWidgetRowManager: instance of ActivityWidgetRowManager
        """
        if ActivityWidgetRowManager._instance is None:
            ActivityWidgetRowManager._is_initialize_allowed = True #The only allowed case of instantiation.
            ActivityWidgetRowManager._instance = ActivityWidgetRowManager()
        return ActivityWidgetRowManager._instance

    def _configure_grid(self, row_key, pad_x):
        """
        For the ActivityWidgetRow at row_key, iterate its Widgets and call a standardized grid_configure().
        Args:
            row_key(int): row_key of activity_widget_row_dict
        """
        all_class_member_values: [Widget] = vars(self._activity_widget_row_dict[row_key]).values()
        col = 0
        pad_y = 2
        for widget in all_class_member_values:
            if isinstance(widget, Widget):
                widget.grid_configure(row=row_key, column=col, padx=pad_x, pady=pad_y)
                col += 1

    def add_row(self, row_key, name_widget, cap_widget, no_cap_widget, button_widget, day, pad_x=activity_widget_pad_x):
        self._activity_widget_row_dict[row_key] = ActivityWidgetRow(name_widget, cap_widget, no_cap_widget, button_widget, day)
        self._configure_grid(row_key, pad_x)

    def get_row(self, row_key) ->ActivityWidgetRow:
        return self._activity_widget_row_dict[row_key]

    def remove_row(self, row_key):
        all_activity_widget_row_members = vars(self._activity_widget_row_dict[row_key]).values()
        for member in all_activity_widget_row_members:
            if isinstance(member, Widget):
                member.destroy()

    def current_number_of_rows(self):
        return len(self._activity_widget_row_dict)

    def remove_all_rows(self):
        for row_key in self._activity_widget_row_dict.keys():
            self.remove_row(row_key)

class AppWidgetId(Enum):
    """
    This enum provides the keys used in AppWidgetStore.
    Add keys as necessary.
    """
    MAIN_WINDOW = auto()
    ACTIVITIES_FRAME = auto()
    DAY_COMBO = auto()
    SAVE_BUTTON = auto()
    ADD_ACTIVITY_BUTTON = auto()

class AppWidgetStore:
    """
    Singleton that manages all the existing AppWidgetStore.
    Use add_widget() to add a widget to the store.
    Use get_widget() to retrieve one.
    """
    _instance = None
    _is_initialize_allowed = False

    def __init__(self):
        """
        __init__() is only allowed to be run when _is_initialize_allowed.
        """
        if not AppWidgetStore._is_initialize_allowed:
            message = "Only one instance is allowed. Use 'get_instance()'."
            raise RuntimeError(message)

        AppWidgetStore._is_initialize_allowed = False
        self._app_widget_store_dict = {}

    @staticmethod
    def get_instance():
        """
        Return singleton instance. Instantiate first if needed.
        Returns:
            AppWidgetStore: instance of AppWidgetStore
        """
        if AppWidgetStore._instance is None:
            AppWidgetStore._is_initialize_allowed = True #The only allowed case of instantiation.
            AppWidgetStore._instance = AppWidgetStore()
        return AppWidgetStore._instance

    def add_widget(self, widget, app_widget_id: AppWidgetId):
        self._app_widget_store_dict[app_widget_id] = widget

    def get_widget(self, app_widget_id: AppWidgetId):
        return self._app_widget_store_dict[app_widget_id]