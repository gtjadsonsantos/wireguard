"""Config flow for the Wireguard."""
import json
from typing import Any, Optional
from aioesphomeapi import Dict
from homeassistant import config_entries
import voluptuous as vol
import logging


from .const import (
    DOMAIN,
    CONFIG_ADDRESS,
    CONFIG_LISTEN_PORT,
    CONFIG_PEER_ALLOWED_IPS,
    CONFIG_PEER_ENDPOINT,
    CONFIG_PEER_PUBLIC_KEY,
    CONFIG_PRIVATE_KEY
)


_LOGGER = logging.getLogger(__name__)

class WireguardConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Wireguard."""

    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL
    VERSION = 1

    async def async_step_user(self, info: Optional[Dict[str, Any]] = None ):
        """Handle a flow initialized by the user."""
        errors = {}
        
        if info is not None:
                return self.async_create_entry(title="Wireguard", data=info)

        return self.async_show_form(
                step_id="user", 
                data_schema=vol.Schema(
                    {  
                        vol.Required(
                            CONFIG_PRIVATE_KEY,
                            description="privatekey",
                        
                        ): str,
                        vol.Required(
                            CONFIG_ADDRESS,
                            description="address",
                            ): str,
                        vol.Required(
                            CONFIG_LISTEN_PORT,default=51871
                            ): int,
                        vol.Required(
                            CONFIG_PEER_PUBLIC_KEY
                            ): str,
                        vol.Required(
                            CONFIG_PEER_ALLOWED_IPS
                            ): str,
                        vol.Required(
                            CONFIG_PEER_ENDPOINT
                            ): str,
                    }
                ),
                errors=errors   
            )

            