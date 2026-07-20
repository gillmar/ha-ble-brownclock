from __future__ import annotations
from homeassistant import config_entries
from homeassistant.components.bluetooth import BluetoothServiceInfoBleak
from .const import DOMAIN

class BraunBleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_bluetooth(self, discovery_info: BluetoothServiceInfoBleak):
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")
        self._discovery_info = discovery_info
        self.context["title_placeholders"] = {"name": discovery_info.name}
        return await self.async_step_confirm()

    async def async_step_confirm(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=self._discovery_info.name,
                data={"address": self._discovery_info.address},
            )
        self._set_confirm_only()
        return self.async_show_form(step_id="confirm")
