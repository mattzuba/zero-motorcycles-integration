"""DataUpdateCoordinator for zero_moto."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from datetime import timedelta

    from homeassistant.core import HomeAssistant
    from zero_motorcycles import Zero

    from .data import ZeroConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class ZeroDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ZeroConfigEntry
    data: dict[str, Zero]

    def __init__(
        self,
        hass: HomeAssistant,
        update_interval: timedelta,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        data = {}
        try:
            # First get all of the units
            units = await self.config_entry.runtime_data.client.async_get_units()
            self.logger.debug("Successfully fetched %d units", len(units))
            for unit in units:
                self.logger.debug("Fetching %s - %s", unit.unit, unit.name)
                data[
                    unit.unit
                ] = await self.config_entry.runtime_data.client.async_get_last_transmit(
                    unit.unit
                )

        except Exception as exception:
            self.logger.exception("Exception while fetching data from API")
            raise UpdateFailed(exception) from exception

        return data
