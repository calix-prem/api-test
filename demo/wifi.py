#!/usr/bin/python3

import json
from bottle import route, run, request, abort, Bottle ,static_file, template

import pydbus
from gi.repository import GLib
from threading import Thread

import time
import datetime
import xmltodict

bus = pydbus.SystemBus()
dev = bus.get("com.calix.exos")

def run_dbus_glib():

    loop = GLib.MainLoop()
    loop.run()

dbus_worker = Thread(target=run_dbus_glib)
dbus_worker.setDaemon(True)
dbus_worker.start()

import gevent
# from gevent import monkey; monkey.patch_all()
# from gevent import queue

import threading

class ev_queues:
    def __init__(self):
        self.main_lock = threading.Lock()
        self.wsocks = {}

    def add_wsock(self, wsock):
        done_lock = threading.Lock()
        done_lock.acquire()
        self.main_lock.acquire()
        try:
            print("add_sock: append wsock")
            self.wsocks[wsock] = done_lock
        finally:
            self.main_lock.release()
        return done_lock

    def send_msg(self, msg):
        self.main_lock.acquire()
        try:
            wsocks = list(self.wsocks)
            for ws in wsocks:
                try:
                    ws.send(msg)
                except WebSocketError:
                    print("Closing socket")
                    self.wsocks[ws].release()
                    del self.wsocks[ws]
        finally:
            self.main_lock.release()

queues = ev_queues()

def evt_handler(sender, object, iface, signal, args):
    global queues
    event, tags = args
    evt = {'time': str(datetime.datetime.now()), 'event': event}
    evt.update(tags)
    print("evt_handler called %s: %s" % (event, tags['mac']))
    queues.send_msg(json.dumps(evt))

bus.subscribe(sender="com.calix.exos", iface="com.calix.exos", signal="events", arg0="station-registered", signal_fired=evt_handler)
bus.subscribe(sender="com.calix.exos", iface="com.calix.exos", signal="events", arg0="station-expired", signal_fired=evt_handler)
bus.subscribe(sender="com.calix.exos", iface="com.calix.exos", signal="events", arg0="dhcp-lease-added", signal_fired=evt_handler)
bus.subscribe(sender="com.calix.exos", iface="com.calix.exos", signal="events", arg0="dhcp-lease-changed", signal_fired=evt_handler)
bus.subscribe(sender="com.calix.exos", iface="com.calix.exos", signal="events", arg0="dhcp-lease-deleted", signal_fired=evt_handler)


from bottle import route, run, template, static_file

app = Bottle()

@app.route('/')
def send_home():
    return static_file('index.html', root='static')

@app.route('/wifi')
def wifi():

    print("wifi")

    xml_doc = dev.xget('/status/emesh/wifi-metrics-sm')
    data = xmltodict.parse(xml_doc)
    # print(json.dumps(data, indent=4))

    if 'sta' in data['status']['emesh']['wifi-metrics-sm']:
       metrics = data['status']['emesh']['wifi-metrics-sm']['sta']
    else:
       metrics = []

    if type(metrics) is not list:
        metrics = [metrics]

    metrics_data = {'time': datetime.datetime.now().isoformat(), 'data': {}}
    for sta in metrics:
       mac = sta['mac']
       sn = int(sta['metrics'].split(',')[5])
       metrics_data['data'][mac] = sn
    return json.dumps(metrics_data)

@app.route('/metrics')
def metrics():
    xml_doc = dev.xget('/status/emesh/wifi-metrics-sm')
    return xml_doc

@app.route('/websocket')
def handle_websocket():
    global queues
    wsock = request.environ.get('wsgi.websocket')
    print("Websocket loop")
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    lock = queues.add_wsock(wsock)
    lock.acquire()
    print("websockt is closed")

@app.route('/<filepath:path>')
def server_static(filepath):
    print("static file %s" % filepath)
    return static_file(filepath, root='static')


from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

def run_web():
    host = "0.0.0.0"
    port = 8080

    server = WSGIServer((host, port), app,
                    handler_class=WebSocketHandler)
    print("access @ http://%s:%s/websocket.html" % (host,port))
    server.serve_forever()

web_worker = Thread(target=run_web)
web_worker.setDaemon(True)
web_worker.start()


dbus_worker.join()
web_worker.join()


