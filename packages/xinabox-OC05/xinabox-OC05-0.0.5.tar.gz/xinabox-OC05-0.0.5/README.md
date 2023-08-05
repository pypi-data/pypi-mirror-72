[![GitHub Issues](https://img.shields.io/github/issues/xinabox/Python-OC05.svg)](https://github.com/xinabox/Python-OC05/issues)
![GitHub Commit](https://img.shields.io/github/last-commit/xinabox/Python-OC05)
![Maintained](https://img.shields.io/maintenance/yes/2020)
![Build status badge](https://github.com/xinabox/Python-OC05/workflows/Python/badge.svg)
![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)
# Python-OC05

The OC05 xChip is an 8-channel servo motor driver. It is based on the popular PCA9685 manufactured by NXP Semiconductor. It is supported by a BU33SD5 regulator to drive and accurately control up to 8 servo motors on a single module and act as system power supply. The module has 8 standard 2.54 mm (0.1") servo headers, plus 1 standard 2.54 mm (0.1") battery/BEC input header.

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
    upip.install("xinabox-OC05")
    ```

### CC03, CS11 and CW03
- Download the .UF2 file for CC03/CS11/CW03 [CircuitPython](https://circuitpython.org/board/xinabox_cs11/) and flash it to the board.
- TO DO

### MicroBit
- TO DO

## Raspberry Pi

Requires Python 3
```
pip3 install xinabox-OC05
```

# Example
```python
from xOC05 import xOC05
from xCore import xCore

# OC05 instance
OC05 = xOC05()

# configure OC05 with frequency of 60Hz
OC05.init(60)

while True:
    OC05.setServoPosition(1, 0)     #  position servo to the right
    xCore.sleep(50)
    OC05.setServoPosition(1, 180)   #  position servo to the left
    xCore.sleep(50)
```
