import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime
#
# class Test:
#
#     DEBUG = logging.DEBUG
#     INFO = logging.INFO
#     WARN = logging.WARN
#     WARNING = logging.WARNING
#     ERROR = logging.ERROR
#
#     """My Logger"""
    # def __init__(self, *args, **kwargs):
    #     self.test = "Test return"
    #     print(kwargs["kayla"])
    #     print("kayla" in kwargs.keys())
    #     print(kwargs)
    #
    # def log(self):
    #     return self.test


# if __name__ == "__main__":
    # lol = Test(adam="Adam", kayla="Kayla")
    # dict = {}
    #
    # dict["lol"] = "one"
    # dict["lol"] = "two"
    #
    # print(dict["lol"])

logger = logging.getLogger("logger_1")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
            fmt='%(asctime)s.%(msecs)03d\t%(levelname)s\t%(name)s\t%(message)s',
            datefmt="%Y-%m-%d %H:%M:%S")

# Create Stream Handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

# Add handlers to logger
# self.logger.addHandler(self.file_handler)  # logs to file
logger.addHandler(stream_handler)  # logs to console

logger.log(logging.INFO, "testing log message")
logger.log(logging.DEBUG, "testing log message testing testing")
logger.log(logging.WARN, "testing log message testing testing testing testing")
logger.log(logging.CRITICAL, "testing log message testing testing testing testing")
