"""Config flow for Digitraffic integration."""
import logging
import voluptuous as vol
import aiohttp
import async_timeout
import asyncio  # Add asyncio import

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import selector

from .const import DOMAIN, CONF_STATION_ID, API_ENDPOINT_STATIONS

_LOGGER = logging.getLogger(__name__)

async def fetch_stations(hass) -> dict:
    """Fetch list of available stations from the API."""
    session = async_get_clientsession(hass)
    url = API_ENDPOINT_STATIONS
    _LOGGER.debug("Fetching stations from URL: %s", url)
    
    try:
        async with async_timeout.timeout(30):
            response = await session.get(url, headers={"Accept-Encoding": "gzip"})
            _LOGGER.debug("Received response for stations: Status %s", response.status)
            
            if response.status != 200:
                _LOGGER.error("Failed to fetch stations with status %s. Response: %s", response.status, await response.text())
                return {}
                
            data = await response.json()
            _LOGGER.debug("Fetched %s stations", len(data.get("features", [])))
            
            stations = {}
            for feature in data.get("features", []):
                properties = feature.get("properties", {})
                station_id = properties.get("id")
                station_name = properties.get("name")
                
                if station_id and station_name:
                    stations[str(station_id)] = station_name
                    
            return stations
            
    except asyncio.TimeoutError:
        _LOGGER.error("Timeout fetching stations from API at URL %s", url)
        return {}
    except aiohttp.ClientError as err:
        _LOGGER.error("Network error fetching stations: %s", err, exc_info=True)
        return {}
    except Exception as exc:
        _LOGGER.exception("Unexpected error fetching stations: %s", exc)
        return {}

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_STATION_ID): str,
    }
)

async def validate_station_id(hass, station_id: str) -> dict | None:
    """Validate the user input allows us to connect."""
    session = async_get_clientsession(hass)
    url = f"{API_ENDPOINT_STATIONS}/{station_id}"
    _LOGGER.debug("Validating station ID %s using URL: %s", station_id, url)

    try:
        # Ensure station_id is potentially an integer before proceeding
        try:
            station_id_int = int(station_id)
        except ValueError:
            _LOGGER.error("Station ID '%s' is not a valid integer.", station_id)
            return None

        async with async_timeout.timeout(10):
            response = await session.get(url)
            _LOGGER.debug("Received response for station ID %s: Status %s", station_id, response.status)

            if response.status == 404:
                _LOGGER.error("Station ID %s not found (404).", station_id)
                return None
            elif response.status != 200:
                _LOGGER.error("API request failed for station ID %s with status %s. Response: %s", station_id, response.status, await response.text())
                response.raise_for_status()  # Raise for other non-200 errors after logging

            # Try parsing JSON
            try:
                data = await response.json()
                _LOGGER.debug("Parsed JSON data for station ID %s: %s", station_id, data)
            except aiohttp.ContentTypeError:
                _LOGGER.error("Failed to parse JSON for station ID %s. Response was not valid JSON. Content-Type: %s, Body: %s", station_id, response.content_type, await response.text())
                return None
            except ValueError:  # json.JSONDecodeError inherits from ValueError
                _LOGGER.error("Failed to parse JSON for station ID %s due to invalid JSON format. Body: %s", station_id, await response.text(), exc_info=True)
                return None

            # Check if the response contains expected station data
            properties = data.get("properties")
            if not properties:
                _LOGGER.warning("Validation failed for station ID %s: 'properties' field missing in response. Data: %s", station_id, data)
                return None

            # Validate using the 'id' field instead of 'tmsNumber'
            station_id_from_api = properties.get("id")
            if station_id_from_api is None:
                _LOGGER.warning("Validation failed for station ID %s: 'id' missing in 'properties'. Data: %s", station_id, data)
                return None

            # Compare id from API with the integer version of station_id
            if station_id_from_api == station_id_int:
                station_name = properties.get("name", f"Station {station_id}")
                _LOGGER.info("Successfully validated station ID %s: Name '%s'", station_id, station_name)
                return {"title": station_name}
            else:
                _LOGGER.warning("Validation failed for station ID %s: Provided ID does not match API ID (%s). Data: %s", station_id, station_id_from_api, data)
                return None

    except asyncio.TimeoutError:
        _LOGGER.error("Timeout connecting to API for station ID %s at URL %s", station_id, url)
        return None
    except aiohttp.ClientError as err:
        _LOGGER.error("Network error validating station ID %s: %s", station_id, err, exc_info=True)
        return None
    except Exception as exc:  # Catch broader exceptions
        _LOGGER.exception("Unexpected error validating station ID %s: %s", station_id, exc)
        return None

class DigitrafficConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Digitraffic."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        
        # Fetch available stations for the dropdown
        stations = await fetch_stations(self.hass)
        
        if not stations:
            errors["base"] = "cannot_connect"
            # Fallback to the original schema if we can't fetch stations
            return self.async_show_form(
                step_id="user", data_schema=DATA_SCHEMA, errors=errors
            )
        
        # Create a text input schema with helpful description
        dynamic_schema = vol.Schema(
            {
                vol.Required("Weather station name or ID", description="Enter station name or partial name to search"): str,
            }
        )
        
        if user_input is not None:
            search_input = user_input["Weather station name or ID"].strip()
            
            # First try to match by exact station ID if it's numeric
            matched_station_id = None
            if search_input.isdigit():
                if search_input in stations:
                    matched_station_id = search_input
            
            # If no direct ID match, search by station name
            if not matched_station_id:
                matching_stations = {}
                search_lower = search_input.lower()
                
                for station_id, station_name in stations.items():
                    if search_lower in station_name.lower():
                        matching_stations[station_id] = station_name
                
                if len(matching_stations) == 1:
                    # Exact match found
                    matched_station_id = list(matching_stations.keys())[0]
                elif len(matching_stations) > 1:
                    # Multiple matches - show them to user
                    match_list = [f"{sid}: {name}" for sid, name in sorted(matching_stations.items(), key=lambda x: x[1])[:10]]
                    if len(matching_stations) > 10:
                        match_list.append(f"... and {len(matching_stations) - 10} more")
                    errors["Weather station name or ID"] = f"Multiple matches found. Please be more specific:\n" + "\n".join(match_list)
                else:
                    # No matches found
                    errors["Weather station name or ID"] = f"No stations found matching '{search_input}'. Try a different search term."
            
            # If we have a matched station, validate it
            if matched_station_id:
                try:
                    int_station_id = int(matched_station_id)
                    station_info = await validate_station_id(self.hass, str(int_station_id))
                    if station_info:
                        await self.async_set_unique_id(str(int_station_id))
                        self._abort_if_unique_id_configured()
                        # Update user_input to contain the station ID, not the search term
                        final_data = {CONF_STATION_ID: matched_station_id}
                        return self.async_create_entry(title=station_info["title"], data=final_data)
                    else:
                        errors["base"] = "invalid_station_id"
                except ValueError:
                    errors["Weather station name or ID"] = "invalid_station_id_format"
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.exception("Unexpected exception")
                    errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=dynamic_schema, errors=errors
        )
