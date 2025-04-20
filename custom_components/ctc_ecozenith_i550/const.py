"""Constants for ctc_ecozenith_i550."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "ctc_ecozenith_i550"
ATTRIBUTION = "Data provided by CTC Ecozenith i550"

# Default values
DEFAULT_NAME = "CTC Ecozenith i550"
DEFAULT_PORT = 502  # Default Modbus TCP port
