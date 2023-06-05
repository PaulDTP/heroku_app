'''
Authored by Isaiah Terrell-Perica
06/04/2023
This file handles Zeppelin's logging.

DEBUG
Detailed information, typically of interest only when diagnosing problems.

INFO
Confirmation that things are working as expected.

WARNING
An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.

ERROR
Due to a more serious problem, the software has not been able to perform some function.

CRITICAL
A serious error, indicating that the program itself may be unable to continue running.
'''

import logging

# Setting configuration for log messages
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Creates a log message with severity and message
def log_status(severity, message):
    if severity == 'debug':
        logging.debug(message)
    elif severity == 'info':
        logging.info(message)
    elif severity == 'warning':
        logging.warning(message)
    elif severity == 'error':
        logging.error(message)
    elif severity == 'critical':
        logging.critical(message)
    else:
        logging.warning(f"Incorrect usage of log_status call. Message: {severity}:{message}")