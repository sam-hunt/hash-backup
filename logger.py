"""
Create a log file handler which logs message to both the screen and the keyboard.
The logfile can be either a rotating logfile or continuous.
"""

import time
import logging
import logging.handlers

import os.path

__author__ = 'Giovanni Moretti'

PROGRAM_NAME      = "myBackup"
LOG_FILENAME      = os.path.join(os.path.dirname(os.path.abspath(__file__)),PROGRAM_NAME + '.log')

CONSOLE_LOG_LEVEL = logging.ERROR  # Only show errors to the console
FILE_LOG_LEVEL    = logging.INFO   # but log info messages to the logfile

logger = logging.getLogger(PROGRAM_NAME)
logger.setLevel(logging.DEBUG)

# ====================================================================================
# FILE-BASED LOG

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# formatter = logging.Formatter('%(levelname)s - %(message)s')

# LOGFILE HANDLER - SELECT ONE OF THE FOLLOWING TWO LINES

fh = logging.FileHandler(LOG_FILENAME)                          # Continuous Single Log
# fh = logging.handlers.RotatingFileHandler(LOG_FILENAME, backupCount=5) # Rotating log

fh.setLevel(FILE_LOG_LEVEL)
fh.setFormatter(formatter)
logger.addHandler(fh)

# logger.handlers[0].doRollover() # Roll to new logfile on application start

# Add timestamp
logger.info('\n---------\nLog started on %s.\n---------\n' % time.asctime())

# =================================================================================
# CONSOLE HANDLER - can have a different loglevel and format to the file-based log
ch = logging.StreamHandler()
ch.setLevel(CONSOLE_LOG_LEVEL)
formatter = logging.Formatter('%(message)s')     # simpler display format
ch.setFormatter(formatter)
logger.addHandler(ch)

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
