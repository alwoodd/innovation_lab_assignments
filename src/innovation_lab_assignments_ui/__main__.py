# Get the path of the file from which this module was loaded.
import pathlib
import sys

project_root = str(pathlib.PurePath(__file__).parent)
# Make sure it is part of sys.path
if project_root not in sys.path:
    sys.path.append(project_root)

# Store this for later use.
from innovation_lab_assignments.classes import Config
Config.get_instance().project_root = project_root

if __name__ == "__main__":
    from innovation_lab_assignments_ui.main import main
    main()