Container Setup
===============

1.	Create an Alpine LXC container. Here I call it `api`.
```
# lxc-create -t alpine-prem2 -n api
```

2.	Add a line at the end of `/exa_data/lxc/api/config` to allow Unix socket bind mount.
```
lxc.mount.entry = /tmp/run/dbus/system_bus_socket run/dbus/system_bus_socket none bind,create=file 0 0
```

3.	Start the `api` container
```
# lxc-start -n api
```

4.	Attach to the `api` container shell
```
# lxc-attach -n api
```

5.	Install git inside the container shell
```
[api] / # apk update && apk add git
```

6.	Clone test script repo
```
[api] / # git clone https://github.com/calix-prem/api-test.git
```

7.	Enable `community` repository in `/etc/apk/repositories` by
        adding this line in the file:
```
http://dl-cdn.alpinelinux.org/alpine/v3.7/community
```

8.	CD to ‘apt-get’ folder and install a few dependencies
```
[api] / # cd api-test
[api] /api-test # ./setup.sh
```

DMs
===

The DM `zmq-event` is responsible for the DBus-to-DCLI proxy.

Register for Events
===================

`zmq-event` registers for a hard coded list of events from `daemonlib`. The list can be changed by
modifying the `main` function in `depot/zmq-event/src/zmqevent.c`.

Current list of registered events:
```
    dl_event_subscribe("rgcommon", "interface-connected");
    dl_event_subscribe("rgcommon", "interface-disconnected");
    dl_event_subscribe("rgcommon", "dhcp-lease-added");
    dl_event_subscribe("rgcommon", "dhcp-lease-deleted");
    dl_event_subscribe("sysmgr", "flash-image-started");
    dl_event_subscribe("sysmgr", "flash-image-completed");
    dl_event_subscribe("rgcommon", "station-registered");
    dl_event_subscribe("rgcommon", "station-expired");
    dl_event_subscribe("rgcommon", "wps-result");
    dl_event_subscribe("devicemgr", "devicemgr-mode-role");
```

Running Test Scripts
====================

xget.py
-------

This example does a simple `xget` and return the XML result converted to JSON format.

```
[api] ~/api-test # python2 xget.py 
Logging JSON-RPC at: xget.log
{
    "config": {
        "rg": {
            "interfaces": {
                "interface": [
                    {
                        "admin": "1", 
                        "ifname": [
                            "/config/rg/lan/eth[port='1']", 
                            "/config/rg/wifi/device[radio='1']/iface[num='1']", 
                            "/config/rg/wifi/device[radio='1']/iface[num='10']", 
                            "/config/rg/wifi/device[radio='1']/iface[num='9']", 
                            "/config/rg/wifi/device[radio='2']/iface[num='1']"
                        ], 
                        "ip6assign": "64", 
                        "ipaddr": "192.168.1.1", 
                        "ipmask": "255.255.255.0", 
                        "name": "lan", 
                        "proto": "static", 
                        "type": "bridge"
                    }, 
                    {
                        "admin": "1", 
                        "ifname": "/config/rg/wifi/device[radio='1']/iface[num='9']", 
                        "ipaddr": "169.254.1.1", 
                        "ipmask": "255.255.255.0", 
                        "name": "pvtlan", 
                        "proto": "static", 
                        "type": "pvtlan"
                    }, 
                    {
                        "admin": "1", 
                        "default-route": "1", 
                        "ifname": "/config/rg/wan/eth[port='1']", 
                        "name": "wan", 
                        "peer-dns": "1", 
                        "proto": "dhcp", 
                        "reqopts": "43 120 121 125", 
                        "service-label": "wan", 
                        "vendorid": "GS2026E.ONT.dslforum.org"
                    }
                ]
            }
        }
    }
}
```

The script generates a log file called `xget.log` and it contains the transcript of the JSON-RPC channel.

```
[api] /api-test # cat xget.log
connect to '/var/run/proxy.sock'
--> '{"jsonrpc": "2.0", "method": "xget", "params": ["user", "auth_token", "lmd"
, "/config/rg/interfaces"], "id": 0}'
<-- '{"jsonrpc": "2.0", "result": "<?xml version=\\"1.0\\"?>\\n<config><rg><inte
rfaces><interface><name>lan<\\/name><type>bridge<\\/type><admin>1<\\/admin><ifna
me>\\/config\\/rg\\/lan\\/eth[port=\'1\']<\\/ifname><ifname>\\/config\\/rg\\/wif
i\\/device[radio=\'1\']\\/iface[num=\'1\']<\\/ifname><ifname>\\/config\\/rg\\/wi
fi\\/device[radio=\'1\']\\/iface[num=\'10\']<\\/ifname><ifname>\\/config\\/rg\\/
wifi\\/device[radio=\'1\']\\/iface[num=\'9\']<\\/ifname><ifname>\\/config\\/rg\\
/wifi\\/device[radio=\'2\']\\/iface[num=\'1\']<\\/ifname><proto>static<\\/proto>
<ipaddr>192.168.1.1<\\/ipaddr><ipmask>255.255.255.0<\\/ipmask><ip6assign>64<\\/i
p6assign><\\/interface><interface><name>pvtlan<\\/name><type>pvtlan<\\/type><adm
in>1<\\/admin><ifname>\\/config\\/rg\\/wifi\\/device[radio=\'1\']\\/iface[num=\'
9\']<\\/ifname><proto>static<\\/proto><ipaddr>169.254.1.1<\\/ipaddr><ipmask>255.
255.255.0<\\/ipmask><\\/interface><interface><name>wan<\\/name><admin>1<\\/admin
><ifname>\\/config\\/rg\\/wan\\/eth[port=\'1\']<\\/ifname><proto>dhcp<\\/proto><
default-route>1<\\/default-route><peer-dns>1<\\/peer-dns><vendorid>GS2026E.ONT.d
slforum.org<\\/vendorid><reqopts>43 120 121 125<\\/reqopts><service-label>wan<\\
/service-label><\\/interface><\\/interfaces><\\/rg><\\/config>", "id": 0}'
close '/var/run/proxy.sock'
```

xpatch.py
---------

This script does an `xpatch` to modify the SSID on the main Wifi radio, and then
`xget` to verify that the SSID has indeed been modified.

```
[api] ~/api-test # python xpatch.py
Logging JSON-RPC at: xpatch.log
SET RESULT: lmd>xpatch /config/rg/wifi/device[radio=1] <device><radio>1</radio><iface><num>1</num><ssid>5E</ssid></iface></device>


GET RESULT: <?xml version="1.0"?>
<config><rg><wifi><device><radio>1</radio><iface><num>1</num><ssid>5E</ssid></iface></device></wifi></rg></config>

{
    "config": {
        "rg": {
            "wifi": {
                "device": {
                    "iface": {
                        "num": "1", 
                        "ssid": "5E"
                    }, 
                    "radio": "1"
                }
            }
        }
    }
}
```


test_event.py
-------------

This example shows how to listen for event on the DBus channel.

When it receives `rgcommon/dhcp-lease-added` event, it retrieves the DHCP lease information using the JSON-RPC
interface and display it in a table format.

When the script is running, start a LAN device and a new `dhcp-lease-added` event should appear on the console.

On Sim Test Gateway, you can simulate a LAN device by using `LXD`. For example, to start a LAN device called `s01`, run on this command on Sim Test Gateway:
```
# lxc launch images:alpine/3.7 -p subbr0 s01
```

Sample output of the program:
```
[api] ~/api-test # python test_event.py 
Logging JSON-RPC API at: test_event.log
evt_handler called rgcommon/dhcp-lease-added
OrderedDict([(u'pool', u'lan'), (u'mac', u'00:16:3e:8a:1a:6a'), (u'ipaddr', u'192.168.1.134'), (u'expiry', u'1533758181'), (u'ifname', u'1'), (u'source', u'dhcp'), (u'iftype', u'eth'), (u'active', u'1'), (u'dhcp-option', [u'0C03613032', u'350103', u'37070103060C0F1C2A', u'39020240', u'3C0C756468637020312E32372E32', u'3D070100163E8A1A6A'])])
 Pool           MAC              IP Address          Expiry              DHCP Option              Ifname  
==========================================================================================================
lan      00:16:3e:8a:1a:6a   192.168.1.134        1533758181     0C03613032                     1         
                                                                 350103                                   
                                                                 37070103060C0F1C2A                       
                                                                 39020240                                 
                                                                 3C0C756468637020312E32372E32             
                                                                 3D070100163E8A1A6A                       
```

Press `Ctrl-C` to stop the execution.

demo/wifi.py
------------

This example shows a dynamic HTML chart displaying WiFi analytics.

```
[api] ~/api-test # ./demo/wifi.py &
access @ http://192.168.1.124/
```

Use a web browser connected to the LAN port to access the displayed URL (your IP address may be different).

