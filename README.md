# Monitor Ring Light

![A monitor ring light](https://raw.githubusercontent.com/AltoRetrato/monitor-ring-light/main/images/monitor_ring_light.jpg)

A custom ring light around a monitor, providing uniform lighting and custom color toning to video recordings and video meetings.
Made with RGB LED Pixels (WS2801), ESP32, MicroPython and Dear PyGUI.

### How it works
A PC client sends data to an ESP32 board, which in turn controls a strip of LEDs assembled in a frame around the monitor.

The PC client is a Python script, using [Dear PyGui](https://github.com/hoffstadt/DearPyGui) for the GUI and using UDP to send data to the ESP32 via Wi-Fi.

The ESP32 board (ESP32-DevKitC V4) has a [MicroPython](https://micropython.org/) firmware installed. A MicroPython script started after boot connects to the Wi-Fi access point, waits for UDP packets, parse the received packets and communicates with the LED strip via SPI. A logic level converter is used since this LED strip requires 5V for data and clock, and the ESP32 provides 3.3V, but the system mighgt work without it - except for the 1st LED, which was flickering on my tests.

### How it was built
(soon)
