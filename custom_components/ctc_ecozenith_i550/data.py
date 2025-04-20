"""Custom types for ctc_ecozenith_i550."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import CTCEcozenithApi
    from .coordinator import BlueprintDataUpdateCoordinator


type IntegrationBlueprintConfigEntry = ConfigEntry[IntegrationBlueprintData]


@dataclass
class IntegrationBlueprintData:
    """Data for the CTC Ecozenith integration."""

    client: CTCEcozenithApi
    coordinator: BlueprintDataUpdateCoordinator
    integration: Integration
