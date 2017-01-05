import logging

import voluptuous as vol

from homeassistant.components.switch import (SwitchDevice, PLATFORM_SCHEMA)
from homeassistant.const import (CONF_NAME, CONF_SWITCHES)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_PORT = 'port'
CONF_BAUD = 'baudrate'
CONF_PIN = 'pin'
CONF_TYPE = 'type'
CONF_DEVICECODE = 'code'

SWITCH_SCHEMA = vol.Schema({
    vol.Required(CONF_DEVICECODE): cv.string,
    vol.Required(CONF_PIN): cv.string,
    vol.Required(CONF_TYPE): cv.string,
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_PORT): cv.string,
    vol.Required(CONF_BAUD): cv.string,
    vol.Required(CONF_SWITCHES): vol.Schema({cv.string: SWITCH_SCHEMA}),
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the SRF component."""
    import llap.messages as lm
    from llap.controller import ControllerThread
    from queue import Queue

    switches = config.get(CONF_SWITCHES)
    port = config.get(CONF_PORT)
    baudrate = config.get(CONF_BAUD)
    event_queue = Queue()
    command_queue = Queue()
    controller = ControllerThread(port, baudrate, event_queue, command_queue)
    controller.start()
    devices = []
    for dev_name, properties in switches.items():
        _LOGGER.debug("srf: %s", dev_name)
        devices.append(
            SrfSwitch(
                hass,
                properties.get(CONF_NAME, dev_name),
                properties.get(CONF_DEVICECODE),
                lm,
                command_queue,
                properties.get(CONF_PIN),
                properties.get(CONF_TYPE)
            )
        )

    add_devices(devices)


class SrfSwitch(SwitchDevice):
    """Representation of a srf switch."""

    def __init__(self, hass, name, code, lm, command_queue, pin, pinType):
        """Initialize the switch."""
        self._hass = hass
        self._name = name
        self._code = code
        self._state = False
        self._lm = lm
        self._queue = command_queue
        self._pin = pin
        self._pinType = pinType

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._state

    def _send_message(self, code, pin, typeIO, state):
        """Send the code with a specified pulselength."""
        #_LOGGER.debug("Sending following message: pin: %s pinType: %s to: %s", pin, state, code)
        device = code
        msg = typeIO + pin
        _LOGGER.debug("msg send: " + msg)
        hello = self._lm.ButtonSwitch(device,msg,state)
        _LOGGER.debug("SRF send: %s", hello)
        self._queue.put(hello)
        return True

    def turn_on(self):
        """Turn the switch on."""
        if self._send_message(self._code, self._pin, self._pinType, True):
            self._state = True
            self.update_ha_state()

    def turn_off(self):
        """Turn the switch off."""
        if self._send_message(self._code, self._pin, self._pinType, False):
            self._state = False
            self.update_ha_state()
