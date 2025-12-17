"""Text entities for Orei HDMI Matrix to configure input and output names."""

from homeassistant.components.text import TextEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import EntityCategory
from .const import DOMAIN, CONF_SOURCES, CONF_ZONES
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up Orei HDMI Matrix text entities."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    config = data["config"]

    sources = config.get(CONF_SOURCES, [])
    zones = config.get(CONF_ZONES, [])

    entities = []

    # Create text entities for configured inputs only
    for idx in range(1, len(sources) + 1):
        current_name = sources[idx - 1]
        entities.append(
            OreiMatrixInputNameText(
                coordinator, config, entry.entry_id, idx, current_name, entry
            )
        )

    # Create text entities for configured outputs only
    for idx in range(1, len(zones) + 1):
        current_name = zones[idx - 1]
        entities.append(
            OreiMatrixOutputNameText(
                coordinator, config, entry.entry_id, idx, current_name, entry
            )
        )

    async_add_entities(entities)


class OreiMatrixInputNameText(CoordinatorEntity, TextEntity):
    """Text entity to configure an input name."""

    _attr_native_min = 1
    _attr_native_max = 50
    _attr_pattern = r"^[a-zA-Z0-9\s\-_]+$"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator, config, entry_id, input_id, current_name, entry):
        """Initialize the text entity."""
        super().__init__(coordinator)
        self._config = config
        self._entry_id = entry_id
        self._input_id = input_id
        self._entry = entry
        self._attr_name = f"Input {input_id} Name"
        self._attr_native_value = current_name
        self._attr_unique_id = f"{DOMAIN}_{config.get('host')}_input_{input_id}_name"
        self._attr_icon = "mdi:video-input-hdmi"

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

    async def async_set_value(self, value: str):
        """Update the input name."""
        _LOGGER.info("Updating input %d name to: %s", self._input_id, value)

        # Get current sources list
        sources = list(self._config.get(CONF_SOURCES, []))

        # Extend list if needed
        while len(sources) < self._input_id:
            sources.append(f"Input {len(sources) + 1}")

        # Update the specific input name
        sources[self._input_id - 1] = value

        # Update config entry data
        new_data = {**self._entry.data, CONF_SOURCES: sources}
        self.hass.config_entries.async_update_entry(self._entry, data=new_data)

        # Update local value
        self._attr_native_value = value
        self.async_write_ha_state()

        # Reload the integration to apply changes
        await self.hass.config_entries.async_reload(self._entry.entry_id)


class OreiMatrixOutputNameText(CoordinatorEntity, TextEntity):
    """Text entity to configure an output name."""

    _attr_native_min = 1
    _attr_native_max = 50
    _attr_pattern = r"^[a-zA-Z0-9\s\-_]+$"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator, config, entry_id, output_id, current_name, entry):
        """Initialize the text entity."""
        super().__init__(coordinator)
        self._config = config
        self._entry_id = entry_id
        self._output_id = output_id
        self._entry = entry
        self._attr_name = f"Output {output_id} Name"
        self._attr_native_value = current_name
        self._attr_unique_id = f"{DOMAIN}_{config.get('host')}_output_{output_id}_name"
        self._attr_icon = "mdi:television"

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

    async def async_set_value(self, value: str):
        """Update the output name."""
        _LOGGER.info("Updating output %d name to: %s", self._output_id, value)

        # Get current zones list
        zones = list(self._config.get(CONF_ZONES, []))

        # Extend list if needed
        while len(zones) < self._output_id:
            zones.append(f"Output {len(zones) + 1}")

        # Update the specific output name
        zones[self._output_id - 1] = value

        # Update config entry data
        new_data = {**self._entry.data, CONF_ZONES: zones}
        self.hass.config_entries.async_update_entry(self._entry, data=new_data)

        # Update local value
        self._attr_native_value = value
        self.async_write_ha_state()

        # Reload the integration to apply changes
        await self.hass.config_entries.async_reload(self._entry.entry_id)
