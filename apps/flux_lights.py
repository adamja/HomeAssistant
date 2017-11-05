import appdaemon.appapi as appapi
from MyLogger2 import MyLogger
from datetime import time


### Comments ###

### Args ###
"""
{app_name}:
    module: flux_lights
    class: FluxLights
    lights: 
    flux_switch: 
    temp_on: 
    default_temp: 
    min_temp: 
    max_temp: 
    bright_on: 
    default_bright: 
    min_bright: 
    max_bright: 
    start_time: 
    stop_time: 
"""

class FluxLights(appapi.AppDaemon):
    def initialize(self):
        # Start logger
        self.logger = MyLogger(__name__, file_location="/conf/logs/flux_lights")
        self.logger.set_module_name(self.name)
        self.logger.debug("Log Started.")

        # APPDAEMON INPUTS
        self.lights = self.args["lights"]
        self.flux_switch = self.args["flux_switch"]
        self.temp_on = bool(self.args["temp_on"])
        self.default_temp = int(self.args["default_temp"])
        self.min_temp = int(self.args["min_temp"])
        self.sunset_temp = int(self.args["sunset_temp"])
        self.max_temp = int(self.args["max_temp"])
        self.bright_on = bool(self.args["bright_on"])
        self.default_bright = int(self.args["default_bright"])
        self.min_bright = int(self.args["min_bright"])
        self.sunset_bright = int(self.args["sunset_bright"])
        self.max_bright = int(self.args["max_bright"])
        self.start_time = self.args["start_time"]
        self.stop_time = self.args["stop_time"]

        # APP VARIABLES
        self.light_list = self.get_app('lights')
        self.callback = None
        # self.flux_light = []

        # ADD ALL LIGHTS
        for light in self.split_device_list(self.lights):
            self.flux_run(light)
       

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTIONS
# -------------------------------------------------------------------------------------------------------------------- #
    def flux_run(self, light):
        # CREATE LIGHT
        self.light_list.add_light(light, default_temp=self.default_temp, min_temp=self.min_temp, sunset_temp=self.sunset_temp, max_temp=self.max_temp,
                                  default_bright=self.default_bright, min_bright=self.min_bright, sunset_bright=self.sunset_bright, max_bright=self.max_bright,
                                  start_time=self.start_time, stop_time=self.stop_time)

        self.logger.info("Started flux for: {}".format(light))
        t = time(0, 0, 0)
        self.handle = self.run_minutely(self.update_callback, t, light=light)


# -------------------------------------------------------------------------------------------------------------------- #
# CALLBACK FUNCTIONS
# -------------------------------------------------------------------------------------------------------------------- #
    # https://stackoverflow.com/questions/1496346/passing-a-list-of-kwargs    
    def update_callback(self, kwargs):       
        light = kwargs["light"]
        if self.get_state(light) == "on" and self.get_state(self.flux_switch) == "on":
                self.light_list.on(light, flux_temp=self.temp_on, flux_bright=self.bright_on)
