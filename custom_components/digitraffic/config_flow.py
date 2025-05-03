"""Config flow for Digitraffic integration."""
import logging
import voluptuous as vol
import aiohttp
import async_timeout
import asyncio  # Add asyncio import

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_STATION_ID, API_ENDPOINT_STATIONS

_LOGGER = logging.getLogger(__name__)

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
        if user_input is not None:
            station_id = user_input[CONF_STATION_ID]
            try:
                # Ensure station_id is an integer before validation
                int_station_id = int(station_id)
                station_info = await validate_station_id(self.hass, str(int_station_id))
                if station_info:
                    await self.async_set_unique_id(str(int_station_id))
                    self._abort_if_unique_id_configured()
                    return self.async_create_entry(title=station_info["title"], data=user_input)
                else:
                    errors["base"] = "invalid_station_id"
            except ValueError:
                errors[CONF_STATION_ID] = "invalid_station_id_format"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
