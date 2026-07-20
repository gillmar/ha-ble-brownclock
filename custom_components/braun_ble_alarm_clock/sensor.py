from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from .coordinator import BraunBleCoordinator

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: BraunBleCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BraunTimeSensor(coordinator, entry)])

class BraunTimeSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Uhrzeit"

    def __init__(self, coordinator: BraunBleCoordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_time"

    @property
    def state(self):
        data = self.coordinator.data or {}
        return data.get("time")  # oder schöner formatieren
