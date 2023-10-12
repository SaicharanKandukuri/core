"""Adds config flow for Wake on LAN integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_BROADCAST_ADDRESS,
    CONF_BROADCAST_PORT,
    CONF_HOST,
    CONF_MAC,
)
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.config_validation import ensure_list, script_action
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    ObjectSelector,
    TextSelector,
)

from .const import CONF_OFF_ACTION, DEFAULT_NAME, DOMAIN

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_MAC): TextSelector(),
        vol.Optional(CONF_BROADCAST_ADDRESS): TextSelector(),
        vol.Optional(CONF_BROADCAST_PORT): NumberSelector(
            NumberSelectorConfig(min=1, max=65535, step=1, mode=NumberSelectorMode.BOX)
        ),
        vol.Optional(CONF_HOST): TextSelector(),
        vol.Optional(CONF_OFF_ACTION): ObjectSelector(),
    }
)


class WOLConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Wake on LAN integration."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if not self._async_current_entries():
            return self.async_show_menu(
                step_id="user",
                menu_options=[
                    "service",
                    "switch",
                ],
            )
        return await self.async_step_switch()

    async def async_step_service(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the add service step."""
        if user_input:
            return self.async_create_entry(
                title=f"{DEFAULT_NAME}",
                data={},
            )

        return self.async_show_form(step_id="service")

    async def async_step_switch(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the add switch step."""

        errors: dict[str, str] = {}

        if user_input:
            if off_action := user_input.get(CONF_OFF_ACTION):
                try:
                    vol.All(ensure_list, [script_action])(off_action)
                except vol.Invalid:
                    errors[CONF_OFF_ACTION] = "incorrect_off_action"
                else:
                    _options = user_input.copy()
                    _options.pop(CONF_MAC)
                    return self.async_create_entry(
                        title=f"{DEFAULT_NAME} {user_input[CONF_MAC]}",
                        data=user_input[CONF_MAC],
                        options=_options,
                    )

        return self.async_show_form(
            step_id="switch",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )
