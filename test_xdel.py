#!/usr/bin/env python3

import xmltodict
import pydbus
from gi.repository import GLib

# D-Bus event bus
bus = pydbus.SystemBus()
dev = bus.get("com.calix.exos")

# ret = dev.xset("/config/rg/system/hostname", "<hostname>newname</hostname>")
# print(ret)

import json

dev.xpatch(
        "/config/rg/system",
        "<system><ntp-server><id>5</id><server>5.openwrt.pool.ntp.org</server></ntp-server></system>")

ret = dev.xget("/config/rg/system")

print(json.dumps(xmltodict.parse(ret), indent=4))

dev.xdel("/config/rg/system/ntp-server[id='5']")

ret = dev.xget("/config/rg/system")

print(json.dumps(xmltodict.parse(ret), indent=4))


