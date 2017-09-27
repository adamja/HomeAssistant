import appdaemon.appapi as appapi
from MyLogger import MyLogger


### Comments ###

### Args ###
'''
{app_name}:
    module: button_entity
    class: ButtonEntity
    buttons: {entity_id for switches}
    devices: {enitiy_id for devices}
    click_type: {single, double, hold}
    mode: {on, off, toggle, toggle_multi}
'''


class ButtonEntity(appapi.AppDaemon):
    def initialize(self):
        # Start logger
        self.logger = MyLogger(__name__ + "-" + self.name, file_location="/conf/logs",
                               log_level=MyLogger.DEBUG)
        self.logger.set_console_log_level(MyLogger.INFO)
        self.logger.set_logfile_log_level(MyLogger.DEBUG)
        self.logger.debug("Log Started.")

        self.buttons = self.args["buttons"]
        self.devices = self.args["devices"]
        self.click_type = self.args["click_type"]
        self.mode = self.args["mode"]
        self.logger.info("Button entity_id(s): {}.".format(self.buttons))
        self.logger.info("Device entity_id(s): {}.".format(self.devices))
        self.logger.info("click_type mode: {}.".format(self.click_type))

        self.state = "off"
        
        for button in self.split_device_list(self.buttons):
            self.listen_event(self.event_callback, entity_id=button, event="click", click_type=self.click_type)

    def event_callback(self, event_name, data, kwargs):
        for device in self.split_device_list(self.devices):
            if (self.mode == "toggle_multi"):
                if (self.state == "on"):
                    self.logger.info("{} turned off.".format(device))
                    self.turn_off(device)
                else:
                    self.logger.info("{} turned on.".format(device))
                    self.turn_on(device)
            elif (self.mode == "toggle"):
                self.logger.info("{} toggled.".format(device))
                self.toggle(device)
            elif (self.mode == "on"):
                self.logger.info("{} turned on.".format(device))
                self.turn_on(device)
            else:
                self.logger.info("{} turned off.".format(device))
                self.turn_off(device)

        if (self.state == "on"):
            self.state = "off"
        else:
            self.state = "on"