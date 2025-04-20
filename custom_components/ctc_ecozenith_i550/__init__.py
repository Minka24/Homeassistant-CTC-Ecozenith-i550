"""
Custom integration to integrate ctc_ecozenith_i550 with Home Assistant.

For more details about this integration, please refer to
https://github.com/ludeeus/integration_blueprint
"""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.components import modbus
from homeassistant.loader import async_get_loaded_integration
from homeassistant.const import CONF_HUB

from .api import CTCEcozenithApi
from .const import DOMAIN, LOGGER
from .coordinator import BlueprintDataUpdateCoordinator
from .data import IntegrationBlueprintData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from .data import IntegrationBlueprintConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]

async def async_setup_entry(
    hass: HomeAssistant,
    entry: IntegrationBlueprintConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    # Set up modbus hub if not already configured
    if modbus.DOMAIN not in hass.data:
        hass.data[modbus.DOMAIN] = {}
    
    if entry.data[CONF_HUB] not in hass.data[modbus.DOMAIN]:
        # Create and store modbus hub
        await hass.config_entries.async_forward_entry_setup(
            entry, modbus.DOMAIN
        )
    
    hub = modbus.get_hub(hass, entry.data[CONF_HUB])
    
    coordinator = BlueprintDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        update_interval=timedelta(minutes=1),  # Update more frequently for temperature readings
    )
    
    entry.runtime_data = IntegrationBlueprintData(
        client=CTCEcozenithApi(hub=hub),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True

async def async_unload_entry(
    hass: HomeAssistant,
    entry: IntegrationBlueprintConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: IntegrationBlueprintConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
