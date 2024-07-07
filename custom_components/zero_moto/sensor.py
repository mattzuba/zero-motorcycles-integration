"""Sensor platform for zero_moto."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)

from .entity import ZeroEntity

if TYPE_CHECKING:
    from collections.abc import Callable

    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import ZeroDataUpdateCoordinator
    from .data import ZeroConfigEntry


@dataclass(kw_only=True)
class ZeroSensorEntityDescription(SensorEntityDescription):
    """Custom sensor entity description."""

    json: str | None = None
    value_fn: Callable[[Any], Any] = lambda x: x


SENSORS = (
    ZeroSensorEntityDescription(
        key="zero_moto",
        name="Mileage",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement="mi",
        value_fn=lambda x: round(float(x) * 0.656290167),
        icon="mdi:road-variant",
    ),
    ZeroSensorEntityDescription(
        key="zero_moto",
        name="Elevation",
        json="altitude",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement="m",
        icon="mdi:elevation-rise",
    ),
    ZeroSensorEntityDescription(
        key="zero_moto", name="Satellites", icon="mdi:satellite-variant"
    ),
    ZeroSensorEntityDescription(
        key="zero_moto", name="Velocity", icon="mdi:speedometer"
    ),
    ZeroSensorEntityDescription(key="zero_moto", name="Heading", icon="mdi:navigation"),
    ZeroSensorEntityDescription(
        key="zero_moto",
        name="12v Battery",
        json="main_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
        icon="mdi:car-battery",
    ),
    ZeroSensorEntityDescription(
        key="zero_moto",
        name="Last Update",
        json="datetime_utc",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda x: datetime.strptime(f"{x}+0000", "%Y%m%d%H%M%S%z"),
        icon="mdi:update",
    ),
    ZeroSensorEntityDescription(
        key="zero_moto",
        name="Battery Level",
        json="soc",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement="%",
    ),
    ZeroSensorEntityDescription(
        key="zero_moto",
        name="Charging Time Left",
        json="chargingtimeleft",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement="min",
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

    entity_description: ZeroSensorEntityDescription

    def __init__(
        self,
        coordinator: ZeroDataUpdateCoordinator,
        unit: str,
        entity_description: ZeroSensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)

        self._unit = unit
        self._json = entity_description.json or entity_description.name.lower()
        self._attr_unique_id = f"{unit}_{self._json}"

        self.entity_description = entity_description

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.entity_description.value_fn(
            self.coordinator.data[self._unit].get(self._json)
        )
