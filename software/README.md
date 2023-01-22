# [WIP] README

## Setup

1. Build and Install CircuitPython 7.3.x

    - Code:
        - 🔗 [takayoshiotake/circuitpython:7.3.x-board-octave-rp2040](https://github.com/takayoshiotake/circuitpython/tree/7.3.x-board-octave-rp2040)
        - 🔗 <https://github.com/takayoshiotake/circuitpython/tree/c3b4d05dc04d74c6229506215eae799fb23f37ce/ports/raspberrypi/boards/takayoshiotake_octave_rp2040>

    - How to build:
        - 🔗 <https://learn.adafruit.com/building-circuitpython/build-circuitpython>
        - 🔗 <https://github.com/takayoshiotake/circuitpython/blob/c3b4d05dc04d74c6229506215eae799fb23f37ce/BUILDING.md>

2. Renaming CIRCUITPY to OCTAVE_CP

    - 🔗 [https://learn.adafruit.com/welcome-to-circuitpython/renaming-circuitpy](https://learn.adafruit.com/welcome-to-circuitpython/renaming-circuitpy)

- 📄 [circuitpython-takayoshiotake_octave_rp2040-7.3.0.uf2](../circuitpython-bin/circuitpython-takayoshiotake_octave_rp2040-7.3.0.uf2) (2023-01-22)

## Install packages

```shell-session
% poetry install
% poetry shell
(.venv) % circup --path /Volumes/OCTAVE_CP install -r requirements.txt
```

## Upload

```shell-session
% cp boot.py code.py /Volumes/OCTAVE_CP/
% cp -r octave_pcb /Volumes/OCTAVE_CP/
```

MEMO: After uploading boot.py, you need to hold down SW13 to boot to enable the USB drive.

## Note

🔗 <https://learn.adafruit.com/circuitpython-essentials/circuitpython-resetting>
