#!/usr/bin/env python3

import xmltodict
import pydbus

# D-Bus event bus
bus = pydbus.SystemBus()
dev = bus.get("com.calix.exos")

ret = dev.xget("/config/rg/interfaces")
print(ret)



