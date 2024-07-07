"""BlueprintEntity class."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN
from .coordinator import ZeroDataUpdateCoordinator


class ZeroEntity(CoordinatorEntity[ZeroDataUpdateCoordinator]):
    """BlueprintEntity class."""

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True
    _unit: str
    coordinator: ZeroDataUpdateCoordinator

    def __init__(self, coordinator: ZeroDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._unit)},
            manufacturer="Zero Motorcycles",
            model="Motorcycle",
            name=f"Zero {self.coordinator.data[self._unit].vin[-5:]}",
            serial_number=self.coordinator.data[self._unit].vin,
            sw_version=self.coordinator.data[self._unit].software_version,
        )
