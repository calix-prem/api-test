#!/bin/sh

if ! grep "alpine/.*/community" /etc/apk/repositories > /dev/null; then
  echo ERROR: Alpine community repository needs to be enabled in /etc/apk/repositories
  echo        See https://wiki.alpinelinux.org/wiki/Enable_Community_Repository
  exit 1
fi

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


