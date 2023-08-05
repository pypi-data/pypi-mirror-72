[![GitHub Issues](https://img.shields.io/github/issues/xinabox/Python-SL06.svg)](https://github.com/xinabox/Python-SL06/issues)
![GitHub Commit](https://img.shields.io/github/last-commit/xinabox/Python-SL06)
![Maintained](https://img.shields.io/maintenance/yes/2020)
![Build status badge](https://github.com/xinabox/Python-SL06/workflows/Python/badge.svg)
![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)

# Python-SL06

The SL06 xChip features advanced Gesture detection, Proximity detection, Digital Ambient Light Sense (ALS) and Colour Sense (RGBC). It is based on the popular APDS9960 manufactured by Avago Technologies.

# Usage

## Mu-editor
Download [Mu-editor](https://github.com/xinabox/mu-editor/releases/tag/v1.1.0a2)

### CW01 and CW02
- Use [XinaBoxUploader](https://github.com/xinabox/XinaBoxUploader/releases/latest) and flash MicroPython to the CW01/CW02.
- Download Python packages from the REPL with the following code:
    ```python
    import network
    import upip
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect("ssid", "password")
    upip.install("xinabox-SL06")
    ```

### CC03, CS11 and CW03
- Download the .UF2 file for CC03/CS11/CW03 [CircuitPython](https://circuitpython.org/board/xinabox_cs11/) and flash it to the board.
- TO DO

### MicroBit
- TO DO

## Raspberry Pi

Requires Python 3
```
pip3 install xinabox-SL06
```

# Example
```python
from xCore import xCore
from xSL06 import xSL06

# SL06 instance
SL06 = xSL06()

# configure SL06
SL06.init()

# enable SL06 for gesture sensing
SL06.enableGestureSensor()

while True:
    if SL06.isGestureAvailable():   # check for gesture
        dir = SL06.getGesture()     # read direction
        print(dir)                  # print direction on console

    xCore.sleep(100)
```