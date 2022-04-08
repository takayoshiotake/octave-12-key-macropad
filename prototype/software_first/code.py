import time

import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from neopixel import NeoPixel

from octave_pcb.key_matrix import KeyMatrix
from octave_pcb.rotary_encoder import RotaryEncoder

print("Hello, Octave!")

pixels = NeoPixel(board.NEOPIXEL, 1, auto_write=True)
pixels[0] = (0, 0, 1)
# Turns off the USER LED
led_pins = [board.LED_RED, board.LED_GREEN, board.LED_BLUE]
led_ios = [digitalio.DigitalInOut(pin) for pin in led_pins]
for led_io in led_ios:
  led_io.switch_to_input(digitalio.Pull.UP)

key_matrix = KeyMatrix()
rotary_encoder = RotaryEncoder()
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
while True:
  try:
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayoutUS(keyboard)
    pixels[0] = (0, 1, 1)

    keys_state = [{'is_pressed': False}
                  for _ in range(len(key_matrix.row_ios) * len(key_matrix.col_ios))]
    scan_key_matrix_timing = time.monotonic()
    while True:
      current_time = time.monotonic()
      if current_time >= scan_key_matrix_timing:
        are_keys_pressed = key_matrix.scan_matrix()
        for i, key_state in enumerate(keys_state):
          if key_state['is_pressed'] != are_keys_pressed[i]:
            key_state['is_pressed'] = are_keys_pressed[i]
            print(
                f"""{"pressed " if key_state['is_pressed'] else "released"}: {i}""")
        scan_key_matrix_timing += 0.01
        if scan_key_matrix_timing <= current_time:
          scan_key_matrix_timing = current_time + 0.01

      direction = rotary_encoder.detect_direction()
      if direction != 0:
        print(f"""rotated : {"CW" if direction > 0 else "CCW"}""")
  except Exception:
    pixels[0] = (0, 0, 1)
    time.sleep(3)
