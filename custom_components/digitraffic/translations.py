"""Value translations for Digitraffic sensors.

This module contains mappings from numeric sensor codes to human-readable descriptions.
Users can extend these mappings by adding new entries to SENSOR_VALUE_TRANSLATIONS.
"""

from typing import Any


# WMO Code Table 4680 - Present Weather (Automatic Weather Station)
# Source: https://codes.wmo.int/306/4680
WMO_4680_PRESENT_WEATHER = {
    0: "No significant weather",
    1: "Clouds dissolving",
    2: "State of sky unchanged",
    3: "Clouds forming or developing",
    4: "Visibility reduced by smoke or ash",
    5: "Haze",
    10: "Mist",
    11: "Patches of shallow fog or ice fog",
    12: "More or less continuous shallow fog or ice fog",
    18: "Squalls",
    20: "Fog or ice fog",
    21: "Precipitation",
    22: "Drizzle (not freezing) or snow grains",
    23: "Rain (not freezing)",
    24: "Snow",
    25: "Freezing drizzle or freezing rain",
    26: "Thunderstorm (with or without precipitation)",
    27: "Blowing or drifting snow or sand",
    28: "Blowing or drifting snow or sand, visibility >= 1km",
    29: "Thunderstorm",
    30: "Fog",
    31: "Fog in patches",
    32: "Fog, sky visible, thinning",
    33: "Fog, sky not visible, no change",
    34: "Fog, sky visible, no change",
    35: "Fog, sky not visible, becoming thicker",
    40: "Precipitation",
    41: "Precipitation, slight or moderate",
    42: "Precipitation, heavy",
    43: "Liquid precipitation, slight or moderate",
    44: "Liquid precipitation, heavy",
    45: "Solid precipitation, slight or moderate",
    46: "Solid precipitation, heavy",
    47: "Freezing precipitation, slight or moderate",
    48: "Freezing precipitation, heavy",
    50: "Drizzle, slight",
    51: "Drizzle, slight continuous",
    52: "Drizzle, moderate continuous",
    53: "Drizzle, heavy continuous",
    54: "Drizzle, slight freezing",
    55: "Drizzle, moderate freezing",
    56: "Drizzle, heavy freezing",
    57: "Drizzle and rain, slight",
    58: "Drizzle and rain, moderate or heavy",
    60: "Rain, slight",
    61: "Rain, slight continuous",
    62: "Rain, moderate continuous",
    63: "Rain, heavy continuous",
    64: "Rain, slight freezing",
    65: "Rain, moderate freezing",
    66: "Rain, heavy freezing",
    67: "Mixed rain and snow, slight",
    68: "Mixed rain and snow, moderate or heavy",
    70: "Snow, slight",
    71: "Snow, slight continuous",
    72: "Snow, moderate continuous",
    73: "Snow, heavy continuous",
    74: "Ice pellets, slight",
    75: "Ice pellets, moderate",
    76: "Ice pellets, heavy",
    77: "Snow grains",
    78: "Ice crystals",
    80: "Rain shower, slight",
    81: "Rain shower, moderate or heavy",
    82: "Rain shower, violent",
    83: "Mixed rain and snow shower, slight",
    84: "Mixed rain and snow shower, moderate or heavy",
    85: "Snow shower, slight",
    86: "Snow shower, moderate or heavy",
    87: "Snow pellet or small hail shower, slight",
    88: "Snow pellet or small hail shower, moderate or heavy",
    89: "Hail",
    90: "Thunderstorm, slight or moderate",
    91: "Thunderstorm with slight rain or snow",
    92: "Thunderstorm with moderate or heavy rain or snow",
    93: "Thunderstorm, slight or moderate with hail",
    94: "Thunderstorm, heavy with hail",
    95: "Thunderstorm, slight or moderate",
    96: "Thunderstorm, slight or moderate with hail",
    99: "Thunderstorm, heavy with hail",
}


# Main translation dictionary
# Add or modify entries here to translate sensor values
SENSOR_VALUE_TRANSLATIONS = {
    # WMO Weather Codes
    "VALLITSEVA_SÄÄ": WMO_4680_PRESENT_WEATHER,

    # Precipitation Type (Vaisala PWD, from API sensor ID 25)
    # Source: /api/weather/v1/sensors sensorValueDescriptions
    "SATEEN_OLOMUOTO_PWDXX": {
        7: "Dry weather",        # Pouta
        8: "Very light rain",    # Hyvin heikko sade, olomuotoa ei voida päätellä
        9: "Drizzle",            # Tihku
        10: "Rain",              # Vesisade
        11: "Snowfall",          # Lumisade
        12: "Wet sleet",         # Märkä räntä
        13: "Sleet",             # Räntä
        14: "Hails",             # Rakeita
        15: "Ice crystals",      # Jääkiteitä
        16: "Snow grains",       # Lumijyväsiä
        17: "Graupel",           # Lumirakeita
        18: "Freezing drizzle",  # Jäätävä tihku
        19: "Freezing rain",     # Jäätävä sade
    },

    # Precipitation State
    "SADE_TILA": {
        0: "No rain",
        1: "Rain detected",
    },

    # Precipitation indicator (from API sensor ID 22)
    # Source: /api/weather/v1/sensors sensorValueDescriptions
    "SADE": {
        0: "Dry weather",         # Pouta
        1: "Weak",                # Heikko
        2: "Moderate",            # Kohtalainen
        3: "Abundant",            # Runsas
        4: "Light snow/sleet",    # Heikko lumi/räntä
        5: "Moderate snow/sleet", # Kohtalainen lumi/räntä
        6: "Abundant snow/sleet", # Runsas lumi/räntä
    },

    # Road Condition Class (Keliluokka, from API sensors 27-28, 105, 115)
    # Source: /api/weather/v1/sensors sensorValueDescriptions
    "KELI_1": {
        0: "Sensor fault",         # Anturissa on vikaa
        1: "Dry",                  # Kuiva
        2: "Moist",                # Kostea
        3: "Wet",                  # Märkä
        4: "Wet and salty",        # Märkä ja suolattu
        5: "Frost",                # Kuura
        6: "Snow",                 # Lumi
        7: "Ice",                  # Jää
        8: "Probably moist/salty", # Todennäköisesti kostea ja suolainen
        9: "Slushy",               # Sohjoinen
    },
    "KELI_2": {
        0: "Sensor fault",         # Anturissa on vikaa
        1: "Dry",                  # Kuiva
        2: "Moist",                # Kostea
        3: "Wet",                  # Märkä
        4: "Wet and salty",        # Märkä ja suolattu
        5: "Frost",                # Kuura
        6: "Snow",                 # Lumi
        7: "Ice",                  # Jää
        8: "Probably moist/salty", # Todennäköisesti kostea ja suolainen
        9: "Slushy",               # Sohjoinen
    },
    "KELI_3": {
        0: "Sensor fault",         # Anturissa on vikaa
        1: "Dry",                  # Kuiva
        2: "Moist",                # Kostea
        3: "Wet",                  # Märkä
        4: "Wet and salty",        # Märkä ja suolattu
        5: "Frost",                # Kuura
        6: "Snow",                 # Lumi
        7: "Ice",                  # Jää
        8: "Probably moist/salty", # Todennäköisesti kostea ja suolainen
        9: "Slushy",               # Sohjoinen
    },
    "KELI_4": {
        0: "Sensor fault",         # Anturissa on vikaa
        1: "Dry",                  # Kuiva
        2: "Moist",                # Kostea
        3: "Wet",                  # Märkä
        4: "Wet and salty",        # Märkä ja suolattu
        5: "Frost",                # Kuura
        6: "Snow",                 # Lumi
        7: "Ice",                  # Jää
        8: "Probably moist/salty", # Todennäköisesti kostea ja suolainen
        9: "Slushy",               # Sohjoinen
    },

    # Road Surface State (Tienpinnan tila)
    # Note: Example mapping - verify with actual sensor data
    "TIENPINNAN_TILA_1": {
        0: "Dry",
        1: "Moist",
        2: "Wet",
        3: "Slush",
        4: "Frost",
        5: "Ice",
    },
    "TIENPINNAN_TILA_2": {
        0: "Dry",
        1: "Moist",
        2: "Wet",
        3: "Slush",
        4: "Frost",
        5: "Ice",
    },
    "TIENPINNAN_TILA_3": {
        0: "Dry",
        1: "Moist",
        2: "Wet",
        3: "Slush",
        4: "Frost",
        5: "Ice",
    },
    "TIENPINNAN_TILA_4": {
        0: "Dry",
        1: "Moist",
        2: "Wet",
        3: "Slush",
        4: "Frost",
        5: "Ice",
    },
    "TIENPINNAN_TILA_OPT1": {
        0: "Dry",
        1: "Moist",
        2: "Wet",
        3: "Slush",
        4: "Frost",
        5: "Ice",
    },
    "TIENPINNAN_TILA_OPT2": {
        0: "Dry",
        1: "Moist",
        2: "Wet",
        3: "Slush",
        4: "Frost",
        5: "Ice",
    },

    # Binary sensors
    "VALOISAA": {
        0: "Dark",
        1: "Light",
    },
    "AURINKOUP": {
        0: "Sun down",
        1: "Sun up",
    },

    # Warning levels (from API sensors 29-30, 106, 116, 175, 185)
    # Source: /api/weather/v1/sensors sensorValueDescriptions
    "VAROITUS_1": {
        0: "OK",
        1: "Beware",  # Varo
        2: "Alarm",   # Häly
        3: "Frost",   # Kuura
        4: "Rain",    # Sade
    },
    "VAROITUS_2": {
        0: "OK",
        1: "Beware",  # Varo
        2: "Alarm",   # Häly
        3: "Frost",   # Kuura
        4: "Rain",    # Sade
    },
    "VAROITUS_3": {
        0: "OK",
        1: "Beware",  # Varo
        2: "Alarm",   # Häly
        3: "Frost",   # Kuura
        4: "Rain",    # Sade
    },
    "VAROITUS_4": {
        0: "OK",
        1: "Beware",  # Varo
        2: "Alarm",   # Häly
        3: "Frost",   # Kuura
        4: "Rain",    # Sade
    },

    # PWD (Present Weather Detector) sensors
    # Note: Placeholder - user should fill in based on observations
    "PWD_STATUS": {},
    "PWD_TILA": {},
    "PWD_NÄK_TILA": {},
    "PWD_TAKAISINSIRONNAN_MUUTOS": {},

    # Station status sensors
    # Note: Placeholder - user should fill in based on observations
    "ASEMAN_STATUS_1": {},
    "ASEMAN_STATUS_2": {},
    "ASEMAN_STATUS_OPT2": {},

    # DSC (Road sensor) status
    # Note: Placeholder - user should fill in based on observations
    "DSC_STAT1": {},
    "DSC_STAT2": {},
    "DSC_VASTAANOTTIMEN_PUHTAUS1": {},
    "DSC_VASTAANOTTIMEN_PUHTAUS2": {},

    # Optical sensor readings
    # Note: Placeholder - user should fill in based on observations
    "OPTISEN_ANTURIN_KELI1": {},
    "OPTISEN_ANTURIN_KELI2": {},
    "OPTISEN_ANTURIN_VAROITUS1": {},
    "OPTISEN_ANTURIN_VAROITUS2": {},

    # Fiber optic sensor responses
    # Note: Placeholder - user should fill in based on observations
    "KUITUVASTE_PIENI_1": {},
    "KUITUVASTE_PIENI_2": {},
    "KUITUVASTE_SUURI_1": {},
    "KUITUVASTE_SUURI_2": {},
    "PIENEMMÄN_KUIDUN_VASTE_1": {},
    "SUUREMMAN_KUIDUN_VASTE_1": {},
}


def translate_sensor_value(sensor_key: str, value: Any) -> Any:
    """Translate a sensor value to human-readable format.

    Args:
        sensor_key: The sensor identifier (e.g., "VALLITSEVA_SÄÄ")
        value: The raw value from the API

    Returns:
        Translated string if mapping exists, otherwise original value.
        For unknown codes with a mapping dictionary, returns "Unknown (X)" format.
    """
    # Return None if value is None
    if value is None:
        return None

    # Check if sensor has translation mapping
    if sensor_key not in SENSOR_VALUE_TRANSLATIONS:
        return value

    mapping = SENSOR_VALUE_TRANSLATIONS[sensor_key]

    # If mapping dictionary is empty (placeholder), return original value
    if not mapping:
        return value

    # Try to convert value to numeric for lookup
    try:
        # Try integer conversion first
        numeric_value = int(float(value))
        translated = mapping.get(numeric_value)

        if translated is not None:
            return translated
        else:
            # Code exists but not in mapping - show as "Unknown (X)"
            return f"Unknown ({numeric_value})"
    except (ValueError, TypeError):
        # Value is not numeric, return as-is
        return value
