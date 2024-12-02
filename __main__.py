_DEBUG = False
def _debug(message):
    if _DEBUG:
        print(message)

_debug("STARTING __main__.py")

import sys
import os

# Get the path of the file from which this module was loaded.
project_root  = os.path.dirname(os.path.abspath(__file__))
# Make sure it is part of sys.path
if project_root not in sys.path:
    sys.path.append(project_root)

# Store this for later use.
from src.classes import Config
Config.get_instance().project_root = project_root

_debug("sys.path:")
for p in sys.path:
    _debug(p)

if __name__ == "__main__":
    from src.main import main
    _debug("INSIDE if")
    main()