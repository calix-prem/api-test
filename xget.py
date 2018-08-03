#!/usr/bin/env python

from jsonrpc import *
import xmltodict
import json

proxy = ServerProxy( JsonRpc20(), TransportUnixSocket(addr="/var/run/proxy.sock", logfunc=log_file("mylog.txt")) )
# proxy = ServerProxy( JsonRpc20(), TransportUnixSocket(addr="/tmp/proxy.sock", logfunc=log_file("mylog.txt")) )
# proxy = ServerProxy( JsonRpc20(), TransportTcpIp(addr=("127.0.0.1",1234), logfunc=log_file("mylog.txt")) )

ret = proxy.xget("user", "auth_token", "lmd", "/config/rg/interfaces")

result = xmltodict.parse(ret)
print(json.dumps(result, sort_keys=True, indent=4))

