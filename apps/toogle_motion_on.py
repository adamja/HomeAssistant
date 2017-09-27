import appdaemon.appapi as appapi


### Comments ###

### Args ###
# input_boolean:
# light:


class ToggleMotionOn(appapi.AppDaemon):
    def initialize(self):
        self.log("Toggle Motion On App Started.")

        self.input_boolean = self.args["input_boolean"]
        self.light = self.args["light"]

        self.listen_state(self.start_func, self.input_boolean)

    def start_func(self, entity, attributes, old, new, kwargs):
        if new == "on":
            if self.get_state(self.light) == "on":
                self.call_service("light/lifx_effect_pulse", entity_id=self.light, brightness=0, period=1, cycles=2)
            else:
                self.call_service("light/lifx_effect_pulse", entity_id=self.light, brightness=125, period=1, cycles=2)
            self.log("{} turned on.".format(self.input_boolean))
        else:
            if self.get_state(self.light) == "on":
                self.call_service("light/lifx_effect_pulse", entity_id=self.light, brightness=0, period=1, cycles=1)
            else:
                self.call_service("light/lifx_effect_pulse", entity_id=self.light, brightness=125, period=1, cycles=1)
            self.log("{} turned off.".format(self.input_boolean))