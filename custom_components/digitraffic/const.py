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
    "AIR_TEMPERATURE": {"name": "Air Temperature", "unit": "°C", "device_class": "temperature", "state_class": "measurement", "icon": "mdi:thermometer"},
    "ROAD_SURFACE_TEMPERATURE": {"name": "Road Surface Temperature", "unit": "°C", "device_class": "temperature", "state_class": "measurement", "icon": "mdi:thermometer"},
    "RELATIVE_HUMIDITY": {"name": "Relative Humidity", "unit": "%", "device_class": "humidity", "state_class": "measurement", "icon": "mdi:water-percent"},
    "WIND_SPEED": {"name": "Wind Speed", "unit": "m/s", "device_class": "wind_speed", "state_class": "measurement", "icon": "mdi:weather-windy"},
    "WIND_DIRECTION": {"name": "Wind Direction", "unit": "°", "device_class": "wind_direction", "state_class": "measurement", "icon": "mdi:compass-outline"},
    "AIR_PRESSURE": {"name": "Air Pressure", "unit": "hPa", "device_class": "pressure", "state_class": "measurement", "icon": "mdi:gauge"},
    "DEW_POINT": {"name": "Dew Point", "unit": "°C", "device_class": "temperature", "state_class": "measurement", "icon": "mdi:thermometer"},
    "PRECIPITATION_AMOUNT": {"name": "Precipitation Amount", "unit": "mm", "device_class": "precipitation", "state_class": "measurement", "icon": "mdi:weather-rainy"},
    "SURFACE_WATER_THICKNESS": {"name": "Surface Water Thickness", "unit": "mm", "device_class": "precipitation", "state_class": "measurement", "icon": "mdi:water"},
    # Add more sensors as needed based on API documentation
}
