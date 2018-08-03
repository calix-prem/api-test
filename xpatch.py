#!/usr/bin/env python

from jsonrpc import *
import xmltodict
import json

proxy = ServerProxy( JsonRpc20(), TransportUnixSocket(addr="/tmp/proxy.sock") )

ret = proxy.xpatch(
  "user",
  "auth_token",
  "lmd",
  "/config/rg/wifi/device[radio='1']",
  "<device><radio>1</radio><iface><num>1</num><ssid>5E</ssid></iface></device>")

print("SET RESULT: " + ret + "\n")

ret = proxy.xget(
  "user",
  "auth_token",
  "lmd",
  "/config/rg/wifi/device[radio='1']/iface[1]/ssid")

print("GET RESULT: " + ret + "\n")
result = xmltodict.parse(ret)
print(json.dumps(result, sort_keys=True, indent=4))

