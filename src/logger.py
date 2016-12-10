"""
Create a log file handler which logs message to both the screen and the keyboard.
The logfile can be either a rotating logfile or continuous.
"""

import time
import logging
import logging.handlers

# import os.path

__author__ = 'Giovanni Moretti'

PROGRAM_NAME = "myBackup"
# LOG_FILENAME      = os.path.join(os.path.dirname(os.path.abspath(__file__)), PROGRAM_NAME + '.log')

CONSOLE_LOG_LEVEL = logging.ERROR  # Only show errors to the console
FILE_LOG_LEVEL = logging.INFO  # but log info messages to the logfile

logger = logging.getLogger(PROGRAM_NAME)
logger.setLevel(logging.DEBUG)

# ====================================================================================
# FILE-BASED LOG

# Create formatter and add it to the handlers
logger.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# formatter = logging.Formatter('%(levelname)s - %(message)s')

logger.fh, logger.ch = None, None


def add_handling(log_filename):
    # LOGFILE HANDLER - SELECT ONE OF THE FOLLOWING TWO LINES

    logger.fh = logging.FileHandler(log_filename)  # Continuous Single Log
    # fh = logging.handlers.RotatingFileHandler(LOG_FILENAME, backupCount=5) # Rotating log

    logger.fh.setLevel(FILE_LOG_LEVEL)
    logger.fh.setFormatter(logger.formatter)
    logger.addHandler(logger.fh)

    # logger.handlers[0].doRollover() # Roll to new logfile on application start

    # Add timestamp
    # logger.info('\n---------\nLog started on %s.\n---------\n' % time.asctime())

    # =================================================================================
    # CONSOLE HANDLER - can have a different log-level and format to the file-based log
    logger.ch = logging.StreamHandler()
    logger.ch.setLevel(CONSOLE_LOG_LEVEL)
    logger.formatter = logging.Formatter('%(message)s')  # simpler display format
    logger.ch.setFormatter(logger.formatter)
    logger.addHandler(logger.ch)


if __name__ == '__main__':

    # =================================================================================
    # In APPLICATION CODE, use whichever of the following is appropriate:

    logger.debug('debug message ' + time.ctime() )
    logger.info('info message '   + time.ctime() )
    # logger.warn('warn message')
    # logger.error('error message')
    # logger.critical('critical message')

    # =================================================================================
    # Test Logger
    f = open("myBackup.log")
    s = f.read()
    print(s)
