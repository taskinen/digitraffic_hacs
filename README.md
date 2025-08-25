# Digitraffic Integration for Home Assistant

Integrates Finnish Transport Infrastructure Agency (FTIA) Digitraffic weather station data into Home Assistant.

**This component is under development.**

## Installation

1. Add this repository as a custom repository in HACS.
2. Install the "Digitraffic" integration.
3. Restart Home Assistant.

## Configuration

Configure via the Home Assistant UI (Integrations page). 

### Adding a Weather Station

1. Go to **Settings > Devices & Services**
2. Click **Add Integration** and search for "Digitraffic"
3. In the **Weather station name or ID** field, you can:
   - Enter a **station ID** directly (e.g., `1001`)
   - Search by **station name** or partial name (e.g., `Helsinki`, `Espoo`, `vt4`)
   - Search by **highway code** (e.g., `vt1`, `kt51`)
   - Search by **city name** (e.g., `Helsinki`, `Tampere`)

### Search Examples

- Type `Helsinki` to find all Helsinki area stations
- Type `vt4` to find stations along highway VT4  
- Type `Espoo` to find stations in Espoo
- Type `1001` to directly select station 1001

If your search returns multiple matches, the system will show you a list of matching stations to help you narrow down your selection.

## Creator

Timo Taskinen (timo.taskinen@iki.fi)