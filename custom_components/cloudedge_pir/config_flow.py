"""Config flow for CloudEdge PIR Integration integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.const import CONF_NAME, CONF_EMAIL, CONF_PASSWORD

from .const import DOMAIN

from .meari_sdk import MeariSDK
from .const import CONF_COUNTRY_CODE, CONF_PHONE_CODE, CONF_WAIT_TO_RESET

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_PHONE_CODE): str,
        vol.Required(CONF_COUNTRY_CODE): str,
        vol.Required(CONF_NAME): str,
        vol.Required(CONF_WAIT_TO_RESET, default=5): int,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for CloudEdge PIR Integration."""

    VERSION = 1

    @staticmethod
    def initialize_meari_sdk(
        user_input: dict[str, Any]
    ) -> tuple[dict[Any, Any], dict[str, Any]]:
        data = {
            CONF_EMAIL: user_input[CONF_EMAIL],
            CONF_PASSWORD: user_input[CONF_PASSWORD],
            CONF_PHONE_CODE: user_input[CONF_PHONE_CODE],
            CONF_COUNTRY_CODE: user_input[CONF_COUNTRY_CODE],
            CONF_NAME: user_input[CONF_NAME],
            CONF_WAIT_TO_RESET: user_input[CONF_WAIT_TO_RESET],
        }

        meari_client = MeariSDK(
            account=data[CONF_EMAIL],
            password=data[CONF_PASSWORD],
            phone_code=data[CONF_PHONE_CODE],
            country_code=data[CONF_COUNTRY_CODE],
        )

        response = meari_client.login()

        if response["resultCode"] != "1001":
            raise InvalidAuth

        return response, data

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            response, data = await self.hass.async_add_executor_job(
                self.initialize_meari_sdk, user_input
            )
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=data[CONF_NAME], data=data)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
