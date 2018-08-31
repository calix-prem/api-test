#!/bin/sh

apk update
apk add git
# apk add py3-pip
apk add py3-gobject3
apk add py3-gevent
pip3 install xmltodict
pip3 install texttable
pip3 install pydbus
pip3 install bottle
pip3 install gevent-websocket


