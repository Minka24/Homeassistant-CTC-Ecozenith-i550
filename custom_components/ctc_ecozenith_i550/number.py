"""Number entities for CTC Ecozenith i550."""

import logging

from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import BMS_REGISTERS
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up number entities for CTC Ecozenith i550."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for key in [
        "max_immersion_heater_dhw_kw_upper",
        "max_immersion_heater_kw_lower",
    ]:
        reg = BMS_REGISTERS[key]
        _LOGGER.warning("Register %s", key)
        entities.append(
            CTCNumberEntity(
                coordinator,
                NumberEntityDescription(
                    key=key + "_number",
                    name=key.replace("_", " ").title(),
                    native_unit_of_measurement="kW",
                ),
                reg,
            )
        )
    async_add_entities(entities)


class CTCNumberEntity(NumberEntity):
    """Number entity for CTC Ecozenith i550."""

    def __init__(self, coordinator, description, feature_register):
        """Initialize the number entity."""
        self.coordinator = coordinator
        self.entity_description = description
        self.feature_register = feature_register
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}-{description.key}"

    @property
    def device_info(self) -> dict:
        """Return device information for this entity."""
        return {
            "identifiers": {(DOMAIN, "ctc_ecozenith_i550")},
            "name": "CTC Ecozenith i550",
            "manufacturer": "CTC",
            "model": "Ecozenith i550",
        }

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        return self.feature_register.value

    @property
    def native_min_value(self) -> float:
        """Return the minimum value."""
        return self.feature_register.min_value

    @property
    def native_max_value(self) -> float:
        """Return the maximum value."""
        return self.feature_register.max_value

    @property
    def native_step(self) -> float:
        """Return the step value."""
        return self.feature_register.step

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        await self.coordinator.async_write_register(
            self.feature_register.address, int(value / self.feature_register.scale)
        )
        await self.coordinator.async_request_refresh()
