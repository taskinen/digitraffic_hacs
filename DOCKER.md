# Docker Development Environment

This directory contains a Docker Compose configuration for local development and testing of the Digitraffic Home Assistant custom component.

## Quick Start

1. **Start Home Assistant:**
   ```bash
   docker compose up -d
   ```

2. **Wait for initialization** (~60 seconds):
   ```bash
   docker compose logs -f homeassistant
   # Wait until you see "Home Assistant is running"
   ```

3. **Access Home Assistant:**
   Open http://localhost:8123 in your browser

4. **Complete onboarding:**
   - Create your user account
   - Set up your home location
   - Skip any integrations for now

5. **Add Digitraffic integration:**
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "Digitraffic"
   - Follow the configuration flow

## Development Workflow

### Making Code Changes

1. **Edit code** in `custom_components/digitraffic/`

2. **Reload the integration:**
   - Option A: In HA UI → Developer Tools → YAML → "Reload custom integrations"
   - Option B: Restart the container: `docker compose restart homeassistant`

3. **Check logs:**
   ```bash
   docker compose logs -f homeassistant | grep digitraffic
   ```

### Enabling Debug Logging

**Option 1: Via UI (easiest)**
1. Go to Settings → System → Logs
2. Click "Load full logs"
3. Set filter to "digitraffic"

**Option 2: Via configuration.yaml**
1. Uncomment the `test-config` volume mount in `docker-compose.yml`
2. Restart: `docker compose restart homeassistant`
3. Debug logs are already enabled in `test-config/configuration.yaml`

**Option 3: Via HA UI configuration**
1. Add to Configuration → Edit configuration.yaml:
   ```yaml
   logger:
     logs:
       custom_components.digitraffic: debug
   ```
2. Reload configuration

### Testing Different Scenarios

**Test with multiple stations:**
1. Add the integration multiple times with different station IDs
2. Each station creates a separate device with its own sensors

**Test error handling:**
1. Use an invalid station ID (e.g., 99999)
2. Check that the config flow shows proper error messages

**Test translation updates:**
1. Edit `custom_components/digitraffic/translations.py`
2. Reload the integration
3. Check that sensor states update with new translations

**Test with different HA versions:**
```bash
# Edit docker-compose.yml and change the image:
# homeassistant/home-assistant:2024.1.0
# homeassistant/home-assistant:dev  # for latest development version
docker compose up -d --pull always
```

## Useful Commands

### Container Management

```bash
# Start the environment
docker compose up -d

# Stop the environment
docker compose down

# Restart Home Assistant
docker compose restart homeassistant

# View logs (follow mode)
docker compose logs -f homeassistant

# View logs (last 100 lines)
docker compose logs --tail=100 homeassistant

# Access container shell
docker exec -it digitraffic-homeassistant /bin/bash
```

### Data Management

```bash
# Fresh start (removes all data including onboarding)
docker compose down -v

# Backup configuration
docker run --rm \
  -v digitraffic-ha-config:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/ha-config-backup.tar.gz -C /data .

# Restore configuration
docker run --rm \
  -v digitraffic-ha-config:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/ha-config-backup.tar.gz -C /data

# Inspect volume
docker volume inspect digitraffic-ha-config

# List files in config volume
docker run --rm -v digitraffic-ha-config:/data alpine ls -la /data
```

### Debugging

```bash
# Check if custom component is mounted correctly
docker exec digitraffic-homeassistant ls -la /config/custom_components/digitraffic/

# Check Python syntax
docker exec digitraffic-homeassistant python3 -m py_compile /config/custom_components/digitraffic/*.py

# View Home Assistant version
docker exec digitraffic-homeassistant python3 -m homeassistant --version

# Search logs for errors
docker compose logs homeassistant | grep -i error

# Search logs for Digitraffic
docker compose logs homeassistant | grep -i digitraffic
```

## Project Structure

```
digitraffic_hacs/
├── custom_components/
│   └── digitraffic/           # Your custom component (mounted read-only)
├── docker-compose.yml          # Docker Compose configuration
├── test-config/
│   └── configuration.yaml      # Optional test configuration
├── .dockerignore              # Files to exclude from Docker context
└── DOCKER.md                  # This file
```

## Volumes

The Docker setup uses the following volumes:

- **`digitraffic-ha-config`**: Persistent Home Assistant configuration
  - Stores: database, configuration files, logs
  - Persists between container restarts
  - Delete with: `docker compose down -v`

## Network

- **Network name:** `digitraffic-network`
- **Port mapping:** 8123 (host) → 8123 (container)
- **Health check:** Polls http://localhost:8123 every 30s

## Troubleshooting

### Home Assistant won't start

**Check logs:**
```bash
docker compose logs homeassistant
```

**Common issues:**
- Port 8123 already in use → Change port in docker-compose.yml
- Permission issues → Check file permissions on custom_components
- Corrupted config → Remove volume: `docker compose down -v`

### Custom component not loading

**Verify mount:**
```bash
docker exec digitraffic-homeassistant ls -la /config/custom_components/digitraffic/
```

**Check manifest:**
```bash
docker exec digitraffic-homeassistant cat /config/custom_components/digitraffic/manifest.json
```

**Check Python syntax:**
```bash
docker exec digitraffic-homeassistant python3 -m py_compile /config/custom_components/digitraffic/*.py
```

**Enable debug logging** and restart to see detailed error messages

### Integration setup fails

**Check station ID:**
- Use a valid station ID from https://tie.digitraffic.fi/api/weather/v1/stations
- Look for stations with `"state": "OK"` and `"collectionStatus": "GATHERING"`

**Check network connectivity:**
```bash
docker exec digitraffic-homeassistant curl -v https://tie.digitraffic.fi/api/weather/v1/stations
```

**Check logs for API errors:**
```bash
docker compose logs homeassistant | grep -A 5 digitraffic
```

### Sensors not updating

**Check coordinator logs:**
```bash
docker compose logs homeassistant | grep "coordinator\|update"
```

**Verify API is accessible:**
```bash
# Replace 12345 with your station ID
docker exec digitraffic-homeassistant curl https://tie.digitraffic.fi/api/weather/v1/stations/12345/data
```

**Check update interval:**
- Default: 5 minutes (configured in const.py)
- Wait at least 5 minutes after setup

### Performance issues

**Reduce database size:**
1. Edit configuration.yaml → recorder.purge_keep_days: 1
2. Restart Home Assistant

**Limit sensors:**
- Unfortunately, the integration creates all available sensors
- You can disable unwanted sensors in HA UI (click sensor → settings icon → disable)

## Advanced Configuration

### Using Custom Configuration File

To use the provided test configuration:

1. **Uncomment the volume mount** in `docker-compose.yml`:
   ```yaml
   volumes:
     - ./test-config/configuration.yaml:/config/configuration.yaml
   ```

2. **Restart:**
   ```bash
   docker compose down
   docker compose up -d
   ```

3. **Warning:** This will override any configuration you've made via the UI

### Adding Additional Services

The docker-compose.yml includes commented examples for:
- **File browser:** Uncomment to browse HA config files via web UI
- Add other services like MQTT broker, databases, etc.

### Environment Variables

You can customize the environment:

```yaml
environment:
  - TZ=Europe/Helsinki          # Change timezone
  - EXTRA_ARGS=--debug          # Add HA startup arguments
```

## Production Deployment

**Note:** This Docker setup is for **development/testing only**.

For production deployment:
- Use Home Assistant OS or Supervised
- Install via HACS
- Or install via manual copy to config/custom_components

## Resources

- **Home Assistant Docker:** https://www.home-assistant.io/installation/linux#docker-compose
- **HA Development:** https://developers.home-assistant.io/
- **Digitraffic API:** https://www.digitraffic.fi/en/road-traffic/

## License

Same as the main project (see repository root).
