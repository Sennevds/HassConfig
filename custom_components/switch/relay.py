from homeassistant.components.switch import (SwitchDevice, PLATFORM_SCHEMA)
from homeassistant.const import CONF_NAME
import logging
import homeassistant.helpers.config_validation as cv
import serial
from serial import SerialException


_LOGGER = logging.getLogger(__name__)
RDEVICE = '/dev/ttyS0'
BAUD = 112500
CONF_NAME = 'Name'
CONF_TYPE = 'Type'
CONF_PIN = 'Pin number'
CONF_NAMES = 'Name receiver'

MESSAGE_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
    vol.Optional(CONF_TYPE): cv.string,
    vol.Optional(CONF_PIN): cv.string,
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAMES, default={}):
        vol.Schema({cv.string: MESSAGE_SCHEMA}),
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Arduino platform."""
    # Verify that Arduino board is present

    try:
        ser = serial.Serial(RDEVICE, BAUD)
    except SerialException:
        _LOGGER.error("port already open")
        return False

    receivers = config.get(CONF_NAMES)

    switches = []
    for pinnum, pin in pins.items():
        switches.append(ArduinoSrfSwitch(pinnum, pin))
    add_devices(switches)


class ArduinoSrfSwitch(SwitchDevice):
    """Representation of an Arduino switch."""

    def __init__(self, pin, options):
        """Initialize the Pin."""

        self._pin = pin
        self._name = options.get(CONF_NAME)
        self.pin_type = CONF_TYPE
        self.direction = 'out'

        self._state = options.get(CONF_INITIAL)

        if options.get(CONF_NEGATE):
            self.turn_on_handler = arduino.BOARD.set_digital_out_low
            self.turn_off_handler = arduino.BOARD.set_digital_out_high
        else:
            self.turn_on_handler = arduino.BOARD.set_digital_out_high
            self.turn_off_handler = arduino.BOARD.set_digital_out_low

        arduino.BOARD.set_mode(self._pin, self.direction, self.pin_type)
        (self.turn_on_handler if self._state else self.turn_off_handler)(pin)

    @property
    def name(self):
        """Get the name of the pin."""
        return self._name

    @property
    def is_on(self):
        """Return true if pin is high/on."""
        return self._state

    def turn_on(self):
        """Turn the pin to high/on."""
        self._state = True
        self.turn_on_handler(self._pin)

    def turn_off(self):
        """Turn the pin to low/off."""
        self._state = False
        self.turn_off_handler(self._pin)
