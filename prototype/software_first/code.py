import time

import board
import digitalio
from neopixel import NeoPixel

DIO_HIGH = True
DIO_LOW = False


print("Hello, Octave!")

pixels = NeoPixel(board.NEOPIXEL, 1, auto_write=True)
pixels[0] = (0, 0, 1)

# Turns off the USER LED
led_pins = [board.LED_RED, board.LED_GREEN, board.LED_BLUE]
led_ios = [digitalio.DigitalInOut(pin) for pin in led_pins]
for led_io in led_ios:
    led_io.direction = digitalio.Direction.INPUT


row_pins = [board.D6, board.D5, board.D3, board.D7]
row_ios = [digitalio.DigitalInOut(pin) for pin in row_pins]
for row_io in row_ios:
    row_io.direction = digitalio.Direction.OUTPUT
    row_io.drive_mode = digitalio.DriveMode.OPEN_DRAIN
    row_io.value = DIO_HIGH

col_pins = [board.D2, board.D1, board.D0, board.D4]
col_ios = [digitalio.DigitalInOut(pin) for pin in col_pins]
for col_io in col_ios:
    col_io.direction = digitalio.Direction.INPUT
    col_io.pull = digitalio.Pull.UP


def select_row(row):
    # Once deselect all rows
    for row_io in row_ios:
        row_io.value = DIO_HIGH
    if 0 <= row <= len(row_ios):
        row_ios[row].value = DIO_LOW


keys_state = [{'is_pressed': False}
              for _ in range(len(row_ios) * len(col_ios))]
while True:
    are_keys_pressed = []
    for row in range(len(row_ios)):
        select_row(row)
        are_keys_pressed.extend(
            [True if col_io.value == DIO_LOW else False for col_io in col_ios]
        )
        time.sleep(0.001)
    for i, key_state in enumerate(keys_state):
        if key_state['is_pressed'] != are_keys_pressed[i]:
            key_state['is_pressed'] = are_keys_pressed[i]
            print(
                f"""{"pressed " if key_state['is_pressed'] else "released"}: {i}""")
    time.sleep(0.01)
