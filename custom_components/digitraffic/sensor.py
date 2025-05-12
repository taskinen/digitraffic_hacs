"""Sensor platform for Digitraffic."""
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SENSOR_MAP, CONF_STATION_ID
from . import DigitrafficDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Digitraffic sensor platform."""
    coordinator: DigitrafficDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    station_id = entry.data[CONF_STATION_ID]

    # Wait for the first update to discover available sensors
    await coordinator.async_config_entry_first_refresh()

    sensors = []
    if coordinator.data:
        # Use the title from the config entry, which holds the validated station name
        station_name = entry.title
        for sensor_key in coordinator.data:
            # Create sensors for all keys except metadata
            if sensor_key not in ["measuredTime", "stationName"]:
                sensors.append(
                    DigitrafficWeatherSensor(
                        coordinator,
                        station_id,
                        station_name,
                        sensor_key,
                    )
                )

    async_add_entities(sensors, True)


class DigitrafficWeatherSensor(CoordinatorEntity[DigitrafficDataUpdateCoordinator], SensorEntity):
    """Representation of a Digitraffic Weather Sensor."""

    def __init__(
        self,
        coordinator: DigitrafficDataUpdateCoordinator,
        station_id: str,
        station_name: str,
        sensor_key: str
    ):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._station_id = station_id
        self._sensor_key = sensor_key
        # Get config if available, otherwise use empty dict (defaults will apply)
        self._config = SENSOR_MAP.get(self._sensor_key, {})

        # Use specific name from SENSOR_MAP if defined, otherwise generate from key
        self._attr_name = f"{station_name} {self._config.get('name', sensor_key.replace('_', ' ').title())}"
        self._attr_unique_id = f"digitraffic_{self._station_id}_{self._sensor_key}"
        self._attr_device_class = self._config.get("device_class")
        self._attr_native_unit_of_measurement = self._config.get("unit")
        self._attr_icon = self._config.get("icon")
        self._attr_state_class = (
            SensorStateClass.MEASUREMENT if self._attr_native_unit_of_measurement else None
        )
        # Link sensor to device
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._station_id)},
            "name": station_name,
            "manufacturer": "Fintraffic",
            "model": "Road Weather Station",
            "entry_type": "service", # or "device" if more appropriate
        }

    @property
    def native_value(self) -> Any | None:
        """Return the state of the sensor."""
        if not self.coordinator.data or self._sensor_key not in self.coordinator.data:
            return None

        value = self.coordinator.data[self._sensor_key]

        if value is None:  # Explicitly handle if the coordinator itself provides None
            return None

        # If this sensor is intended for measurements (has a unit and thus state_class MEASUREMENT)
        if self._attr_state_class == SensorStateClass.MEASUREMENT:
            try:
                return float(value)
            except (ValueError, TypeError):
                _LOGGER.warning(
                    "Sensor %s (key: %s, unit: %s) is configured for measurement "
                    "but received non-numeric value: '%s'. Reporting as unavailable for this update.",
                    self._attr_unique_id,
                    self._sensor_key,
                    self._attr_native_unit_of_measurement,
                    value,
                )
                return None  # Return None if conversion fails for a measurement sensor
        else:
            # For sensors not configured as SensorStateClass.MEASUREMENT.
            # These might be textual, or numeric without a specific unit/state_class.
            if isinstance(value, (int, float)):
                return float(value) # Ensure it's float if already numeric
            if isinstance(value, str):
                try:
                    # Try to convert string to float if it represents a number
                    return float(value)
                except ValueError:
                    # If it's a string but not a valid float, return the string as is
                    return value
            # For other types (e.g. bool), or if value is not str/int/float,
            # convert to string as a general fallback.
            return str(value)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return super().available and self.coordinator.data is not None and self._sensor_key in self.coordinator.data

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attrs = {}
        if self.coordinator.data and "measuredTime" in self.coordinator.data:
            attrs["measured_time"] = self.coordinator.data["measuredTime"]
        return attrs
