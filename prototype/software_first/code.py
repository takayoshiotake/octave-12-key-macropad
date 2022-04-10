import collections
import time

import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
from neopixel import NeoPixel

from octave_pcb.key_matrix import KeyMatrix
from octave_pcb.rotary_encoder import RotaryEncoder


class KeyEvent:
  PRESS = 0
  LONG_PRESS = 1
  RELEASE = 2


class KeyEventPlanner:
  def __init__(self):
    self._is_pressed = False
    self._long_press_timing = None

  def make_event(self, current_time, is_pressed):
    key_event = None

    if is_pressed == True:
      if self._is_pressed != is_pressed:
        key_event = KeyEvent.PRESS
        self._long_press_timing = current_time + 0.5
      elif current_time >= self._long_press_timing:
        key_event = KeyEvent.LONG_PRESS
        self._long_press_timing = current_time + 0.1
    elif self._is_pressed != is_pressed:
      key_event = KeyEvent.RELEASE
      self._long_press_timing = None

    self._is_pressed = is_pressed
    return key_event


KeyAssignment = collections.namedtuple('KeyAssignment', ['code'])

KEY_MAP = [
    KeyAssignment(Keycode.F1),
    KeyAssignment(Keycode.F2),
    KeyAssignment(Keycode.F3),
    KeyAssignment(Keycode.F4),
    KeyAssignment(Keycode.F5),
    KeyAssignment(Keycode.F6),
    KeyAssignment(Keycode.F7),
    KeyAssignment(Keycode.F8),
    KeyAssignment(Keycode.F9),
    KeyAssignment(Keycode.F10),
    KeyAssignment(Keycode.F11),
    KeyAssignment(Keycode.F12),
    None,
    None,
    KeyAssignment(Keycode.SPACEBAR),
]

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
    mouse = Mouse(usb_hid.devices)
    pixels[0] = (0, 1, 1)

    key_event_planners = [KeyEventPlanner()
                          for _ in range(len(key_matrix.row_ios) * len(key_matrix.col_ios))]
    pressed_keys = [None for _ in range(len(key_event_planners))]
    scan_key_matrix_timing = time.monotonic()  # For debounce
    while True:
      current_time = time.monotonic()
      if current_time >= scan_key_matrix_timing:
        are_keys_pressed = key_matrix.scan_matrix()
        for i, key_event_planner in enumerate(key_event_planners):
          key_event = key_event_planner.make_event(
              current_time, are_keys_pressed[i])
          # print(f"""pressed : {i}""")
          if key_event == KeyEvent.PRESS:
            print(f"""pressed : {i}""")
            keycode = KEY_MAP[i].code
            pressed_keys[i] = keycode
            keyboard.press(pressed_keys[i])
          elif key_event == KeyEvent.LONG_PRESS:
            print(f"""pressed : {i}""")
            keyboard.press(pressed_keys[i])
          elif key_event == KeyEvent.RELEASE:
            print(f"""released: {i}""")
            keyboard.release(pressed_keys[i])

        scan_key_matrix_timing += 0.01
        if scan_key_matrix_timing <= current_time:
          scan_key_matrix_timing = current_time + 0.01

      direction = rotary_encoder.detect_direction()
      if direction != 0:
        print(f"""rotated : {"CW" if direction > 0 else "CCW"}""")
        if direction > 0:
          mouse.move(wheel=1)
        else:
          mouse.move(wheel=-1)
  except Exception:
    pixels[0] = (0, 0, 1)
    time.sleep(3)
