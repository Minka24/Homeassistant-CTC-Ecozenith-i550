"""Integration for CTC Ecozenith i550."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import BMS_REGISTERS, DOMAIN
from .coordinator import CTCEcozenithDataUpdateCoordinator


def update_method(client) -> dict:
    """Fetch all required registers from the heat pump using a shared client."""
    result = {}
    for key, feature_register in BMS_REGISTERS.items():
        feature_register.update(client)
        result[key] = feature_register.value
    return result


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up CTC Ecozenith i550 from a config entry."""
    coordinator = CTCEcozenithDataUpdateCoordinator(
        hass, entry.data["host"], entry.data["port"], update_method
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Only this line should forward to the sensor platform
    await hass.config_entries.async_forward_entry_setups(
        entry, ["sensor", "select", "number"]
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the config entry and close the Modbus connection."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, ["sensor", "select", "number"]
    )
    coordinator = hass.data[DOMAIN].pop(entry.entry_id)
    await coordinator.async_close()
    return unload_ok
