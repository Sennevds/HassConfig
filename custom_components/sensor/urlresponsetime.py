from homeassistant.helpers.entity import Entity
from homeassistant.const import (CONF_NAME)
import logging
from datetime import timedelta
from homeassistant.util import Throttle

REQUIREMENTS = [
    'numpy',
    'httplib2']

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)
ATTR_TIME = 'Response time'
CONF_URL = 'url'

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the buienradar platform."""
    name = config.get(CONF_NAME)
    url = config.get(CONF_URL)
    add_devices([UrlResponseTimeSensor(name, url)])


class UrlResponseTimeSensor(Entity):
    """Representation of a Sensor."""
    def __init__(self, name, url):
        """Initialize the sensor."""
        import timeit as ti
        import numpy as np
        self._np = np
        self._ti = ti
        self._url = url
        self._state = None
        self._name = name
        self._unit_of_measurement = 's'
        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        if self.data is not None:
            return {
                ATTR_TIME: self.data
            }

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data and updates the state."""
        t = self._ti.Timer("h.request('http://www.google.com',headers={'cache-control':'no-cache'})", "from httplib2 import Http; h=Http()")
        times_p1 = t.repeat(10, 1)
        average = self._np.mean(times_p1)
        self._state = average
        self.data = average
