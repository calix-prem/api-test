Container Setup
===============

1.	Pull in an Alpine Linux example container image. Note: Please replace `armhf` with `x86_64` or `x86` for simulation platforms on Intel architecture.
```
# cd /tmp
# curl -o al-armhf-1.7.unc.app https://exos-apps.s3.amazonaws.com/examples/07/armhf/al-armhf-1.7.unc.app
```

2.	The application name is `al` for the example container image. Install the container. The LXC name for
container is `app-al-1.7.unc`.
```
# dcli appmgr xexec install al 1.7.unc /tmp/al-armhf-1.7.unc.app

# lxc-ls -f
NAME                  STATE   AUTOSTART GROUPS IPV4          IPV6
app-al-1.7.unc        STOPPED 0         -      -             -
#
```

3.      Start the newly installed container.
```
# dcli appmgr xexec start al

# lxc-ls -f
NAME                  STATE   AUTOSTART GROUPS IPV4          IPV6
app-al-1.7.unc        RUNNING 0         -      -             -
#
```

4.	Attach to the container shell
```
# lxc-attach -n app-al-1.7.unc
```

5.	Install git inside the container shell
```
[al] /tmp # cd /root 
[al] / # apk update && apk add git
```

6.	Clone test script repo
```
[al] / # cd
[al] ~ # git clone https://github.com/calix-prem/api-test.git
```

7.	Enable `community` repository in `/etc/apk/repositories` by
        adding this line at the end of the file:
```
http://dl-cdn.alpinelinux.org/alpine/v3.10/community
```

8.	CD to ‘apt-get’ folder and install a few dependencies
```
[api] ~ # cd api-test
[api] /api-test # ./setup.sh
```

Running Test Python Scripts
===========================

This respository contains a number of Python scripts that demonstrate the capability of the EXOS platform
API through the D-Bus interface.

test_xget.py
------------

This example does a simple `xget` and return the XML result converted to JSON format.

```
[al] ~/api-test # ./test_xget.py
<?xml version="1.0"?>
<config><rg><interfaces><interface><name>lan</name><type>bridge</type><admin>1</admin><ifname>/config/rg/lan/eth[port='1']</ifname><ifname>/config/rg/wifi/device[radio='1']/iface[num='1']</ifname><ifname>/config/rg/wifi/device[radio='1']/iface[num='10']</ifname><ifname>/config/rg/wifi/device[radio='1']/iface[num='11']</ifname><ifname>/config/rg/wifi/device[radio='1']/iface[num='9']</ifname><ifname>/config/rg/wifi/device[radio='2']/iface[num='1']</ifname><ifname>/config/rg/wifi/device[radio='2']/iface[num='11']</ifname><proto>static</proto><ipaddr>192.168.1.1</ipaddr><ipmask>255.255.255.0</ipmask><ip6assign>64</ip6assign><mac-br>cc:be:59:fc:03:5f</mac-br></interface><interface><name>pvtlan</name><type>pvtlan</type><admin>1</admin><ifname>/config/rg/wifi/device[radio='1']/iface[num='9']</ifname><proto>static</proto><ipaddr>169.254.2.1</ipaddr><ipmask>255.255.255.0</ipmask></interface><interface><name>wan</name><admin>1</admin><ifname>/config/rg/wan/eth[port='1']</ifname><proto>dhcp</proto><default-route>1</default-route><peer-dns>1</peer-dns><vendorid>GS2026E.ONT.dslforum.org</vendorid><reqopts>43 120 121 125</reqopts><service-label>wan</service-label></interface><interface><name>wan6</name><admin>1</admin><ifname>/config/rg/wan/eth[port='1']</ifname><proto>dhcpv6</proto><default-route>1</default-route><peer-dns>1</peer-dns><reqopts>17</reqopts><reqaddress>try</reqaddress><reqprefix>auto</reqprefix><service-label>wan6</service-label></interface></interfaces></rg></config>
[al] ~/api-test #
```

test_xpatch.py
--------------

This script does an `xpatch` to modify the SSID on the main Wifi radio, and then
`xget` to verify that the SSID has indeed been modified.

```
[al] ~/api-test # ./test_xpatch.py
[al] ~/api-test # 
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
[al] ~/api-test # ./test_event.py 
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

Start the application:
```
[api] ~/api-test # cd demo
[api] ~/api-test/demo # ./wifi.py &
access @ http://192.168.1.124/
```

Use a web browser connected to the LAN port to access the displayed URL (your IP address may be different).

Terminate the application:
```
[api] ~/api-test/demo # killall -9 wifi.py
```

![Image of Demo](https://raw.githubusercontent.com/calix-prem/api-test/master/wifi_analytics.png)

Running example C programs
==========================

The repository also contains a couple of C language examples of accessing the EXOS platform D-Bus interface.
Run the `setup.sh` shell script to install the native compiler and required libraries, and then the `compile.sh`
script to compile the example source into executable binaries.
```
[al] ~/api-test # cd c-examples
[al] ~/api-test/c-examples # ./setup.sh
[al] ~/api-test/c-examples # ./compile.sh
[al] ~/api-test/c-examples # ls -l test_method test_signal
[al] ~/api-test/c-examples # ls -l test_method test_signal
-rwxr-xr-x    1 root     root         11048 Nov  5 22:27 test_method
-rwxr-xr-x    1 root     root         16040 Nov  5 22:27 test_signal
[al] ~/api-test/c-examples #
```

test_method
-----------

This program is functionally equivalent to `test_xget.py` script. It demonstrates the ability to make the `xget`
call using C language code.

```
[al] ~/api-test/c-examples # ./test_method
test-method:main Connecting to the D-Bus.
test-method:main Invoking method.
Response: <?xml version="1.0"?>
<status><emesh><wifi-metrics-sm><last-update>50</last-update><sequence>1863</sequence><device><radio>1</radio><freq-band>5g</freq-band><mac>cc:be:59:fc:03:62</mac><tx-power>29</tx-power><channel-width>80</channel-width><metrics>100,10,10,-103,0,0,0,0,0,0</metrics></device><device><radio>2</radio><freq-band>2.4g</freq-band><mac>cc:be:59:fc:03:61</mac><tx-power>29</tx-power><channel-width>20</channel-width><metrics>6,20,430,-103,0,0,0,0,0,0</metrics></device><iface><radio>1</radio><num>1</num><ssid>5EE</ssid><usage>primary</usage><sta-count>0</sta-count><metrics>0,000000,000000,000000,000000</metrics></iface><iface><radio>1</radio><num>9</num><ssid>Calix-5G-backhaul5762F0</ssid><usage>backhaul</usage><sta-count>0</sta-count><metrics>0,000000,000000,000000,000000</metrics></iface><iface><radio>1</radio><num>11</num><ssid>Mon-Ap5762F0</ssid><usage>pro-mon</usage><sta-count>0</sta-count><metrics>0,000000,000000,000000,000000</metrics></iface><iface><radio>2</radio><num>1</num><ssid>CXNK005762F0</ssid><usage>primary</usage><sta-count>0</sta-count><metrics>0,000000,000000,000000,000000</metrics></iface><iface><radio>2</radio><num>11</num><ssid>Mon-Ap5762F0</ssid><usage>pro-mon</usage><sta-count>0</sta-count><metrics>0,000000,000000,000000,000000</metrics></iface></wifi-metrics-sm></emesh></status>
[al] ~/api-test/c-examples #
```

test_signal
-----------

This program is functionally equivalent to the `test_event.py` script. It listens for any events arriving on the
system bus and display them to the console.

```
[al] ~/api-test/c-examples # ./test_signal
test-signal:main Connecting to the D-Bus.
test-signal:main Subscribing signals.

Got signal: events
Event type: probe-report
Tag[STRING]: devname = ath1
Tag[STRING]: sta-mac = 40:98:ad:94:36:23
Tag[INT32]: rssi = -36
Tag[STRING]: file = emesh_core_db.c
Tag[INT32]: line = 281

Got signal: events
Event type: cleanup-app
Tag[STRING]: name = al
Tag[INT32]: delay = 5
Tag[STRING]: file = appmgr_lxc.c
Tag[INT32]: line = 2166
```
