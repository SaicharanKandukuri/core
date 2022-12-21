"""Custom data coordinator for Cloudflare."""
from __future__ import annotations

import logging

from pycfdns import CFRecord, CloudflareException, CloudflareUpdater

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER: logging.Logger = logging.getLogger(__name__)


class CloudflareDataUpdateCoordinator(DataUpdateCoordinator[list[CFRecord]]):
    """Class to manage fetching Cloudflare data."""

    def __init__(
        self,
        hass: HomeAssistant,
        updater: CloudflareUpdater,
        zone_id: str,
    ) -> None:
        """Initialize the Android IP Webcam."""
        self.hass = hass
        self.updater = updater
        self.zone_id = zone_id

        super().__init__(
            self.hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=None,
        )

    async def _async_update_data(self) -> list[CFRecord]:
        """Update data."""
        try:
            return await self.updater.get_record_info(self.zone_id)
        except CloudflareException as exception:
            raise UpdateFailed(exception) from exception
