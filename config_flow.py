"""Config flow for CTC Ecozenith i550."""

from __future__ import annotations

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.core import callback

from .const import DEFAULT_NAME, DEFAULT_PORT, DOMAIN


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Required("has_cooling", default=True): bool,
        vol.Required("num_heating_systems", default=1): vol.All(
            int, vol.Range(min=0, max=4)
        ),
        vol.Required("has_solar", default=False): bool,
    }
)

OPTIONS_SCHEMA = vol.Schema({})


class CTCEcozenithConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for CTC Ecozenith i550."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> config_entries.FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Test the connection
                client = ModbusTcpClient(
                    host=user_input[CONF_HOST], port=user_input[CONF_PORT]
                )
                if not await self.hass.async_add_executor_job(client.connect):
                    errors["base"] = "cannot_connect"
                else:
                    await self.hass.async_add_executor_job(client.close)
                    # Create entry if connection test passed
                    return self.async_create_entry(
                        title=user_input[CONF_NAME],
                        data=user_input,
                    )
            except ModbusException:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return CTCEcozenithOptionsFlowHandler(config_entry)


class CTCEcozenithOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for CTC Ecozenith i550."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=OPTIONS_SCHEMA,
        )
