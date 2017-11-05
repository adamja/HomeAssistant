import appdaemon.appapi as appapi
from datetime import datetime
from MyLogger2 import MyLogger

### Comments ###

### Args ###
"""
{app_name}:
    module: door_bell
    class: DoorBell
    motion_entity: # optional, motion sensor trigger
    button_entity: # optional button trigger. Will trigger on all three click_type events: single, double, hold
    gateway_mac:   # required mac address of gateway
    tone:          # gateway tone, defaults to tone 10 (ding dong)
                   # alarm ringtones [0-8], doorbell ring [10-13] alarm clock [20-29]
    volume:        # gateway volume, defaults to 100%
    start:         # start time for motion, defaults to 7:00 if not set
    end:           # end time for motion, defaults to 22:00 if not set
"""

# https://home-assistant.io/components/xiaomi_aqara/
class DoorBell(appapi.AppDaemon):
    def initialize(self):
        # Start logger
        self.logger = MyLogger(__name__, file_location="/conf/logs/" + __name__)
        self.logger.set_module_name(self.name)
        self.logger.debug("Started.")

        self.motion_entity = None
        self.button_entity = None
        self.gateway_mac = None
        self.tone = 10       # alarm ringtones [0-8], doorbell ring [10-13] alarm clock [20-29]
        self.volume = '100'  # in percent
        self.start = '7:00'
        self.end = '22:00'

        if "motion_entity" in self.args.keys():
            self.motion_entity = self.args["motion_entity"]
        if "button_entity" in self.args.keys():
            self.button_entity = self.args["button_entity"]
        if "gateway_mac" in self.args.keys():
            self.gateway_mac = self.args["gateway_mac"]
        if "tone" in self.args.keys():
            self.tone = self.args["tone"]
        if "volume" in self.args.keys():
            self.volume = self.args["volume"]
        if "start" in self.args.keys():
            self.start = self.args["start"]
        if "end" in self.args.keys():
            self.end = self.args["end"]

        if self.motion_entity is not None and self.gateway_mac is not None:
            self.listen_state(self.motion_callback, self.motion_entity)
        if self.button_entity is not None:
            self.listen_event(self.button_callback, entity_id=self.button_entity, event="click")
            # Can add click type to listen_event if required: click_type=self.click_type

    def motion_callback(self, entity, attributes, old, new, kwargs):
        # self.logger.debug("callback reached")
        if new == "on":
            self.logger.debug("Triggered via motion")
            now = datetime.now().time()
            t_start = datetime.strptime(self.start, '%H:%M').time()
            t_end = datetime.strptime(self.end, '%H:%M').time()

            if t_start < now:
                if t_end > now:
                    self.notify_callback()

    def button_callback(self, event_name, data, kwargs):
        if data["click_type"] != "hold":  # don't trigger when releasing the button
            self.logger.debug("Triggered via button press: {}".format(data))
            self.notify_callback()

    def notify_callback(self):
        self.logger.info("Gateway Tone Triggered. Tone: {}, Volume: {}".format(self.tone, self.volume))
        self.call_service("xiaomi_aqara/play_ringtone", ringtone_id=self.tone, gw_mac=self.gateway_mac, ringtone_vol=self.volume)
