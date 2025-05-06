"""Data models for CTC Ecozenith i550 integration."""

from dataclasses import dataclass


@dataclass
class EcozenithStatus:
    """Data model for the status of the CTC Ecozenith i550."""

    temperature: float | None = None
    humidity: float | None = None
    operational_status: str | None = None


@dataclass
class EcozenithSettings:
    """Data model for the settings of the CTC Ecozenith i550."""

    set_temperature: float | None = None
    mode: str | None = None
    schedule: dict | None = (
        None  # Could be a more complex structure depending on requirements
    )
