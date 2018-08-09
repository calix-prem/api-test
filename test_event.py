#!/usr/bin/env python

from jsonrpc import *
import xmltodict
import json
import pydbus
from gi.repository import GLib
from texttable import Texttable

log="test_event.log"

# JSON-RPC server proxy
proxy = ServerProxy(
        JsonRpc20(),
        TransportUnixSocket(addr="/var/run/proxy.sock",
        logfunc=log_file(log)))

print("Logging JSON-RPC API at: " + log)

# D-Bus event bus
bus = pydbus.SystemBus()
dev = bus.get("com.calix.exos", "events")

# Event handler
def evt_handler(producer, event, tags=None):
    print "evt_handler called %s/%s" % (producer, event)

    if producer == 'rgcommon' and event == 'dhcp-lease-added':
        print "event %s for mac %s" % (event, tags['mac'])
        ret = proxy.xget(
            "user",
            "auth_token",
            "lmd",
            "/status/rg/dhcp[pool='%s'][mac='%s']/leases" % (tags['pool-name'], tags['mac']))
  
        result = xmltodict.parse(ret)
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
dev.Event.connect(evt_handler)

# Start thread loop
loop = GLib.MainLoop()
loop.run()



