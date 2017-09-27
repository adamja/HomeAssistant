import appdaemon.appapi as appapi

### Args ###
# buttons: {entity_id for switches}
# lights: {enitiy_id for lights}
# click_type: {single, double, hold}
# mode: {on, off, toggle, toggle_multi}

class ButtonLights(appapi.AppDaemon):

    def initialize(self):
        self.log("Started.")
        self.buttons = self.args["buttons"]
        self.lights = self.args["lights"]
        self.click_type = self.args["click_type"]
        self.mode = self.args["mode"]
        self.state = "off"

        for button in self.split_device_list(self.buttons):
            self.listen_event(self.event_callback, entity_id=button,event="click", click_type=self.click_type)

    def event_callback(self, event_name, data, kwargs):
        for light in self.split_device_list(self.lights):
            if (self.mode == "toggle_multi"):
                if (self.state == "on"):
                    self.log("{} turned off.".format(light))
                    self.turn_off(light)
                else:
                    self.log("{} turned on.".format(light))
                    self.turn_on(light)
            elif (self.mode == "toggle"):
                self.log("{} toggled.".format(light))
                self.toggle(light)
            elif (self.mode == "on"):
                self.log("{} turned on.".format(light))
                self.turn_on(light)
            else:
                self.log("{} turned off.".format(light))
                self.turn_off(light)
                
        if (self.state == "on"):
            self.state = "off"
        else:
            self.state = "on"