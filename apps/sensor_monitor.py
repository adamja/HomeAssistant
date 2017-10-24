import appdaemon.appapi as appapi
from MyLogger import MyLogger

### Args ###
"""
{app_name}:
    module: sensor_monitor
    class: SensorMonitor
    sensors:
"""

class SensorMonitor(appapi.AppDaemon):
    """Monitor and logs the changes in rain forcast"""
    def initialize(self):
        # LOGGER
        self.logger = MyLogger(__name__, file_location="/conf/logs", log_level=MyLogger.DEBUG)
        self.logger.set_console_log_level(MyLogger.INFO)
        self.logger.set_logfile_log_level(MyLogger.DEBUG)
        self.logger.debug("Log Started.")

        # APPDAEMON INPUTS
        self.sensors = None

        if "sensors" in self.args.keys():
            self.sensors = self.args["sensors"]

        # START LISTENERS
        for sensor in self.split_device_list(self.sensors):
            self.logger.debug("Started listening for state changes to sensor: {}.".format(sensor))
            self.listen_state(self.state_callback, sensor)

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTIONS
# -------------------------------------------------------------------------------------------------------------------- #
    def state_callback(self, entity, attribute, old, new, kwargs):
        """Callback function to log when a weather sensor changes states"""
        self.logger.debug("Sensor: {} has updated state to: {} from {}.".format(entity, new, old))
