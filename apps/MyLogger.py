import logging
import os
from datetime import datetime


class MyLogger:
    """A simple logger"""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    WARNING = logging.WARNING
    ERROR = logging.ERROR

    def __init__(self, logger_name, file_location=os.curdir, log_level=DEBUG):
        """Initialising function"""
        # Logger Settings
        self.logger_name = logger_name
        self.file_timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.file_location = file_location
        self.file_name = self.logger_name + "_" + self.file_timestamp + ".log"
        self.log_level = log_level
        self.formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d - %(levelname)s - %(name)s -  %(message)s',
                                           datefmt="%Y-%m-%d %H:%M:%S")

        # Create Logger
        self.logger = logging.getLogger(self.logger_name)
        # Check if logger already has handlers
        if self.logger.handlers:
            for handler in self.logger.handlers:
                if isinstance(handler, logging.FileHandler):
                    self.file_handler = handler
                if isinstance(handler, logging.StreamHandler):
                    self.stream_handler = handler
        # If no current handlers, add new handlers
        else:
            self.logger.setLevel(self.log_level)
            self.logger.propagate = False

            # Create File Handler
            self.file_handler = logging.FileHandler(os.path.join(self.file_location, self.file_name), 'w')
            self.file_handler.setLevel(self.log_level)
            self.file_handler.setFormatter(self.formatter)

            # Create Stream Handler
            self.stream_handler = logging.StreamHandler()
            self.stream_handler.setLevel(self.log_level)
            self.stream_handler.setFormatter(self.formatter)

            # Add handlers to logger
            self.logger.addHandler(self.file_handler)  # logs to file
            self.logger.addHandler(self.stream_handler)  # logs to console

    def set_file_location(self, file_location):
        """change the logfile save location"""
        self.file_location = file_location
        self.file_name = self.logger_name + "_" + self.file_timestamp + ".log"

    def set_logfile_log_level(self, level):
        """change the logfile logging level"""
        self.file_handler.setLevel(level)

    def set_console_log_level(self, level):
        """change the console logging level"""
        self.stream_handler.setLevel(level)

    def get_logger(self):
        """get logger object"""
        return self.logger

    def debug(self, message):
        """create an debug log entry using logging object"""
        self.logger.debug(message)

    def info(self, message):
        """create an info log entry using logging object"""
        self.logger.info(message)

    def warning(self, message):
        """create an warning log entry using logging object"""
        self.logger.warning(message)

    def error(self, message):
        """create an error log entry using logging object"""
        self.logger.error(message)

if __name__ == "__main__":
    myLogger = MyLogger("Logger_name")  # create a logger object
    myLogger.info("Test")  # send a log
    myLogger.debug("debug test")
    myLogger.warning("warning test")
    myLogger.error("error test")

# -------------------------------------------------------------------------------------------------------------------- #

# Example for using from a different file:
#
# from MyLogger import MyLogger
#
#
# log = MyLogger("module name")
# log.debug("Testing debug logging")

