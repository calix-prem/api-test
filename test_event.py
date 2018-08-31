#!/usr/bin/env python

from jsonrpc import *
import xmltodict
import json
import pydbus
from gi.repository import GLib
from texttable import Texttable

# D-Bus event bus
bus = pydbus.SystemBus()
dev = bus.get("com.calix.exos")

# Event handler
def evt_handler(sender, object, iface, signal, args):
    event, tags = args
    print "evt_handler called %s" % event

    if event == 'dhcp-lease-added':
        print "event %s for mac %s" % (event, tags['mac'])
        ret = dev.xget(
            "/status/rg/dhcp[pool='%s'][mac='%s']/leases" % (tags['pool-name'], tags['mac']))
  
        try:
            result = xmltodict.parse(ret)
        except:
            print("XML = " + ret)
            raise 
        # print(json.dumps(result, sort_keys=True, indent=4))
        lease = result['status']['rg']['dhcp']['leases']['lease']
        print(lease)

        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(['t', 't', 't', 'i', 't', 't'])
        table.set_cols_width([6, 17, 18, 12, 28, 10])
        table.header(['Pool','MAC','IP Address','Expiry','DHCP Option','Ifname'])
        table.add_row([
            lease['pool'],
            lease['mac'],
            lease['ipaddr'],
            lease['expiry'],
            '\n'.join(lease['dhcp-option']),
            lease['ifname']])
        print(table.draw())

# Register event handler
# dev.events.connect(evt_handler)
bus.subscribe(sender="com.calix.exos", iface="com.calix.exos", signal="events", arg0="interface-connected", signal_fired=evt_handler)
bus.subscribe(sender="com.calix.exos", iface="com.calix.exos", signal="events", arg0="dhcp-lease-added", signal_fired=evt_handler)
# dev.events.connect(evt_handler)

# Start thread loop
loop = GLib.MainLoop()
loop.run()



