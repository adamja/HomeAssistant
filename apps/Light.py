import appdaemon.appapi as appapi
from MyLogger2 import MyLogger
import math
from datetime import datetime
from datetime import timedelta
from datetime import time

'''
{app_name}:
    module: flux_lights
    class: FluxLights
    lights: 
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
'''

class Light(appapi.AppDaemon):

    FMT = "%H:%M"
    name = "Light"

    def __init__(self, entity_id, **kwargs):
        """Initialising function"""
        # super.__init__()
        self.entity_id = entity_id

        # Start logger
        self.logger = MyLogger(__name__, file_location="/conf/logs/" + __name__)
        self.logger.set_module_name(self.name)
        self.logger.debug("Started.")

        # self.default_temp = 300
        self.temp = 300
        self.min_temp = 200
        self.sunset_temp = 250
        self.max_temp = 400

        # self.default_bright = 200
        self.bright = 200
        self.min_bright = 100
        self.sunset_bright = 255
        self.max_bright = 255

        self.start_time = self.get_sunrise_stime()
        self.sunrise_time = self.get_sunrise_stime()
        self.sunset_time = self.get_sunset_stime()
        self.stop_time = "23:00"

        # self.last_on = None
        # self.last_off = None
        self.manual_override = False
        self.manual_last_triggered = None
        self.manual_timeout = "01:00"

        self.update_settings(**kwargs)

    def __repr__(self):
        return self.entity_id

    def __str__(self):
        return self.entity_id

    def update_settings(self, **kwargs):
        if "min_temp" in kwargs.keys():
            self.min_temp = kwargs["min_temp"]
        if "sunset_temp" in kwargs.keys():
            self.sunset_temp = kwargs["sunset_temp"]
        if "max_temp" in kwargs.keys():
            self.max_temp = kwargs["max_temp"]
        if "min_bright" in kwargs.keys():
            self.min_bright = kwargs["min_bright"]
        if "sunset_bright" in kwargs.keys():
            self.sunset_bright = kwargs["sunset_bright"]
        if "max_bright" in kwargs.keys():
            self.max_bright = kwargs["max_bright"]
        if "start_time" in kwargs.keys():
            self.start_time = self.check_time(kwargs["start_time"])
        if "sunset_time" in kwargs.keys():
            self.sunset_time = self.check_time(kwargs["sunset_time"])
        if "stop_time" in kwargs.keys():
            self.stop_time = self.check_time(kwargs["stop_time"])
        if "manual_timeout" in kwargs.keys():
            self.manual_timeout = self.check_time(kwargs["manual_timeout"])

# -------------------------------------------------------------------------------------------------------------------- #
# ON / OFF
# -------------------------------------------------------------------------------------------------------------------- #

    def on(self, brightness=None, **kwargs):
        """Turn a light on"""

        flux_temp = False
        flux_bright = False

        if "flux_temp" in kwargs.keys():
            flux_temp = kwargs["flux_temp"]
        if "flux_bright" in kwargs.keys():
            flux_bright = kwargs["flux_bright"]
        if "manual_trigger" in kwargs.keys():
            if kwargs["manual_trigger"] is True or kwargs["manual_trigger"] == "on":
                self.update_manual_override()

        self.update_sunrise_sunset()  # update sunrise and sunset to latest values
        self.update_flux_values()  # update temp and bright to latest flux values
        # self.check_manual_override()  # check to see if manual override is turned on

        if flux_temp and flux_temp and not self.manual_override:
            # Temperature and Brightness
            self.turn_on(self.entity_id, color_temp=self.temp, brightness=self.bright)
            self.logger.debug("Turned on light: {} with T: {} and B: {}".format(self.entity_id, self.temp, self.bright))
        elif flux_temp:
            # Temperature
            self.turn_on(self.entity_id, color_temp=self.temp)
            self.logger.debug("Turned on light: {} with T: {}".format(self.entity_id, self.temp))
        elif flux_bright and not self.manual_override:
            # Brightness
            self.turn_on(self.entity_id, brightness=self.bright)
            self.logger.debug("Turned on light: {} with B: {}".format(self.entity_id, self.bright))
        else:
            # None
            if brightness is not None:
                self.turn_on(self.entity_id, brightness=brightness)
            else:
                self.turn_on(self.entity_id)
            self.logger.debug("Turned on light: {}".format(self.entity_id))

    def off(self):
        """Turn a light off"""
        self.turn_off(self.entity_id)
        return "Turned off light: {}".format(self.entity_id)

# -------------------------------------------------------------------------------------------------------------------- #
# FLUX
# -------------------------------------------------------------------------------------------------------------------- #

    def update_flux_values(self):
        """Generate flux value and return to caller"""
        self.temp = self.get_flux_temp()
        self.bright = self.get_flux_bright()
        return ("Temperature:{} Brightness:{}".format(self.temp, self.bright))

    def get_flux_temp(self):
        now_str = datetime.now().strftime(self.FMT)
        now_dt = self.to_datetime(now_str)  # removes days

        if self.time_compare(self.start_time, now_str) and self.time_compare(now_str, self.stop_time):
            # start time less than now and stop time more than now
            temp_diff = self.max_temp - self.min_temp
            time_steps = self.time_diff(self.start_time, self.stop_time) / temp_diff
            now_start_diff = now_dt - self.to_datetime(self.start_time)
            steps = math.ceil(int(now_start_diff / time_steps))
            temp = self.min_temp + steps
        else:
            # Set to max temp
            temp = self.max_temp
        return temp

    def get_flux_bright(self):
        now_str = datetime.now().strftime(self.FMT)
        now_dt = self.to_datetime(now_str)  # removes days

        if self.time_compare(self.start_time, now_str) and  self.time_compare(now_str, self.stop_time):
            bright_diff = self.max_bright - self.min_bright
            time_steps = self.time_diff(self.start_time, self.stop_time) / bright_diff
            now_start_diff = now_dt - self.to_datetime(self.start_time)
            steps = math.ceil(int(now_start_diff / time_steps))
            bright = self.max_bright - steps
        else:
            # Set to min brightness
            bright = self.min_bright
        return bright

# -------------------------------------------------------------------------------------------------------------------- #
# DATE / TIME FUNCTIONS
# -------------------------------------------------------------------------------------------------------------------- #

    def check_manual_override(self):
        """Checks to see when manual override was last triggered and compares with the timeout period"""
        if self.manual_last_triggered != None:
            t1 = datetime.now()
            t2 = self.manual_last_triggered + self.str_to_timedelta(self.manual_timeout)
            self.manual_override = t1 < t2

    def update_manual_override(self):
        self.manual_last_triggered = datetime.now()

    def time_compare(self, t1, t2):
        """Returns true if t2 > t1"""
        return self.to_datetime(t2) > self.to_datetime(t1)

    def time_diff(self, t1, t2):
        """Return difference as time delta"""
        tdelta = self.to_datetime(t2) - self.to_datetime(t1)

        if tdelta.days < 0:
            tdelta = timedelta(days=0, seconds=tdelta.seconds, microseconds=tdelta.microseconds)

        return tdelta

    def time_diff_str(self, t1, t2):
        tdelta = self.to_datetime(t2) - self.to_datetime(t1)
        
        if tdelta.days < 0:
            tdelta = timedelta(days=0, seconds=tdelta.seconds, microseconds=tdelta.microseconds)
        
            sec = tdelta.seconds
            hours = sec // 3600
            minutes = (sec // 60) - (hours * 60)
            hhmm = str(hours) + ':' + str(minutes).zfill(2)
            return hhmm


    def to_datetime(self, time):
        return datetime.strptime(time, self.FMT)

    def str_to_timedelta(self, time):
        h, m = time.split(':')
        return timedelta(hours=int(h), minutes=int(m))

# -------------------------------------------------------------------------------------------------------------------- #
# SUNRISE / SUNSET
# -------------------------------------------------------------------------------------------------------------------- #
    def get_sunrise(self):
        return self.sunrise()

    def get_sunset(self):
        return self.sunset()

    def get_sunrise_stime(self):
        return self.sunrise().strftime(self.FMT)

    def get_sunset_stime(self):
        return self.sunset().strftime(self.FMT)

    def check_time(self, t):
        if t == "sunrise":
            return self.get_sunrise_stime()
        elif t == "sunset":
            return self.get_sunset_stime()
        else:
            return t

    def update_sunrise_sunset(self):
        self.sunrise_time = self.get_sunrise_stime()
        self.sunset_time = self.get_sunset_stime()

# -------------------------------------------------------------------------------------------------------------------- #
# LOGGING
# -------------------------------------------------------------------------------------------------------------------- #
    def log(self, msg):
        print(msg)

# -------------------------------------------------------------------------------------------------------------------- #
# EXAMPLE
# -------------------------------------------------------------------------------------------------------------------- #
if __name__ == "__main__":
    light = Light("light.sleepout")
    light.on()
    light.log(light.get_sunrise_stime())