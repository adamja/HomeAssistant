from Light import Light
from MyLogger2 import MyLogger
import appdaemon.appapi as appapi

### Comments ###

### Args ###
'''
{app_name}:
    module: Lights
    class: Lights
'''


class Lights(appapi.AppDaemon):

    def initialize(self):
        """Initializing function"""
        # VARIABLES
        self.light_list = {}

        # LOGGER
        self.logger = MyLogger(__name__, file_location="/conf/logs/" + __name__)
        self.logger.set_module_name(self.name)
        self.logger.debug("Started.")

# -------------------------------------------------------------------------------------------------------------------- #
# Functions
# -------------------------------------------------------------------------------------------------------------------- #

    def add_light(self, entity_id, **kwargs):
        """Add a light to light_list"""
        self.light_list[entity_id] = Light(entity_id, **kwargs)
        self.logger.debug("Add light to list: {} - kwargs: {}".format(entity_id, kwargs))
        return True

    def remove_light(self, entity_id):
        '''Remove a light from light_list'''
        try:
            del self.light_list[entity_id]
            self.logger.debug("Removed light from list: {}".format(entity_id))
        except:
            return False
        return True

    def get_light(self, entity_id):
        '''Get the light from light_list'''
        for key, value in self.light_list.items():
            if key == entity_id:
                return value
        self.add_light(entity_id)
        return self.light_list[entity_id]

    def update_light(self, entity_id, **kwargs):
        light = self.get_light(entity_id)
        light.update_settings(**kwargs)
        self.logger.debug("Updated lights settings. kwargs: {}".format(kwargs))
        return True

    def on(self, entity_id, **kwargs):
        '''Turn the light on with the settings from the Light class'''
        light = self.get_light(entity_id)
        light.on(**kwargs)
        self.logger.debug("Turned light on: {} - kwargs: {}".format(entity_id, kwargs))
        return True

    def off(self, entity_id):
        '''Turn the light off from the light class'''
        light = self.get_light(entity_id)
        light.off()
        self.logger.debug("Turned light off: {}".format(entity_id))
        return True

    def toggle(self, entity_id, **kwargs):
        """Toggle the light from the light class"""
        light = self.get_light(entity_id)
        if self.get_state(entity_id) == 'on':
            light.off()
            self.logger.debug("Turned light on(toggle): {} - kwargs: {}".format(entity_id, kwargs))
        else:
            light.on()
            self.logger.debug("Turned light off(toggle): {}".format(entity_id))
