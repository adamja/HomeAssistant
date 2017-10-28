import appdaemon.appapi as appapi
from MyLogger2 import MyLogger

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
        # Start logger
        self.logger = MyLogger(__name__, file_location="/conf/logs/" + __name__)
        self.logger.set_module_name(self.name)
        self.logger.debug("Started.")

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
