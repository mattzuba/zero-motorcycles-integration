"""Binary sensor platform for zero_moto."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.device_tracker import SourceType
from homeassistant.components.device_tracker.config_entry import TrackerEntity

from .entity import ZeroEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import ZeroDataUpdateCoordinator
    from .data import ZeroConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: ZeroConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        ZeroTrackerEntity(
            coordinator=entry.runtime_data.coordinator,
            unit=unit,
        )
        for unit in entry.runtime_data.coordinator.data
    )


class ZeroTrackerEntity(ZeroEntity, TrackerEntity):
    """tracker_entity class."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: ZeroDataUpdateCoordinator, unit: str) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._unit = unit
        self._attr_unique_id = f"{unit}_location"
        self._attr_name = "Location"
        self._attr_icon = "mdi:map-marker-radius-outline"

    @property
    def should_poll(self) -> bool:
        """Need to poll on this one."""
        return True

    @property
    def source_type(self) -> SourceType:
        """Return the source type."""
        return SourceType.GPS

    @property
    def battery_level(self) -> int | None:
        """Return the battery level."""
        return int(self.coordinator.data[self._unit].get("soc"))

    @property
    def location_name(self) -> str | None:
        """Return the location_name."""
        return self.coordinator.data[self._unit].get("address")

    @property
    def latitude(self) -> float | None:
        """Return the latitude."""
        return self.coordinator.data[self._unit].get("latitude")

    @property
    def longitude(self) -> float | None:
        """Return the longitude."""
        return self.coordinator.data[self._unit].get("longitude")
