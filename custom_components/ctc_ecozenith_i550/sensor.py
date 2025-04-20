"""Sensor platform for CTC Ecozenith i550."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity, 
    SensorEntityDescription,
)
from homeassistant.const import UnitOfTemperature

from .const import DOMAIN
from .entity import CTCEcozenithEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeassistant.config_entries import ConfigEntry

TEMPERATURE_SENSORS = (
    SensorEntityDescription(
        key="outdoor_temp",
        name="Outdoor Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    SensorEntityDescription(
        key="indoor_temp",
        name="Indoor Temperature",
        device_class=SensorDeviceClass.TEMPERATURE, 
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    SensorEntityDescription(
        key="hot_water_temp",
        name="Hot Water Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS, 
    ),
    SensorEntityDescription(
        key="tank_temp",
        name="Tank Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    SensorEntityDescription(
        key="heating_circuit_temp", 
        name="Heating Circuit Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    async_add_entities(
        CTCEcozenithSensor(
            coordinator=coordinator,
            entity_description=description,
        )
        for description in TEMPERATURE_SENSORS
    )

class CTCEcozenithSensor(CTCEcozenithEntity, SensorEntity):
    """CTC Ecozenith temperature sensor."""

    def __init__(
        self,
        coordinator: Any,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{DOMAIN}_{entity_description.key}"

    @property
    def native_value(self) -> float | None:
        """Return the sensor value."""
        return self.coordinator.data.get(self.entity_description.key)
