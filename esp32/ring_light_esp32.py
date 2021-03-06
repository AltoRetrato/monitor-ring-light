#!/usr/bin/python3
# -*- coding: utf-8 -*-
# By Ricardo Mendonça Ferreira - ric@mpcnet.com.br
#
# 2021.03.06: 1st release.
# 2021.02.18: 1st version.

import socket
import gc
from math import copysign
from time import sleep_ms
from machine import Pin, SPI, freq
from ws2801 import WS2801
from cfg import Cfg


freq(240000000) # Default CPU freq.: 160 MHz

print("Loading configuration")
cfg = Cfg()
cfg.load(ignore_not_found=True)

hspi  = SPI(1, baudrate=int(250e3), sck=Pin(14), mosi=Pin(13), miso=Pin(12))
leds  = WS2801(spi=hspi, num_led=40)


def set_rgb(color):
    # color=="0,0,0"
    try:
        r, g, b = [int(x) & 255 for x in color.split(b",")]
    except:
        r, g, b = [0, 0, 0]
    leds.set_all(r=r, g=g, b=b)
    leds.write()
    return "OK"


def set_all(color):
    # color=="0"
    try:
        color = int(color) & 255
    except:
        color = 0
    leds.clear(color)
    leds.write()
    return "OK"


def set_def(color):
    # color=="0,0,0"
    try:
        cfg["default"] = color
        cfg.save()
        return "OK"
    except Exception as e:
        return "Exception saving color {}: {}".format(color, e)


def route(data):
    try:
        # data == "rgb=0,0,0"
        cmd, val = data.split(b"=")
        if   cmd == b"rgb": return set_rgb(val)
        elif cmd == b"all": return set_all(val)
        elif cmd == b"def": return set_def(val)
        else: return "Can't handle cmd {} [{}]".format(cmd, data)
    except Exception as e:
        print("Exception:", e)
        pass
    return "Error routing: {}".format(data)


def fade(start, end, step_ms):
    for gray_level in range(start, end, int(copysign(1, end -start))):
        set_all(gray_level)
        sleep_ms(step_ms)
    sleep_ms(50)
    set_all(end)


def main():
    # https://wiki.python.org/moin/UdpCommunication
    IP   = "0.0.0.0"
    PORT = 8008
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((IP, PORT))
    color = cfg.get("default", "128,128,128").encode()
    print("Lighting up default color ({}): {}".format(color, set_rgb(color)) )
    print('UDP server listening on {}:{}'.format(IP,PORT))
    try:
        while True:
            data, addr = s.recvfrom(32)
            print("<", data, end=" - ")
            response = route(data)
            print(response)
            #s.sendto(response, addr)
            gc.collect()
    except KeyboardInterrupt:
        print('Got ctrl-c')
    print("Shutting down")
    s.close()


if __name__ == "__main__":
    main()
