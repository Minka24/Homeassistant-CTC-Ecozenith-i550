"""Feature register model for CTC Ecozenith i550."""

from dataclasses import dataclass
from typing import Any


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
    value: float | None = None
    visible: bool = False
    step: float | None = None
    min_value: float | None = None
    max_value: float | None = None

    def read(self, address: int, scale: float, client: Any) -> float | None:
        """Read the value from the register, extracting bit if specified."""
        rr = client.read_holding_registers(address, 1, 1)
        if rr.isError():
            return None
        return rr.registers[0] * scale

    def update(self, client: Any):
        """Update visibility, value, min, max, and step from their respective registers."""
        # Read visibility register and extract bit

        rr_visible = client.read_holding_registers(self.visible_adresss, 1, 1)
        if not rr_visible.isError():
            self.visible = bool((rr_visible.registers[0] >> self.visible_bit) & 1)
        else:
            self.visible = False

        # Read value
        if self.visible:
            value = self.read(self.address, self.scale, client)
            self.value = value

        # Read min value
        # Check if min_value_adresss is not None before reading
        # This is to avoid unnecessary Modbus calls
        # and to ensure that the code is more robust
        # and maintainable
        if self.min_value_adresss is not None:
            min_rr = client.read_holding_registers(self.min_value_adresss, 1, 1)
            self.min_value = (
                min_rr.registers[0] * self.scale if not min_rr.isError() else None
            )

        # Read max value
        # Check if max_value_adresss is not None before reading
        # This is to avoid unnecessary Modbus calls
        # and to ensure that the code is more robust
        # and maintainable
        if self.max_value_adresss is not None:
            max_rr = client.read_holding_registers(self.max_value_adresss, 1, 1)
            self.max_value = (
                max_rr.registers[0] * self.scale if not max_rr.isError() else None
            )

        # Read step value
        # Check if step_adresss is not None before reading
        # This is to avoid unnecessary Modbus calls
        # and to ensure that the code is more robust
        # and maintainable
        if (
            self.step_adresss is not None
        ):  # Check if step_adresss is not None before reading
            step_rr = client.read_holding_registers(self.step_adresss, 1, 1)
            self.step = (
                step_rr.registers[0] * self.scale if not step_rr.isError() else None
            )

    async def async_write(self, client: Any, value: float | bool) -> bool:
        """Write a value to the register, handling bit if specified."""
        if self.bit is not None:
            rr = await client.read_holding_registers(self.address, 1, 1)
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
