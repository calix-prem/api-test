#!/bin/sh

gcc -I /usr/include/dbus-1.0 -I /usr/include/glib-2.0 -I /usr/lib/glib-2.0/include \
  -o test_signal test_signal.c \
  -ldbus-glib-1 -lglib-2.0 -ldbus-1 -lgobject-2.0 -lgio-2.0

gcc -I /usr/include/dbus-1.0 -I /usr/include/glib-2.0 -I /usr/lib/glib-2.0/include \
  -o test_method test_method.c \
  -ldbus-glib-1 -lglib-2.0 -ldbus-1 -lgobject-2.0 -lgio-2.0

