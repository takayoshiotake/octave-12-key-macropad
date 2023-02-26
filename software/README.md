# README

## Setup

1. Install CircuitPython 8.0.x
    1. Connect Octave via USB
    2. Reboot Octave by holding down BOOT and pressing RESET
    3. Copy (drag & drop) uf2 to RPI-RP2
        - 📄 [adafruit-circuitpython-takayoshiotake_octave_rp2040-en_US-8.0.3.uf2](../circuitpython-bin/adafruit-circuitpython-takayoshiotake_octave_rp2040-en_US-8.0.3.uf2)
        - 

2. Renaming CIRCUITPY to OCTAVE_CP

    - 🔗 [https://learn.adafruit.com/welcome-to-circuitpython/renaming-circuitpy](https://learn.adafruit.com/welcome-to-circuitpython/renaming-circuitpy)

## Install packages

```shell-session
% poetry install
% poetry shell
(.venv) % circup --path /Volumes/OCTAVE_CP install -r requirements.txt
```

Alternatively:

```shell-session
% cp -r lib /Volumes/OCTAVE_CP/
```

## Upload

```shell-session
% cp boot.py code.py /Volumes/OCTAVE_CP/
% cp -r octave_pcb /Volumes/OCTAVE_CP/
```

MEMO: After uploading boot.py, you need to hold down SW1 to boot to enable the USB drive.

## Note

🔗 <https://learn.adafruit.com/circuitpython-essentials/circuitpython-resetting>
