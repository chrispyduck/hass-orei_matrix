"""Select entities for Orei HDMI Matrix."""

from homeassistant.components.select import SelectEntity
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Orei HDMI Matrix output selectors."""
    data = hass.data[DOMAIN][entry.entry_id]
    client = data["client"]
    coordinator = data["coordinator"]
    config = data["config"]

    sources = config.get("sources", [])
    zones = config.get("zones", [])

    entities = [
        OreiMatrixOutputSelect(
            client, coordinator, config, zone_name, idx, entry.entry_id
        )
        for idx, zone_name in enumerate(zones, start=1)
    ]

    async_add_entities(entities)


class OreiMatrixOutputSelect(CoordinatorEntity, SelectEntity):
    """Select entity to control which input is routed to an HDMI output."""

    def __init__(self, client, coordinator, config, name, output_id, entry_id):
        """Initialize the select entity."""
        super().__init__(coordinator)
        self._client = client
        self._config = config
        self._attr_name = f"{name} Input"
        self._output_id = output_id
        self._entry_id = entry_id

        # Get the list of input sources
        sources = config.get("sources", [])

        # If sources list is empty, generate default names
        if not sources:
            # Determine number of inputs from the matrix type
            matrix_type = coordinator.data.get("type", "")
            # Most common Orei matrices are 4x2, 4x4, 8x8, etc.
            # Default to 8 inputs if we can't determine
            num_inputs = 8
            sources = [f"Input {i}" for i in range(1, num_inputs + 1)]

        self._attr_options = sources
        self._attr_current_option = None
        self._attr_unique_id = (
            f"{DOMAIN}_{config.get('host')}_output_{output_id}_select"
        )
        self._attr_icon = "mdi:hdmi-port"

        # Set initial state from coordinator data
        self._update_current_option()

    @property
    def available(self):
        """Return if entity is available."""
        return bool(self.coordinator.data.get("power"))

    @property
    def device_info(self):
        """Return device info for grouping entities."""
        model = self.coordinator.data.get("type", "Unknown")
        name = f"Orei {model}" if model != "Unknown" else "Orei HDMI Matrix"
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": name,
            "manufacturer": "Orei",
            "model": model,
            "configuration_url": f"http://{self._config.get('host')}",
        }

    def _update_current_option(self):
        """Update the current option from coordinator data."""
        if not self.coordinator.data:
            return

        if not self.coordinator.data.get("power"):
            self._attr_current_option = None
            return

        outputs = self.coordinator.data.get("outputs", {})
        if not outputs:
            return

        # Get the current input assigned to this output
        src_id = outputs.get(self._output_id)

        if src_id and 1 <= src_id <= len(self._attr_options):
            # Convert input ID (1-based) to source name
            self._attr_current_option = self._attr_options[src_id - 1]
        else:
            self._attr_current_option = None

    @callback
    def _handle_coordinator_update(self):
        """Handle updated data from the coordinator."""
        self._update_current_option()
        self.async_write_ha_state()

    async def async_select_option(self, option: str):
        """Change the selected input for this output."""
        if not self.available:
            _LOGGER.warning("Matrix is off; cannot change input for %s.", self.name)
            return

        if option not in self._attr_options:
            _LOGGER.warning("Unknown input %s for %s", option, self.name)
            return

        # Convert source name to input ID (1-based)
        input_id = self._attr_options.index(option) + 1

        _LOGGER.info(
            "Setting output %d to input %d (%s)", self._output_id, input_id, option
        )

        # Send command to matrix
        await self._client.set_output_source(input_id, self._output_id)

        # Update the current option immediately for better UX
        self._attr_current_option = option
        self.async_write_ha_state()

        # Request a refresh to sync state
        await self.coordinator.async_request_refresh()
