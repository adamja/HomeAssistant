import appdaemon.appapi as appapi
from MyLogger2 import MyLogger

### Args ###
'''
{app name}:
    module: motion_lights
    class: MotionLights
    motion_sensor_entity = entity_id of motion sensor
    light = entity_id of light
    delay = time in seconds to wait until turning the light off after the motion is off
    motion_time_start = tba
    motion_time_end = tba
    days = tba
    motion_active_entity = entity_id of an input_boolean that states whether to turn the light on with motion or not
    listen_mode = state or event
'''


class MotionLights(appapi.AppDaemon):

    def initialize(self):
        # Start logger
        self.logger = MyLogger(__name__, file_location="/conf/logs/motion_lights")
        self.logger.set_module_name(self.name)
        self.logger.debug("Log Started.")

        # APPDAEMON INPUTS
        self.motion_sensor_entity = self.args["motion_sensor_entity"]
        self.light = self.args["light"]
        self.delay = "60"
        self.motion_active_entity = None
        self.listen_mode = "state"

        if "delay" in self.args.keys():
            self.delay = self.args["delay"]
        if "motion_active_entity" in self.args.keys():
            self.motion_active_entity = self.args["motion_active_entity"]
        if "listen_mode" in self.args.keys():
            self.listen_mode = self.args["listen_mode"]

        # APP VARIABLES
        self.handle = None

        # START LISTENERS
        if self.listen_mode == "event":
            self.listen_event(self.event_callback, entity_id=self.motion_sensor_entity, event="motion")
            self.logger.debug("event mode")
        else:
            self.listen_state(self.state_callback, self.motion_sensor_entity)
            self.logger.debug("state mode")

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTIONS
# -------------------------------------------------------------------------------------------------------------------- #
    def state_callback(self, entity, attribute, old, new, kwargs):
        """Callback function to turn light on when motion state change is triggered"""
        self.logger.debug("state_callback triggered")
        if self.check_motion_active():
            if new == "on":
                self.logger.debug("motion on")
                for light in self.split_device_list(self.light):
                    if self.get_state(light) != "on":
                        self.logger.info("Turning {} on".format(light))
                        self.turn_on(light)
                self.cancel_timer(self.handle)
            else:
                self.logger.debug("motion off")
                self.handle = self.run_in(self.light_off_callback, self.delay)

    def event_callback(self, event_name, data, kwargs):
        """Callback function to turn light on when the motion event is triggered"""
        self.logger.debug("event_callback triggered")
        if self.check_motion_active():
            self.logger.debug("motion_active = true")
            for light in self.split_device_list(self.light):
                if self.get_state(light) != "on":
                    self.logger.info("Turning {} on".format(light))
                    self.turn_on(light)
            self.cancel_timer(self.handle)
            self.handle = self.run_in(self.light_off_callback, self.delay)

    def light_off_callback(self, kwargs):
        """Turn light off after motion has not been detected for delay period"""
        if self.check_motion_active():
            for light in self.split_device_list(self.light):
                self.logger.info("Turning {} off".format(light))
                self.turn_off(light)

    def check_motion_active(self):
        """Check is there is a motion active entity and that it is turned on otherwise return true"""
        if self.motion_active_entity is None:
            return True
        if self.get_state(self.motion_active_entity) == "off":
            return False
        else:
            return True
