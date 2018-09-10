#!/usr/bin/env python3

import xmltodict
import pydbus
from gi.repository import GLib
import json
import time

# D-Bus event bus
bus = pydbus.SystemBus()
dev = bus.get("com.calix.exos")

outer = 0
while outer < 1000:
  loop = 0
  while loop < 1000:
    ret = dev.xget("/config/rg/wifi/device[radio='1']")
    if ret.startswith("ERROR"):
      print(ret)
    else:
      # try:
      #   obj = xmltodict.parse(ret)
      # except:
      #   print("XML = " + ret)
      #   raise
      pass
    loop += 1
  print("%d" % outer)
  outer += 1


