#!/usr/bin/python3
# -*- coding: utf-8 -*-
# By Ricardo Mendonça Ferreira - ric@mpcnet.com.br
#
# 2021.03.06  1st release

import socket
import json
from cfg import Cfg
from dearpygui.core import *
from dearpygui.simple import *


ADDR  = "192.168.1.2"  # Address reserved in Router > DHCP > Address reservation
PORT  = 8008
LEDs  = "LEDs color"   # label & ID of the color picker widget
COLORS = {
    "Off"   : [  0,   0,   0],
    "White" : [255, 255, 255],
    "Beige" : [255, 213,  64],
}
DBG   = not True # set True for debugging
cfg   = Cfg(fn="pc_config.json") # cfg = dictionary with configuration (default color)


def send_udp(ip, port, data):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (ip, port))
        if DBG: txt = data.decode()
    except Exception as e:
        if DBG: txt = f"{data.decode()} == {e}"
    if DBG: log_debug(f"{ip}:{port} -> {txt}")


def send_color(sender, data):
    leds = get_value(LEDs)
    data = f"rgb={leds[0]:.0f},{leds[1]:.0f},{leds[2]:.0f}".encode()
    send_udp(ADDR, PORT, data)


def set_widget_color(sender, data):
    set_value(LEDs, data)
    send_color(sender, data)


def save_color(sender, data):
    leds = get_value(LEDs)
    data = f"def={leds[0]:.0f},{leds[1]:.0f},{leds[2]:.0f}".encode()
    send_udp(ADDR, PORT, data)
    cfg["default"] = [int(x) for x in leds[:3]]
    cfg.save()


if __name__ == "__main__":
    cfg.load(ignore_not_found=True)

    with window("LEDs interface", x_pos=5, y_pos=5, autosize=True, no_close=True, no_move=True):
        add_color_picker3(LEDs, callback=send_color)
        for cor in COLORS:
            add_button(cor, callback=set_widget_color, callback_data=COLORS[cor])
            add_same_line()
        add_dummy()
        add_button("Save color as default", callback=save_color)
        #add_input_text("Address", default_value=ADDR, width=115)
        set_widget_color(None, cfg.get("default", [0,0,0]))


    if DBG: show_logger()
    set_main_window_resizable(DBG)
    set_main_window_size(300,333)
    set_main_window_title("Ring Light")

    start_dearpygui(primary_window="LEDs interface")
