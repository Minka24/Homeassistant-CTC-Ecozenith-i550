"""Feature register model for CTC Ecozenith i550."""

from dataclasses import dataclass
import logging
from typing import Any

_LOGGER = logging.getLogger(__name__)

@dataclass(slots=True)
class FeatureRegister:
    """Model representing a register for CTC devices."""

    address: int
    visible_adresss: int
    visible_bit: int
    min_value_adresss: int | None = None
    max_value_adresss: int | None = None
    step_adresss: int | None = None
    scale: float = 1.0
    signed: bool = True
    value: float | None = None
    visible: bool = False
    step: float | None = None
    min_value: float | None = None
    max_value: float | None = None
    bit: int | None = None  # for async_write

    def read(self, address: int, scale: float, client: Any) -> float | None:
        """Read the value from the register, extracting bit if specified."""
        rr = client.read_holding_registers(address)
        if rr.isError():
            return None
        raw = rr.registers[0]
        if self.signed and raw >= 32768:
            raw -= 65536  # convert to signed int16
        return raw * scale

    def update(self, client: Any):
        """Update visibility, value, min, max, and step from their respective registers."""
        # Read visibility register and extract bit
        rr_visible = client.read_holding_registers(self.visible_adresss)
        if not rr_visible.isError():
            self.visible = bool((rr_visible.registers[0] >> self.visible_bit) & 1)
        else:
            self.visible = False
            _LOGGER.error(
                "Unable to read visible address %s, error: %s",
                self.visible_adresss,
                rr_visible,
            )

        # Read value
        if self.visible or self.address == 62006:
            value = self.read(self.address, self.scale, client)
            self.value = value
        else:
            _LOGGER.warning(
                "Register %s is not visible, skipping read. Visible bit: %s, visible value %s",
                self.visible_bit,
                self.address,
                rr_visible.registers[0] if hasattr(rr_visible, "registers") else None,
            )

        # Read min value
        if self.min_value_adresss is not None:
            min_rr = client.read_holding_registers(self.min_value_adresss)
            self.min_value = (
                min_rr.registers[0] * self.scale if not min_rr.isError() else None
            )

        # Read max value
        if self.max_value_adresss is not None:
            max_rr = client.read_holding_registers(self.max_value_adresss)
            self.max_value = (
                max_rr.registers[0] * self.scale if not max_rr.isError() else None
            )

        # Read step value
        if self.step_adresss is not None:
            step_rr = client.read_holding_registers(self.step_adresss)
            self.step = (
                step_rr.registers[0] * self.scale if not step_rr.isError() else None
            )

    async def async_write(self, client: Any, value: float | bool) -> bool:
        """Write a value to the register, handling bit if specified."""
        if self.bit is not None:
            rr = await client.read_holding_registers(self.address)
            if rr.isError():
                return False
            reg_val = rr.registers[0]
            if value:
                reg_val |= 1 << self.bit
            else:
                reg_val &= ~(1 << self.bit)
            result = await client.write_register(self.address, reg_val)
            return not result.isError()

        scaled = int(value / self.scale)
        result = await client.write_register(self.address, scaled)
        return not result.isError()
