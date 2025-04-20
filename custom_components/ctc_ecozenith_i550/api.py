"""CTC Ecozenith i550 API Client."""

from __future__ import annotations

import asyncio
import socket
from typing import Any

import aiohttp
import async_timeout
from homeassistant.components.modbus import ModbusHub
from homeassistant.const import UnitOfTemperature


class IntegrationBlueprintApiClientError(Exception):
    """Exception to indicate a general API error."""


class IntegrationBlueprintApiClientCommunicationError(
    IntegrationBlueprintApiClientError,
):
    """Exception to indicate a communication error."""


class IntegrationBlueprintApiClientAuthenticationError(
    IntegrationBlueprintApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise IntegrationBlueprintApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class CTCEcozenithModbusError(Exception):
    """Exception class for Modbus errors."""


class CTCEcozenithApi:
    """CTC Ecozenith i550 API client."""

    def __init__(self, hub: ModbusHub) -> None:
        """Initialize the API client."""
        self._hub = hub
        self._lock = asyncio.Lock()

    async def async_read_holding_registers(self, address: int, count: int) -> list[int]:
        """Read holding registers."""
        async with self._lock:
            result = await self._hub.async_read_holding_registers(
                slave=1,  # Default slave address
                address=address,
                count=count,
            )
            if result.isError():
                raise CTCEcozenithModbusError(f"Error reading registers: {result}")
            return result.registers

    async def async_read_temperature(self, address: int) -> float:
        """Read temperature value from register."""
        registers = await self.async_read_holding_registers(address, 1)
        return float(registers[0]) / 10.0

    async def async_get_data(self) -> dict[str, Any]:
        """Get data from the heat pump."""
        try:
            data = {
                "outdoor_temp": await self.async_read_temperature(62000),
                "stop_temperature_dhw ": await self.async_read_temperature(62001), 
                "hot_water_temp": await self.async_read_temperature(62002),
                "setpoint_outlet_temperature_dhw": await self.async_read_temperature(62003),
                "hot_water_temperature": await self.async_read_temperature(62006),
                "radiator_water": UnitOfTemperature.CELSIUS
            }
            return data
        except Exception as ex:
            raise CTCEcozenithModbusError(f"Error getting data: {ex}") from ex


class IntegrationBlueprintApiClient:
    """Sample API Client."""

    def __init__(
        self,
        username: str,
        password: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._username = username
        self._password = password
        self._session = session

    async def async_get_data(self) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="get",
            url="https://jsonplaceholder.typicode.com/posts/1",
        )

    async def async_set_title(self, value: str) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="patch",
            url="https://jsonplaceholder.typicode.com/posts/1",
            data={"title": value},
            headers={"Content-type": "application/json; charset=UTF-8"},
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise IntegrationBlueprintApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise IntegrationBlueprintApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise IntegrationBlueprintApiClientError(
                msg,
            ) from exception
