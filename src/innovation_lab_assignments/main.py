from innovation_lab_assignments.functions import *
from innovation_lab_assignments.classes import Config
from my_utilities import init_log
import logging

log_file_name = "innovation_lab_assignment.log"

# def _die():
#     logging.error("Unable to continue")

def main():
    config = Config.get_instance()
    init_log(prepend_project_root_if_required(log_file_name, config.project_root), logging_level=logging.DEBUG, truncate_log=True)

    config.parse_cmd_line_args()

    config.load_config()
    logging.info("Config file contents:\n" + str(config.json_data))
    if len(config.json_data) == 0:
        return die()

    main_loop()

    logging.info("Done")