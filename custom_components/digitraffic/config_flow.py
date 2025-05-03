"""Config flow for Digitraffic integration."""
import logging
import voluptuous as vol
import aiohttp
import async_timeout

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
    try:
        async with async_timeout.timeout(10):
            response = await session.get(url)
            response.raise_for_status()
            data = await response.json()
            # Check if the response contains expected station data
            if data and data.get("properties", {}).get("tmsNumber") == int(station_id):
                return {"title": data.get("properties", {}).get("name", f"Station {station_id}")}
            else:
                return None # Station ID might exist but response format unexpected
    except (aiohttp.ClientError, asyncio.TimeoutError):
        _LOGGER.error("Failed to connect or validate station ID %s", station_id, exc_info=True)
        return None
    except ValueError:
         _LOGGER.error("Station ID %s is not a valid integer", station_id)
         return None # Station ID must be an integer
    except Exception:
        _LOGGER.exception("Unexpected error validating station ID %s", station_id)
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
