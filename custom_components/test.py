import logging

import homeassistant.loader as loader

from homeassistant.components import light

from homeassistant.helpers.event import async_track_state_change


DOMAIN = 'slider_update'

DEPENDENCIES = ['light']

LOGGER = logging.getLogger(__name__)


def setup(hass, config):

    LOGGER.info("The 'slider_update' component is ready!")


    CONF_PAIRS = config[DOMAIN]

    LOGGER.info(CONF_PAIRS)
