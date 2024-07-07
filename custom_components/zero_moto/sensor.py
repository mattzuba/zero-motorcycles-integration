"""Sensor platform for zero_moto."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)

from .entity import ZeroEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import ZeroDataUpdateCoordinator
    from .data import ZeroConfigEntry


@dataclass(kw_only=True)
class ZeroSensorEntityDescription(SensorEntityDescription):
    """Custom sensor entity description."""

    json: str


SENSORS = (
    ZeroSensorEntityDescription(
        key="zero_moto",
        name="Mileage",
        json="mileage",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement="km",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: ZeroConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        ZeroSensor(
            coordinator=entry.runtime_data.coordinator,
            unit=unit,
            entity_description=description,
        )
        for unit in entry.runtime_data.coordinator.data
        for description in SENSORS
    )


class ZeroSensor(ZeroEntity, SensorEntity):
    """zero_moto Sensor class."""

    def __init__(
        self,
        coordinator: ZeroDataUpdateCoordinator,
        unit: str,
        entity_description: ZeroSensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)

        self._unit = unit
        self._json = entity_description.json
        self._attr_unique_id = f"{unit}_{entity_description.json}"

        self.entity_description = entity_description

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data[self._unit].get(self._json)
