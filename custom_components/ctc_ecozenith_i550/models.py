"""Data models for CTC Ecozenith i550 integration."""

from dataclasses import dataclass
from typing import Optional

@dataclass
class EcozenithStatus:
    """Data model for the status of the CTC Ecozenith i550."""
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    operational_status: Optional[str] = None

@dataclass
class EcozenithSettings:
    """Data model for the settings of the CTC Ecozenith i550."""
    set_temperature: Optional[float] = None
    mode: Optional[str] = None
    schedule: Optional[dict] = None  # Could be a more complex structure depending on requirements
