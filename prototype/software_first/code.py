import time

import board
import digitalio
from neopixel import NeoPixel

print("Hello, Octave!")

pixels = NeoPixel(board.NEOPIXEL, 1, auto_write=True)
pixels[0] = (0, 0, 1)

# Turns off the USER LED
ledpins = [board.LED_RED, board.LED_GREEN, board.LED_BLUE]
led = [digitalio.DigitalInOut(pin) for pin in ledpins]
for ledio in led:
    ledio.direction = digitalio.Direction.OUTPUT
    ledio.value = True


# Test SW14
row3pin = digitalio.DigitalInOut(board.D7)
col3pin = digitalio.DigitalInOut(board.D4)

row3pin.direction = digitalio.Direction.OUTPUT
row3pin.drive_mode = digitalio.DriveMode.OPEN_DRAIN
row3pin.value = True

col3pin.direction = digitalio.Direction.INPUT
col3pin.pull = digitalio.Pull.UP

while True:
    row3pin.value = False
    if col3pin.value:
        pixels[0] = (0, 0, 1)
    else:
        pixels[0] = (0, 1, 0)
    row3pin.value = True
    time.sleep(0.01)
