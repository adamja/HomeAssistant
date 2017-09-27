import appdaemon.appapi as appapi
from datetime import datetime
from datetime import time

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
        
        # self.entity = "binary_sensor.motion_sensor_158d00010f7f3c"
        # self.event_type = "motion"
        # self.log(str(datetime.datetime.now()))
        # self.log(str(datetime.datetime.tzname(datetime.datetime.now())))
        #self.listen_state(self.state_callback, entity)
        
        # self.listen_event(self.event_callback, event=self.event_type)
        """
        entity_id=
        event=
        click_type=
        """

        
    def state_callback(self, entity, attribute, old, new, kwargs):
        self.log("entity: {} | attribute: {} | old: {} | new: {} | kwargs: {}".format(entity, attribute, old, new, kwargs))
    
    
    def event_callback(self, event_name, data, kwargs):
        self.log("event_name: {} | data: {} | kwargs: {}".format(event_name, data, kwargs))