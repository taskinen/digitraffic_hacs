# CLAUDE.md - Digitraffic Home Assistant Integration

**Last Updated:** 2026-01-03 (GitHub Actions CI/CD implementation)

---
## ⚠️ CLAUDE CODE: UPDATE CHECKLIST - READ THIS FIRST!

**Before completing ANY task, check if you modified:**
- [ ] Any .py files (especially `__init__.py`, `config_flow.py`, `const.py`, `sensor.py`, `translations.py`)
- [ ] Constants, API endpoints, or headers
- [ ] API request patterns or error handling
- [ ] Sensor definitions or translation mappings
- [ ] Data flow or architecture

**If YES to ANY:** You MUST update this CLAUDE.md file NOW:
1. Update "Last Updated" date at top
2. Add entry to Changelog section (at bottom)
3. Update relevant documentation sections

---

> **IMPORTANT:** This file must be kept up-to-date whenever significant changes are made to the codebase. Update this file BEFORE committing changes that affect architecture, add new features, modify data flows, or change development patterns.

## Project Overview

This is a Home Assistant custom component that integrates weather data from Fintraffic's (Finnish Transport Infrastructure Agency) Digitraffic API into Home Assistant. It provides real-time road weather station data including temperature, precipitation, road surface conditions, visibility, and more.

### Key Information
- **Type:** Home Assistant Custom Component (HACS)
- **Language:** Python 3
- **Integration Class:** Cloud Polling
- **Update Interval:** 5 minutes (configurable in `const.py`)
- **API:** Fintraffic Digitraffic REST API (public, no authentication required)
- **Repository:** https://github.com/taskinen/digitraffic_hacs
- **Version:** 0.1.0

## Architecture Overview

### Data Flow

```
Digitraffic API
    ↓ (HTTP GET every 5 minutes)
DigitrafficDataUpdateCoordinator (_async_update_data)
    ↓ (parses sensorValues array into dict)
coordinator.data = {"SENSOR_KEY": value, "measuredTime": "...", ...}
    ↓ (Home Assistant polls coordinator)
DigitrafficWeatherSensor (native_value property)
    ↓ (checks if sensor needs translation)
translate_sensor_value() [if translate=True]
    ↓ (looks up code in SENSOR_VALUE_TRANSLATIONS)
Displayed in Home Assistant UI
```

### Component Structure

```
custom_components/digitraffic/
├── __init__.py                 # Integration setup & data coordinator
├── manifest.json               # Component metadata & dependencies
├── config_flow.py              # UI configuration flow
├── const.py                    # Constants, API endpoints, sensor definitions
├── sensor.py                   # Sensor platform implementation
├── translations.py             # Sensor value translation mappings
└── brand/                      # Logo and icon assets
    ├── icon.png
    └── logo.png

.github/workflows/
├── ci.yml                      # CI syntax validation workflow
└── release.yml                 # Release automation workflow
```

## File Purposes and Key Components

### `__init__.py` - Integration Core

**Purpose:** Entry point for the integration. Manages setup, teardown, and data fetching.

**Key Classes:**
- `DigitrafficDataUpdateCoordinator`: Inherits from `DataUpdateCoordinator`
  - Fetches data from API every 5 minutes
  - Processes JSON response into a flat dictionary
  - Handles errors and timeouts

**API Data Structure (Response):**
```json
{
  "stationId": 12345,
  "stationName": "Vantaa",
  "measuredTime": "2026-01-02T12:00:00Z",
  "sensorValues": [
    {"name": "ILMA", "value": -5.2},
    {"name": "KELI_1", "value": 2},
    {"name": "VALLITSEVA_SÄÄ", "value": 63}
  ]
}
```

**Processed Data (coordinator.data):**
```python
{
    "ILMA": -5.2,
    "KELI_1": 2,
    "VALLITSEVA_SÄÄ": 63,
    "measuredTime": "2026-01-02T12:00:00Z",
    "stationName": "Vantaa"
}
```

**Important Methods:**
- `async_setup_entry()`: Creates coordinator and forwards to platforms
- `async_unload_entry()`: Cleanup on integration removal
- `_async_update_data()`: Fetches and processes API data

### `manifest.json` - Component Metadata

Defines integration properties:
- Domain: `digitraffic`
- Config flow enabled
- IoT class: `cloud_polling`
- Dependency: `aiohttp` (HTTP client)
- Codeowner: @taskinen

### `config_flow.py` - User Configuration

**Purpose:** Handles integration setup via Home Assistant UI.

**Features:**
- Fetches list of all available weather stations from API
- Provides search functionality (by name or ID)
- Validates station ID exists before creating entry
- Prevents duplicate station configurations (uses unique_id)

**Key Functions:**
- `fetch_stations()`: Retrieves all stations from `/api/weather/v1/stations` (GeoJSON)
- `validate_station_id()`: Verifies station exists and is accessible
- `DigitrafficConfigFlow.async_step_user()`: User interaction flow with search

**API Endpoints Used:**
- List stations: `https://tie.digitraffic.fi/api/weather/v1/stations` (returns GeoJSON FeatureCollection)
- Validate station: `https://tie.digitraffic.fi/api/weather/v1/stations/{id}`
- Get station data: `https://tie.digitraffic.fi/api/weather/v1/stations/{id}/data`

### `const.py` - Constants and Sensor Definitions

**Purpose:** Central location for all constants, API endpoints, and sensor metadata.

**Key Constants:**
```python
DOMAIN = "digitraffic"
PLATFORMS = ["sensor"]
CONF_STATION_ID = "station_id"
UPDATE_INTERVAL_MINUTES = 5

# API Endpoints
API_ENDPOINT_STATIONS = "https://tie.digitraffic.fi/api/weather/v1/stations"
API_ENDPOINT_STATION_DATA = "https://tie.digitraffic.fi/api/weather/v1/stations/{}/data"

# API Headers
API_USER_AGENT = "Home Assistant github.com/taskinen/digitraffic_hacs"
```

**SENSOR_MAP Structure:**
Massive dictionary (200+ sensors) mapping sensor keys to metadata:
```python
SENSOR_MAP = {
    "ILMA": {
        "name": "Ilman lämpötila n. 4 metrin korkeudelta",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",  # Optional: HA device class
        "state_class": "measurement"     # Optional: HA state class
    },
    "KELI_1": {
        "name": "Keliluokka 1",
        "icon": "mdi:road",
        "translate": True  # NEW: Mark sensor for translation
    },
    # ... 200+ more sensors
}
```

**Sensor Categories:**
1. Air temperature (ILMA, ILMA_DERIVAATTA, etc.)
2. Road surface temperature (TIE_1, TIE_2, etc.)
3. Ground temperature (MAA_1, MAA_2, etc.)
4. Wind (KESKITUULI, MAKSIMITUULI, TUULENSUUNTA)
5. Precipitation (SADE, SADESUMMA, SATEEN_OLOMUOTO_PWDXX, etc.)
6. Visibility (NÄKYVYYS_KM, NÄKYVYYS_M)
7. Road conditions (KELI_1-4, TIENPINNAN_TILA_1-4)
8. PWD (Present Weather Detector) status
9. DSC (Dynamic Surface Condition) sensors
10. Forecasts (ILMAN_LÄMPÖTILA_ENNUSTE, etc.)

**Important:** Sensors with `"translate": True` flag will have their numeric values translated to human-readable text.

### `sensor.py` - Sensor Platform

**Purpose:** Creates and manages individual sensor entities.

**Setup Function (`async_setup_entry`):**
- Retrieves coordinator from hass.data
- Calls `coordinator.async_config_entry_first_refresh()` to ensure initial data is loaded
- **Dynamic sensor discovery:** Iterates through coordinator.data to discover available sensors
  - Creates sensors for ALL sensor keys returned by API (not just those in SENSOR_MAP)
  - Sensors not in SENSOR_MAP will use default formatting (key → "Key Name")
  - Excludes metadata keys: "measuredTime", "stationName"
- Uses `entry.title` (validated station name from config flow) for display
- Adds all sensor entities to Home Assistant with immediate update

**Key Classes:**

**`DigitrafficWeatherSensor`** - Main sensor entity class

**Initialization (`__init__`):**
- Extends `CoordinatorEntity` and `SensorEntity`
- Retrieves sensor config from `SENSOR_MAP` (uses empty dict if sensor not defined)
- Sets sensor name, unique_id, icon, unit, device_class
- **IMPORTANT:** If `translate=True`, sets `state_class=None` (categorical data, not measurements)
- Links sensor to device (weather station) via device_info

**Properties:**
- `native_value`: Returns sensor state
  - **If `translate=True`**: Calls `translate_sensor_value()` to convert numeric codes to text
  - **If `translate=False`**: Converts to float for numeric measurements
  - Returns `None` for invalid/non-numeric values

- `available`: Sensor is available if coordinator has data and sensor key exists

- `extra_state_attributes`: Additional sensor metadata
  - `measured_time`: Timestamp from API
  - `raw_value`: For translated sensors, preserves original numeric value

**Device Info:**
All sensors from the same station are grouped under a single device:
```python
{
    "identifiers": {(DOMAIN, station_id)},
    "name": station_name,  # From config entry title
    "manufacturer": "Fintraffic",
    "model": "Road Weather Station",
    "entry_type": "service",  # Indicates this is a service/cloud integration
}
```

### `translations.py` - Sensor Value Translation (NEW)

**Purpose:** Translates numeric sensor codes to human-readable descriptions.

**Added:** 2026-01-02

**Architecture:**
```python
SENSOR_VALUE_TRANSLATIONS = {
    "SENSOR_KEY": {
        numeric_code: "Human readable description",
        ...
    },
    ...
}

def translate_sensor_value(sensor_key: str, value: Any) -> Any:
    """Main translation function"""
```

**Translation Categories:**

1. **Complete Mappings (verified from API):**
   - `VALLITSEVA_SÄÄ`: WMO Code 4680 (0-99) - Present weather from automatic weather stations
     - Example: 63 → "Rain, heavy continuous"
     - Example: 71 → "Snow, slight continuous"
     - Source: https://codes.wmo.int/306/4680

   - `SADE`: Precipitation intensity (codes 0-6)
     - Source: API sensor ID 22
     - Example: 0 → "Dry weather", 3 → "Abundant", 6 → "Abundant snow/sleet"

   - `SATEEN_OLOMUOTO_PWDXX`: Precipitation type from PWD sensor (codes 7-19)
     - Source: API sensor ID 25
     - Example: 7 → "Dry weather", 10 → "Rain", 11 → "Snowfall", 19 → "Freezing rain"

   - `KELI_1/2/3/4`: Road condition class (codes 0-9)
     - Source: API sensors 27-28, 105, 115
     - Example: 0 → "Sensor fault", 1 → "Dry", 3 → "Wet", 7 → "Ice", 9 → "Slushy"

   - `VAROITUS_1/2/3/4`: Warning levels (codes 0-4)
     - Source: API sensors 29-30, 106, 116, 175, 185
     - Example: 0 → "OK", 1 → "Beware", 2 → "Alarm", 3 → "Frost"

   - `PWD_STATUS`: PWD sensor hardware status (codes 0-4)
     - Source: Vaisala PWD22 User Manual
     - Example: 0 → "OK", 1 → "Hardware error", 3 → "Backscatter alarm", 4 → "Backscatter warning"

   - `SADE_TILA`: Precipitation state (codes 7-19)
     - Source: User observation - uses same PWD precipitation type codes as SATEEN_OLOMUOTO_PWDXX
     - Example: 17 → "Graupel", 18 → "Freezing drizzle"
     - Note: API has empty sensorValueDescriptions, but observed values match PWD codes

2. **Complete Mappings (verified, simple binary):**
   - `VALOISAA`: Light level binary (0: Dark, 1: Light)
   - `AURINKOUP`: Sun position binary (0: Sun down, 1: Sun up)

3. **Example Mappings (not verified from API - user should verify):**
   - `TIENPINNAN_TILA_1-4/OPT1/OPT2`: Road surface state (0-5)
     - Example codes: 0: Dry, 1: Moist, 2: Wet, 3: Slush, 4: Frost, 5: Ice
     - Note: These codes are inferred but not verified from API data

4. **Placeholder Mappings (empty, user must fill):**
   - PWD state sensors: `PWD_TILA`, `PWD_NÄK_TILA`, `PWD_LÄHETTIMEN_TAKAISINSIRONNAN_MUUTOS`
   - Station status: `ASEMAN_STATUS_1`, `ASEMAN_STATUS_2`, `ASEMAN_STATUS_OPT1`, `ASEMAN_STATUS_OPT2`, `ANTURIVIKA`
   - DSC sensors: `DSC_STAT1`, `DSC_STAT2`, `DSC_VASTAANOTTIMEN_PUHTAUS1`, `DSC_VASTAANOTTIMEN_PUHTAUS2`
   - Optical sensors: `OPTISEN_ANTURIN_KELI1`, `OPTISEN_ANTURIN_KELI2`, `OPTISEN_ANTURIN_VAROITUS1`, `OPTISEN_ANTURIN_VAROITUS2`
   - Fiber sensors: All `KUITUVASTE_*` variants
   - Forecast: `SATEEN_OLOMUOTO_ENNUSTE`

   **Note:** These sensors have empty dictionaries as placeholders because the API does not provide `sensorValueDescriptions` for them and no manufacturer documentation could be found. Users should monitor actual sensor values and populate mappings based on observed codes and corresponding conditions.

**Translation Logic:**
```python
1. Check if sensor_key has a mapping in SENSOR_VALUE_TRANSLATIONS
2. If no mapping exists → return raw value
3. If mapping exists but is empty (placeholder) → return raw value
4. Try to convert value to int(float(value)) for lookup
5. If code found in mapping → return translated string
6. If code not found → return "Unknown (X)" where X is the code
7. If value is not numeric → return raw value
```

**Adding New Translations:**
To add or update translations, edit `translations.py`:
```python
# Find the sensor in SENSOR_VALUE_TRANSLATIONS
"SENSOR_KEY": {
    0: "Description for code 0",
    1: "Description for code 1",
    # Add more codes as you discover them
}
```

**Example Sensor Outputs:**

Before translation:
```
sensor.vantaa_sateen_olomuoto: "20"
sensor.vantaa_vallitseva_saa: "63"
sensor.vantaa_keli_1: "2"
```

After translation:
```
sensor.vantaa_sateen_olomuoto: "Rain"
sensor.vantaa_vallitseva_saa: "Rain, heavy continuous"
sensor.vantaa_keli_1: "Wet"
```

With raw values preserved in attributes:
```yaml
sensor.vantaa_sateen_olomuoto:
  state: "Rain"
  attributes:
    raw_value: 20
    measured_time: "2026-01-02T12:00:00Z"
```

## API Documentation

### Base URL
`https://tie.digitraffic.fi/api/weather/v1`

### Endpoints

**1. List All Stations**
```
GET /stations
Returns: GeoJSON FeatureCollection with all weather stations
```

Response structure:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {"type": "Point", "coordinates": [lon, lat]},
      "properties": {
        "id": 12345,
        "name": "Vantaa",
        "collectionStatus": "GATHERING",
        "state": "OK",
        "dataUpdatedTime": "2026-01-02T12:00:00Z"
      }
    }
  ]
}
```

**2. Get Station Info**
```
GET /stations/{id}
Returns: Single GeoJSON Feature with station metadata
```

**3. Get Station Data (Used by Integration)**
```
GET /stations/{id}/data
Returns: Latest sensor readings from the station
```

Response structure:
```json
{
  "id": 12345,
  "stationId": 12345,
  "stationName": "Vantaa",
  "measuredTime": "2026-01-02T12:00:00Z",
  "sensorValues": [
    {
      "id": 67890,
      "roadStationId": 12345,
      "name": "ILMA",
      "oldName": "ilman lämpötila",
      "shortName": "ilma",
      "value": -5.2,
      "unit": "°C",
      "timeWindowStart": "2026-01-02T11:55:00Z",
      "timeWindowEnd": "2026-01-02T12:00:00Z",
      "measuredTime": "2026-01-02T12:00:00Z"
    }
  ]
}
```

### API Characteristics
- **No Authentication Required:** Public API
- **User Identification:** All requests include `Digitraffic-User` header to identify the client
- **Rate Limiting:** Not officially documented, but use reasonable intervals (5 minutes default)
- **Timeout:** 10 seconds (configured in `__init__.py`)
- **Content-Type:** `application/json`
- **Compression:** Supports gzip encoding
- **Reliability:** Generally stable, but implement error handling for network issues

### API Error Handling
The coordinator handles:
- `aiohttp.ClientError`: Network/connection errors
- `asyncio.TimeoutError`: Request timeout (10s)
- `response.raise_for_status()`: HTTP error codes (404, 500, etc.)
- `UpdateFailed`: Raised to Home Assistant when data fetch fails

## Sensor Naming Conventions

### Sensor Keys (from API)
- ALL_CAPS_WITH_UNDERSCORES (e.g., `ILMA`, `TIE_1`, `KELI_2`)
- Numbers suffix variants (e.g., `TIE_1`, `TIE_2`, `TIE_3`, `TIE_4`)
- Some have special suffixes:
  - `_DERIVAATTA`: Rate of change (derivative)
  - `_ENNUSTE`: Forecast
  - `_OPT1`, `_OPT2`: Optical sensors
  - `_PWDXX`: Present Weather Detector

### Sensor Names (displayed in UI)
- Finnish language descriptions
- Stored in `SENSOR_MAP["name"]`
- Combined with station name: `"{station_name} {sensor_name}"`
- Example: "Vantaa Ilman lämpötila n. 4 metrin korkeudelta"

### Unique IDs
Format: `digitraffic_{station_id}_{sensor_key}`
Example: `digitraffic_12345_ILMA`

## Development Patterns and Best Practices

### Adding New Sensor Support

1. **Find the sensor key** from API response
2. **Add to `SENSOR_MAP` in `const.py`:**
   ```python
   "NEW_SENSOR_KEY": {
       "name": "Finnish description",
       "unit": "Unit (if applicable)",  # Optional
       "icon": "mdi:icon-name",
       "device_class": "temperature",   # Optional, if HA has matching class
       "state_class": "measurement",    # Optional: "measurement", "total", or None
       "translate": False  # Set to True if sensor returns codes that need translation
   }
   ```

3. **If sensor needs translation (returns numeric codes):**
   - Set `"translate": True` in SENSOR_MAP
   - Add mapping to `translations.py`:
     ```python
     "NEW_SENSOR_KEY": {
         0: "Description for code 0",
         1: "Description for code 1",
         # ...
     }
     ```

### Home Assistant Device Classes

Common device classes used:
- `temperature`: Temperature sensors (enables correct display)
- `pressure`: Atmospheric pressure
- `humidity`: Relative humidity
- `wind_speed`: Wind sensors
- `precipitation`: Rain/snow amount

Full list: https://developers.home-assistant.io/docs/core/entity/sensor/#available-device-classes

### State Classes

- `measurement`: Instantaneous values (temperature, wind speed, etc.)
- `total`: Cumulative values (rain sum, etc.)
- `total_increasing`: Monotonically increasing totals
- `None`: Categorical data (road conditions, weather descriptions) - **Required for translated sensors**

**IMPORTANT:** Sensors with `translate=True` MUST have `state_class=None` because translated text values are categorical, not numeric measurements.

### Error Handling Pattern

Always use this pattern for API calls:
```python
try:
    async with async_timeout.timeout(10):
        response = await session.get(
            url,
            headers={"Digitraffic-User": API_USER_AGENT}
        )
        response.raise_for_status()
        data = await response.json()
        # Process data
        return processed_data
except aiohttp.ClientError as err:
    _LOGGER.error("Error message: %s", err)
    raise UpdateFailed(f"Error: {err}") from err
except asyncio.TimeoutError as err:
    _LOGGER.error("Timeout message")
    raise UpdateFailed("Timeout") from err
except Exception as err:
    _LOGGER.exception("Unexpected error")
    raise UpdateFailed(f"Unexpected: {err}") from err
```

### Logging Levels

Use appropriate log levels:
- `_LOGGER.debug()`: Detailed information, API responses, validation details
- `_LOGGER.info()`: Important events, successful operations
- `_LOGGER.warning()`: Unexpected but handled situations
- `_LOGGER.error()`: Errors that affect functionality
- `_LOGGER.exception()`: Errors with full stack trace

## Common Tasks

### Update API Endpoint
1. Edit `const.py`: Update `API_ENDPOINT_*` constants
2. Test with a real station ID to verify response format
3. Update data parsing in `__init__.py` if response structure changed

### Change Update Interval
1. Edit `const.py`: Change `UPDATE_INTERVAL_MINUTES`
2. Restart Home Assistant or reload integration

### Add Support for New Weather Station Type
Currently supports road weather stations. To add marine or rail stations:
1. Create new constant for API endpoint
2. Might need separate sensor platform or entity types
3. Consider creating separate integration vs. expanding this one

### Debug API Issues

Enable debug logging in Home Assistant:
```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.digitraffic: debug
```

Check logs: Settings → System → Logs → Filter by "digitraffic"

### Test Translation Changes

1. Edit `translations.py` to add/modify mappings
2. Reload integration: Developer Tools → YAML → Reload "Template entities" or restart HA
3. Check sensor states update to show new translations
4. Verify `raw_value` attribute still shows original numeric code

## CI/CD and Release Management

### GitHub Actions Workflows

The repository uses GitHub Actions for automated testing and release management.

**Workflow Files:**
- `.github/workflows/ci.yml` - Continuous Integration
- `.github/workflows/release.yml` - Release Management

### CI Workflow (Automatic)

**Triggers:** Every push and pull request to any branch

**What it does:**
- Validates Python syntax for all `.py` files using `python -m py_compile`
- Validates `manifest.json` as valid JSON
- Validates `hacs.json` as valid JSON
- Runs in ~10-15 seconds

**Purpose:** Catch syntax errors early before they're merged. When branch protection is enabled, this prevents broken code from being committed.

**Viewing Results:**
- Go to the "Actions" tab in GitHub
- Click on the latest workflow run
- View the output of each validation step

### Release Workflow (Manual)

**Trigger:** Manual dispatch only (Actions → Release → Run workflow)

**What it does:**
1. Determines the next version number (auto-increment or manual)
2. Updates `manifest.json` with the new version
3. Generates release notes from commit history
4. Commits the manifest.json change
5. Creates a git tag (format: `vX.Y.Z`)
6. Creates a GitHub release
7. HACS users see the new version available

**Version Management:**

The workflow uses **semantic versioning** (X.Y.Z format) and stores versions as git tags:

- **Source of truth:** Git tags matching `v*.*.*` pattern
- **Default behavior:** Auto-increment minor version (1.0.0 → 1.1.0 → 1.2.0)
- **Manual override:** You can specify any version number
- **First release:** Will be `v1.0.0` (existing `0.0.1` tag is ignored)

**Workflow Inputs:**

1. **Version** (optional):
   - Leave empty for auto-increment
   - Or enter version number (e.g., `2.0.0` or `v2.0.0`)
   - Format must be `X.Y.Z` (three numbers separated by dots)

2. **Release Notes** (optional):
   - Leave empty for auto-generated from commits since last release
   - Or enter custom release notes

3. **Prerelease** (checkbox):
   - Check to mark as pre-release
   - HACS won't auto-install pre-releases

### Creating a Release

**Step-by-step:**

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Click "Release" in the left sidebar
4. Click "Run workflow" button (top right)
5. Fill in the inputs (or leave empty for auto-increment):
   - Version: [empty] or `1.0.0`
   - Release notes: [empty] or custom text
   - Prerelease: unchecked (unless testing)
6. Click "Run workflow"
7. Wait ~30 seconds for workflow to complete
8. Verify the release at: `https://github.com/taskinen/digitraffic_hacs/releases`

**What happens:**

- Tag created: `vX.Y.Z`
- GitHub release created with release notes
- `manifest.json` updated and committed
- HACS shows the new version to users

### Release Examples

**Example 1: First Release (Auto-increment)**
```
Inputs:
  Version: [empty]
  Release notes: [empty]
  Prerelease: unchecked

Result: v1.0.0 created
Release notes: Auto-generated from all commits
```

**Example 2: Next Release (Auto-increment)**
```
Current version: v1.0.0

Inputs:
  Version: [empty]
  Release notes: [empty]
  Prerelease: unchecked

Result: v1.1.0 created
Release notes: Commits since v1.0.0
```

**Example 3: Major Release (Manual)**
```
Current version: v1.5.0

Inputs:
  Version: 2.0.0
  Release notes: "Major update with breaking changes"
  Prerelease: unchecked

Result: v2.0.0 created
Next auto-increment will be v2.1.0
```

**Example 4: Pre-release**
```
Inputs:
  Version: 1.2.0-beta
  Release notes: [empty]
  Prerelease: checked

Result: v1.2.0-beta created (marked as pre-release)
HACS won't auto-install this version
```

### Version History Tracking

To see all releases:
```bash
# List all version tags
git tag -l 'v*.*.*'

# View specific release
git show v1.0.0

# Compare releases
git diff v1.0.0...v1.1.0
```

### Troubleshooting Releases

**Error: "Tag already exists"**
- You're trying to create a version that already exists
- Check existing tags: `git tag -l 'v*.*.*'`
- Use a different version number

**Error: "Invalid version format"**
- Version must be `X.Y.Z` format (three numbers)
- Examples: `1.0.0`, `2.5.3` (not `1.0`, `v1.0.0`, `1.0.0-rc1`)
- Pre-release versions like `1.0.0-beta` are allowed

**Workflow failed during commit**
- Check GitHub Actions logs for details
- May need to fix merge conflicts manually
- Tag and release will NOT be created if commit fails

**Want to undo a release:**
1. Delete the GitHub release (go to Releases → Delete)
2. Delete the tag:
   ```bash
   git tag -d vX.Y.Z
   git push origin :refs/tags/vX.Y.Z
   ```
3. Revert the manifest.json commit:
   ```bash
   git revert <commit-hash>
   git push origin main
   ```

### HACS Integration

**How HACS uses releases:**
- HACS reads GitHub releases (not tags alone)
- Version displayed in HACS UI comes from tag name (e.g., `v1.0.0` shows as `1.0.0`)
- Users can see available versions and release notes
- Updates notify users when new versions are available

**What users see:**
```
Digitraffic
Current version: 1.0.0
Available version: 1.1.0

Release notes:
- Fix temperature sensor translation
- Add support for new weather codes
- Update API headers
```

**Without releases (before CI/CD):**
```
Digitraffic
Current version: abc1234 (commit hash)
Available version: def5678 (commit hash)
```

## Known Issues and Limitations

### Current Known Issues
- **Translation mappings incomplete:** Many sensors have empty placeholder dictionaries in `translations.py`. User must observe sensor values and fill in mappings based on real-world correlation with weather conditions.
- **No multi-language support:** All sensor names and translations are in Finnish. Could add i18n support in future.
- **No historical data:** Only fetches latest readings, no history or graphs beyond HA's built-in recorder.

### Limitations
- **Public API only:** No authentication = can't access restricted data if it exists
- **5-minute updates:** Faster updates would hit API more frequently (not recommended)
- **Finnish stations only:** Digitraffic is Finland-specific
- **Read-only:** No ability to control or configure stations via API

## Testing

### Manual Testing Checklist
1. Install integration via config flow
2. Verify station search works
3. Check that sensors are created (should be 50-100+ sensors depending on station)
4. Verify sensor values update every 5 minutes
5. Check translated sensors show text, not numbers
6. Verify raw_value attribute exists on translated sensors
7. Test removing and re-adding integration
8. Verify unique_id prevents duplicate station setup

### Test Station IDs
Some known station IDs for testing:
- Check `/api/weather/v1/stations` for current list
- Look for stations with `"state": "OK"` and `"collectionStatus": "GATHERING"`

### Validation
```bash
# Syntax check all Python files
python3 -m py_compile custom_components/digitraffic/*.py

# Check manifest
python3 -c "import json; json.load(open('custom_components/digitraffic/manifest.json'))"
```

## Future Enhancement Ideas

### Potential Features
1. **Translation improvements:**
   - Complete all sensor code mappings
   - Add English translations
   - User-customizable mappings via config flow

2. **Additional data:**
   - Road weather forecasts (already in API, not fully utilized)
   - Weather warnings and alerts
   - Road condition cameras (separate API endpoint)

3. **Better organization:**
   - Sensor grouping/categorization
   - Hide sensors user doesn't want
   - Custom sensor names via UI

4. **Automation helpers:**
   - Binary sensors for road conditions (is_icy, is_snowing, etc.)
   - Template sensors for common use cases
   - Blueprints for common automations

5. **Performance:**
   - Selective sensor updates (not all sensors every time)
   - Conditional polling based on time of day
   - Caching strategy for rarely-changing metadata

## Resources and References

### Official Documentation
- **Digitraffic Home:** https://www.digitraffic.fi/en/
- **Road Traffic API Docs:** https://www.digitraffic.fi/en/road-traffic/
- **API Swagger UI:** https://tie.digitraffic.fi/swagger/

### External References
- **WMO Code 4680:** https://codes.wmo.int/306/4680 (Present weather codes)
- **WMO Code Descriptions:** https://artefacts.ceda.ac.uk/badc_datadocs/surface/code.html
- **Vaisala PWD Sensors:** https://www.vaisala.com/en/products/weather-environmental-sensors/present-weather-detectors-visbility-sensors-pwd-series

### Home Assistant Development
- **Integration Development:** https://developers.home-assistant.io/docs/creating_integration_manifest
- **Sensor Platform:** https://developers.home-assistant.io/docs/core/entity/sensor
- **Config Flow:** https://developers.home-assistant.io/docs/config_entries_config_flow_handler
- **Data Update Coordinator:** https://developers.home-assistant.io/docs/integration_fetching_data

### GitHub Repository
- **Main Repo:** https://github.com/taskinen/digitraffic_hacs
- **Issues:** https://github.com/taskinen/digitraffic_hacs/issues

## Changelog

### 2026-01-03 - GitHub Actions CI/CD Implementation

**Added:**
- `.github/workflows/ci.yml`: Continuous Integration workflow
  - Automatic Python syntax validation on every push and pull request
  - Validates all `.py` files using `python -m py_compile`
  - Validates `manifest.json` and `hacs.json` as valid JSON
  - Runs in ~10-15 seconds

- `.github/workflows/release.yml`: Release automation workflow
  - Manual trigger for creating releases
  - Auto-increment minor version by default (1.0.0 → 1.1.0 → 1.2.0)
  - Manual version override option
  - Auto-generated release notes from commit history
  - Updates `manifest.json` version field automatically
  - Creates GitHub releases for HACS compatibility
  - Workflow inputs: version (optional), release_notes (optional), prerelease (boolean)

**Documentation:**
- Added comprehensive "CI/CD and Release Management" section to CLAUDE.md
- Documented version management strategy (git tags as source of truth)
- Step-by-step release creation guide
- Troubleshooting section for common release issues
- HACS integration explanation

**Version Management:**
- Git tags matching `v*.*.*` are the source of truth for versions
- First release will be `v1.0.0` (existing `0.0.1` tag is ignored)
- Semantic versioning enforced (X.Y.Z format)

**Purpose:**
Enables professional release management with clean version numbers in HACS UI. Users will see versions like "1.0.0" and "1.1.0" instead of commit hashes, with proper release notes for each update.

### 2026-01-03 - API-Sourced Translation Corrections and PWD Status Codes

**Updated:**
- `translations.py`: Corrected sensor value mappings using official API data, Vaisala documentation, and user observations
  - **SADE**: Fixed codes (now 0-6 instead of 0-1) - Added 5 additional precipitation intensity levels
  - **SATEEN_OLOMUOTO_PWDXX**: Replaced incorrect codes with API codes 7-19 (was using codes 0, 10, 20, 30...)
  - **SADE_TILA**: Corrected from binary (0-1) to PWD precipitation type codes (7-19) based on user observations
  - **KELI_1/2/3/4**: Corrected all codes (0-9) to match API definitions - Code 0 now correctly shows "Sensor fault" instead of "Dry"
  - **VAROITUS_1/2/3/4**: Added missing mappings (codes 0-4) for warning levels
  - **PWD_STATUS**: Added hardware status codes (0-4) from Vaisala PWD22 User Manual
- All translations now use English descriptions with Finnish originals preserved in comments

**Sources:**
- `/api/weather/v1/sensors` endpoint - `sensorValueDescriptions` field
- Vaisala PWD22 User Manual - Hardware status and diagnostic codes
- User observations of actual sensor values in production

**Purpose:**
Ensures sensor value translations match the official Digitraffic API definitions and manufacturer documentation, providing accurate road condition, weather status, and sensor diagnostics displays. This fixes incorrect mappings that were based on assumptions rather than verified data.

**Sensors Still Without Documentation:**
The following sensors have empty `sensorValueDescriptions` in the API and no available manufacturer documentation:
- PWD_TILA, PWD_NÄK_TILA, PWD_LÄHETTIMEN_TAKAISINSIRONNAN_MUUTOS
- ASEMAN_STATUS_1/2/OPT1/OPT2, ANTURIVIKA
- DSC_STAT1/2, DSC_VASTAANOTTIMEN_PUHTAUS1/2
- OPTISEN_ANTURIN_KELI1/2, OPTISEN_ANTURIN_VAROITUS1/2
- KUITUVASTE_* (all fiber sensor variants)
- TIENPINNAN_TILA_* (all road surface state variants - have example mappings but not API-verified)
- SATEEN_OLOMUOTO_ENNUSTE

Users should monitor actual sensor values in Home Assistant and populate these mappings based on observed codes and corresponding conditions.

**How to find API mappings in the future:**
1. Access `https://tie.digitraffic.fi/api/weather/v1/sensors`
2. Search for sensor by name or ID
3. Look for `sensorValueDescriptions` array containing code-to-description mappings
4. For sensors without API mappings, consult manufacturer documentation (Vaisala PWD, DSC, etc.)
5. Note that not all sensors have value descriptions available - those remain as empty placeholders for user observation

### 2026-01-03 - Documentation Improvements
**Improved:**
- sensor.py section: Added detailed `async_setup_entry` documentation
- Device Info section: Added `entry_type: "service"` field documentation
- Sensor discovery: Documented dynamic sensor creation for all API-returned sensors
- Translations section: More accurate placeholder sensor listings
- Added prominent Claude Code update checklist at top of file

**Purpose:**
Ensured CLAUDE.md accurately reflects current implementation details that were previously undocumented or incomplete.

### 2026-01-03 - API User Identification
**Added:**
- `API_USER_AGENT` constant in `const.py`
- `Digitraffic-User` header to all API requests

**Modified:**
- `__init__.py`: Added header to coordinator API requests
- `config_flow.py`: Added header to station fetch and validation requests

**Purpose:**
Properly identifies the integration to Digitraffic API as requested by API guidelines. The header value is "Home Assistant github.com/taskinen/digitraffic_hacs".

### 2026-01-02 - Sensor Value Translation Framework
**Added:**
- `translations.py` module with translation mappings
- Complete WMO 4680 weather code mappings (0-99)
- Example mappings for Finnish road condition codes
- `translate_sensor_value()` function
- `translate` flag support in SENSOR_MAP
- Raw value preservation in sensor attributes
- State class handling for categorical vs. measurement sensors

**Modified:**
- `sensor.py`: Added translation logic to `native_value`, conditional `state_class`, raw value attributes
- `const.py`: Added `translate: True` flag to 40+ sensors

**Purpose:**
Converts cryptic numeric sensor codes to human-readable descriptions (e.g., "63" → "Rain, heavy continuous")

---

## Maintenance Instructions

### Keeping CLAUDE.md Updated

**When to update this file:**
1. **Architecture changes:** New modules, changed data flows, modified patterns
2. **New features:** Translation system, forecasting, automations, etc.
3. **API changes:** Endpoint updates, response format changes, new error handling
4. **Configuration changes:** New constants, modified defaults, changed behavior
5. **Bug fixes with architectural impact:** Workarounds that change patterns
6. **Deprecations:** Removed features, changed recommendations

**What to update:**
- Add entries to **Changelog** section with date and description
- Update relevant sections (Architecture, File Purposes, Common Tasks, etc.)
- Update **Last Updated** date at the top
- Add new examples if patterns change
- Update Known Issues if bugs are fixed or new ones discovered

**Update workflow:**
1. Make code changes
2. Update CLAUDE.md BEFORE committing
3. Commit both code and documentation together
4. Reference CLAUDE.md changes in commit message

**Example commit message:**
```
Add sensor grouping feature

- Implement sensor category grouping in sensor.py
- Add SENSOR_CATEGORIES to const.py
- Update CLAUDE.md with new architecture and usage

See CLAUDE.md changelog for details.
```

### File Format
- Use Markdown
- Keep sections in current order for consistency
- Use code blocks with language hints (python, json, yaml, bash)
- Include examples for complex concepts
- Link to external resources when helpful
- Keep line length reasonable (80-120 chars) for readability

---

**Remember:** A well-maintained CLAUDE.md makes future development easier for everyone (including AI assistants like me!). Treat it as living documentation that evolves with the codebase.
