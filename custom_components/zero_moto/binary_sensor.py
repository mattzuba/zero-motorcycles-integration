"""Binary sensor platform for zero_moto."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .const import LOGGER
from .entity import ZeroEntity

if TYPE_CHECKING:
    from collections.abc import Callable

    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import ZeroDataUpdateCoordinator
    from .data import ZeroConfigEntry


@dataclass(kw_only=True)
class ZeroBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Custom binary sensor entity description."""

    json: str
    on_fn: Callable[[Any], int] = lambda x: x


BINARY_SENSORS = (
    ZeroBinarySensorEntityDescription(
        key="zero_moto",
        json="tip_over",
        name="Tipped Over",
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:alert",
    ),
    ZeroBinarySensorEntityDescription(
        key="zero_moto",
        json="charging",
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
        icon="mdi:ev-station",
    ),
    ZeroBinarySensorEntityDescription(
        key="zero_moto",
        json="charge_complete",
        name="Charge Complete",
        icon="mdi:battery-charging-high",
    ),
    ZeroBinarySensorEntityDescription(
        key="zero_moto",
        json="plugged",
        name="Plugged In",
        device_class=BinarySensorDeviceClass.PLUG,
        icon="mdi:ev-plug-type1",
    ),
    ZeroBinarySensorEntityDescription(
        key="zero_moto", json="storage", name="Storage Mode", icon="mdi:sleep"
    ),
    ZeroBinarySensorEntityDescription(
        key="zero_moto",
        json="gps_valid",
        name="GPS Valid",
        device_class=BinarySensorDeviceClass.PROBLEM,
        on_fn=lambda x: not x,
        icon="mdi:map-marker-alert",
    ),
    ZeroBinarySensorEntityDescription(
        key="zero_moto",
        json="gps_connected",
        name="GPS Connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        icon="mdi:map-marker",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: ZeroConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        ZeroBinarySensor(
            coordinator=entry.runtime_data.coordinator,
            unit=unit,
            entity_description=description,
        )
        for unit in entry.runtime_data.coordinator.data
        for description in BINARY_SENSORS
    )


class ZeroBinarySensor(ZeroEntity, BinarySensorEntity):
    """zero_moto binary_sensor class."""

    entity_description: ZeroBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: ZeroDataUpdateCoordinator,
        unit: str,
        entity_description: ZeroBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator)

        self._unit = unit
        self._json = entity_description.json
        self._attr_unique_id = f"{unit}_{entity_description.json}"

        self.entity_description = entity_description

        LOGGER.debug(f"Setting up {self._attr_unique_id}")

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return self.entity_description.on_fn(
            getattr(self.coordinator.data[self._unit], self._json)
        )
