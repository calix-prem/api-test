#!/usr/bin/env python3

import xmltodict
import pydbus
from gi.repository import GLib

log="test_event.log"

# D-Bus event bus
bus = pydbus.SystemBus()
dev = bus.get("com.calix.exos")

# ret = dev.xget("xget /config/rg/interfaces")
# ret = dev.xget("Return Unregistered")

ret = dev.xpatch("/config/rg/wifi/device[radio='1']",
                 "<device><radio>1</radio><iface><num>1</num><ssid>5EE</ssid></iface></device>")

print(ret)



