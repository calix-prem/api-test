#!/usr/bin/env python3

import xmltodict
import pydbus
from gi.repository import GLib

# D-Bus event bus
bus = pydbus.SystemBus()
dev = bus.get("com.calix.exos")

ret = dev.xset("/config/rg/system/hostname", "<hostname>newname</hostname>")
print(ret)

ret = dev.xget("/config/rg/system/hostname")
print(ret)


