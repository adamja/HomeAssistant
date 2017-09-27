import appdaemon.appapi as appapi
from datetime import datetime, timedelta
from time import sleep
from MyLogger import MyLogger

### Comments ###

### Args ###
'''
back_grass: # module name
    module: retic
    class: Retic
    days: mon,tue,wed,thu,fri,sat,sun # days to run
    start_times: 05:30:00, 06:00:00 # comma serperate for multiple
    duration: 3 # in minutes
    stations: switch.relay1,switch.relay4 # comma serperate for multiple
'''


class Retic(appapi.AppDaemon):
    
    def initialize(self):
        # Start logger
        self.logger = MyLogger(__name__ + "-" + self.name, file_location="/conf/logs/retic",
                               log_level=MyLogger.DEBUG)
        self.logger.set_console_log_level(MyLogger.INFO)
        self.logger.set_logfile_log_level(MyLogger.DEBUG)
        self.logger.debug("Log Started.")

        self.days = self.args["days"]
        self.start_times = self.args["start_times"]
        self.duration = self.args["duration"]
        self.stations = self.args["stations"]
        self.raining = self.args["raining"]
        
        # set up callbacks for each time
        for time in self.split_device_list(self.start_times):
            start_time = datetime.strptime(time, "%H:%M:%S").time()
            self.logger.info("Retic Starting: {} - Duration: {}m - Stations: {} - Days: {}".format(str(start_time), self.duration, self.stations, self.days))
            on_handle = self.run_daily(self.retic_on_callback, start_time, constrain_days=self.days)
            
            stop_time =  (datetime.strptime(time, "%H:%M:%S") + timedelta(minutes=self.duration)).time()
            #self.logger.info("Retic Stopping: {} - Stations: {} - Days: {}".format(str(stop_time), self.stations, self.days))
            off_handle = self.run_daily(self.retic_off_callback, stop_time)
  
        
    def retic_on_callback(self, kwargs):
        self.logger.debug("retic_on_callback() triggered.")
        if (self.get_state(self.raining) == "off"):   
            for station in self.split_device_list(self.stations):
                self.turn_on(station)
                self.logger.info("{} turned on".format(station))
                sleep(1)
        else:
            self.logger.info("Raining is turned on. Retic not being activated")
    
    def retic_off_callback(self, kwargs):
        self.logger.debug("retic_off_callback() triggered.")
        for station in self.split_device_list(self.stations):
            self.turn_off(station)
            self.logger.info("{} turned off".format(station))
            sleep(1)

        # dummy values
        # self.start_times = "17:25:00"
        # self.duration = 1
        # self.days = "mon,wed,sat,sun"    # constrain_days="mon,tue,wed,thur,fri,sat,sun"
        # self.stations = "switch.relay1,switch.relay4"