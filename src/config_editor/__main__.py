# Get the path of the file from which this module was loaded.
import os
import sys

project_root  = os.path.dirname(os.path.abspath(__file__))
# Make sure it is part of sys.path
if project_root not in sys.path:
    sys.path.append(project_root)

# Store this for later use.
from innovation_lab_assignments.classes import Config
Config.get_instance().project_root = project_root

if __name__ == "__main__":
    from config_editor.main import main
    main()