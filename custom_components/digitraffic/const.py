"""Constants for the Digitraffic integration."""

DOMAIN = "digitraffic"
PLATFORMS = ["sensor"]

CONF_STATION_ID = "station_id"

# API Endpoints
API_ENDPOINT_STATION_DATA = "https://tie.digitraffic.fi/api/weather/v1/stations/{}/data"
API_ENDPOINT_STATIONS = "https://tie.digitraffic.fi/api/weather/v1/stations"

# Default update interval
UPDATE_INTERVAL_MINUTES = 5

# Sensor mapping (Example - needs refinement based on actual API data)
SENSOR_MAP = {
    "AIR_TEMPERATURE": {"name": "Air Temperature", "unit": "°C", "device_class": "temperature", "icon": "mdi:thermometer"},
    "ROAD_SURFACE_TEMPERATURE": {"name": "Road Surface Temperature", "unit": "°C", "device_class": "temperature", "icon": "mdi:thermometer"},
    "RELATIVE_HUMIDITY": {"name": "Relative Humidity", "unit": "%", "device_class": "humidity", "icon": "mdi:water-percent"},
    "WIND_SPEED": {"name": "Wind Speed", "unit": "m/s", "icon": "mdi:weather-windy"},
    "WIND_DIRECTION": {"name": "Wind Direction", "unit": "°", "icon": "mdi:compass-outline"},
    # Add more sensors based on API exploration
}
