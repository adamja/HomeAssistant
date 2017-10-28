import appdaemon.appapi as appapi
from MyLogger2 import MyLogger

### Comments ###

### Args ###
''' 
app_name:
    module: motion_timer
    class: MotionTimer
    motion_sensor_entity: 
    power_socket_entity: 
    delay_mins: 
    delay_secs:
'''


class MotionTimer(appapi.AppDaemon):
    """Turns off something if motion has not been detected within the given time frame"""
    def initialize(self):
        # Start logger
        # Start logger
        self.logger = MyLogger(__name__, file_location="/conf/logs/__name__")
        self.logger.set_module_name(self.name)
        self.logger.debug("Log Started.")

        # Handle
        self.handle = None

        # App Args
        self.motion_sensor_entity = self.args["motion_sensor_entity"]
        self.power_socket_entity = self.args["power_socket_entity"]
        self.delay_mins = int(self.args["delay_mins"])
        self.delay_secs = int(self.args["delay_secs"])
        self.delay = (self.delay_mins*60) + self.delay_secs
        self.logger.info("Motion Sensor Entity: {}.".format(self.motion_sensor_entity))
        self.logger.info("Power Socket Entity: {}.".format(self.power_socket_entity))
        self.logger.info("Delay: {} minutes, {} seconds.".format(self.delay_mins, self.delay_secs))

        # Start listening to motion state/event changes
        self.listen_event(self.event_callback, entity_id=self.motion_sensor_entity, event="motion")
        self.logger.info("Started Event Mode.")

    def event_callback(self, event_name, data, kwargs):
        self.logger.debug("event_callback() triggered.")
        self.cancel_timer(self.handle)
        self.handle = self.run_in(self.power_off_callback, self.delay)

    def power_off_callback(self, kwargs):
        self.logger.info("No motion detected for {} minutes and {} seconds.".format(self.delay_mins, self.delay_secs))
        for power in self.split_device_list(self.power_socket_entity):
            self.logger.info("Turning {} off".format(power))
            self.turn_off(power)