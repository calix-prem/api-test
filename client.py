#!/usr/bin/env python

from jsonrpc import *
import xmltodict
import json

proxy = ServerProxy( JsonRpc20(), TransportUnixSocket(addr="/var/run/test_server.sock", logfunc=log_file("test_client.txt")) )
# proxy = ServerProxy( JsonRpc20(), TransportTcpIp(addr=("127.0.0.1",1234), logfunc=log_file("mylog.txt")) )

proxy.echo("hello")

