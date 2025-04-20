"""Config flow for CTC Ecozenith i550."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.components.modbus.const import (
    CONF_TYPE,
    DEFAULT_HUB,
    MODBUS_DOMAIN,
    CONF_TCP_IP
)

from .const import DOMAIN, DEFAULT_NAME, DEFAULT_PORT

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Optional(CONF_TYPE, default=CONF_TCP_IP): str,
    }
)

class CTCEcozenithConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for CTC Ecozenith i550."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> config_entries.FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Create Modbus hub config entry
            hub_name = DEFAULT_HUB
            modbus_data = {
                CONF_NAME: hub_name,
                CONF_HOST: user_input[CONF_HOST],
                CONF_PORT: user_input[CONF_PORT],
                CONF_TYPE: user_input[CONF_TYPE],
            }

            # Create the Modbus hub first
            hub_entry = await self.async_set_unique_id(f"{DOMAIN}_{user_input[CONF_HOST]}")
            self._abort_if_unique_id_configured()
            
            # Store the hub configuration
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data={
                    **user_input,
                    "hub": hub_name,
                    "modbus_data": modbus_data,
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
