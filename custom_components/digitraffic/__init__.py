"""The Digitraffic integration."""
import asyncio
import logging
from datetime import timedelta

import async_timeout
import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, PLATFORMS, CONF_STATION_ID, API_ENDPOINT_STATION_DATA, UPDATE_INTERVAL_MINUTES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Digitraffic from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    station_id = entry.data[CONF_STATION_ID]
    session = async_get_clientsession(hass)

    coordinator = DigitrafficDataUpdateCoordinator(
        hass,
        session,
        station_id,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class DigitrafficDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Digitraffic data."""

    def __init__(self, hass: HomeAssistant, session: aiohttp.ClientSession, station_id: str):
        """Initialize."""
        self.station_id = station_id
        self.session = session
        self.api_url = API_ENDPOINT_STATION_DATA.format(self.station_id)

        update_interval = timedelta(minutes=UPDATE_INTERVAL_MINUTES)
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            async with async_timeout.timeout(10):
                response = await self.session.get(self.api_url)
                response.raise_for_status() # Raise exception for bad status codes
                data = await response.json()
                # Process data: Extract relevant sensor values
                # The API returns a structure like {"stationId": ..., "measuredTime": ..., "sensorValues": [...]} 
                # We need to parse the sensorValues array.
                processed_data = {}
                if data and "sensorValues" in data:
                    for sensor in data["sensorValues"]:
                        # Use sensor name or id as key, store value
                        # Need to decide on a consistent key (e.g., sensor["name"])
                        sensor_key = sensor.get("name") # Or sensor.get("id")
                        if sensor_key:
                            processed_data[sensor_key] = sensor.get("value")
                    processed_data["measuredTime"] = data.get("measuredTime")
                    processed_data["stationName"] = data.get("stationName", f"Station {self.station_id}") # Fallback name
                return processed_data
        except aiohttp.ClientError as err:
            _LOGGER.error("Error communicating with API: %s", err)
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        except asyncio.TimeoutError as err:
            _LOGGER.error("Timeout fetching data from API")
            raise UpdateFailed("Timeout fetching data from API") from err
        except Exception as err:
            _LOGGER.exception("Unexpected error fetching data")
            raise UpdateFailed(f"Unexpected error: {err}") from err
