'''
Authored by Isaiah Terrell-Perica
06/04/2023
This file handles Zeppelin's logging.

DEBUG
- Detailed information, typically of interest only when diagnosing problems.
INFO
- Confirmation that things are working as expected.
WARNING
- An indication that something unexpected happened, or indicative of some problem in the near future (e.g. `disk space low`). The software is still working as expected.
ERROR
- Due to a more serious problem, the software has not been able to perform some function.
CRITICAL
- A serious error, indicating that the program itself may be unable to continue running.
'''

import logging, logging.handlers
import sys

# Setting default configuration for All loggers
logging.basicConfig(
<<<<<<< HEAD
    # formatse each log line like so: 2024-01-03 10:04:25,148 - INFO - Data received.
=======
    # formats each log line like so: 2024-01-03 10:04:25,148 - INFO - Data received.
>>>>>>> simple
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)

# Creating main logger instance
log_handler = logging.StreamHandler()
memory_handler = logging.handlers.MemoryHandler(capacity=100, target=log_handler)
file_handler = logging.FileHandler('app.log')

# Initializing new logger and adding handlers
zep_log = logging.getLogger('Zeppelin')
zep_log.addHandler(memory_handler)
zep_log.addHandler(log_handler)
zep_log.addHandler(file_handler)

# Creating formatter from the basicConfig formatting
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Applying the formatter to each handler
log_handler.setFormatter(formatter)
memory_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

def get_logs():
    records = memory_handler.buffer.copy()
    return [x.getMessage() for x in records]

# Creates a custom log message with severity and message
def log_status(severity, message):
    if severity == 'debug':
        zep_log.debug(message)
    elif severity == 'info':
        zep_log.info(message)
    elif severity == 'warning':
        zep_log.warning(message)
    elif severity == 'error':
        zep_log.error(message)
    elif severity == 'critical':
        zep_log.critical(message)
    else:
<<<<<<< HEAD
        zep_log.warning(f"Incorrect usage of log status call. Message: {severity}:{message}")
=======
        zep_log.warning(f"Incorrect usage of log status call. Message: {severity}:{message}")
>>>>>>> simple
