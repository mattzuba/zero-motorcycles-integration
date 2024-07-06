"""Custom types for zero_moto."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from zero_motorcycles import Zero as ZeroApiClient
    from .coordinator import ZeroDataUpdateCoordinator


@dataclass
class ZeroData:
    """Data for the Blueprint integration."""

    client: ZeroApiClient
    coordinator: ZeroDataUpdateCoordinator
    integration: Integration


type ZeroConfigEntry = ConfigEntry[ZeroData]
