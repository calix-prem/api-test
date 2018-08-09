#!/bin/sh

apk update
apk add git
apk add py2-pip
apk add py2-gobject3
pip install xmltodict
pip install texttable
pip install pydbus

