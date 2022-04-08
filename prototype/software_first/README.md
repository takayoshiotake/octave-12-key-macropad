# README 

Board: Seeed XIAO RP-2040


## Setup

1. Install CircuitPython
 
- 🔗 [https://circuitpython.org/board/seeeduino_xiao_rp2040/](https://circuitpython.org/board/seeeduino_xiao_rp2040/)
- 🔗 [https://github.com/adafruit/circuitpython/releases/tag/7.2.3](https://github.com/adafruit/circuitpython/releases/tag/7.2.3)
- 🔗 [https://wiki.seeedstudio.com/XIAO-RP2040-with-CircuitPython/](https://wiki.seeedstudio.com/XIAO-RP2040-with-CircuitPython/)


2. Renaming CIRCUITPY to OCTAVE_CP

- 🔗 [https://learn.adafruit.com/welcome-to-circuitpython/renaming-circuitpy](https://learn.adafruit.com/welcome-to-circuitpython/renaming-circuitpy)


## Install packages

```shell-session
% poetry install
% poetry shell
(.venv) % circup --path /Volumes/OCTAVE_CP install -r requirements.txt
```


## upload

```shell-session
% cp boot.py code.py /Volumes/OCTAVE_CP/
% cp -r octave_pcb /Volumes/OCTAVE_CP/
```
