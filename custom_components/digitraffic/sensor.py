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
        station_name = coordinator.data.get("stationName", f"Station {station_id}")
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
        if self.coordinator.data and self._sensor_key in self.coordinator.data:
            value = self.coordinator.data[self._sensor_key]
            # Attempt to convert to float if possible (most sensor values are numeric)
            try:
                return float(value)
            except (ValueError, TypeError):
                return value # Return as string if not numeric
        return None

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
