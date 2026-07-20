from __future__ import annotations
import asyncio
from bleak import BleakClient
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import DOMAIN, UPDATE_INTERVAL, TIME_CHAR_UUID, ALARM_CHAR_UUID

class BraunBleCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(
            hass,
            entry,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )
        self.address = entry.data["address"]
        self._client: BleakClient | None = None
        self._lock = asyncio.Lock()

    async def _async_update_data(self):
        # Optional: periodisches Lesen, falls dein Wecker Werte per Read liefert
        async with self._lock:
            async with BleakClient(self.address, timeout=10.0) as client:
                # Beispiel: Uhrzeit lesen (falls unterstützt)
                # value = await client.read_gatt_char(TIME_CHAR_UUID)
                return {"time": None}  # Plaschhalter

    async def set_time(self, hour: int, minute: int):
        async with self._lock:
            async with BleakClient(self.address, timeout=10.0) as client:
                # Beispiel-Befehl anpassen an dein Protokoll
                payload = bytearray([0x01, hour, minute])  # <- laut Reverse Engineering
                await client.write_gatt_char(TIME_CHAR_UUID, payload)

    async def set_alarm(self, enabled: bool, hour: int, minute: int):
        async with self._lock:
            async with BleakClient(self.address, timeout=10.0) as client:
                payload = bytearray([0x02, 1 if enabled else 0, hour, minute])
                await client.write_gatt_char(ALARM_CHAR_UUID, payload)

    async def async_close(self):
        # Aufräumen, falls nötig
        pass
