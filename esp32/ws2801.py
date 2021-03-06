#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Code by Razanur: https://forum.micropython.org/memberlist.php?mode=viewprofile&u=5987
# Modified by Ricardo Mendonça Ferreira - ric@mpcnet.com.br
#
# 2020.02.12 - 1st version


class WS2801:

  def __init__(self, num_led, spi):
    self.NUM_LED = num_led
    self._databuffer = bytearray(3*num_led)
    self._spi = spi

  def set_led(self, num, r=0x00, g=0x00, b=0x00):
    if num < self.NUM_LED:
      self._databuffer[num*3  ] = r
      self._databuffer[num*3+1] = g
      self._databuffer[num*3+2] = b

  def write(self):
    self._spi.write(self._databuffer)

  def clear(self, default=0x00):
    for i in range(len(self._databuffer)):
      self._databuffer[i] = default

  def set_all(self, r=0xff, g=0xff, b=0xff):
    for i in range(self.NUM_LED):
      self.set_led(num=i, r=r, g=g, b=b)
