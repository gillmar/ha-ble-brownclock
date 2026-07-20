from __future__ import annotations
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.bluetooth import async_scanner_by_source
from .coordinator import BraunBleCoordinator
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})

    # Coordinator initialisieren
    coordinator = BraunBleCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "switch"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator: BraunBleCoordinator = hass.data[DOMAIN][entry.entry_id]
    await coordinator.async_close()
    await hass.config_entries.async_unload_platforms(entry, ["sensor", "switch"])
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
