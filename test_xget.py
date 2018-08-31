#!/usr/bin/env python

import xmltodict
import pydbus
from gi.repository import GLib

# D-Bus event bus
bus = pydbus.SystemBus()
dev = bus.get("com.calix.exos")

ret = dev.xget("/config/rg/interfaces")
print(ret)



