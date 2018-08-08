#!/bin/sh

apk update
apk add git
apk add py2-pip
pip install xmltodict
pip install texttable

