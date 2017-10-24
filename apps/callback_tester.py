import appdaemon.appapi as appapi
from MyLogger import MyLogger
from datetime import datetime
from datetime import time
from Light import Light

### Comments ###
"""
Appdaemon.yaml entry
{app_name}:
    module: callback_tester
    class: CallbackTester
"""

### Args ###
class CallbackTester(appapi.AppDaemon):
    def initialize(self):
        self.log("Started.")
        #self.logger = MyLogger(__name__ + "-" + self.name, file_location="/conf/logs",
        #                       log_level=MyLogger.DEBUG)
        #self.logger.set_console_log_level(MyLogger.INFO)
        #self.logger.set_logfile_log_level(MyLogger.DEBUG)
        #self.logger.debug("Log Started.")
        #self.light = Light(__name__, "light.sleepout", logger=self.logger, flux_on=True, fluxT=True, fluxB=True, min_temp=200, max_temp=400, min_bright=50, max_bright=255, start_time="6:00", stop_time="23:00")
        #self.logger.info("bright:{} temp:{}".format(str(self.light.get_flux_bright()), str(self.light.get_flux_temp())))
        #self.logger.info(self.light.time_diff_str("7:00", "1:00"))
        #self.log(__name__)
          
        # self.entity = "binary_sensor.motion_sensor_158d00010f7f3c"
        # self.event_type = "motion"
        # self.log(str(datetime.datetime.now()))
        # self.log(str(datetime.datetime.tzname(datetime.datetime.now())))
        #self.listen_state(self.state_callback, entity)
        
        # self.listen_event(self.event_callback, event=self.event_type)
    #    """
    #    entity_id=
    #    event=
    #    click_type=
    #    """

        
    #def state_callback(self, entity, attribute, old, new, kwargs):
    #    self.log("entity: {} | attribute: {} | old: {} | new: {} | kwargs: {}".format(entity, attribute, old, new, kwargs))
    
    
    #def event_callback(self, event_name, data, kwargs):
    #    self.log("event_name: {} | data: {} | kwargs: {}".format(event_name, data, kwargs))