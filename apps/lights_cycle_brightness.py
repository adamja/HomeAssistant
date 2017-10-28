import appdaemon.appapi as appapi
import threading
import time
from MyLogger2 import MyLogger

### Comments ###

### Args ###
"""
# switch_id: {entity_id of switch}
# light_id: {entity_id of light}
# delay: {1 = one second. Can go below 1 second. Anything below 0.4 was not working well for me}
# step: {how many brightness steps to go up/down per change}
# minimum: {brightness to go to. Lowest = 0}
# maximum:{brightness to go to. Highest = 255}

EXAMPLE appdaemon.yaml entry:

adams_bedside_light_switch_LCB:
  module: lights_cycle_brightness
  class: Lights_Cycle_Brightness
  switch_id: binary_sensor.switch_158
  light_id: light.bedside_one
  delay: 0.4
  step: 25
  minimum: 25
  maximum: 250
  always_down_first: on / off
"""

class Lights_Cycle_Brightness(appapi.AppDaemon):
    def initialize(self):
        # Start logger
        self.logger = MyLogger(__name__, file_location="/conf/logs/lights_cycle_brightness")
        self.logger.set_module_name(self.name)
        self.logger.debug("Log Started.")

        # APPDAEMON INPUTS
        self.delay = float(self.args["delay"])
        self.minimum = int(self.args["minimum"])
        self.maximum = int(self.args["maximum"])
        self.step = int(self.args["step"])
        self.switch_id = self.args["switch_id"]
        self.light_id = self.args["light_id"]
        self.always_down_first = False
        if "always_down_first" in self.args.keys():
            self.always_down_first = self.args["always_down_first"]

        # APP VARIABLES
        self.going_up = True
        self.light_list = self.get_app('lights')

        for switch in self.split_device_list(self.switch_id):
            self.listen_state(self.start_func, switch)

    def start_func(self, entity, attributes, old, new, kwargs):
        if new == "on":
            self.t = threading.Thread(target=self.run_thread, args=(entity,))
            self.t.start()

    def run_thread(self, switch):
        self.log(self.always_down_first)
        if self.always_down_first:
            self.going_up = False
        while self.get_state(switch) == "on":
            if self.get_state(self.light_id) == "off":
                self.light_list.on(self.light_id)

            brightness = self.get_brightness(self.light_id)

            if brightness is not None:
                if self.going_up:
                    brightness += self.step
                    if brightness > self.maximum:
                        brightness = self.maximum
                        self.going_up = False
                else:
                    brightness = brightness - self.step
                    if brightness < self.minimum:
                        brightness = self.minimum
                        self.going_up = True

                self.logger.info("{} changed to brightness: {}".format(self.light_id, brightness))

                self.light_list.on(self.light_id, brightness=brightness, manual_trigger=True)
            time.sleep(self.delay)

    def get_brightness(self, light_id):
        try:
            brightness = int(self.get_state(self.light_id, "brightness"))
            return brightness
        except:
            return None