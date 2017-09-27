import appdaemon.appapi as appapi
import datetime

class HeaterTimer(appapi.AppDaemon):


    def initialize(self):
        self.log("Started.")
        self.heater = self.args["heater"]
        self.on_time = datetime.datetime.strptime(self.args["on_time"], "%H:%M:%S").time()
        self.off_time = datetime.datetime.strptime(self.args["off_time"], "%H:%M:%S").time()

        #self.on_time = datetime.time(5,30,00)
        #self.off_time = datetime.time(7,00,00)

        self.log("On time is {} and off time is {}.".format(str(self.on_time), str(self.off_time)))
        self.handle1 = self.run_daily(self.heater_on_callback, self.on_time)
        self.handle2 = self.run_daily(self.heater_off_callback, self.off_time)


    def heater_on_callback(self, kwargs):
        self.log("Heater {} turned on.".format(self.heater))
        self.turn_on(self.heater)


    def heater_off_callback(self, kwargs):
        self.log("Heater {} turned off.".format(self.heater))
        self.turn_off(self.heater)
