import logging
import asyncio

from .meari_sdk import MeariSDK
import paho.mqtt.client as mqtt
from homeassistant.config_entries import ConfigEntry

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import CONF_NAME

from .const import (
    CONF_WAIT_TO_RESET,
    DEVICE_CLASS,
    DOMAIN,
)

from homeassistant.components.binary_sensor import BinarySensorEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    device_name = entry.data[CONF_NAME]
    wait_to_reset = entry.data[CONF_WAIT_TO_RESET]

    meari_client: MeariSDK = hass.data[DOMAIN][entry.entry_id]
    mqtt_cred = meari_client.mqtt_credentials()

    mqtt_client = mqtt.Client(mqtt_cred["client_id"])
    mqtt_client.username_pw_set(mqtt_cred["username"], mqtt_cred["password"])
    mqtt_client.connect(mqtt_cred["host"], mqtt_cred["port"], mqtt_cred["keepalive"])
    mqtt_client.subscribe(mqtt_cred["topic"])

    mqtt_client.loop_start()

    async_add_entities(
        [CloudEdgePIRBinarySensor(device_name, wait_to_reset, mqtt_client)]
    )


class CloudEdgePIRBinarySensor(BinarySensorEntity):
    def __init__(self, name, wait_to_reset, mqtt_client):
        self._state = False
        self._name = name
        self._mqtt_client = mqtt_client
        self._wait_to_reset = wait_to_reset

        self._mqtt_client.on_message = self.on_motion_detection

    @property
    def name(self):
        """Name of the entity."""
        return self._name

    @property
    def is_on(self):
        return self._state

    @property
    def device_class(self):
        return DEVICE_CLASS

    async def reset_state(self):
        """Reset motion sensor state after motion detected"""
        await asyncio.sleep(self._wait_to_reset)
        self._state = False

        self.schedule_update_ha_state()

    def on_motion_detection(self, mqtt_client, userdata, msg):
        """Event of motion detection"""
        self._state = True
        self.schedule_update_ha_state()

        asyncio.run(self.reset_state())
