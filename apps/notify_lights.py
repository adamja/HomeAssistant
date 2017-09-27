import appdaemon.appapi as appapi

### Comments ###

### Args ###
"""
trigger_entity: 
light_entity: 
mode: 
brightness: 
color_name: 
period: 
cycles: 
"""


class NotifyLights(appapi.AppDaemon):
    
    def initialize(self):
        self.log("Started.")
        
        self.trigger_entity = self.args["trigger_entity"]
        self.light_entity = self.args["light_entity"]
        self.mode = self.args["mode"]
        self.brightness = self.args["brightness"]
        self.color_name = self.args["color_name"]
        self.period = self.args["period"]
        self.cycles = self.args["cycles"]
        
        self.listen_state(self.state_callback, self.trigger_entity)
            
          
    def state_callback(self, entity, attributes, old, new, kwargs):
        #self.log("callback reached")
        if new == "on":
            self.notify_callback()
            
            
    def notify_callback(self):
        for light in self.split_device_list(self.light_entity):
            self.call_service("light/lifx_effect_pulse", entity_id=light, mode=self.mode, brightness=self.brightness , color_name=self.color_name, period=self.period , cycles=self.cycles )