from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from .coordinator import BraunBleCoordinator

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: BraunBleCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BraunAlarmSwitch(coordinator, entry)])

class BraunAlarmSwitch(CoordinatorEntity, SwitchEntity):
    _attr_has_entity_name = True
    _attr_name = "Alarm"

    def __init__(self, coordinator: BraunBleCoordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_alarm"
        self._enabled = False

    @property
    def is_on(self):
        return self._enabled

    async def async_turn_on(self, **kwargs):
        self._enabled = True
        # hour/minute müssten vorher bekannt sein oder separat gesetzt werden
        await self.coordinator.set_alarm(True, 7, 0)  # Beispiel
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._enabled = False
        await self.coordinator.set_alarm(False, 0, 0)
        self.async_write_ha_state()
