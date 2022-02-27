
import os
from homeassistant.core import HomeAssistant,Config
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry

from subprocess import (run)

import logging

from .const import (
    DOMAIN,
    INTERFACE,
    CONFIG_PRIVATE_KEY,
    CONFIG_ADDRESS,
    CONFIG_LISTEN_PORT,
    CONFIG_PEER_ALLOWED_IPS,
    CONFIG_PEER_ENDPOINT,
    CONFIG_PEER_PUBLIC_KEY
)


_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry)-> bool:
    wg = Wireguard(hass, config_entry)
    await wg.install()
    await wg.start()
    
    dr = await device_registry.async_get_registry(hass)
    dr.async_get_or_create(
        config_entry_id=config_entry.entry_id,
        identifiers={(const.DOMAIN)},
        name="Wireguard",
        model="Wireguard",
        sw_version=const.VERSION,
        manufacturer="@jadson179",
    )
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = config_entry.data
    
    return True

class Wireguard:
    private_key:str = INTERFACE
    address:str = None
    listen_port:int = None
    peer_public_key:str = None
    peer_allowed_ips:str = None
    peer_endpoint:str = None

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry): 
        self.private_key = config_entry.data[CONFIG_PRIVATE_KEY]
        self.address = config_entry.data[CONFIG_ADDRESS]
        self.listen_port = config_entry.data[CONFIG_LISTEN_PORT]
        self.peer_public_key = config_entry.data[CONFIG_PEER_PUBLIC_KEY]
        self.peer_allowed_ips = config_entry.data[CONFIG_PEER_ALLOWED_IPS]
        self.peer_endpoint = config_entry.data[CONFIG_PEER_ENDPOINT]
        pass
    async def install(self):
       if not os.path.exists("/usr/bin/wg"):
            run(["apk","add","-U","wireguard-tools"])
    async def uninstall(self):
        if os.path.exists("/usr/bin/wg"):
            run(["apk","del","wireguard-tools"])
    async def restart(self): 
            await self.stop()
            await self.start()
    async def start(self):
        with open(f'/etc/wireguard/{INTERFACE}.conf', 'w') as f:
            f.write(
                f"""
                [Interface]
                PrivateKey= {self.private_key}
                Address= {self.address}
                ListenPort= {self.listen_port}

                [Peer]
                PublicKey= {self.peer_public_key}
                AllowedIPs= {self.peer_allowed_ips}
                Endpoint= {self.peer_endpoint}
                """
            )
        run(["wg-quick","up",INTERFACE])
    async def stop(self):
        os.remove(f'/etc/wireguard/{INTERFACE}.conf')
        run(["wg-quick","down",INTERFACE])
    