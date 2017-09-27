import appdaemon.appapi as appapi
import threading
import time
from MyLogger import MyLogger

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
"""

class Lights_Cycle_Brightness(appapi.AppDaemon):
    def initialize(self):
        # Start logger
        self.logger = MyLogger(__name__ + "-" + self.name, file_location="/conf/logs/dimmer_lights",
                               log_level=MyLogger.DEBUG)
        self.logger.set_console_log_level(MyLogger.INFO)
        self.logger.set_logfile_log_level(MyLogger.DEBUG)
        self.logger.debug("Log Started.")

        self.going_up = True

        self.delay = float(self.args["delay"])
        self.minimum = int(self.args["minimum"])
        self.maximum = int(self.args["maximum"])
        self.step = int(self.args["step"])
        self.switch_id = self.args["switch_id"]
        self.light_id = self.args["light_id"]
        
        for switch in self.split_device_list(self.switch_id):
            self.listen_state(self.start_func, switch)


    def start_func(self, entity, attributes, old, new, kwargs):
        if new == "on":
            self.t = threading.Thread(target=self.run_thread, args=(entity,))
            self.t.start()

    def run_thread(self, switch):
        while(self.get_state(switch) == "on"):
            if self.get_state(self.light_id) == "off":
                self.turn_on(self.light_id)

            try:
                self.brightness = int(self.get_state(self.light_id, "brightness")) # get lights current brightness
            except:
                while(self.brightness == None and self.get_state(switch) == "on"):
                    try:
                        self.brightness = int(self.get_state(self.light_id, "brightness"))
                    except:
                        pass

            if self.going_up:
                self.brightness += self.step
                if self.brightness > self.maximum:
                    self.brightness = self.maximum
                    self.going_up = False
            else:
                self.brightness = self.brightness - self.step
                if self.brightness < self.minimum:
                    self.brightness = self.minimum
                    self.going_up = True

            self.logger.info("{} changed to brightness: {}".format(self.light_id, self.brightness))

            self.turn_on(self.light_id, brightness=self.brightness)
            time.sleep(self.delay)