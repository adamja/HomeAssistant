import appdaemon.appapi as appapi
from datetime import datetime, timedelta
from time import sleep
from MyLogger2 import MyLogger

### Args ###
'''
{module_name}:
    module: retic_manual
    class: ReticManual
    input_select:
    input_boolean: 
    input_number:
    station_select_name:
    station_entites:
'''

class ReticManual(appapi.AppDaemon):
    def initialize(self):
        # Start logger
        self.logger = MyLogger(__name__, file_location="/conf/logs/" + __name__)
        self.logger.set_module_name(self.name)
        self.logger.debug("Started.")

        self.input_select = self.args["input_select"]
        self.input_boolean = self.args["input_boolean"]
        self.input_number = self.args["input_number"]
        self.station_select_name = self.args["station_select_name"]
        self.station_entites = self.args["station_entites"]

        self.handle = []


        self.listen_state(self.on_callback, self.input_boolean)

    def on_callback(self, entity, attributes, old, new, kwargs):
        if new == 'on':
            station = self.get_state(self.input_select)

            if station == self.station_select_name:
                self.on(self.station_entites)

    def off_callback(self, kwargs):
        stn = kwargs["stn"]
        self.logger.debug("Turning off: {}".format(stn))
        self.turn_off(stn)

    def on(self, stns):
        duration = float(self.get_state(self.input_number))
        stop_time = datetime.now() + timedelta(minutes=duration)
        self.logger.info("Activating {} for {} minutes".format(self.station_select_name, duration))
        n = 0
        for stn in self.split_device_list(stns):
            self.logger.debug("Turning on: {}".format(stn))
            self.turn_on(stn)
            stop_time += timedelta(seconds=n)
            if len(self.handle) > n:
                self.cancel_timer(self.handle[n])
                self.handle[n] = self.run_at(self.off_callback, stop_time, stn=stn)
            else:
                self.handle.append(self.run_at(self.off_callback, stop_time, stn=stn))
            n += 1
        self.turn_off(self.input_boolean)


