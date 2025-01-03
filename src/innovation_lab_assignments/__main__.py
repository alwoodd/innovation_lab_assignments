_DEBUG = False
def _debug(message):
    if _DEBUG:
        print(message)

_debug("STARTING __main__.py")

import sys
import pathlib

# Get the path of the file from which this module was loaded.
project_root  = str(pathlib.PurePath(__file__).parent)
# Make sure it is part of sys.path
if project_root not in sys.path:
    sys.path.append(project_root)

# Store this for later use.
from innovation_lab_assignments.classes import Config
Config.get_instance().project_root = project_root

_debug("sys.path:")
for p in sys.path:
    _debug(p)

if __name__ == "__main__":
    from innovation_lab_assignments.main import main
    _debug("INSIDE if")
    main()