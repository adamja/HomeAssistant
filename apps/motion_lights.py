import appdaemon.appapi as appapi

### Comments ###
"""

Xiaomi motion sensor sample:
2017-09-07 15:09:00.293267 INFO entity_tester: event_name: motion | data: {'entity_id': 'binary_sensor.motion_sensor_158d00010f7f3c'} | kwargs: {'entity_id': 'binary_sensor.motion_sensor_158d00010f7f3c'}

"""


### Args ###
# motion_sensor_entity = entity_id of motion sensor
# light = entity_id of light
# delay = time in seconds to wait until turning the light off after the motion is off
# motion_time_start = tba
# motion_time_end = tba
# days = tba
# motion_active_entity = entity_id of an input_boolean that states whether to turn the light on with motion or not
# listen_mode = state or event

class MotionLights(appapi.AppDaemon):

    def initialize(self):
        self.log("Started.")
        
        self.handle = None
        
        self.motion_sensor_entity = self.args["motion_sensor_entity"]
        self.light = self.args["light"]
        self.delay = "60"
        self.motion_time_start = ""
        self.motion_time_end = ""
        self.days = ""
        self.motion_active_entity = ""
        self.listen_mode = "state"
        try:
            self.delay = self.args["delay"]
        except:
            pass
        try:
            self.time_start = self.args["time_start"]
        except:
            pass
        try:
            self.time_end = self.args["time_end"]
        except:
            pass
        try:
            self.days = self.args["days"]
        except:
            pass
        try:
            self.motion_active_entity = self.args["motion_active_entity"]
        except:
            pass
        try:
            self.listen_mode = self.args["listen_mode"]
        except:
            pass
            
        if (self.listen_mode == "event"):
            self.listen_event(self.event_callback, entity_id=self.motion_sensor_entity, event="motion")
            # self.log("event mode")
        else:
            self.listen_state(self.state_callback, self.motion_sensor_entity)
            # self.log("state mode")
        

    def state_callback(self, entity, attribute, old, new, kwargs):
        #self.log("state_callback triggered")
        if self.check_motion_active():
            if (new == "on"):
                #self.log("motion on")
                for light in self.split_device_list(self.light):
                    if (self.get_state(light) != "on"):
                        self.log("Turning {} on".format(light))
                        self.turn_on(light)
                self.cancel_timer(self.handle)
            else:
                #self.log("motion off")
                self.handle = self.run_in(self.light_off_callback, self.delay)
                
                
    def event_callback(self, event_name, data, kwargs):
        #self.log("event_callback triggered")
        if (self.check_motion_active()):
            #self.log("motion_active = true")
            for light in self.split_device_list(self.light):
                if (self.get_state(light) != "on"):
                    self.log("Turning {} on".format(light))
                    self.turn_on(light)
            self.cancel_timer(self.handle)
            self.handle = self.run_in(self.light_off_callback, self.delay)


    def light_off_callback(self, kwargs):
        for light in self.split_device_list(self.light):
            self.log("Turning {} off".format(light))
            self.turn_off(light)
      
    def check_motion_active(self):
            if (self.motion_active_entity == ""):
                return True
            if (self.get_state(self.motion_active_entity) == "off"):
                #self.log("return false")
                return False
            else:
                return True