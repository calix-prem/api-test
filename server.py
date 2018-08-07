#!/usr/bin/env python

from jsonrpc import *
import xmltodict
import json

server = Server( JsonRpc20(), TransportUnixSocket(addr="/var/run/test_server.sock", logfunc=log_file("test_server.txt")) )
# proxy = ServerProxy( JsonRpc20(), TransportTcpIp(addr=("127.0.0.1",1234), logfunc=log_file("mylog.txt")) )

def echo(s):
  return s

server.register_function(echo)
server.serve()

