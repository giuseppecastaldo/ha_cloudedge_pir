"""The Cloud integration."""
from __future__ import annotations

import logging
from .meari_sdk import MeariSDK

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_COUNTRY_CODE, CONF_PHONE_CODE, DOMAIN
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, Platform

PLATFORMS = [Platform.BINARY_SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    meari_client = await hass.async_add_executor_job(_get_meari_client_instance, entry)
    hass.data[DOMAIN][entry.entry_id] = meari_client

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


def _get_meari_client_instance(entry: ConfigEntry) -> MeariSDK:
    """Initialize a new instance of MeariClientApi."""

    email = entry.data[CONF_EMAIL]
    password = entry.data[CONF_PASSWORD]
    country_code = entry.data[CONF_COUNTRY_CODE]
    phone_code = entry.data[CONF_PHONE_CODE]

    meari_client = MeariSDK(
        account=email,
        password=password,
        country_code=country_code,
        phone_code=phone_code,
    )

    meari_client.login()

    return meari_client


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
