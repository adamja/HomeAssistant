import logging
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import WatchedFileHandler
import os
import re
from datetime import datetime

'''
Use:

logger = MyLogger(logger_name, 
                   file_location=os.curdir
                   log_level=self.DEBUG
                   stream_log_level=self.INFO
                   file_log_level=self.DEBUG
                   )
logger.set_module_name("app_name")
logger.log(level, msg, name='')
'''

class MyLogger:
    """My Logger"""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    WARNING = logging.WARNING
    ERROR = logging.ERROR

    def __init__(self, logger_name, **kwargs):
        """Initialising function"""

        #  Logger Settings
        self.logger_name = logger_name
        self.file_location = os.curdir
        self.file_name = self.get_file_name(self.logger_name)
        self.log_level = self.DEBUG
        self.stream_log_level = self.INFO
        self.file_log_level = self.DEBUG
        self.module_name = None

        # Add kwargs
        if "file_location" in kwargs.keys():
            self.file_location = kwargs["file_location"]
        if "log_level" in kwargs.keys():
            self.log_level = kwargs["log_level"]
        if "stream_log_level" in kwargs.keys():
            self.stream_log_level = kwargs["stream_log_level"]
        if "file_log_level" in kwargs.keys():
            self.file_log_level = kwargs["file_log_level"]

        # Set Formatter
        self.formatter = logging.Formatter(
            fmt='%(asctime)s.%(msecs)03d\t%(levelname)s\t%(name)s\t%(message)s',
            datefmt="%Y-%m-%d %H:%M:%S")

        # Create Logger
        self.logger = logging.getLogger(self.logger_name)

        # Check if logger already has handlers because it was previously created
        if self.logger.handlers:
            for handler in self.logger.handlers:
                if isinstance(handler, WatchedFileHandler):
                    self.file_handler = handler
                if isinstance(handler, logging.StreamHandler):
                    self.stream_handler = handler
                if isinstance(handler, TimedRotatingFileHandler):
                    self.rotating_file_handler = handler

        # If no current handlers, add new handlers
        else:
            self.logger.setLevel(self.log_level)
            self.logger.propagate = False

            # Create File Handler
            self.create_file_handler()

            # Create File Rotation Handler
            # self.rotating_file_handler = TimedRotatingFileHandler(filename=filename, when='midnight', interval=1, backupCount=60)

            # Create Stream Handler
            self.stream_handler = logging.StreamHandler()
            self.stream_handler.setLevel(self.stream_log_level)
            self.stream_handler.setFormatter(self.formatter)

            # Add handlers to logger
            self.logger.addHandler(self.file_handler)  # logs to file
            self.logger.addHandler(self.stream_handler)  # logs to console
            # self.logger.addHandler(self.rotating_file_handler)  # creates a new log file at midnight

# -------------------------------------------------------------------------------------------------------------------- #
#  LOGGING
# -------------------------------------------------------------------------------------------------------------------- #
    def log(self, level, msg, **kwargs):
        self.check_logfile()

        lvl = self.get_log_level(level)
        name = self.module_name

        if "name" in kwargs.keys():
            name = kwargs["name"]

        if name:
            msg = name + "\t" + msg
        else:
            msg = '\t' + msg

        self.logger.log(lvl, msg)

    def set_module_name(self, name):
        self.module_name = name

    def check_logfile(self):
        """ Check to see if the currently log file is still todays date.
            If not, create a new log file with todays date. """
        curlogname = self.file_handler.baseFilename
        curlogdate = self.get_date(curlogname)
        curdate = str(datetime.now().date())

        # check if log file exists
        if os.path.isfile(curlogname):
            if curlogdate != curdate:
                # no logfile for the date
                self.remove_file_handler()
                self.create_file_handler()
                self.add_file_handler()
        else:
            # no logfile created
            self.remove_file_handler()
            self.create_file_handler()
            self.add_file_handler()

    def debug(self, msg, **kwargs):
        self.log(self.DEBUG, msg, **kwargs)

    def info(self, msg, **kwargs):
        self.log(self.INFO, msg, **kwargs)

    def warning(self, msg, **kwargs):
        self.log(self.WARNING, msg, **kwargs)

    def error(self, msg, **kwargs):
        self.log(self.ERROR, msg, **kwargs)

# -------------------------------------------------------------------------------------------------------------------- #
#  FILE HANDLER
# -------------------------------------------------------------------------------------------------------------------- #
    def create_file_handler(self):
        # Create File Handler
        self.file_name = self.get_file_name(self.logger_name)

        # Check file location exists
        if not os.path.exists(self.file_location):
            os.makedirs(self.file_location)

        filename = os.path.join(self.file_location, self.file_name)
        self.file_handler = WatchedFileHandler(filename)
        self.file_handler.setLevel(self.file_log_level)
        self.file_handler.setFormatter(self.formatter)

    def remove_file_handler(self):
        if self.logger.handlers:
            for handler in self.logger.handlers:
                if isinstance(handler, WatchedFileHandler):
                    self.logger.removeHandler(handler)

    def add_file_handler(self):
        self.logger.addHandler(self.file_handler)

# -------------------------------------------------------------------------------------------------------------------- #
#  STATIC METHODS
# -------------------------------------------------------------------------------------------------------------------- #

    @staticmethod
    def get_log_level(level):
        """Check for string log levels and converts to actual log levels"""
        if level == "DEBUG":
            return logging.DEBUG
        elif level == "INFO":
            return logging.INFO
        elif level == "WARN" or level == "WARNING":
            return logging.WARNING
        elif level == "ERROR":
            return logging.ERROR
        else:
            return level

    @staticmethod
    def get_date(name):
        pat = r'.*(\d{4}-\d{1,2}-\d{1,2}).*'
        match = re.fullmatch(pat, name)
        if match:
            return match.group(1)
        else:
            return None

    @staticmethod
    def get_file_name(logger_name):
        return logger_name + "_" + datetime.now().strftime('%Y-%m-%d') + ".log"


if __name__ == "__main__":
    logger = MyLogger("rain", log_level="DEBUG")
    logger.set_module_name("my app")
    logger.info("testing", name="changed it")
    logger.info("This is a log message.", name="Front: "+__name__)
    logger.log("INFO", "This is a log message2.", name="Back")
    logger.log("INFO", "This is a log message3.", name="House")
    # logger.debug("This is a log message4.", name="Front")
    # logger.log("WARN", "This is a log message5.", name="Back")
    # logger.log("ERROR", "This is a log message6.")
    logger2 = MyLogger("rain", log_level="DEBUG")
    logger2.log("INFO", "This is a log message2.", name="logger2")
    logger2.log("INFO", "This is a log message3.", name="logger2")