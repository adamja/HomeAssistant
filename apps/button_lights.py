import appdaemon.appapi as appapi
from MyLogger2 import MyLogger

### Args ###
# buttons: {entity_id for switches}
# lights: {enitiy_id for lights}
# click_type: {single, double, hold}
# mode: {on, off, toggle, toggle_multi}


class ButtonLights(appapi.AppDaemon):

    def initialize(self):
        # Start logger
        self.logger = MyLogger(__name__, file_location="/conf/logs/button_lights")
        self.logger.set_module_name(self.name)
        self.logger.debug("Log Started.")

        self.buttons = self.args["buttons"]
        self.lights = self.args["lights"]
        self.click_type = self.args["click_type"]
        self.mode = self.args["mode"]

        # APP VARIABLES
        self.light_list = self.get_app('lights')
        self.state = "off"
        for button in self.split_device_list(self.buttons):
            self.listen_event(self.event_callback, entity_id=button, event="click", click_type=self.click_type)

    def event_callback(self, event_name, data, kwargs):
        for light in self.split_device_list(self.lights):
            if self.mode == "toggle_multi":
                if self.state == "on":
                    self.logger.info("{} turned off.".format(light))
                    self.light_list.off(light)
                else:
                    self.logger.info("{} turned on.".format(light))
                    self.light_list.on(light)
            elif self.mode == "toggle":
                self.logger.info("{} toggled.".format(light))
                self.light_list.toggle(light)
            elif self.mode == "on":
                self.logger.info("{} turned on.".format(light))
                self.light_list.on(light)
            else:
                self.logger.info("{} turned off.".format(light))
                self.light_list.off(light)
        # change the state outside for loop to prevent multiple toggling for each light
        if self.state == 'on':
            self.state = 'off'
        else:
            self.state = 'on'
