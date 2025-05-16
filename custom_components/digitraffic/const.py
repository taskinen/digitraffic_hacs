"""Constants for the Digitraffic integration."""

DOMAIN = "digitraffic"
PLATFORMS = ["sensor"]

CONF_STATION_ID = "station_id"

# API Endpoints
API_ENDPOINT_STATION_DATA = "https://tie.digitraffic.fi/api/weather/v1/stations/{}/data"
API_ENDPOINT_STATIONS = "https://tie.digitraffic.fi/api/weather/v1/stations"

# Default update interval
UPDATE_INTERVAL_MINUTES = 5

# Sensor mapping to names, units and icons
# The keys in this dictionary should match the keys in the API response
SENSOR_MAP = {
    "ILMA": {"name": "Ilman lämpötila", "unit": "°C", "icon": "mdi:thermometer"},
    "ILMA_DERIVAATTA": {"name": "Ilman lämpötilan muutos", "unit": "°C/h", "icon": "mdi:thermometer"},
    "TIE_1": {"name": "Tienpinnan lämpötila 1", "unit": "°C", "icon": "mdi:road-variant"},
    "TIE_1_DERIVAATTA": {"name": "Tienpinnan lämpötilan muutos 1", "unit": "°C/h", "icon": "mdi:road-variant"},
    "TIE_2": {"name": "Tienpinnan lämpötila 2", "unit": "°C", "icon": "mdi:road-variant"},
    "TIE_2_DERIVAATTA": {"name": "Tienpinnan lämpötilan muutos 2", "unit": "°C/h", "icon": "mdi:road-variant"},
    "MAA_1": {"name": "Maan lämpötila 1", "unit": "°C", "icon": "mdi:shovel"},
    "MAA_2": {"name": "Maan lämpötila 2", "unit": "°C", "icon": "mdi:shovel"},
    "KASTEPISTE": {"name": "Kastepiste", "unit": "°C", "icon": "mdi:water"},
    "JÄÄTYMISPISTE_1": {"name": "Jäätymispiste 1", "unit": "°C", "icon": "mdi:snowflake"},
    "JÄÄTYMISPISTE_2": {"name": "Jäätymispiste 2", "unit": "°C", "icon": "mdi:snowflake"},
    "RUNKO_1": {"name": "Tien rungon lämpötila", "unit": "°C", "icon": "mdi:thermometer"},
    "KESKITUULI": {"name": "Keskituuli", "unit": "m/s", "icon": "mdi:weather-windy"},
    "MAKSIMITUULI": {"name": "Maksimituuli", "unit": "m/s", "icon": "mdi:weather-windy"},
    "TUULENSUUNTA": {"name": "Tuulensuunta", "unit": "°", "icon": "mdi:compass-outline"},
    "ILMANPAINE": {"name": "Ilmanpaine", "unit": "hPa", "icon": "mdi:gauge"},
    "ILMANPAINE_DERIVAATTA": {"name": "Ilmanpaineen muutos", "unit": "hPa/3h", "icon": "mdi:gauge"},
    "ILMAN_KOSTEUS": {"name": "Ilman suhteellinen kosteus", "unit": "%", "icon": "mdi:water-percent"},
    "SADE": {"name": "Sade", "unit": "///", "icon": "mdi:weather-rainy"},
    "SADE_INTENSITEETTI": {"name": "Sateen intensiteetti", "unit": "mm/h", "icon": "mdi:weather-pouring"},
    "SADESUMMA": {"name": "Sadesumma", "unit": "mm", "icon": "mdi:weather-rainy"},
    "SATEEN_OLOMUOTO_PWDXX": {"name": "Sateen olomuoto", "unit": "///", "icon": "mdi:weather-pouring"},
    "NÄKYVYYS_KM": {"name": "Näkyvyys km", "unit": "km", "icon": "mdi:eye"},
    "KELI_1": {"name": "Keliluokka 1", "unit": "***", "icon": "mdi:road"},
    "KELI_2": {"name": "Keliluokka 2", "unit": "***", "icon": "mdi:road"},
    "VAROITUS_1": {"name": "Varoitustaso 1", "unit": "???", "icon": "mdi:alert"},
    "VAROITUS_2": {"name": "Varoitustaso 2", "unit": "???", "icon": "mdi:alert"},
    "JOHTAVUUS_1": {"name": "Johtavuus 1", "unit": "V", "icon": "mdi:flash"},
    "JOHTAVUUS_2": {"name": "Johtavuus 2", "unit": "V", "icon": "mdi:flash"},
    "PINTASIGNAALI_1": {"name": "Pintasignaali 1", "unit": "V", "icon": "mdi:flash"},
    "PINTASIGNAALI_2": {"name": "Pintasignaali 2", "unit": "V", "icon": "mdi:flash"},
    "JÄÄTAAJUUS_1": {"name": "Jäätaajuus 1", "unit": "Hz", "icon": "mdi:snowflake"},
    "JÄÄTAAJUUS_2": {"name": "Jäätaajuus 2", "unit": "Hz", "icon": "mdi:snowflake"},
}
