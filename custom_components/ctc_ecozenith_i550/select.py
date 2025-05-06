"""Select entities for CTC Ecozenith i550."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval

from .const import DOMAIN

# Common select maps
HOT_WATER_MODE_MAP = {
    0: "Economy",
    1: "Normal",
    2: "Comfort",
}
HOT_WATER_MODE_REVERSE_MAP = {v: k for k, v in HOT_WATER_MODE_MAP.items()}

HP_BLOCKED_MODE_MAP = {
    0: "Blocked",
    1: "Allowed",
}

HP_BLOCKED_MODE_REVERSE_MAP = {v: k for k, v in HP_BLOCKED_MODE_MAP.items()}

HS_MODE_MAP = {
    0: "Automatic",
    1: "On",
    2: "Off",
}

HS_MODE_REVERSE_MAP = {v: k for k, v in HS_MODE_MAP.items()}

HC_HEATING_PROGRAM_MAP = {
    0: "Economy",
    1: "Normal",
    2: "Comfort",
    3: "Custom",
}

HC_HEATING_PROGRAM_REVERSE_MAP = {v: k for k, v in HS_MODE_MAP.items()}

SG_MODE_MAP = {
    0: "None/Normal",
    1: "Block",
    2: "Low price",
    3: "High cap",
}
SGMODE_READ_TO_WRITE = {
    0: 0,
    1: 64,
    2: 128,
    3: 192,
}
SGMODE_WRITE_TO_READ = {v: k for k, v in SGMODE_READ_TO_WRITE.items()}


@dataclass(frozen=True, kw_only=True)
class CTCSelectEntityDescription(SelectEntityDescription):
    """Describes a CTC Ecozenith select entity."""

    register: int
    options_map: dict[int, str]
    reverse_map: dict[str, int]
    value_key: str


SELECTS: tuple[CTCSelectEntityDescription, ...] = (
    CTCSelectEntityDescription(
        key="hot_water_mode",
        name="Hot Water Mode",
        register=61500,
        options_map=HOT_WATER_MODE_MAP,
        reverse_map=HOT_WATER_MODE_REVERSE_MAP,
        value_key="hot_water_mode",
    ),
    CTCSelectEntityDescription(
        key="heat_pump_1_blocked",
        name="Heat Pump Blocked Mode",
        register=61521,
        options_map=HP_BLOCKED_MODE_MAP,
        reverse_map=HP_BLOCKED_MODE_REVERSE_MAP,
        value_key="heat_pump_1_blocked",
    ),
    CTCSelectEntityDescription(
        key="heat_pump_2_blocked",
        name="Heat Pump 2 Blocked Mode",
        register=61522,
        options_map=HP_BLOCKED_MODE_MAP,
        reverse_map=HP_BLOCKED_MODE_REVERSE_MAP,
        value_key="heat_pump_2_blocked",
    ),
    CTCSelectEntityDescription(
        key="heat_pump_3_blocked",
        name="Heat Pump 3 Blocked Mode",
        register=61523,
        options_map=HP_BLOCKED_MODE_MAP,
        reverse_map=HP_BLOCKED_MODE_REVERSE_MAP,
        value_key="heat_pump_3_blocked",
    ),
    CTCSelectEntityDescription(
        key="heat_pump_4_blocked",
        name="Heat Pump 4 Blocked Mode",
        register=61524,
        options_map=HP_BLOCKED_MODE_MAP,
        reverse_map=HP_BLOCKED_MODE_REVERSE_MAP,
        value_key="heat_pump_4_blocked",
    ),
    CTCSelectEntityDescription(
        key="heat_pump_5_blocked",
        name="Heat Pump 5 Blocked Mode",
        register=61525,
        options_map=HP_BLOCKED_MODE_MAP,
        reverse_map=HP_BLOCKED_MODE_REVERSE_MAP,
        value_key="heat_pump_5_blocked",
    ),
    CTCSelectEntityDescription(
        key="heat_pump_6_blocked",
        name="Heat Pump 6 Blocked Mode",
        register=61526,
        options_map=HP_BLOCKED_MODE_MAP,
        reverse_map=HP_BLOCKED_MODE_REVERSE_MAP,
        value_key="heat_pump_6_blocked",
    ),
    CTCSelectEntityDescription(
        key="heat_pump_7_blocked",
        name="Heat Pump 7 Blocked Mode",
        register=61527,
        options_map=HP_BLOCKED_MODE_MAP,
        reverse_map=HP_BLOCKED_MODE_REVERSE_MAP,
        value_key="heat_pump_7_blocked",
    ),
    CTCSelectEntityDescription(
        key="heat_pump_8_blocked",
        name="Heat Pump 8 Blocked Mode",
        register=61528,
        options_map=HP_BLOCKED_MODE_MAP,
        reverse_map=HP_BLOCKED_MODE_REVERSE_MAP,
        value_key="heat_pump_8_blocked",
    ),
    CTCSelectEntityDescription(
        key="heat_pump_9_blocked",
        name="Heat Pump 9 Blocked Mode",
        register=61529,
        options_map=HP_BLOCKED_MODE_MAP,
        reverse_map=HP_BLOCKED_MODE_REVERSE_MAP,
        value_key="heat_pump_9_blocked",
    ),
    CTCSelectEntityDescription(
        key="heat_pump_10_blocked",
        name="Heat Pump 10 Blocked Mode",
        register=61530,
        options_map=HP_BLOCKED_MODE_MAP,
        reverse_map=HP_BLOCKED_MODE_REVERSE_MAP,
        value_key="heat_pump_10_blocked",
    ),
    CTCSelectEntityDescription(
        key="hs_1_heating_mode",
        name="Heating system 1: Heating mode",
        register=61542,
        options_map=HS_MODE_MAP,
        reverse_map=HS_MODE_REVERSE_MAP,
        value_key="hs_1_heating_mode",
    ),
    CTCSelectEntityDescription(
        key="hs_2_heating_mode",
        name="Heating system 2: Heating mode",
        register=61543,
        options_map=HS_MODE_MAP,
        reverse_map=HS_MODE_REVERSE_MAP,
        value_key="hs_2_heating_mode",
    ),
    CTCSelectEntityDescription(
        key="hs_3_heating_mode",
        name="Heating system 3: Heating mode",
        register=61544,
        options_map=HS_MODE_MAP,
        reverse_map=HS_MODE_REVERSE_MAP,
        value_key="hs_3_heating_mode",
    ),
    CTCSelectEntityDescription(
        key="hs_4_heating_mode",
        name="Heating system 4: Heating mode",
        register=61545,
        options_map=HS_MODE_MAP,
        reverse_map=HS_MODE_REVERSE_MAP,
        value_key="hs_4_heating_mode",
    ),
    CTCSelectEntityDescription(
        key="hc_1_heating_program",
        name="Heating circuit 1: Heating program",
        register=61671,
        options_map=HC_HEATING_PROGRAM_MAP,
        reverse_map=HC_HEATING_PROGRAM_REVERSE_MAP,
        value_key="hc_1_heating_program",
    ),
    CTCSelectEntityDescription(
        key="hc_2_heating_program",
        name="Heating circuit 2: Heating program",
        register=61672,
        options_map=HC_HEATING_PROGRAM_MAP,
        reverse_map=HC_HEATING_PROGRAM_REVERSE_MAP,
        value_key="hc_2_heating_program",
    ),
    CTCSelectEntityDescription(
        key="hc_3_heating_program",
        name="Heating circuit 3: Heating program",
        register=61673,
        options_map=HC_HEATING_PROGRAM_MAP,
        reverse_map=HC_HEATING_PROGRAM_REVERSE_MAP,
        value_key="hc_3_heating_program",
    ),
    CTCSelectEntityDescription(
        key="hc_4_heating_program",
        name="Heating circuit 4: Heating program",
        register=61674,
        options_map=HC_HEATING_PROGRAM_MAP,
        reverse_map=HC_HEATING_PROGRAM_REVERSE_MAP,
        value_key="hc_4_heating_program",
    ),
    CTCSelectEntityDescription(
        key="sgmode",
        name="SmartGrid Mode",
        register=1100,
        options_map=SG_MODE_MAP,
        reverse_map={v: k for k, v in SG_MODE_MAP.items()},
        value_key="sgmode",
    ),
    # Add more selects here, reusing maps if needed
)


def get_device_info(entity_key: str) -> dict:
    """Return device info for grouping entities by heat pump or main device."""
    if entity_key.startswith("heat_pump_"):
        parts = entity_key.split("_")
        if len(parts) > 2 and parts[2].isdigit():
            hp_number = parts[2]
            return {
                "identifiers": {(DOMAIN, f"ctc_hp_{hp_number}")},
                "name": f"Heat Pump {hp_number}",
                "manufacturer": "CTC",
                "model": "Ecozenith i550",
            }
    return {
        "identifiers": {(DOMAIN, "ctc_ecozenith_i550")},
        "name": "CTC Ecozenith i550",
        "manufacturer": "CTC",
        "model": "Ecozenith i550",
    }


class CTCEcozenithSelect(SelectEntity):
    """Generic select entity for CTC Ecozenith i550."""

    entity_description: CTCSelectEntityDescription

    def __init__(
        self, coordinator: Any, description: CTCSelectEntityDescription
    ) -> None:
        """Initialize the select entity."""
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_name = description.name
        self._attr_options = list(description.options_map.values())
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}-{description.key}"

    @property
    def device_info(self) -> dict:
        """Return device info for grouping selects by heat pump or main device."""
        return get_device_info(self.entity_description.key)

    @property
    def current_option(self) -> str | None:
        """Return the current option."""
        value = self.coordinator.data.get(self.entity_description.value_key)
        return self.entity_description.options_map.get(value)

    async def async_select_option(self, option: str) -> None:
        """Set the selected option."""
        value = self.entity_description.reverse_map[option]
        await self.coordinator.async_write_register(
            self.entity_description.register, value
        )
        await self.coordinator.async_request_refresh()

    @property
    def available(self) -> bool:
        """Return True if select data is available."""
        return self.entity_description.value_key in self.coordinator.data


def filter_heatpump_sensors(
    sensor_descriptions: list[SelectEntityDescription],
) -> list[SelectEntityDescription]:
    """Filter sensor descriptions to only include the configured number of heat pumps."""
    filtered: list[SelectEntityDescription] = []
    for desc in sensor_descriptions:
        if desc.key.startswith("heat_pump_"):
            parts = desc.key.split("_")
            if len(parts) > 2 and parts[2].isdigit():
                filtered.append(desc)
                continue
        if desc.key.startswith("hs") or desc.key.startswith("hc"):
            parts = desc.key.split("_")
            if len(parts) > 2 and parts[1].isdigit():
                filtered.append(desc)
        filtered.append(desc)
    return filtered


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CTC Ecozenith i550 select entities from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for description in SELECTS:
        if coordinator.data.get(description.key) is None:
            continue
        if description.key == "sgmode":
            entities.append(CTCEcozenithSGModeSelect(coordinator, description))
        else:
            entities.append(CTCEcozenithSelect(coordinator, description))
    async_add_entities(entities)


class CTCEcozenithSGModeSelect(CTCEcozenithSelect):
    """SmartGrid select entity with periodic write."""

    def __init__(self, coordinator, description) -> None:
        """Initialize the SmartGrid select entity."""

        super().__init__(coordinator, description)
        self._unsub_timer = None
        self._write_lock = asyncio.Lock()

    async def async_added_to_hass(self) -> None:
        """Start periodic write when entity is added."""
        await super().async_added_to_hass()
        self._unsub_timer = async_track_time_interval(
            self.hass, self._async_periodic_write, timedelta(minutes=5)
        )

    async def async_will_remove_from_hass(self) -> None:
        """Cleanup on remove."""
        if self._unsub_timer:
            self._unsub_timer()
        await super().async_will_remove_from_hass()

    @property
    def current_option(self) -> str | None:
        """Return the current option."""
        value = self.coordinator.data.get(self.entity_description.value_key)
        return self.entity_description.options_map.get(value)

    async def async_select_option(self, option: str) -> None:
        """Set the selected option."""
        value = self.entity_description.reverse_map[option]
        write_value = SGMODE_READ_TO_WRITE.get(value)
        if write_value is not None:
            async with self._write_lock:
                await self.coordinator.async_write_register(
                    self.entity_description.register, write_value
                )
                await self.coordinator.async_request_refresh()

    async def _async_periodic_write(self, now) -> None:
        """Periodically write the current value to prevent reset."""
        value = self.coordinator.data.get(self.entity_description.value_key)
        write_value = SGMODE_READ_TO_WRITE.get(value)
        if write_value is not None:
            async with self._write_lock:
                await self.coordinator.async_write_register(
                    self.entity_description.register, write_value
                )
