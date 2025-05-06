"""Coordinator for CTC Ecozenith i550 integration."""

from __future__ import annotations

from datetime import timedelta
import logging

from pymodbus.client import ModbusTcpClient

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVAL = timedelta(seconds=5)


class CTCEcozenithDataUpdateCoordinator(DataUpdateCoordinator[dict]):
    """Coordinator for CTC Ecozenith i550."""

    def __init__(
        self, hass: HomeAssistant, host: str, port: int, update_method
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )
        self._client = ModbusTcpClient(host=host, port=port)
        self.update_method = update_method

    async def _async_update_data(self) -> dict:
        """Fetch data from the heat pump."""
        try:
            # Only connect if not already connected
            if not self._client.connected:
                if not await self.hass.async_add_executor_job(self._client.connect):
                    raise UpdateFailed("Could not connect to Modbus device")
            return await self.hass.async_add_executor_job(
                self.update_method, self._client
            )
        except Exception as err:
            raise UpdateFailed(
                f"Error communicating with the heat pump: {err}"
            ) from err

    async def async_write_register(self, address: int, value: int) -> None:
        """Write a value to a Modbus register asynchronously."""

        # Ensure connection
        if not self._client.connected:
            _LOGGER.debug("Modbus client not connected, attempting to connect")
            if not await self.hass.async_add_executor_job(self._client.connect):
                raise UpdateFailed("Could not connect to Modbus device")

        def _write():
            # Write a single register (16 bit)
            return self._client.write_register(address, value, 1)

        result = await self.hass.async_add_executor_job(_write)
        # Add debug logging
        _LOGGER.debug(
            "Modbus write_register(%s, %s) result: %s", address, value, result
        )
        if not hasattr(result, "isError") or result.isError():
            _LOGGER.error("Modbus write_register failed: %s", result)
            raise UpdateFailed(f"Failed to write value {value} to register {address}")

    async def async_close(self) -> None:
        """Close the Modbus client connection."""
        await self.hass.async_add_executor_job(self._client.close)
