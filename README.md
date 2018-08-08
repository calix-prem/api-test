Container Setup
===============

1.	Create an Alpine LXC container. Here I call it `api`.
```
# lxc-create -t alpine-prem2 -n api
```

2.	Add a line at the end of `/exa_data/lxc/api/config` to allow Unix socket bind mount.
```
lxc.mount.entry = /tmp/run/proxy.sock run/proxy.sock none bind,create=file 0 0
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

7.	CD to ‘apt-get’ folder and install a few dependencies
```
[api] / # cd api-test
[api] /api-test # ./setup.sh
```

Running Test Scripts
====================

There are 2 test scripts currently `xget.py` and `xpatch.py`.

Run `xget.py` by issuing command `python xget.py` under `api-test` directory. If successful, you
should get the format result in JSON format at the output.

```
[api] ~/api-test # python2 xget.py 
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

The script generates a log file called `mylog.txt` and it contains the transcript of the JSON-RPC channel.

```
[api] /api-test # cat mylog.txt 
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
