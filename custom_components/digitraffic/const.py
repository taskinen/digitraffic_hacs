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
    "MAA_1": {"name": "Maan lämpötila 1", "unit": "°C", "icon": "mdi:earth"},
    "MAA_2": {"name": "Maan lämpötila 2", "unit": "°C", "icon": "mdi:earth"},
    "KASTEPISTE": {"name": "Kastepiste", "unit": "°C", "icon": "mdi:thermometer-water"},
    "JÄÄTYMISPISTE_1": {"name": "Jäätymispiste 1", "unit": "°C", "icon": "mdi:snowflake-thermometer"},
    "JÄÄTYMISPISTE_2": {"name": "Jäätymispiste 2", "unit": "°C", "icon": "mdi:snowflake-thermometer"},
    "RUNKO_1": {"name": "Tien rungon lämpötila", "unit": "°C", "icon": "mdi:road-variant"},
    "KESKITUULI": {"name": "Keskituuli", "unit": "m/s", "icon": "mdi:weather-windy"},
    "MAKSIMITUULI": {"name": "Maksimituuli", "unit": "m/s", "icon": "mdi:weather-windy"},
    "TUULENSUUNTA": {"name": "Tuulensuunta", "unit": "°", "icon": "mdi:compass-outline"},
    "ILMANPAINE": {"name": "Ilmanpaine", "unit": "hPa", "icon": "mdi:gauge"},
    "ILMANPAINE_DERIVAATTA": {"name": "Ilmanpaineen muutos", "unit": "hPa/3h", "icon": "mdi:gauge"},
    "ILMAN_KOSTEUS": {"name": "Ilman suhteellinen kosteus", "unit": "%", "icon": "mdi:water-percent"},
    "SADE": {"name": "Sade", "icon": "mdi:weather-rainy"},
    "SADE_INTENSITEETTI": {"name": "Sateen intensiteetti", "unit": "mm/h", "icon": "mdi:weather-pouring"},
    "SADESUMMA": {"name": "Sadesumma", "unit": "mm", "icon": "mdi:weather-rainy"},
    "SATEEN_OLOMUOTO_PWDXX": {"name": "Sateen olomuoto", "icon": "mdi:weather-pouring"},
    "NÄKYVYYS_KM": {"name": "Näkyvyys km", "unit": "km", "icon": "mdi:eye"},
    "KELI_1": {"name": "Keliluokka 1", "icon": "mdi:road"},
    "KELI_2": {"name": "Keliluokka 2", "icon": "mdi:road"},
    "VAROITUS_1": {"name": "Varoitustaso 1", "icon": "mdi:alert"},
    "VAROITUS_2": {"name": "Varoitustaso 2", "icon": "mdi:alert"},
    "JOHTAVUUS_1": {"name": "Johtavuus 1", "unit": "V", "icon": "mdi:flash"},
    "JOHTAVUUS_2": {"name": "Johtavuus 2", "unit": "V", "icon": "mdi:flash"},
    "PINTASIGNAALI_1": {"name": "Pintasignaali 1", "unit": "V", "icon": "mdi:flash"},
    "PINTASIGNAALI_2": {"name": "Pintasignaali 2", "unit": "V", "icon": "mdi:flash"},
    "JÄÄTAAJUUS_1": {"name": "Jäätaajuus 1", "unit": "Hz", "icon": "mdi:snowflake-variant"},
    "JÄÄTAAJUUS_2": {"name": "Jäätaajuus 2", "unit": "Hz", "icon": "mdi:snowflake-variant"},
    "ASEMAN_STATUS_1": {"name": "Aseman status 1", "icon": "mdi:alert-circle-outline"},
    "ASEMAN_STATUS_2": {"name": "Aseman status 2", "icon": "mdi:alert-circle-outline"},
    "SADE_TILA": {"name": "Sateen tila", "icon": "mdi:weather-pouring"},
    "KOSTEUDEN_MÄÄRÄ_2": {"name": "Kosteuden määrä 2", "unit": "mm", "icon": "mdi:water"},
    "SUOLAN_MÄÄRÄ_2": {"name": "Suolan määrä 2", "unit": "g/m²", "icon": "mdi:beaker-outline"},
    "SUOLAN_VÄKEVYYS_2": {"name": "Suolan väkevyys 2", "unit": "g/l", "icon": "mdi:beaker-outline"},
    "TURVALLISUUSLÄMPÖ_2": {"name": "Turvallisuuslämpö 2", "unit": "°C", "icon": "mdi:thermometer-alert"},
    "NÄKYVYYS_M": {"name": "Näkyvyys m", "unit": "m", "icon": "mdi:eye"},
    "KASTEPISTE_ERO_ILMA": {"name": "Kastepiste-ero ilmaan", "unit": "°C", "icon": "mdi:thermometer-water"},
    "PWD_STATUS": {"name": "PWD status", "icon": "mdi:alert-circle-outline"},
    "PWD_TILA": {"name": "PWD tila", "icon": "mdi:alert-circle-outline"},
    "PWD_NÄK_TILA": {"name": "PWD näkyvyystila", "icon": "mdi:alert-circle-outline"},
    "AURINKOUP": {"name": "Aurinko ylhäällä", "icon": "mdi:weather-sunny"},
    "VALOISAA": {"name": "Valoisaa", "icon": "mdi:brightness-5"},
    "KUURAPISTE": {"name": "Kuurapiste", "unit": "°C", "icon": "mdi:snowflake"},
    "KUURAPISTE_ERO_ILMA": {"name": "Kuurapiste-ero ilmaan", "unit": "°C", "icon": "mdi:snowflake"},
    "KUITUVASTE_PIENI_2": {"name": "Kuituvaste pieni 2", "icon": "mdi:chart-bar"},
    "KUITUVASTE_SUURI_2": {"name": "Kuituvaste suuri 2", "icon": "mdi:chart-bar"},
    "PWD_LÄHETTIMEN_TAKAISINSIRONNAN_MUUTOS": {"name": "PWD takaisinsironnan muutos", "icon": "mdi:signal" },
    "TIENPINNAN_TILA_OPT2": {"name": "Tienpinnan tila OPT2", "icon": "mdi:road"},
    "TIENPINNAN_TILA_1": {"name": "Tienpinnan tila 1", "icon": "mdi:road"},
    "TIENPINNAN_TILA_2": {"name": "Tienpinnan tila 2", "icon": "mdi:road"},
    "OPTISEN_ANTURIN_KELI2": {"name": "Optisen anturin keli 2", "icon": "mdi:road"},
    "OPTISEN_ANTURIN_VAROITUS2": {"name": "Optisen anturin varoitus 2", "icon": "mdi:alert-circle-outline"},
    "KITKA2": {"name": "Kitka 2", "unit": "µ", "icon": "mdi:chart-line"},
    "VEDEN_MÄÄRÄ2": {"name": "Veden määrä 2", "unit": "mm", "icon": "mdi:water"},
    "LUMEN_MÄÄRÄ2": {"name": "Lumen määrä 2", "unit": "mm", "icon": "mdi:snowflake"},
    "JÄÄN_MÄÄRÄ2": {"name": "Jään määrä 2", "unit": "mm", "icon": "mdi:snowflake"},
    "ASEMAN_STATUS_OPT2": {"name": "Aseman status OPT2", "icon": "mdi:alert-circle-outline"},
    "KITKA2_LUKU": {"name": "Kitka 2 luku", "unit": "µ", "icon": "mdi:chart-line"},
    "DSC_VASTAANOTTIMEN_PUHTAUS2": {"name": "DSC vastaanottimen puhtaus 2", "icon": "mdi:alert-circle-outline"},
    "DSC_STAT2": {"name": "DSC status 2", "icon": "mdi:alert-circle-outline"},
    "ILMAN_LÄMPÖTILA_24H_MIN": {"name": "Ilman lämpötila 24 h min", "unit": "°C", "icon": "mdi:thermometer-low"},
    "ILMAN_LÄMPÖTILA_24H_MAX": {"name": "Ilman lämpötila 24 h max", "unit": "°C", "icon": "mdi:thermometer-high"},
    "SADESUMMA_LIUKUVA_24H": {"name": "Sadesumma liukuva 24 h", "unit": "mm", "icon": "mdi:weather-rainy"},
    "KASTEPISTE_ERO_TIE2": {"name": "Kastepiste-ero tie 2", "unit": "°C", "icon": "mdi:thermometer-water"},
}
