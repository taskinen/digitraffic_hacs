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
    # === AIR TEMPERATURE SENSORS ===
    "ILMA": {"name": "Ilman lämpötila n. 4 metrin korkeudelta", "unit": "°C", "icon": "mdi:thermometer"},
    "ILMA_DERIVAATTA": {"name": "Ilman lämpötilan muutos", "unit": "°C/h", "icon": "mdi:thermometer"},
    "ILMAN_LÄMPÖTILA_24H_MIN": {"name": "Ilman lämpötila 24 h min", "unit": "°C", "icon": "mdi:thermometer-low"},
    "ILMAN_LÄMPÖTILA_24H_MAX": {"name": "Ilman lämpötila 24 h max", "unit": "°C", "icon": "mdi:thermometer-high"},
    
    # === ROAD SURFACE TEMPERATURE SENSORS ===
    "TIE_1": {"name": "Tienpinnan lämpötila 1", "unit": "°C", "icon": "mdi:road-variant"},
    "TIE_1_DERIVAATTA": {"name": "Tienpinnan lämpötilan muutos 1", "unit": "°C/h", "icon": "mdi:road-variant"},
    "TIE_2": {"name": "Tienpinnan lämpötila 2", "unit": "°C", "icon": "mdi:road-variant"},
    "TIE_2_DERIVAATTA": {"name": "Tienpinnan lämpötilan muutos 2", "unit": "°C/h", "icon": "mdi:road-variant"},
    "TIE_3": {"name": "Tienpinnan lämpötila tieanturi 3:lta", "unit": "°C", "icon": "mdi:road-variant"},
    "TIE_3_DERIVAATTA": {"name": "Tienpinnan lämpötilan muutos tieanturilta 3 mitattuna", "unit": "°C/h", "icon": "mdi:road-variant"},
    "TIE_4": {"name": "Tienpinnan lämpötila tieanturi 4:ssd", "unit": "°C", "icon": "mdi:road-variant"},
    "TIE_4_DERIVAATTA": {"name": "Tienpinnan lämpötilan muutos tieanturilta 4 mitattuna", "unit": "°C/h", "icon": "mdi:road-variant"},
    "RUNKO_1": {"name": "Tien rungon lämpötila", "unit": "°C", "icon": "mdi:road-variant"},
    "TIEN_LÄMPÖTILA_DST-ANT": {"name": "Tienpinnan lämpötila optiselta DST111-anturilta", "unit": "°C", "icon": "mdi:road-variant"},
    
    # === GROUND TEMPERATURE SENSORS ===
    "MAA_1": {"name": "Maan lämpötila 1", "unit": "°C", "icon": "mdi:earth"},
    "MAA_2": {"name": "Maan lämpötila 2", "unit": "°C", "icon": "mdi:earth"},
    "MAA_3": {"name": "Maan lämpötila n. 4-7 cm:n syvyydestä tieanturi 3:lta", "unit": "°C", "icon": "mdi:earth"},
    "MAA_4": {"name": "Maan lämpötila n. 4-7 cm:n syvyydestä tieanturi 4:lta", "unit": "°C", "icon": "mdi:earth"},
    
    # === DEW POINT AND FREEZING POINT SENSORS ===
    "KASTEPISTE": {"name": "Lämpötila, jossa ilman suhteellinen kosteus on 100%", "unit": "°C", "icon": "mdi:thermometer-water"},
    "KASTEPISTE_ERO_ILMA": {"name": "Kastepiste-ero ilmaan", "unit": "°C", "icon": "mdi:thermometer-water"},
    "KASTEPISTE_ERO_TIE": {"name": "Tienpinta- ja kastepistelämpötilojen välinen ero", "unit": "°C", "icon": "mdi:thermometer-water"},
    "KASTEPISTE_ERO_TIE2": {"name": "Kastepiste-ero tie 2", "unit": "°C", "icon": "mdi:thermometer-water"},
    "JÄÄTYMISPISTE_1": {"name": "Jäätymispiste 1", "unit": "°C", "icon": "mdi:snowflake-thermometer"},
    "JÄÄTYMISPISTE_2": {"name": "Jäätymispiste 2", "unit": "°C", "icon": "mdi:snowflake-thermometer"},
    "JÄÄTYMISPISTE_3": {"name": "Tienpinnalla olevan kosteuden/veden jäätymislämpötila ant. 3", "unit": "°C", "icon": "mdi:snowflake-thermometer"},
    "JÄÄTYMISPISTE_4": {"name": "Tienpinnalla olevan kosteuden/veden jäätymislämpötila ant. 4", "unit": "°C", "icon": "mdi:snowflake-thermometer"},
    "KUURAPISTE": {"name": "Kuurapiste", "unit": "°C", "icon": "mdi:snowflake"},
    "KUURAPISTE_ERO_ILMA": {"name": "Kuurapiste-ero ilmaan", "unit": "°C", "icon": "mdi:snowflake"},
    "KUURAPISTE_ERO_TIE": {"name": "Kuurapiste-ero tiehen", "unit": "°C", "icon": "mdi:snowflake"},
    
    # === WIND SENSORS ===
    "KESKITUULI": {"name": "Tuulen keskinopeus 10 minuutin ajalta", "unit": "m/s", "icon": "mdi:weather-windy"},
    "MAKSIMITUULI": {"name": "Tuulen maksiminopeus 10 minuutin ajalta", "unit": "m/s", "icon": "mdi:weather-windy"},
    "TUULENSUUNTA": {"name": "Keskimääräinen tuulensuunta 10 minuutin ajalta", "unit": "°", "icon": "mdi:compass-outline"},
    
    # === ATMOSPHERIC PRESSURE SENSORS ===
    "ILMANPAINE": {"name": "Ilmanpaine, muutettu merenpinnan tasoon", "unit": "hPa", "icon": "mdi:gauge"},
    "ILMANPAINE_DERIVAATTA": {"name": "Ilmanpaineen muutos 3 tunnin aikana", "unit": "hPa/3h", "icon": "mdi:gauge"},
    
    # === HUMIDITY SENSORS ===
    "ILMAN_KOSTEUS": {"name": "Ilman suhteellinen kosteus", "unit": "%", "icon": "mdi:water-percent"},
    
    # === PRECIPITATION SENSORS ===
    "SADE": {"name": "Sade", "icon": "mdi:weather-rainy"},
    "SADE I/O": {"name": "Sataa", "icon": "mdi:weather-rainy"},
    "SADE_INTENSITEETTI": {"name": "Sateen intensiteetti", "unit": "mm/h", "icon": "mdi:weather-pouring"},
    "SADESUMMA": {"name": "Sadesumma: nollataan aamulla kello 6.00", "unit": "mm", "icon": "mdi:weather-rainy"},
    "SADESUMMA_LIUKUVA_24H": {"name": "Sadesumma liukuva 24 h", "unit": "mm", "icon": "mdi:weather-rainy"},
    "SATEEN_OLOMUOTO_PWDXX": {"name": "Sateen olomuoto", "icon": "mdi:weather-pouring"},
    "SADE_TILA": {"name": "Sateen tila", "icon": "mdi:weather-pouring"},
    "VALLITSEVA_SÄÄ": {"name": "PWD sääanturin ilmoittama vallitseva sää WMO-luokiteltuna", "icon": "mdi:weather-cloudy"},
    
    # === VISIBILITY SENSORS ===
    "NÄKYVYYS_KM": {"name": "Näkyvyys PWD-sääanturilta mitattuna kilometreissä", "unit": "km", "icon": "mdi:eye"},
    "NÄKYVYYS_M": {"name": "Näkyvyys PWD-sääanturilta mitattuna metreissä", "unit": "m", "icon": "mdi:eye"},
    "NÄKYVYYS_DSC_1": {"name": "Näkyvyys DSC -anturilta", "unit": "m", "icon": "mdi:eye"},
    "NÄKYVYYS_DSC_2": {"name": "Näkyvyys DSC -anturilta 2", "unit": "m", "icon": "mdi:eye"},
    
    # === SNOW MEASUREMENT SENSORS ===
    "LUMENMITTAUS_A": {"name": "Lumikerroksen paksuus tien reunaviivan kohdilla", "unit": "mm", "icon": "mdi:snowflake"},
    "LUMENMITTAUS_B": {"name": "Lumikerroksen paksuus tien ajouran kohdalla", "unit": "mm", "icon": "mdi:snowflake"},
    "LUMENMITTAUS_C": {"name": "Lumikerroksen paksuus keskemmällä tietä", "unit": "mm", "icon": "mdi:snowflake"},
    "LUMENMITTAUS_KA": {"name": "Lumikerroksen paksuus tiellä keskimäärin", "unit": "mm", "icon": "mdi:snowflake"},
    "LUMEN_MÄÄRÄ1": {"name": "Lumen määrä tienpinnalla DSC-anturilta", "unit": "mm", "icon": "mdi:snowflake"},
    "LUMEN_MÄÄRÄ2": {"name": "Lumen määrä 2", "unit": "mm", "icon": "mdi:snowflake"},
    
    # === SOLAR RADIATION AND LIGHT SENSORS ===
    "AURINGON_SÄTEILY_ULOS": {"name": "Auringon säteily ulospäin", "unit": "W/m2", "icon": "mdi:weather-sunny"},
    "AURINGON_SÄTEILY_ALAS": {"name": "Auringon säteily alaspäin", "unit": "W/m2", "icon": "mdi:weather-sunny"},
    "AURINGON_IR_SATEILY_ULOS": {"name": "Auringon ir säteily ulospäin", "unit": "W/m2", "icon": "mdi:weather-sunny"},
    "AURINGON_IR_SATEILY_ALAS": {"name": "Auringon ir säteily alaspäin", "unit": "W/m2", "icon": "mdi:weather-sunny"},
    "NETTOSÄTEILY(ANT97)": {"name": "Nettosäteily", "unit": "W/m2", "icon": "mdi:weather-sunny"},
    "AURINKOUP": {"name": "Aurinko ylhäällä", "icon": "mdi:weather-sunny"},
    "VALOISAA": {"name": "Valoisaa", "icon": "mdi:brightness-5"},
    
    # === ROAD CONDITIONS AND FRICTION SENSORS ===
    "KELI_1": {"name": "Keliluokka 1", "icon": "mdi:road"},
    "KELI_2": {"name": "Keliluokka 2", "icon": "mdi:road"},
    "KELI_3": {"name": "Tiesääaseman päättelemä keliluokka 3. anturilta", "icon": "mdi:road"},
    "KELI_4": {"name": "Tiesääaseman päättelemä keliluokka 4. anturilta", "icon": "mdi:road"},
    "TIENPINNAN_TILA_1": {"name": "Tienpinnan tila 1", "icon": "mdi:road"},
    "TIENPINNAN_TILA_2": {"name": "Tienpinnan tila 2", "icon": "mdi:road"},
    "TIENPINNAN_TILA_3": {"name": "Tienpinnan tila 3", "icon": "mdi:road"},
    "TIENPINNAN_TILA_4": {"name": "Tienpinnan tila 4", "icon": "mdi:road"},
    "TIENPINNAN_TILA_OPT1": {"name": "Tienpinnan tila OPT1", "icon": "mdi:road"},
    "TIENPINNAN_TILA_OPT2": {"name": "Tienpinnan tila OPT2", "icon": "mdi:road"},
    "KITKA1": {"name": "Tienpinnan laskennallinen kitka DSC-anturista 1", "unit": "µ", "icon": "mdi:chart-line"},
    "KITKA1_LUKU": {"name": "Tienpinnan laskennallinen kitka DSC-anturista 1. Pelkkä lukuarvo!", "unit": "µ", "icon": "mdi:chart-line"},
    "KITKA2": {"name": "Kitka 2", "unit": "µ", "icon": "mdi:chart-line"},
    "KITKA2_LUKU": {"name": "Kitka 2 luku", "unit": "µ", "icon": "mdi:chart-line"},
    
    # === ROAD SURFACE MOISTURE AND SUBSTANCE SENSORS ===
    "KOSTEUDEN_MÄÄRÄ_1": {"name": "Tienpinnalla olevan kosteuden määrä tienpinta-anturilla 1", "unit": "mm", "icon": "mdi:water"},
    "KOSTEUDEN_MÄÄRÄ_2": {"name": "Kosteuden määrä 2", "unit": "mm", "icon": "mdi:water"},
    "KOSTEUDEN_MÄÄRÄ_3": {"name": "Tien pinnalla oleva kosteuden määrä tienpinta-anturilla 3", "unit": "mm", "icon": "mdi:water"},
    "KOSTEUDEN_MÄÄRÄ_4": {"name": "Tien pinnalla oleva kosteuden määrä tienpinta-anturilla 4", "unit": "mm", "icon": "mdi:water"},
    "VEDEN_MÄÄRÄ1": {"name": "Veden määrä tienpinnalla DSC-anturilta 1", "unit": "mm", "icon": "mdi:water"},
    "VEDEN_MÄÄRÄ2": {"name": "Veden määrä 2", "unit": "mm", "icon": "mdi:water"},
    "JÄÄN_MÄÄRÄ1": {"name": "Jään määrä tienpinnalla DSC-anturilta 1", "unit": "mm", "icon": "mdi:snowflake"},
    "JÄÄN_MÄÄRÄ2": {"name": "Jään määrä 2", "unit": "mm", "icon": "mdi:snowflake"},
    "SUOLAN_MÄÄRÄ_1": {"name": "Tienpinnalla olevan suolan määrä tienpinta-anturilla 1", "unit": "g/m2", "icon": "mdi:beaker-outline"},
    "SUOLAN_MÄÄRÄ_2": {"name": "Suolan määrä 2", "unit": "g/m²", "icon": "mdi:beaker-outline"},
    "SUOLAN_MÄÄRÄ_3": {"name": "Tienpinnalla olevan suolan määrä tienpinta-anturilla 3", "unit": "g/m2", "icon": "mdi:beaker-outline"},
    "SUOLAN_MÄÄRÄ_4": {"name": "Tienpinnalla olevan suolan määrä tienpinta-anturilla 4", "unit": "g/m2", "icon": "mdi:beaker-outline"},
    "SUOLAN_VÄKEVYYS_1": {"name": "Tienpinnalla olevan suolan väkevyys tienpinta-anturilla 1", "unit": "g/l", "icon": "mdi:beaker-outline"},
    "SUOLAN_VÄKEVYYS_2": {"name": "Suolan väkevyys 2", "unit": "g/l", "icon": "mdi:beaker-outline"},
    "SUOLAN_VÄKEVYYS_3": {"name": "Tienpinnalla olevan suolan väkevyys tienpinta-anturilla 3", "unit": "g/l", "icon": "mdi:beaker-outline"},
    "SUOLAN_VÄKEVYYS_4": {"name": "Tienpinnalla olevan suolan väkevyys tienpinta-anturilla 4", "unit": "g/l", "icon": "mdi:beaker-outline"},
    
    # === SAFETY TEMPERATURE SENSORS ===
    "TURVALLISUUSLÄMPÖ_1": {"name": "Lämpötila, jonka yläpuolella tiellä olevan kosteuden ei pitäisi varmasti jäätyä", "unit": "°C", "icon": "mdi:thermometer-alert"},
    "TURVALLISUUSLÄMPÖ_2": {"name": "Turvallisuuslämpö 2", "unit": "°C", "icon": "mdi:thermometer-alert"},
    "TURVALLISUUSLÄMPÖ_3": {"name": "Lämpötila, jonka yläpuolella tiellä olevan kosteuden ei pitäisi varmasti jäätyä", "unit": "°C", "icon": "mdi:thermometer-alert"},
    "TURVALLISUUSLÄMPÖ_4": {"name": "Lämpötila, jonka yläpuolella tiellä olevan kosteuden ei pitäisi varmasti jäätyä", "unit": "°C", "icon": "mdi:thermometer-alert"},
    
    # === WARNING AND ALERT SENSORS ===
    "VAROITUS_1": {"name": "Varoitustaso 1", "icon": "mdi:alert"},
    "VAROITUS_2": {"name": "Varoitustaso 2", "icon": "mdi:alert"},
    "VAROITUS_3": {"name": "Tiesääaseman päättelemä varoitustaso 3. anturilta", "icon": "mdi:alert"},
    "VAROITUS_4": {"name": "Tiesääaseman päättelemä varoitustaso 4. anturilta", "icon": "mdi:alert"},
    "OPTISEN_ANTURIN_VAROITUS1": {"name": "Optisen DSC-kelianturin 1 päättelemä varoitustaso", "icon": "mdi:alert"},
    "OPTISEN_ANTURIN_VAROITUS2": {"name": "Optisen anturin varoitus 2", "icon": "mdi:alert-circle-outline"},
    "OPTISEN_ANTURIN_KELI1": {"name": "Optisen DSC-kelianturin 1 päättelemä keliluokka", "icon": "mdi:road"},
    "OPTISEN_ANTURIN_KELI2": {"name": "Optisen anturin keli 2", "icon": "mdi:road"},
    
    # === ELECTRICAL AND TECHNICAL SENSORS ===
    "JOHTAVUUS_1": {"name": "Johtavuus 1", "unit": "V", "icon": "mdi:flash"},
    "JOHTAVUUS_2": {"name": "Johtavuus 2", "unit": "V", "icon": "mdi:flash"},
    "JOHTAVUUS_3": {"name": "Johtavuus tienpinta-anturilta 3", "unit": "V", "icon": "mdi:flash"},
    "JOHTAVUUS_4": {"name": "Johtavuus tienpinta-anturilta 4", "unit": "V", "icon": "mdi:flash"},
    "PINTASIGNAALI_1": {"name": "Pintasignaali 1", "unit": "V", "icon": "mdi:flash"},
    "PINTASIGNAALI_2": {"name": "Pintasignaali 2", "unit": "V", "icon": "mdi:flash"},
    "PINTASIGNAALI_3": {"name": "Pintasignaali tienpinta-anturilta 3", "unit": "V", "icon": "mdi:flash"},
    "PINTASIGNAALI_4": {"name": "Pintasignaali tienpinta-anturilta 4", "unit": "V", "icon": "mdi:flash"},
    "JÄÄTAAJUUS_1": {"name": "Jäätaajuus 1", "unit": "Hz", "icon": "mdi:snowflake-variant"},
    "JÄÄTAAJUUS_2": {"name": "Jäätaajuus 2", "unit": "Hz", "icon": "mdi:snowflake-variant"},
    "JÄÄTAAJUUS_3": {"name": "Jäätaajuus tienpinta-anturilta 3", "unit": "Hz", "icon": "mdi:snowflake-variant"},
    "JÄÄTAAJUUS_4": {"name": "Jäätaajuus tienpinta-anturilta 4", "unit": "Hz", "icon": "mdi:snowflake-variant"},
    
    # === FIBER OPTIC SENSORS ===
    "KUITUVASTE_PIENI_1": {"name": "Pienemmän kuidun vaste, tieanturi 1", "icon": "mdi:chart-bar"},
    "KUITUVASTE_PIENI_2": {"name": "Kuituvaste pieni 2", "icon": "mdi:chart-bar"},
    "KUITUVASTE_PIENI_3": {"name": "Pienemmän kuidun vaste, tieanturi 3", "icon": "mdi:chart-bar"},
    "KUITUVASTE_PIENI_4": {"name": "Pienemmän kuidun vaste, tieanturi 4", "icon": "mdi:chart-bar"},
    "KUITUVASTE_SUURI_1": {"name": "Suuremman kuidun vaste, tieanturi 1", "icon": "mdi:chart-bar"},
    "KUITUVASTE_SUURI_2": {"name": "Kuituvaste suuri 2", "icon": "mdi:chart-bar"},
    "KUITUVASTE_SUURI_3": {"name": "Suuremman kuidun vaste, tieanturi 3", "icon": "mdi:chart-bar"},
    "KUITUVASTE_SUURI_4": {"name": "Suuremman kuidun vaste, tieanturi 4", "icon": "mdi:chart-bar"},
    
    # === SYSTEM STATUS AND DIAGNOSTIC SENSORS ===
    "ASEMAN_STATUS_1": {"name": "Aseman status 1", "icon": "mdi:alert-circle-outline"},
    "ASEMAN_STATUS_2": {"name": "Aseman status 2", "icon": "mdi:alert-circle-outline"},
    "ASEMAN_STATUS_OPT1": {"name": "Status1 DSC-anturilta: hälytys, keli", "icon": "mdi:alert-circle-outline"},
    "ASEMAN_STATUS_OPT2": {"name": "Aseman status OPT2", "icon": "mdi:alert-circle-outline"},
    "ANTURIVIKA": {"name": "Onko antureissa vikaa?", "icon": "mdi:alert-circle-outline"},
    
    # === PWD (Present Weather Detector) SENSORS ===
    "PWD_STATUS": {"name": "PWD status", "icon": "mdi:alert-circle-outline"},
    "PWD_TILA": {"name": "PWD tila", "icon": "mdi:alert-circle-outline"},
    "PWD_NÄK_TILA": {"name": "PWD näkyvyystila", "icon": "mdi:alert-circle-outline"},
    "PWD_LÄHETTIMEN_TAKAISINSIRONNAN_MUUTOS": {"name": "PWD takaisinsironnan muutos", "icon": "mdi:signal"},
    "PWD_VASTAANOTTIMEN_TAKAISINSIRONNAN_MUUTOS": {"name": "PWD:n likaisuusarvoja", "unit": "Hz", "icon": "mdi:signal"},
    
    # === DSC (Dynamic Surface Condition) SENSORS ===
    "DSC_VASTAANOTTIMEN_PUHTAUS1": {"name": "DSC-anturin status, ykkösten arvojen kertoma tilatieto", "icon": "mdi:alert-circle-outline"},
    "DSC_VASTAANOTTIMEN_PUHTAUS2": {"name": "DSC vastaanottimen puhtaus 2", "icon": "mdi:alert-circle-outline"},
    "DSC_STAT1": {"name": "DSC-anturin status, kymppiarvojen kertoma tilatieto", "icon": "mdi:alert-circle-outline"},
    "DSC_STAT2": {"name": "DSC status 2", "icon": "mdi:alert-circle-outline"},
    
    # === WEATHER FORECAST SENSORS ===
    # Wind Forecast
    "TUULEN_SUUNTA_ENNUSTE": {"name": "Ennustettu tuulensuunta", "unit": "°", "icon": "mdi:compass-outline"},
    "TUULEN_NOPEUS_ENNUSTE": {"name": "Ennustettu tuulen nopeus", "unit": "m/s", "icon": "mdi:weather-windy"},
    
    # General Weather Forecast
    "PILVISYYS_ENNUSTE": {"name": "Ennustettu pilvisyys taivaankannen kahdeksasosina", "unit": "1/8", "icon": "mdi:weather-cloudy"},
    "SATEEN_OLOMUOTO_ENNUSTE": {"name": "Ennustettu sateen olomuoto", "icon": "mdi:weather-pouring"},
    "SATEEN_INTENSITEETTI_ENNUSTE": {"name": "Ennustettu sateen intensiteetti vetenä", "unit": "mm/h", "icon": "mdi:weather-pouring"},
    "SATEEN_ESTOD_ENNUSTE": {"name": "Ennustettu sateen todennäköisyys", "unit": "%", "icon": "mdi:weather-pouring"},
    "SADEMÄÄRÄ_1H_ENNUSTE": {"name": "Ennustettu edellisen 1 tunnin sademäärä millimetreinä", "unit": "mm", "icon": "mdi:weather-rainy"},
    
    # Temperature Forecast
    "ILMAN_LÄMPÖTILA_ENNUSTE": {"name": "Ennustettu ilman lämpötila", "unit": "°C", "icon": "mdi:thermometer"},
    "TIEN_LÄMPÖTILA_ENNUSTE": {"name": "Ennustettu tien lämpötila", "unit": "°C", "icon": "mdi:road-variant"},
    "KASTEP_LÄMPÖTILA_ENNUSTE": {"name": "Ennustettu kastepistelämpötila", "unit": "°C", "icon": "mdi:thermometer-water"},
    "KASTEPISTE_ERO_TIE_ENNUSTE": {"name": "Ennustettu tienpinnan- ja kastepistelämpötilan välinen ero", "unit": "°C", "icon": "mdi:thermometer-water"},
}
