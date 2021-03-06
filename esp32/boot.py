#!/usr/bin/python3
# -*- coding: utf-8 -*-
# By Ricardo Mendonça Ferreira - ric@mpcnet.com.br
# This file is executed on every boot (including wake-boot from deepsleep)
import esp
import network
from time import sleep


esp.osdebug(None)
#import webrepl
#webrepl.start()

# Init Wi-Fi
hostname = "LEDs"
essid    = "<write here your Wi-Fi router network name>"
pwd      = "<write here your Wi-Fi password>"
timeout  = 10
try:
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active():
        wlan.active(True)
    if hostname:
        wlan.config(dhcp_hostname=hostname)
    if not wlan.isconnected():
        wlan.connect(essid, pwd)
        time_passed = 0
        while not wlan.isconnected() and time_passed < timeout:
            sleep(1)
            time_passed += 1
        if not wlan.isconnected():
            print("Could not connect to router after {} s!".format(time_passed))
    print("Connected to", essid)
except Exception as e:
    print("Exception:", e)
