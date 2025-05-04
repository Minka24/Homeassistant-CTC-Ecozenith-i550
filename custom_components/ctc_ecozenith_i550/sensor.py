"""Sensors for CTC Ecozenith i550."""

from __future__ import annotations

from dataclasses import dataclass
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_registry import EntityRegistry

from .const import DOMAIN

SENSOR_DESCRIPTIONS = [
    # Hot Water Settings
    SensorEntityDescription(
        key="hot_water_mode",
        name="Hot Water Mode",
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="manual_stop_temp_hot_water",
        name="Manual Stop Temperature Hot Water",
        native_unit_of_measurement="°C",
        icon="mdi:water-boiler",
    ),
    SensorEntityDescription(
        key="setting_outlet_temp_hot_water",
        name="Setting Outlet Temperature Hot Water",
        native_unit_of_measurement="°C",
        icon="mdi:water-boiler",
    ),
    SensorEntityDescription(
        key="extra_hot_water_timer",
        name="Extra Hot Water Timer",
        native_unit_of_measurement="min",
        icon="mdi:timer",
    ),
    SensorEntityDescription(
        key="max_time_heating_heat_pump",
        name="Maximum Time Heating Heat Pump",
        native_unit_of_measurement="min",
        icon="mdi:timer-sand",
    ),
    SensorEntityDescription(
        key="max_time_hot_water",
        name="Maximum Time Hot Water",
        native_unit_of_measurement="min",
        icon="mdi:timer-sand",
    ),
    SensorEntityDescription(
        key="min_rps_hot_water",
        name="Minimum RPS Hot Water",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="min_rps_pool",
        name="Minimum RPS Pool",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    # Vacation and Room Settings
    SensorEntityDescription(
        key="vacation_days_timer",
        name="Number of Vacation Days Timer",
        native_unit_of_measurement="d",
        icon="mdi:calendar-clock",
    ),
    SensorEntityDescription(
        key="hs_1_setting_room_temp",
        name="Heating System 1: Setting Room Temp",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="hs_2_setting_room_temp",
        name="Heating System 2: Setting Room Temp",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="hs_3_setting_room_temp",
        name="Heating System 3: Setting Room Temp",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="hs_4_setting_room_temp",
        name="Heating System 4: Setting Room Temp",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer",
    ),
    # Heating System Curves
    SensorEntityDescription(
        key="hs_1_change_inclination",
        name="Heating System 1: Change Inclination",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hs_2_change_inclination",
        name="Heating System 2: Change Inclination",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hs_3_change_inclination",
        name="Heating System 3: Change Inclination",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hs_4_change_inclination",
        name="Heating System 4: Change Inclination",
        icon="mdi:chart-line",
    ),
    # Room Adjustments
    SensorEntityDescription(
        key="room1_adjustment",
        name="Room 1: Adjustment",
        icon="mdi:tune",
    ),
    SensorEntityDescription(
        key="room2_adjustment",
        name="Room 2: Adjustment",
        icon="mdi:tune",
    ),
    SensorEntityDescription(
        key="room3_adjustment",
        name="Room 3: Adjustment",
        icon="mdi:tune",
    ),
    SensorEntityDescription(
        key="room4_adjustment",
        name="Room 4: Adjustment",
        icon="mdi:tune",
    ),
    # Heat Pump Block Status
    SensorEntityDescription(
        key="heat_pump_1_blocked",
        name="Heat Pump 1 Blocked",
        icon="mdi:lock",
    ),
    SensorEntityDescription(
        key="heat_pump_2_blocked",
        name="Heat Pump 2 Blocked",
        icon="mdi:lock",
    ),
    SensorEntityDescription(
        key="heat_pump_3_blocked",
        name="Heat Pump 3 Blocked",
        icon="mdi:lock",
    ),
    SensorEntityDescription(
        key="heat_pump_4_blocked",
        name="Heat Pump 4 Blocked",
        icon="mdi:lock",
    ),
    SensorEntityDescription(
        key="heat_pump_5_blocked",
        name="Heat Pump 5 Blocked",
        icon="mdi:lock",
    ),
    SensorEntityDescription(
        key="heat_pump_6_blocked",
        name="Heat Pump 6 Blocked",
        icon="mdi:lock",
    ),
    SensorEntityDescription(
        key="heat_pump_7_blocked",
        name="Heat Pump 7 Blocked",
        icon="mdi:lock",
    ),
    SensorEntityDescription(
        key="heat_pump_8_blocked",
        name="Heat Pump 8 Blocked",
        icon="mdi:lock",
    ),
    SensorEntityDescription(
        key="heat_pump_9_blocked",
        name="Heat Pump 9 Blocked",
        icon="mdi:lock",
    ),
    SensorEntityDescription(
        key="heat_pump_10_blocked",
        name="Heat Pump 10 Blocked",
        icon="mdi:lock",
    ),
    # Pool Settings
    SensorEntityDescription(
        key="pool_stop_temp",
        name="Pool: Stop Temp Setting",
        native_unit_of_measurement="°C",
        icon="mdi:pool-thermometer",
    ),
    SensorEntityDescription(
        key="pool_max_time",
        name="Pool: Maximum Time",
        native_unit_of_measurement="min",
        icon="mdi:timer-sand",
    ),
    SensorEntityDescription(
        key="pool_start_diff",
        name="Pool: Start Difference",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer-lines",
    ),
    # Heating System Max/Min Flow Temperatures
    SensorEntityDescription(
        key="hs_1_max_primary_flow",
        name="Heating System 1: Max Primary Flow °C",
        native_unit_of_measurement="°C",
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="hs_2_max_primary_flow",
        name="Heating System 2: Max Primary Flow °C",
        native_unit_of_measurement="°C",
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="hs_3_max_primary_flow",
        name="Heating System 3: Max Primary Flow °C",
        native_unit_of_measurement="°C",
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="hs_4_max_primary_flow",
        name="Heating System 4: Max Primary Flow °C",
        native_unit_of_measurement="°C",
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="hs_1_min_primary_flow",
        name="Heating System 1: Min Primary Flow °C",
        native_unit_of_measurement="°C",
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="hs_2_min_primary_flow",
        name="Heating System 2: Min Primary Flow °C",
        native_unit_of_measurement="°C",
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="hs_3_min_primary_flow",
        name="Heating System 3: Min Primary Flow °C",
        native_unit_of_measurement="°C",
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="hs_4_min_primary_flow",
        name="Heating System 4: Min Primary Flow °C",
        native_unit_of_measurement="°C",
        icon="mdi:water-thermometer",
    ),
    # Heating System Modes
    SensorEntityDescription(
        key="hs_1_heating_mode",
        name="Heating System 1: Heating Mode",
        icon="mdi:radiator",
    ),
    SensorEntityDescription(
        key="hs_2_heating_mode",
        name="Heating System 2: Heating Mode",
        icon="mdi:radiator",
    ),
    SensorEntityDescription(
        key="hs_3_heating_mode",
        name="Heating System 3: Heating Mode",
        icon="mdi:radiator",
    ),
    SensorEntityDescription(
        key="hs_4_heating_mode",
        name="Heating System 4: Heating Mode",
        icon="mdi:radiator",
    ),
    SensorEntityDescription(
        key="hs_1_heating_off_out",
        name="Heating System 1: Heating Off, Out °C",
        native_unit_of_measurement="°C",
        icon="mdi:radiator-off",
    ),
    SensorEntityDescription(
        key="hs_2_heating_off_out",
        name="Heating System 2: Heating Off, Out °C",
        native_unit_of_measurement="°C",
        icon="mdi:radiator-off",
    ),
    SensorEntityDescription(
        key="hs_3_heating_off_out",
        name="Heating System 3: Heating Off, Out °C",
        native_unit_of_measurement="°C",
        icon="mdi:radiator-off",
    ),
    SensorEntityDescription(
        key="hs_4_heating_off_out",
        name="Heating System 4: Heating Off, Out °C",
        native_unit_of_measurement="°C",
        icon="mdi:radiator-off",
    ),
    SensorEntityDescription(
        key="hs_1_heating_off_time",
        name="Heating System 1: Heating Off Time",
        native_unit_of_measurement="min",
        icon="mdi:timer-off",
    ),
    SensorEntityDescription(
        key="hs_2_heating_off_time",
        name="Heating System 2: Heating Off Time",
        native_unit_of_measurement="min",
        icon="mdi:timer-off",
    ),
    SensorEntityDescription(
        key="hs_3_heating_off_time",
        name="Heating System 3: Heating Off Time",
        native_unit_of_measurement="min",
        icon="mdi:timer-off",
    ),
    SensorEntityDescription(
        key="hs_4_heating_off_time",
        name="Heating System 4: Heating Off Time",
        native_unit_of_measurement="min",
        icon="mdi:timer-off",
    ),
    SensorEntityDescription(
        key="hs_1_room_temp_night_reduction",
        name="Heating System 1: Room Temp Night Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_2_room_temp_night_reduction",
        name="Heating System 2: Room Temp Night Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_3_room_temp_night_reduction",
        name="Heating System 3: Room Temp Night Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_4_room_temp_night_reduction",
        name="Heating System 4: Room Temp Night Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_1_primary_flow_night_reduction",
        name="Heating System 1: Primary Flow Night Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_2_primary_flow_night_reduction",
        name="Heating System 2: Primary Flow Night Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_3_primary_flow_night_reduction",
        name="Heating System 3: Primary Flow Night Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_4_primary_flow_night_reduction",
        name="Heating System 4: Primary Flow Night Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_1_outdoor_temp_night_reduction",
        name="Heating System 1: Outdoor Temp Night Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_2_outdoor_temp_night_reduction",
        name="Heating System 2: Outdoor Temp Night Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_3_outdoor_temp_night_reduction",
        name="Heating System 3: Outdoor Temp Night Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_4_outdoor_temp_night_reduction",
        name="Heating System 4: Outdoor Temp Night Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_1_alarm_low_room_temp",
        name="Heating System 1: Alarm Low Room Temperature",
        native_unit_of_measurement="°C",
        icon="mdi:alert",
    ),
    SensorEntityDescription(
        key="hs_2_alarm_low_room_temp",
        name="Heating System 2: Alarm Low Room Temperature",
        native_unit_of_measurement="°C",
        icon="mdi:alert",
    ),
    SensorEntityDescription(
        key="hs_3_alarm_low_room_temp",
        name="Heating System 3: Alarm Low Room Temperature",
        native_unit_of_measurement="°C",
        icon="mdi:alert",
    ),
    SensorEntityDescription(
        key="hs_4_alarm_low_room_temp",
        name="Heating System 4: Alarm Low Room Temperature",
        native_unit_of_measurement="°C",
        icon="mdi:alert",
    ),
    SensorEntityDescription(
        key="radiator_pump_setting",
        name="Radiator Pump Setting",
        native_unit_of_measurement="%",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="start_at_degree_minute",
        name="Start at Degree Minute",
        native_unit_of_measurement="°C",
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key="heat_pump_1_max_rps",
        name="Heat Pump 1: Max RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="heat_pump_2_max_rps",
        name="Heat Pump 2: Max RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="heat_pump_3_max_rps",
        name="Heat Pump 3: Max RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="heat_pump_4_max_rps",
        name="Heat Pump 4: Max RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="heat_pump_5_max_rps",
        name="Heat Pump 5: Max RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="heat_pump_6_max_rps",
        name="Heat Pump 6: Max RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="heat_pump_7_max_rps",
        name="Heat Pump 7: Max RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="heat_pump_8_max_rps",
        name="Heat Pump 8: Max RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="heat_pump_9_max_rps",
        name="Heat Pump 9: Max RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="heat_pump_10_max_rps",
        name="Heat Pump 10: Max RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="e1_start_add_heat_degree_minute",
        name="E1: Start Add Heat, Degree Minute",
        native_unit_of_measurement="°C",
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key="external_boiler_diff",
        name="External Boiler Diff",
        native_unit_of_measurement="°C",
        icon="mdi:fire",
    ),
    SensorEntityDescription(
        key="blocking_additional_heat_outdoor_temp",
        name="Blocking Additional Heat Outdoor Temp",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer-off",
    ),
    SensorEntityDescription(
        key="boiler_open_mixing_valve",
        name="Boiler Open Mixing Valve °C",
        native_unit_of_measurement="°C",
        icon="mdi:valve",
    ),
    SensorEntityDescription(
        key="delay_stop_external_boiler",
        name="Delay Stop External Boiler",
        native_unit_of_measurement="min",
        icon="mdi:timer-off",
    ),
    SensorEntityDescription(
        key="ext_boiler_mode",
        name="External Boiler Mode",
        icon="mdi:fire",
    ),
    SensorEntityDescription(
        key="ehs_open_shunt_degrees",
        name="EHS Open Shunt Degrees",
        native_unit_of_measurement="°C",
        icon="mdi:valve",
    ),
    SensorEntityDescription(
        key="ehs_start_stop_diff",
        name="EHS Start/Stop Diff",
        native_unit_of_measurement="°C",
        icon="mdi:swap-horizontal",
    ),
    SensorEntityDescription(
        key="max_immersion_heater_kw_lower",
        name="Max Immersion Heater kW Lower",
        native_unit_of_measurement="kW",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="max_immersion_heater_dhw_kw_upper",
        name="Max Immersion Heater DHW kW Upper",
        native_unit_of_measurement="kW",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="hs_1_holiday_reduction",
        name="Heating System 1: Holiday Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_2_holiday_reduction",
        name="Heating System 2: Holiday Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_3_holiday_reduction",
        name="Heating System 3: Holiday Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_4_holiday_reduction",
        name="Heating System 4: Holiday Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_1_primary_flow_holiday_reduction",
        name="Heating System 1: Primary Flow Holiday Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_2_primary_flow_holiday_reduction",
        name="Heating System 2: Primary Flow Holiday Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_3_primary_flow_holiday_reduction",
        name="Heating System 3: Primary Flow Holiday Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="hs_4_primary_flow_holiday_reduction",
        name="Heating System 4: Primary Flow Holiday Reduction",
        native_unit_of_measurement="°C",
        icon="mdi:weather-night",
    ),
    SensorEntityDescription(
        key="heat_pump_diff_degree_minute",
        name="Heat Pump: Diff Heat Pump, Degree Minute",
        native_unit_of_measurement="°C",
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key="heat_pump_delay_between",
        name="Heat Pump: Delay Between Heat Pump",
        native_unit_of_measurement="min",
        icon="mdi:timer-sand",
    ),
    SensorEntityDescription(
        key="e1_diff_add_heat_degree_minute",
        name="E1: Diff Add Heat, Degree Minute",
        native_unit_of_measurement="°C",
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key="e2_start_0_10v_degree_minute",
        name="E2: Start 0-10V Degree Minute",
        native_unit_of_measurement="°C",
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key="e2_diff_0_10v_degree_minute",
        name="E2: Diff 0-10V, Degree Minute",
        native_unit_of_measurement="°C",
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key="e3_start_ecominiel_degree_minute",
        name="E3: Start EcoMiniEl, Degree Minute",
        native_unit_of_measurement="°C",
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key="e3_number_of_steps_heating",
        name="E3: Number of Steps Heating",
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key="e3_number_of_steps_dhw",
        name="E3: Number of Steps DHW",
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key="e3_diff_step_ecominiel",
        name="E3: Diff Step EcoMiniEl",
        native_unit_of_measurement="°C",
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key="e1_delay_add_heat_e1",
        name="E1: Delay Add Heat E1",
        native_unit_of_measurement="min",
        icon="mdi:timer-sand",
    ),
    SensorEntityDescription(
        key="e2_delay_add_heat_0_10v",
        name="E2: Delay Add Heat 0-10V",
        native_unit_of_measurement="min",
        icon="mdi:timer-sand",
    ),
    SensorEntityDescription(
        key="e2_diff_0_10v_delay",
        name="E2: Diff 0-10V Delay",
        native_unit_of_measurement="°C",
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key="e3_delay_ecominiel",
        name="E3: Delay EcoMiniEl",
        native_unit_of_measurement="min",
        icon="mdi:timer-sand",
    ),
    SensorEntityDescription(
        key="cooling_primary_flow_outdoor_20",
        name="Cooling: Primary Flow at Outdoor Temp +20°C",
        native_unit_of_measurement="°C",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="cooling_primary_flow_outdoor_40",
        name="Cooling: Primary Flow at Outdoor Temp +40°C",
        native_unit_of_measurement="°C",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="cooling_min_flow_temp",
        name="Cooling: Min Flow Temperature",
        native_unit_of_measurement="°C",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="delay_mixing_valve_setting",
        name="Delay Mixing Valve Setting",
        native_unit_of_measurement="min",
        icon="mdi:timer-sand",
    ),
    SensorEntityDescription(
        key="wood_boiler_start_flue_gas",
        name="Wood Boiler Start Flue Gas",
        native_unit_of_measurement="°C",
        icon="mdi:fire",
    ),
    SensorEntityDescription(
        key="wood_boiler_start_boiler_temp",
        name="Wood Boiler Start Boiler Temperature",
        native_unit_of_measurement="°C",
        icon="mdi:fire",
    ),
    SensorEntityDescription(
        key="wood_boiler_hysteresis",
        name="Wood Boiler Hysteresis",
        native_unit_of_measurement="°C",
        icon="mdi:fire",
    ),
    SensorEntityDescription(
        key="boiler_lower_temp",
        name="Boiler Lower °C",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="boiler_upper_temp",
        name="Boiler Upper °C",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="boiler_add_heat_temp",
        name="Boiler Add Heat °C",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="boiler_dhw_temp",
        name="Boiler DHW °C",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="diff_thermostat_start_temp_diff",
        name="Diff Thermostat Start Temp Diff",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer-lines",
    ),
    SensorEntityDescription(
        key="diff_thermostat_stop_temp_diff",
        name="Diff Thermostat Stop Temp Diff",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer-lines",
    ),
    SensorEntityDescription(
        key="diff_thermostat_charge_temp",
        name="Diff Thermostat Charge Temperature",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer-lines",
    ),
    SensorEntityDescription(
        key="solar_deltat_max",
        name="Solar DeltaT Max",
        native_unit_of_measurement="°C",
        icon="mdi:solar-power",
    ),
    SensorEntityDescription(
        key="solar_deltat_min",
        name="Solar DeltaT Min",
        native_unit_of_measurement="°C",
        icon="mdi:solar-power",
    ),
    SensorEntityDescription(
        key="solar_charge_pump_min",
        name="Solar Charge Pump Min",
        native_unit_of_measurement="%",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="solar_deltat_max_borehole",
        name="Solar DeltaT Max Borehole",
        native_unit_of_measurement="°C",
        icon="mdi:solar-power",
    ),
    SensorEntityDescription(
        key="solar_deltat_min_borehole",
        name="Solar DeltaT Min Borehole",
        native_unit_of_measurement="°C",
        icon="mdi:solar-power",
    ),
    SensorEntityDescription(
        key="solar_h_tank_charge_temp",
        name="Solar H-Tank Charge Temp",
        native_unit_of_measurement="°C",
        icon="mdi:solar-power",
    ),
    SensorEntityDescription(
        key="solar_x_tank_charge_temp",
        name="Solar X-Tank Charge Temp",
        native_unit_of_measurement="°C",
        icon="mdi:solar-power",
    ),
    SensorEntityDescription(
        key="solar_eco_tank_charge_temp",
        name="Solar Eco-Tank Charge Temp",
        native_unit_of_measurement="°C",
        icon="mdi:solar-power",
    ),
    SensorEntityDescription(
        key="solar_h_tank_charge_start_diff",
        name="Solar H-Tank Charge Start Diff",
        native_unit_of_measurement="°C",
        icon="mdi:solar-power",
    ),
    SensorEntityDescription(
        key="solar_h_tank_charge_stop_diff",
        name="Solar H-Tank Charge Stop Diff",
        native_unit_of_measurement="°C",
        icon="mdi:solar-power",
    ),
    SensorEntityDescription(
        key="solar_h_tank_charge_stop_temp",
        name="Solar H-Tank Charge Stop Temp",
        native_unit_of_measurement="°C",
        icon="mdi:solar-power",
    ),
    SensorEntityDescription(
        key="wood_boiler_buffer_tank_delay_recharge_time",
        name="Wood Boiler Buffer Tank Delay Recharge Time",
        native_unit_of_measurement="min",
        icon="mdi:fire",
    ),
    SensorEntityDescription(
        key="setpoint_upper_tank_el_heater",
        name="Setpoint Upper Tank El. Heater",
        native_unit_of_measurement="°C",
        icon="mdi:target",
    ),
    SensorEntityDescription(
        key="capacity_start_point_charging_dhw",
        name="Capacity Start Point Charging DHW",
        native_unit_of_measurement="°C",
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="lower_temp_sensor_start_point_charging_dhw",
        name="Lower Temp Sensor Start Point Charging DHW",
        native_unit_of_measurement="°C",
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="ventilation_mode",
        name="Ventilation Mode",
        icon="mdi:fan",
    ),
    SensorEntityDescription(
        key="night_cooling_on_off",
        name="Night Cooling On/Off",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="ventilation_away_mode",
        name="Ventilation Away Mode",
        icon="mdi:fan",
    ),
    SensorEntityDescription(
        key="pool_enable",
        name="Pool Enable",
        icon="mdi:pool",
    ),
    SensorEntityDescription(
        key="room_temp_cooling",
        name="Room Temp Cooling",
        native_unit_of_measurement="°C",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="cooling_permitted_from_outdoor_temp",
        name="Cooling Permitted From Outdoor Temp",
        native_unit_of_measurement="°C",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="cooling_delay_active",
        name="Cooling Delay Active",
        native_unit_of_measurement="min",
        icon="mdi:timer-sand",
    ),
    SensorEntityDescription(
        key="delay_cooling_from_heating_off",
        name="Delay Cooling From Heating Off",
        native_unit_of_measurement="min",
        icon="mdi:timer-sand",
    ),
    SensorEntityDescription(
        key="cooling_start_delay",
        name="Cooling Start Delay",
        native_unit_of_measurement="min",
        icon="mdi:timer-sand",
    ),
    SensorEntityDescription(
        key="cooling_diff_calc_delay",
        name="Cooling Diff Calc Delay",
        native_unit_of_measurement="min",
        icon="mdi:timer-sand",
    ),
    SensorEntityDescription(
        key="primary_flow_temp_outdoor_20",
        name="Primary Flow Temp at Outdoor +20°C",
        native_unit_of_measurement="°C",
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="primary_flow_temp_outdoor_40",
        name="Primary Flow Temp at Outdoor +40°C",
        native_unit_of_measurement="°C",
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="primary_flow_diff_outdoor_20",
        name="Primary Flow Diff at Outdoor +20°C",
        native_unit_of_measurement="°C",
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="primary_flow_diff_outdoor_40",
        name="Primary Flow Diff at Outdoor +40°C",
        native_unit_of_measurement="°C",
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="cooling_max_time_hp_active",
        name="Cooling Max Time HP Active",
        native_unit_of_measurement="min",
        icon="mdi:timer-sand",
    ),
    SensorEntityDescription(
        key="cooling_hp_charge_pump_speed",
        name="Cooling HP Charge Pump Speed",
        native_unit_of_measurement="%",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="hc_1_curve_point_1_x",
        name="HC1 Heating Curve Point 1 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_1_curve_point_1_y",
        name="HC1 Heating Curve Point 1 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_1_curve_point_2_x",
        name="HC1 Heating Curve Point 2 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_1_curve_point_2_y",
        name="HC1 Heating Curve Point 2 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_1_curve_point_3_x",
        name="HC1 Heating Curve Point 3 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_1_curve_point_3_y",
        name="HC1 Heating Curve Point 3 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_1_curve_point_4_x",
        name="HC1 Heating Curve Point 4 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_1_curve_point_4_y",
        name="HC1 Heating Curve Point 4 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_1_curve_point_5_x",
        name="HC1 Heating Curve Point 5 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_1_curve_point_5_y",
        name="HC1 Heating Curve Point 5 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_2_curve_point_1_x",
        name="HC2 Heating Curve Point 1 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_2_curve_point_1_y",
        name="HC2 Heating Curve Point 1 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_2_curve_point_2_x",
        name="HC2 Heating Curve Point 2 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_2_curve_point_2_y",
        name="HC2 Heating Curve Point 2 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_2_curve_point_3_x",
        name="HC2 Heating Curve Point 3 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_2_curve_point_3_y",
        name="HC2 Heating Curve Point 3 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_2_curve_point_4_x",
        name="HC2 Heating Curve Point 4 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_2_curve_point_4_y",
        name="HC2 Heating Curve Point 4 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_2_curve_point_5_x",
        name="HC2 Heating Curve Point 5 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_2_curve_point_5_y",
        name="HC2 Heating Curve Point 5 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_3_curve_point_1_x",
        name="HC3 Heating Curve Point 1 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_3_curve_point_1_y",
        name="HC3 Heating Curve Point 1 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_3_curve_point_2_x",
        name="HC3 Heating Curve Point 2 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_3_curve_point_2_y",
        name="HC3 Heating Curve Point 2 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_3_curve_point_3_x",
        name="HC3 Heating Curve Point 3 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_3_curve_point_3_y",
        name="HC3 Heating Curve Point 3 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_3_curve_point_4_x",
        name="HC3 Heating Curve Point 4 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_3_curve_point_4_y",
        name="HC3 Heating Curve Point 4 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_3_curve_point_5_x",
        name="HC3 Heating Curve Point 5 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_3_curve_point_5_y",
        name="HC3 Heating Curve Point 5 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_4_curve_point_1_x",
        name="HC4 Heating Curve Point 1 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_4_curve_point_1_y",
        name="HC4 Heating Curve Point 1 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_4_curve_point_2_x",
        name="HC4 Heating Curve Point 2 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_4_curve_point_2_y",
        name="HC4 Heating Curve Point 2 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_4_curve_point_3_x",
        name="HC4 Heating Curve Point 3 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_4_curve_point_3_y",
        name="HC4 Heating Curve Point 3 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_4_curve_point_4_x",
        name="HC4 Heating Curve Point 4 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_4_curve_point_4_y",
        name="HC4 Heating Curve Point 4 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_4_curve_point_5_x",
        name="HC4 Heating Curve Point 5 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="hc_4_curve_point_5_y",
        name="HC4 Heating Curve Point 5 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="cooling_curve_point_1_x",
        name="Cooling Curve Point 1 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="cooling_curve_point_1_y",
        name="Cooling Curve Point 1 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="cooling_curve_point_2_x",
        name="Cooling Curve Point 2 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="cooling_curve_point_2_y",
        name="Cooling Curve Point 2 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="cooling_curve_point_3_x",
        name="Cooling Curve Point 3 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="cooling_curve_point_3_y",
        name="Cooling Curve Point 3 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="cooling_curve_point_4_x",
        name="Cooling Curve Point 4 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="cooling_curve_point_4_y",
        name="Cooling Curve Point 4 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="cooling_curve_point_5_x",
        name="Cooling Curve Point 5 X (Outside Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="cooling_curve_point_5_y",
        name="Cooling Curve Point 5 Y (Setpoint Temp)",
        native_unit_of_measurement="°C",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="hs_1_heating_on_time",
        name="Heating System 1: Heating On Time",
        native_unit_of_measurement="min",
        icon="mdi:timer-outline",
    ),
    SensorEntityDescription(
        key="hs_2_heating_on_time",
        name="Heating System 2: Heating On Time",
        native_unit_of_measurement="min",
        icon="mdi:timer-outline",
    ),
    SensorEntityDescription(
        key="hs_3_heating_on_time",
        name="Heating System 3: Heating On Time",
        native_unit_of_measurement="min",
        icon="mdi:timer-outline",
    ),
    SensorEntityDescription(
        key="hs_4_heating_on_time",
        name="Heating System 4: Heating On Time",
        native_unit_of_measurement="min",
        icon="mdi:timer-outline",
    ),
    SensorEntityDescription(
        key="outdoor_temperature",
        name="Outdoor Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="stop_temp_dhw",
        name="Stop Temperature DHW",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-off",
    ),
    SensorEntityDescription(
        key="setpoint_outlet_temp_dhw",
        name="Setpoint Outlet Temperature DHW",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-lines",
    ),
    SensorEntityDescription(
        key="hot_water_temp",
        name="Hot Water Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="delay_mixing_valve",
        name="Delay Mixing Valve",
        native_unit_of_measurement="min",
        icon="mdi:timer-sand",
    ),
    SensorEntityDescription(
        key="status",
        name="Status",
        icon="mdi:information-outline",
    ),
    SensorEntityDescription(
        key="radiator_water",
        name="Radiator Water",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:radiator",
    ),
    SensorEntityDescription(
        key="hs_1_temp_setpoint",
        name="HS1 Temp Setpoint",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:target",
    ),
    SensorEntityDescription(
        key="hs_2_temp_setpoint",
        name="HS2 Temp Setpoint",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:target",
    ),
    SensorEntityDescription(
        key="hs_3_temp_setpoint",
        name="HS3 Temp Setpoint",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:target",
    ),
    SensorEntityDescription(
        key="hs_4_temp_setpoint",
        name="HS4 Temp Setpoint",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:target",
    ),
    SensorEntityDescription(
        key="hs_1_primary_flow_temp",
        name="HS1 Primary Flow Temp",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="hs_2_primary_flow_temp",
        name="HS2 Primary Flow Temp",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="hs_3_primary_flow_temp",
        name="HS3 Primary Flow Temp",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="hs_4_primary_flow_temp",
        name="HS4 Primary Flow Temp",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="return_temp",
        name="Return Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-chevron-down",
    ),
    SensorEntityDescription(
        key="dhw_circulation",
        name="DHW Circulation",
        native_unit_of_measurement="min",
        icon="mdi:water-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_1_status",
        name="Heat Pump 1 Status",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_2_status",
        name="Heat Pump 2 Status",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_3_status",
        name="Heat Pump 3 Status",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_4_status",
        name="Heat Pump 4 Status",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_5_status",
        name="Heat Pump 5 Status",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_6_status",
        name="Heat Pump 6 Status",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_7_status",
        name="Heat Pump 7 Status",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_8_status",
        name="Heat Pump 8 Status",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_9_status",
        name="Heat Pump 9 Status",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_10_status",
        name="Heat Pump 10 Status",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_1_hp_in",
        name="Heat Pump 1 HP In",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_2_hp_in",
        name="Heat Pump 2 HP In",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_3_hp_in",
        name="Heat Pump 3 HP In",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_4_hp_in",
        name="Heat Pump 4 HP In",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_5_hp_in",
        name="Heat Pump 5 HP In",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_6_hp_in",
        name="Heat Pump 6 HP In",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_7_hp_in",
        name="Heat Pump 7 HP In",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_8_hp_in",
        name="Heat Pump 8 HP In",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_9_hp_in",
        name="Heat Pump 9 HP In",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_10_hp_in",
        name="Heat Pump 10 HP In",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_1_hp_out",
        name="Heat Pump 1 HP Out",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_2_hp_out",
        name="Heat Pump 2 HP Out",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_3_hp_out",
        name="Heat Pump 3 HP Out",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_4_hp_out",
        name="Heat Pump 4 HP Out",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_5_hp_out",
        name="Heat Pump 5 HP Out",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_6_hp_out",
        name="Heat Pump 6 HP Out",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_7_hp_out",
        name="Heat Pump 7 HP Out",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_8_hp_out",
        name="Heat Pump 8 HP Out",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_9_hp_out",
        name="Heat Pump 9 HP Out",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_10_hp_out",
        name="Heat Pump 10 HP Out",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-water",
    ),
    SensorEntityDescription(
        key="heat_pump_1_discharge_temp",
        name="Heat Pump 1 Discharge Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_2_discharge_temp",
        name="Heat Pump 2 Discharge Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_3_discharge_temp",
        name="Heat Pump 3 Discharge Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_4_discharge_temp",
        name="Heat Pump 4 Discharge Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_5_discharge_temp",
        name="Heat Pump 5 Discharge Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_6_discharge_temp",
        name="Heat Pump 6 Discharge Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_7_discharge_temp",
        name="Heat Pump 7 Discharge Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_8_discharge_temp",
        name="Heat Pump 8 Discharge Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_9_discharge_temp",
        name="Heat Pump 9 Discharge Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_10_discharge_temp",
        name="Heat Pump 10 Discharge Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_1_suction_gas_temp",
        name="Heat Pump 1 Suction Gas Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_2_suction_gas_temp",
        name="Heat Pump 2 Suction Gas Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_3_suction_gas_temp",
        name="Heat Pump 3 Suction Gas Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_4_suction_gas_temp",
        name="Heat Pump 4 Suction Gas Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_5_suction_gas_temp",
        name="Heat Pump 5 Suction Gas Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_6_suction_gas_temp",
        name="Heat Pump 6 Suction Gas Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_7_suction_gas_temp",
        name="Heat Pump 7 Suction Gas Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_8_suction_gas_temp",
        name="Heat Pump 8 Suction Gas Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_9_suction_gas_temp",
        name="Heat Pump 9 Suction Gas Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_10_suction_gas_temp",
        name="Heat Pump 10 Suction Gas Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_1_high_pressure",
        name="Heat Pump 1 High Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_2_high_pressure",
        name="Heat Pump 2 High Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_3_high_pressure",
        name="Heat Pump 3 High Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_4_high_pressure",
        name="Heat Pump 4 High Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_5_high_pressure",
        name="Heat Pump 5 High Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_6_high_pressure",
        name="Heat Pump 6 High Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_7_high_pressure",
        name="Heat Pump 7 High Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_8_high_pressure",
        name="Heat Pump 8 High Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_9_high_pressure",
        name="Heat Pump 9 High Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_10_high_pressure",
        name="Heat Pump 10 High Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_1_low_pressure",
        name="Heat Pump 1 Low Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_2_low_pressure",
        name="Heat Pump 2 Low Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_3_low_pressure",
        name="Heat Pump 3 Low Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_4_low_pressure",
        name="Heat Pump 4 Low Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_5_low_pressure",
        name="Heat Pump 5 Low Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_6_low_pressure",
        name="Heat Pump 6 Low Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_7_low_pressure",
        name="Heat Pump 7 Low Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_8_low_pressure",
        name="Heat Pump 8 Low Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_9_low_pressure",
        name="Heat Pump 9 Low Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_10_low_pressure",
        name="Heat Pump 10 Low Pressure",
        native_unit_of_measurement="bar",
        icon="mdi:gauge",
    ),
    SensorEntityDescription(
        key="heat_pump_1_charge_pump",
        name="Heat Pump 1 Charge Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_2_charge_pump",
        name="Heat Pump 2 Charge Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_3_charge_pump",
        name="Heat Pump 3 Charge Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_4_charge_pump",
        name="Heat Pump 4 Charge Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_5_charge_pump",
        name="Heat Pump 5 Charge Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_6_charge_pump",
        name="Heat Pump 6 Charge Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_7_charge_pump",
        name="Heat Pump 7 Charge Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_8_charge_pump",
        name="Heat Pump 8 Charge Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_9_charge_pump",
        name="Heat Pump 9 Charge Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_10_charge_pump",
        name="Heat Pump 10 Charge Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_1_brine_pump",
        name="Heat Pump 1 Brine Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_2_brine_pump",
        name="Heat Pump 2 Brine Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_3_brine_pump",
        name="Heat Pump 3 Brine Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_4_brine_pump",
        name="Heat Pump 4 Brine Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_5_brine_pump",
        name="Heat Pump 5 Brine Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_6_brine_pump",
        name="Heat Pump 6 Brine Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_7_brine_pump",
        name="Heat Pump 7 Brine Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_8_brine_pump",
        name="Heat Pump 8 Brine Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_9_brine_pump",
        name="Heat Pump 9 Brine Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_10_brine_pump",
        name="Heat Pump 10 Brine Pump",
        native_unit_of_measurement="°C",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="heat_pump_1_fan",
        name="Heat Pump 1 Fan",
        native_unit_of_measurement="%",
        icon="mdi:fan",
    ),
    SensorEntityDescription(
        key="heat_pump_2_fan",
        name="Heat Pump 2 Fan",
        native_unit_of_measurement="%",
        icon="mdi:fan",
    ),
    SensorEntityDescription(
        key="heat_pump_3_fan",
        name="Heat Pump 3 Fan",
        native_unit_of_measurement="%",
        icon="mdi:fan",
    ),
    SensorEntityDescription(
        key="heat_pump_4_fan",
        name="Heat Pump 4 Fan",
        native_unit_of_measurement="%",
        icon="mdi:fan",
    ),
    SensorEntityDescription(
        key="heat_pump_5_fan",
        name="Heat Pump 5 Fan",
        native_unit_of_measurement="%",
        icon="mdi:fan",
    ),
    SensorEntityDescription(
        key="heat_pump_6_fan",
        name="Heat Pump 6 Fan",
        native_unit_of_measurement="°C",
        icon="mdi:fan",
    ),
    SensorEntityDescription(
        key="heat_pump_7_fan",
        name="Heat Pump 7 Fan",
        native_unit_of_measurement="%",
        icon="mdi:fan",
    ),
    SensorEntityDescription(
        key="heat_pump_8_fan",
        name="Heat Pump 8 Fan",
        native_unit_of_measurement="%",
        icon="mdi:fan",
    ),
    SensorEntityDescription(
        key="heat_pump_9_fan",
        name="Heat Pump 9 Fan",
        native_unit_of_measurement="%",
        icon="mdi:fan",
    ),
    SensorEntityDescription(
        key="heat_pump_10_fan",
        name="Heat Pump 10 Fan",
        native_unit_of_measurement="%",
        icon="mdi:fan",
    ),
    SensorEntityDescription(
        key="heat_pump_1_defrost_timer",
        name="Heat Pump 1 Defrost Timer",
        native_unit_of_measurement="s",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="heat_pump_2_defrost_timer",
        name="Heat Pump 2 Defrost Timer",
        native_unit_of_measurement="s",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="heat_pump_3_defrost_timer",
        name="Heat Pump 3 Defrost Timer",
        native_unit_of_measurement="s",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="heat_pump_4_defrost_timer",
        name="Heat Pump 4 Defrost Timer",
        native_unit_of_measurement="s",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="heat_pump_5_defrost_timer",
        name="Heat Pump 5 Defrost Timer",
        native_unit_of_measurement="s",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="heat_pump_6_defrost_timer",
        name="Heat Pump 6 Defrost Timer",
        native_unit_of_measurement="s",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="heat_pump_7_defrost_timer",
        name="Heat Pump 7 Defrost Timer",
        native_unit_of_measurement="s",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="heat_pump_8_defrost_timer",
        name="Heat Pump 8 Defrost Timer",
        native_unit_of_measurement="s",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="heat_pump_9_defrost_timer",
        name="Heat Pump 9 Defrost Timer",
        native_unit_of_measurement="s",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="heat_pump_10_defrost_timer",
        name="Heat Pump 10 Defrost Timer",
        native_unit_of_measurement="s",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="heat_pump_1_outdoor_temp",
        name="Heat Pump 1 Outdoor Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_2_outdoor_temp",
        name="Heat Pump 2 Outdoor Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_3_outdoor_temp",
        name="Heat Pump 3 Outdoor Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_4_outdoor_temp",
        name="Heat Pump 4 Outdoor Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_5_outdoor_temp",
        name="Heat Pump 5 Outdoor Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_6_outdoor_temp",
        name="Heat Pump 6 Outdoor Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_7_outdoor_temp",
        name="Heat Pump 7 Outdoor Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_8_outdoor_temp",
        name="Heat Pump 8 Outdoor Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_9_outdoor_temp",
        name="Heat Pump 9 Outdoor Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_10_outdoor_temp",
        name="Heat Pump 10 Outdoor Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_1_software_version",
        name="Heat Pump 1 Software Version",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="heat_pump_2_software_version",
        name="Heat Pump 2 Software Version",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="heat_pump_3_software_version",
        name="Heat Pump 3 Software Version",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="heat_pump_4_software_version",
        name="Heat Pump 4 Software Version",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="heat_pump_5_software_version",
        name="Heat Pump 5 Software Version",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="heat_pump_6_software_version",
        name="Heat Pump 6 Software Version",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="heat_pump_7_software_version",
        name="Heat Pump 7 Software Version",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="heat_pump_8_software_version",
        name="Heat Pump 8 Software Version",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="heat_pump_9_software_version",
        name="Heat Pump 9 Software Version",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="heat_pump_10_software_version",
        name="Heat Pump 10 Software Version",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="degree_minute",
        name="Degree Minute",
        native_unit_of_measurement="°C",
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key="power_kw_immersion_heater",
        name="Power kW Immersion Heater",
        native_unit_of_measurement="kW",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="power_kw_immersion_heater_lower",
        name="Power kW Immersion Heater Lower",
        native_unit_of_measurement="kW",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="maximum_current",
        name="Maximum Current",
        native_unit_of_measurement="A",
        icon="mdi:current-ac",
    ),
    SensorEntityDescription(
        key="current_l1",
        name="Current L1",
        native_unit_of_measurement="A",
        icon="mdi:current-ac",
    ),
    SensorEntityDescription(
        key="current_l2",
        name="Current L2",
        native_unit_of_measurement="A",
        icon="mdi:current-ac",
    ),
    SensorEntityDescription(
        key="current_l3",
        name="Current L3",
        native_unit_of_measurement="A",
        icon="mdi:current-ac",
    ),
    SensorEntityDescription(
        key="pump_diff_thermostat",
        name="Pump Diff Thermostat",
        icon="mdi:thermometer-lines",
    ),
    SensorEntityDescription(
        key="diff_thermostat_c",
        name="Diff Thermostat °C",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer-lines",
    ),
    SensorEntityDescription(
        key="ehs_temperature",
        name="EHS Temperature",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="ehs_primary_flow_mode",
        name="EHS Primary Flow Mode",
        icon="mdi:swap-horizontal",
    ),
    SensorEntityDescription(
        key="pool_mode",
        name="Pool Mode",
        icon="mdi:pool",
    ),
    SensorEntityDescription(
        key="pool_temperature",
        name="Pool Temperature",
        native_unit_of_measurement="°C",
        icon="mdi:pool-thermometer",
    ),
    SensorEntityDescription(
        key="pool_stop_temperature",
        name="Pool Stop Temperature",
        native_unit_of_measurement="°C",
        icon="mdi:pool-thermometer",
    ),
    SensorEntityDescription(
        key="solar_mode",
        name="Solar Mode",
        icon="mdi:solar-power",
    ),
    SensorEntityDescription(
        key="solar_temperature_out",
        name="Solar Temperature Out",
        native_unit_of_measurement="°C",
        icon="mdi:solar-power",
    ),
    SensorEntityDescription(
        key="solar_temperature_in",
        name="Solar Temperature In",
        native_unit_of_measurement="°C",
        icon="mdi:solar-power",
    ),
    SensorEntityDescription(
        key="solar_pump_panel",
        name="Solar Pump Panel",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="tank_timer",
        name="Tank Timer",
        icon="mdi:timer-outline",
    ),
    SensorEntityDescription(
        key="stat_total_operation_lsb",
        name="Stat Total Operation LSB",
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key="stat_immersion_heater_kwh",
        name="Stat Immersion Heater kWh",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="function_test",
        name="Function Test",
        icon="mdi:check-circle-outline",
    ),
    SensorEntityDescription(
        key="heat_pump_1_current_rps",
        name="Heat Pump 1 Current RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="heat_pump_2_current_rps",
        name="Heat Pump 2 Current RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="heat_pump_3_current_rps",
        name="Heat Pump 3 Current RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="heat_pump_4_current_rps",
        name="Heat Pump 4 Current RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="heat_pump_5_current_rps",
        name="Heat Pump 5 Current RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="heat_pump_6_current_rps",
        name="Heat Pump 6 Current RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="heat_pump_7_current_rps",
        name="Heat Pump 7 Current RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="heat_pump_8_current_rps",
        name="Heat Pump 8 Current RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="heat_pump_9_current_rps",
        name="Heat Pump 9 Current RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="heat_pump_10_current_rps",
        name="Heat Pump 10 Current RPS",
        native_unit_of_measurement="Hz",
        icon="mdi:rotate-right",
    ),
    SensorEntityDescription(
        key="current_room_temp_1",
        name="Current Room Temperature 1",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="current_room_temp_2",
        name="Current Room Temperature 2",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="current_room_temp_3",
        name="Current Room Temperature 3",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="current_room_temp_4",
        name="Current Room Temperature 4",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="system_type",
        name="System Type",
        icon="mdi:cog-outline",
    ),
    SensorEntityDescription(
        key="wood_flue_gas_temp_b8",
        name="Wood Flue Gas Temperature (B8)",
        native_unit_of_measurement="°C",
        icon="mdi:fire",
    ),
    SensorEntityDescription(
        key="wood_boiler_temp_b9",
        name="Wood Boiler Temperature (B9)",
        native_unit_of_measurement="°C",
        icon="mdi:fire",
    ),
    SensorEntityDescription(
        key="e1_boiler_temp_b9",
        name="E1 Boiler Temperature (B9)",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="e1_boiler_out_temp_b10",
        name="E1 Boiler Out Temperature (B10)",
        native_unit_of_measurement="°C",
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="e2_number_of_steps",
        name="E2 Number of Steps",
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key="e3_status",
        name="E3 Status",
        icon="mdi:information-outline",
    ),
    SensorEntityDescription(
        key="heat_pump_1_compressor_operating_time_lsb",
        name="Compressor Operating Time LSB",
        icon="mdi:timer-outline",
    ),
    SensorEntityDescription(
        key="heat_pump_2_compressor_operating_time_lsb",
        name="Compressor Operating Time LSB",
        icon="mdi:timer-outline",
    ),
    SensorEntityDescription(
        key="heat_pump_3_compressor_operating_time_lsb",
        name="Compressor Operating Time LSB",
        icon="mdi:timer-outline",
    ),
    SensorEntityDescription(
        key="heat_pump_4_compressor_operating_time_lsb",
        name="Compressor Operating Time LSB",
        icon="mdi:timer-outline",
    ),
    SensorEntityDescription(
        key="heat_pump_5_compressor_operating_time_lsb",
        name="Compressor Operating Time LSB",
        icon="mdi:timer-outline",
    ),
    SensorEntityDescription(
        key="heat_pump_6_compressor_operating_time_lsb",
        name="Compressor Operating Time LSB",
        icon="mdi:timer-outline",
    ),
    SensorEntityDescription(
        key="heat_pump_7_compressor_operating_time_lsb",
        name="Compressor Operating Time LSB",
        icon="mdi:timer-outline",
    ),
    SensorEntityDescription(
        key="heat_pump_8_compressor_operating_time_lsb",
        name="Compressor Operating Time LSB",
        icon="mdi:timer-outline",
    ),
    SensorEntityDescription(
        key="heat_pump_9_compressor_operating_time_lsb",
        name="Compressor Operating Time LSB",
        icon="mdi:timer-outline",
    ),
    SensorEntityDescription(
        key="heat_pump_10_compressor_operating_time_lsb",
        name="Compressor Operating Time LSB",
        icon="mdi:timer-outline",
    ),
    SensorEntityDescription(
        key="heat_pump_1_compressor_last_24h",
        name="Compressor Last 24h",
        icon="mdi:history",
    ),
    SensorEntityDescription(
        key="heat_pump_2_compressor_last_24h",
        name="Compressor Last 24h",
        icon="mdi:history",
    ),
    SensorEntityDescription(
        key="heat_pump_3_compressor_last_24h",
        name="Compressor Last 24h",
        icon="mdi:history",
    ),
    SensorEntityDescription(
        key="heat_pump_4_compressor_last_24h",
        name="Compressor Last 24h",
        icon="mdi:history",
    ),
    SensorEntityDescription(
        key="heat_pump_5_compressor_last_24h",
        name="Compressor Last 24h",
        icon="mdi:history",
    ),
    SensorEntityDescription(
        key="heat_pump_6_compressor_last_24h",
        name="Compressor Last 24h",
        icon="mdi:history",
    ),
    SensorEntityDescription(
        key="heat_pump_7_compressor_last_24h",
        name="Compressor Last 24h",
        icon="mdi:history",
    ),
    SensorEntityDescription(
        key="heat_pump_8_compressor_last_24h",
        name="Compressor Last 24h",
        icon="mdi:history",
    ),
    SensorEntityDescription(
        key="heat_pump_9_compressor_last_24h",
        name="Compressor Last 24h",
        icon="mdi:history",
    ),
    SensorEntityDescription(
        key="heat_pump_10_compressor_last_24h",
        name="Compressor Last 24h",
        icon="mdi:history",
    ),
    SensorEntityDescription(
        key="software_version_display_month_day",
        name="Software Version Display Month Day",
        icon="mdi:calendar",
    ),
    SensorEntityDescription(
        key="software_version_display_year",
        name="Software Version Display Year",
        icon="mdi:calendar",
    ),
    SensorEntityDescription(
        key="hs_1_status",
        name="Heating System 1 Status",
        icon="mdi:radiator",
    ),
    SensorEntityDescription(
        key="hs_2_status",
        name="Heating System 2 Status",
        icon="mdi:radiator",
    ),
    SensorEntityDescription(
        key="hs_3_status",
        name="Heating System 3 Status",
        icon="mdi:radiator",
    ),
    SensorEntityDescription(
        key="hs_4_status",
        name="Heating System 4 Status",
        icon="mdi:radiator",
    ),
    SensorEntityDescription(
        key="ext_buffer_tank_upper_b41",
        name="Ext Buffer Tank Upper B41",
        native_unit_of_measurement="°C",
        icon="mdi:water",
    ),
    SensorEntityDescription(
        key="ext_buffer_tank_lower_b42",
        name="Ext Buffer Tank Lower B42",
        native_unit_of_measurement="°C",
        icon="mdi:water",
    ),
    SensorEntityDescription(
        key="ext_dhw_buffer_tank_b43",
        name="Ext DHW Buffer Tank B43",
        native_unit_of_measurement="°C",
        icon="mdi:water",
    ),
    SensorEntityDescription(
        key="product_type",
        name="Product Type",
        icon="mdi:information-outline",
    ),
    SensorEntityDescription(
        key="heat_pump_1_type",
        name="Heat Pump 1 Type",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_2_type",
        name="Heat Pump 2 Type",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_3_type",
        name="Heat Pump 3 Type",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_4_type",
        name="Heat Pump 4 Type",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_5_type",
        name="Heat Pump 5 Type",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_6_type",
        name="Heat Pump 6 Type",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_7_type",
        name="Heat Pump 7 Type",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_8_type",
        name="Heat Pump 8 Type",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_9_type",
        name="Heat Pump 9 Type",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_10_type",
        name="Heat Pump 10 Type",
        icon="mdi:heat-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_1_compressor_model",
        name="Heat Pump 1 Compressor Model",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="heat_pump_2_compressor_model",
        name="Heat Pump 2 Compressor Model",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="heat_pump_3_compressor_model",
        name="Heat Pump 3 Compressor Model",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="heat_pump_4_compressor_model",
        name="Heat Pump 4 Compressor Model",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="heat_pump_5_compressor_model",
        name="Heat Pump 5 Compressor Model",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="heat_pump_7_compressor_model",
        name="Heat Pump 7 Compressor Model",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="heat_pump_8_compressor_model",
        name="Heat Pump 8 Compressor Model",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="heat_pump_9_compressor_model",
        name="Heat Pump 9 Compressor Model",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="heat_pump_10_compressor_model",
        name="Heat Pump 10 Compressor Model",
        icon="mdi:chip",
    ),
    SensorEntityDescription(
        key="setpoint_lower_tank",
        name="Setpoint Lower Tank",
        native_unit_of_measurement="°C",
        icon="mdi:target",
    ),
    SensorEntityDescription(
        key="actual_temp_dhw_lower",
        name="Actual Temperature DHW Lower",
        native_unit_of_measurement="°C",
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="actual_temp_dhw",
        name="Actual Temperature DHW",
        native_unit_of_measurement="°C",
        icon="mdi:water-thermometer",
    ),
    SensorEntityDescription(
        key="actual_temp_tank_solar_coil",
        name="Actual Temperature Tank Solar Coil",
        native_unit_of_measurement="°C",
        icon="mdi:solar-power",
    ),
    SensorEntityDescription(
        key="calculated_setpoint_upper_tank_el_heater",
        name="Calculated Setpoint Upper Tank El. Heater",
        native_unit_of_measurement="°C",
        icon="mdi:target",
    ),
    SensorEntityDescription(
        key="current_dhw_capacity_percent",
        name="Current DHW Capacity Percent",
        native_unit_of_measurement="%",
        icon="mdi:percent",
    ),
    SensorEntityDescription(
        key="exhaust_fan_speed_percent",
        name="Exhaust Fan Speed Percent",
        native_unit_of_measurement="%",
        icon="mdi:fan",
    ),
    SensorEntityDescription(
        key="highest_measured_co2",
        name="Highest Measured CO2",
        native_unit_of_measurement="ppm",
        icon="mdi:molecule-co2",
    ),
    SensorEntityDescription(
        key="highest_measured_humidity",
        name="Highest Measured Humidity",
        native_unit_of_measurement="%",
        icon="mdi:water-percent",
    ),
    SensorEntityDescription(
        key="days_until_filter_maintenance",
        name="Days Until Filter Maintenance",
        native_unit_of_measurement="d",
        icon="mdi:calendar-clock",
    ),
    SensorEntityDescription(
        key="ventilation_night_cooling_status",
        name="Ventilation Night Cooling Status",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="cooling_tank_setp",
        name="Cooling Tank Setpoint",
        native_unit_of_measurement="°C",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="cooling_tank_temp",
        name="Cooling Tank Temperature",
        native_unit_of_measurement="°C",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="active_cooling_return_temp",
        name="Active Cooling Return Temperature",
        native_unit_of_measurement="°C",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="heat_pump_1_primary_system_flow",
        name="Heat Pump 1 Primary System Flow",
        native_unit_of_measurement="l/min",
        icon="mdi:water-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_2_primary_system_flow",
        name="Heat Pump 2 Primary System Flow",
        native_unit_of_measurement="l/min",
        icon="mdi:water-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_3_primary_system_flow",
        name="Heat Pump 3 Primary System Flow",
        native_unit_of_measurement="l/min",
        icon="mdi:water-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_4_primary_system_flow",
        name="Heat Pump 4 Primary System Flow",
        native_unit_of_measurement="l/min",
        icon="mdi:water-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_5_primary_system_flow",
        name="Heat Pump 5 Primary System Flow",
        native_unit_of_measurement="l/min",
        icon="mdi:water-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_6_primary_system_flow",
        name="Heat Pump 6 Primary System Flow",
        native_unit_of_measurement="l/min",
        icon="mdi:water-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_7_primary_system_flow",
        name="Heat Pump 7 Primary System Flow",
        native_unit_of_measurement="l/min",
        icon="mdi:water-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_8_primary_system_flow",
        name="Heat Pump 8 Primary System Flow",
        native_unit_of_measurement="l/min",
        icon="mdi:water-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_9_primary_system_flow",
        name="Heat Pump 9 Primary System Flow",
        native_unit_of_measurement="l/min",
        icon="mdi:water-pump",
    ),
    SensorEntityDescription(
        key="heat_pump_10_primary_system_flow",
        name="Heat Pump 10 Primary System Flow",
        native_unit_of_measurement="l/min",
        icon="mdi:water-pump",
    ),
    SensorEntityDescription(
        key="sgmode",
        name="SG Mode",
        icon="mdi:transmission-tower",
    ),
    SensorEntityDescription(
        key="elspot_price_mwh_int",
        name="Elspot Price/MWh Integer",
        icon="mdi:currency-eur",
    ),
    SensorEntityDescription(
        key="elspot_price_mwh_dec",
        name="Elspot Price/MWh Decimals",
        icon="mdi:currency-eur",
    ),
    SensorEntityDescription(
        key="radiator_pump_1",
        name="Radiator Pump 1",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="radiator_pump_2",
        name="Radiator Pump 2",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="radiator_pump_3_g3",
        name="Radiator Pump 3 G3",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="radiator_pump_4_g4",
        name="Radiator Pump 4 G4",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="hs_1_shunt_state",
        name="Heating System 1 Shunt State",
        icon="mdi:valve",
    ),
    SensorEntityDescription(
        key="hs_2_shunt_state",
        name="Heating System 2 Shunt State",
        icon="mdi:valve",
    ),
    SensorEntityDescription(
        key="hs_3_shunt_state",
        name="Heating System 3 Shunt State",
        icon="mdi:valve",
    ),
    SensorEntityDescription(
        key="hs_4_shunt_state",
        name="Heating System 4 Shunt State",
        icon="mdi:valve",
    ),
    SensorEntityDescription(
        key="pumpg41_extern_dhw",
        name="PumpG41 Extern DHW",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="hotwatervalve",
        name="Hot Water Valve",
        icon="mdi:valve",
    ),
    SensorEntityDescription(
        key="extboileron",
        name="Ext Boiler On",
        icon="mdi:fire",
    ),
    SensorEntityDescription(
        key="el1_relay",
        name="EL1 Relay",
        icon="mdi:toggle-switch",
    ),
    SensorEntityDescription(
        key="el2_relay",
        name="EL2 Relay",
        icon="mdi:toggle-switch",
    ),
    SensorEntityDescription(
        key="el3_relay",
        name="EL3 Relay",
        icon="mdi:toggle-switch",
    ),
    SensorEntityDescription(
        key="elheater3_6kw",
        name="ElHeater 3 6kW",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="evk_shunt_state",
        name="EVK Shunt State",
        icon="mdi:valve",
    ),
    SensorEntityDescription(
        key="extboiler_shunt_state",
        name="Ext Boiler Shunt State",
        icon="mdi:valve",
    ),
    SensorEntityDescription(
        key="active_cooling_valve",
        name="Active Cooling Valve",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="active_cooling_demand",
        name="Active Cooling Demand",
        icon="mdi:snowflake",
    ),
    SensorEntityDescription(
        key="dhwpump",
        name="DHW Pump",
        icon="mdi:pump",
    ),
    SensorEntityDescription(
        key="solartankselection",
        name="Solar Tank Selection",
        icon="mdi:solar-power",
    ),
    SensorEntityDescription(
        key="solarbedrockselection",
        name="Solar Bedrock Selection",
        icon="mdi:solar-power",
    ),
    SensorEntityDescription(
        key="hotwatervalve2",
        name="Hot Water Valve 2",
        icon="mdi:valve",
    ),
    SensorEntityDescription(
        key="e4",
        name="E4",
        icon="mdi:alpha-e",
    ),
    SensorEntityDescription(
        key="e1",
        name="E1",
        icon="mdi:alpha-e",
    ),
    SensorEntityDescription(
        key="stat_immersion_heater_kwh_msb",
        name="Stat Immersion Heater kWh MSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="current_room_temp_cooling",
        name="Current Room Temp Cooling",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="heat_pump_1_power_consumption_kw",
        name="HP1 Power Consumption kW",
        native_unit_of_measurement="kW",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_2_power_consumption_kw",
        name="HP2 Power Consumption kW",
        native_unit_of_measurement="kW",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_3_power_consumption_kw",
        name="HP3 Power Consumption kW",
        native_unit_of_measurement="kW",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_4_power_consumption_kw",
        name="HP4 Power Consumption kW",
        native_unit_of_measurement="kW",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_5_power_consumption_kw",
        name="HP5 Power Consumption kW",
        native_unit_of_measurement="kW",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_6_power_consumption_kw",
        name="HP6 Power Consumption kW",
        native_unit_of_measurement="kW",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_7_power_consumption_kw",
        name="HP7 Power Consumption kW",
        native_unit_of_measurement="kW",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_8_power_consumption_kw",
        name="HP8 Power Consumption kW",
        native_unit_of_measurement="kW",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_9_power_consumption_kw",
        name="HP9 Power Consumption kW",
        native_unit_of_measurement="kW",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_10_power_consumption_kw",
        name="HP10 Power Consumption kW",
        native_unit_of_measurement="kW",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_1_compressor_power_consumption_kwh_lsb",
        name="Compressor Power Consumption kWh LSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_1_compressor_power_consumption_kwh_msb",
        name="Compressor Power Consumption kWh MSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_2_compressor_power_consumption_kwh_lsb",
        name="Compressor Power Consumption kWh LSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_2_compressor_power_consumption_kwh_msb",
        name="Compressor Power Consumption kWh MSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_3_compressor_power_consumption_kwh_lsb",
        name="Compressor Power Consumption kWh LSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_3_compressor_power_consumption_kwh_msb",
        name="Compressor Power Consumption kWh MSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_4_compressor_power_consumption_kwh_lsb",
        name="Compressor Power Consumption kWh LSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_4_compressor_power_consumption_kwh_msb",
        name="Compressor Power Consumption kWh MSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_5_compressor_power_consumption_kwh_lsb",
        name="Compressor Power Consumption kWh LSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_5_compressor_power_consumption_kwh_msb",
        name="Compressor Power Consumption kWh MSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_6_compressor_power_consumption_kwh_lsb",
        name="Compressor Power Consumption kWh LSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_6_compressor_power_consumption_kwh_msb",
        name="Compressor Power Consumption kWh MSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_7_compressor_power_consumption_kwh_lsb",
        name="Compressor Power Consumption kWh LSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_7_compressor_power_consumption_kwh_msb",
        name="Compressor Power Consumption kWh MSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_8_compressor_power_consumption_kwh_lsb",
        name="Compressor Power Consumption kWh LSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_8_compressor_power_consumption_kwh_msb",
        name="Compressor Power Consumption kWh MSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_9_compressor_power_consumption_kwh_lsb",
        name="Compressor Power Consumption kWh LSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_9_compressor_power_consumption_kwh_msb",
        name="Compressor Power Consumption kWh MSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_10_compressor_power_consumption_kwh_lsb",
        name="Compressor Power Consumption kWh LSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="heat_pump_10_compressor_power_consumption_kwh_msb",
        name="Compressor Power Consumption kWh MSB",
        native_unit_of_measurement="kWh",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="power_kw_immersion_heaters",
        name="Power kW Immersion Heaters",
        native_unit_of_measurement="kW",
        icon="mdi:flash",
    ),
    # ...existing code...
]

import logging

_logger = logging.getLogger(__name__)

STATUS_MAP = {
    0: "HP upper",
    1: "HP lower",
    2: "Add",
    3: "HP + Add",
    4: "HC",
    5: "DHW",
    6: "Pool",
    7: "Off",
    8: "Heating mix",
    9: "Wood",
    10: "DHW/HC",
    11: "Cooling",
    12: "Swap",
}

HP_STATUS_MAP = {
    0: "Compressor_off_start_delay",
    1: "Compressor_off_redy_to_start",
    2: "Compressor_wait_until_flow",
    3: "Comperssor_on_heating",
    4: "Defrost_active",
    5: "Compressor_on_cooling",
    6: "Compressor_off_blocked",
    7: "Compressor_off_alarm",
    8: "Function_test",
    30: "HP not defined",
    31: "Compressor not enabled",
    32: "Communication error",
    33: "Charge dhw",
}

SOLAR_MODE_MAP = {
    0: "Off",
    1: "On",
}

HEATING_SYSTEM_MODE_MAP = {
    0: "Heating off",
    1: "Vacation",
    2: "Night reduction",
    3: "On (normal mode)",
}

SG_MODE_MAP = {
    0: "None/Normal",
    1: "Block",
    2: "Low price",
    3: "High cap",
}


def filter_heatpump_sensors(
    sensor_descriptions: list[SensorEntityDescription],
    num_heatpumps: int,
    num_heating_systems: int,
) -> list[SensorEntityDescription]:
    """Filter sensor descriptions to only include the configured number of heat pumps."""
    filtered: list[SensorEntityDescription] = []
    for desc in sensor_descriptions:
        if desc.key.startswith("heat_pump_"):
            parts = desc.key.split("_")
            if len(parts) > 2 and parts[2].isdigit():
                hp_number = int(parts[2])
                if 1 <= hp_number <= num_heatpumps:
                    filtered.append(desc)
                continue
        if desc.key.startswith("hs") or desc.key.startswith("hc"):
            parts = desc.key.split("_")
            _logger.debug("parts: %s", parts)
            if len(parts) > 2 and parts[1].isdigit():
                hs_number = int(parts[1])
                if 1 <= hs_number <= num_heating_systems:
                    filtered.append(desc)
                continue
        filtered.append(desc)
    return filtered


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CTC Ecozenith i550 sensors from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [
        CTCEcozenithSensor(coordinator, description)
        for description in SENSOR_DESCRIPTIONS
        if coordinator.data.get(description.key) is not None
    ]
    async_add_entities(entities)


class CTCEcozenithSensor(SensorEntity):
    """Sensor for a CTC Ecozenith i550 register."""

    def __init__(self, coordinator, description: SensorEntityDescription) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}-{description.key}"

    @property
    def device_info(self) -> dict:
        """Return device info for grouping sensors by heat pump or main device."""
        if self.entity_description.key.startswith("heat_pump_"):
            parts = self.entity_description.key.split("_")
            if parts[2].isdigit():
                hp_number = parts[2]
                return {
                    "identifiers": {(DOMAIN, f"ctc_hp_{hp_number}")},
                    "name": f"Heat Pump {hp_number}",
                    "manufacturer": "CTC",
                    "model": "Ecozenith i550",
                }
        # All other sensors belong to the main device
        return {
            "identifiers": {(DOMAIN, "ctc_ecozenith_i550")},
            "name": "CTC Ecozenith i550",
            "manufacturer": "CTC",
            "model": "Ecozenith i550",
        }

    @property
    def native_value(self):
        """Return the state of the sensor."""
        raw_value = self.coordinator.data.get(self.entity_description.key)
        # Extract value from FeatureRegister if present
        if hasattr(raw_value, "value"):
            raw_value = raw_value.value
        # Return None if value is not available
        if raw_value is None:
            return None
        if self.entity_description.key == "status":
            return STATUS_MAP.get(raw_value)
        if self.entity_description.key == "heat_pump_1_status":
            return HP_STATUS_MAP.get(raw_value)
        if self.entity_description.key == "heat_pump_2_status":
            return HP_STATUS_MAP.get(raw_value)
        if self.entity_description.key == "heat_pump_3_status":
            return HP_STATUS_MAP.get(raw_value)
        if self.entity_description.key == "heat_pump_4_status":
            return HP_STATUS_MAP.get(raw_value)
        if self.entity_description.key == "heat_pump_5_status":
            return HP_STATUS_MAP.get(raw_value)
        if self.entity_description.key == "heat_pump_6_status":
            return HP_STATUS_MAP.get(raw_value)
        if self.entity_description.key == "heat_pump_7_status":
            return HP_STATUS_MAP.get(raw_value)
        if self.entity_description.key == "heat_pump_8_status":
            return HP_STATUS_MAP.get(raw_value)
        if self.entity_description.key == "heat_pump_9_status":
            return HP_STATUS_MAP.get(raw_value)
        if self.entity_description.key == "heat_pump_10_status":
            return HP_STATUS_MAP.get(raw_value)
        if self.entity_description.key == "solar_mode":
            return SOLAR_MODE_MAP.get(raw_value)
        if self.entity_description.key == "hs_1_status":
            return HEATING_SYSTEM_MODE_MAP.get(raw_value)
        if self.entity_description.key == "hs_2_status":
            return HEATING_SYSTEM_MODE_MAP.get(raw_value)
        if self.entity_description.key == "hs_3_status":
            return HEATING_SYSTEM_MODE_MAP.get(raw_value)
        if self.entity_description.key == "hs_4_status":
            return HEATING_SYSTEM_MODE_MAP.get(raw_value)
        if self.entity_description.key == "sgmode":
            return SG_MODE_MAP.get(raw_value)
        return raw_value

    @property
    def available(self) -> bool:
        """Return True if sensor data is available."""
        return self.coordinator.data.get(self.entity_description.key) is not None

    async def async_update(self):
        """Update the sensor."""
        await self.coordinator.async_request_refresh()
