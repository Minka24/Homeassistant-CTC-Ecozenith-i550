"""Config flow for CTC Ecozenith i550."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PORT,
    CONF_TYPE,
)
from homeassistant.components.modbus import (
    CONF_HUB,
    DEFAULT_HUB,
    DEFAULT_PORT,
    DEFAULT_TYPE,
    MODBUS_DOMAIN,
)
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, LOGGER

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default="CTC Ecozenith"): str,
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Required(CONF_TYPE, default=DEFAULT_TYPE): str,
    }
)

class CTCEcozenithConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for CTC Ecozenith i550."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
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
            self._async_abort_entries_match({CONF_HOST: user_input[CONF_HOST]})
            
            # Store the hub configuration
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data={
                    **user_input,
                    CONF_HUB: hub_name,
                    "modbus_data": modbus_data,
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
