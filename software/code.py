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


class CodeType:
  KEYBOARD = 0
  MOUSE_MOVE = 1
  MOUSE_BUTTON = 2
  LAYER_MOMENTRY = 3


KeyAssignment = collections.namedtuple('KeyAssignment', ['type', 'code'])

KEYCODE_MO = 'MO'
KEY_MAP_LAYERS = [
    [
        KeyAssignment(CodeType.KEYBOARD, Keycode.F1),
        KeyAssignment(CodeType.KEYBOARD, Keycode.F2),
        KeyAssignment(CodeType.KEYBOARD, Keycode.F3),
        KeyAssignment(CodeType.KEYBOARD, Keycode.F4),
        KeyAssignment(CodeType.KEYBOARD, Keycode.F5),
        KeyAssignment(CodeType.KEYBOARD, Keycode.F6),
        KeyAssignment(CodeType.KEYBOARD, Keycode.F7),
        KeyAssignment(CodeType.KEYBOARD, Keycode.F8),
        KeyAssignment(CodeType.KEYBOARD, Keycode.F9),
        KeyAssignment(CodeType.KEYBOARD, Keycode.F10),
        KeyAssignment(CodeType.KEYBOARD, Keycode.F11),
        KeyAssignment(CodeType.KEYBOARD, Keycode.F12),
        KeyAssignment(CodeType.LAYER_MOMENTRY, None),
        None,
        None,
        None,
    ],
    [
        None,
        None,
        KeyAssignment(CodeType.KEYBOARD, Keycode.UP_ARROW),
        None,
        None,
        KeyAssignment(CodeType.KEYBOARD, Keycode.LEFT_ARROW),
        KeyAssignment(CodeType.KEYBOARD, Keycode.DOWN_ARROW),
        KeyAssignment(CodeType.KEYBOARD, Keycode.RIGHT_ARROW),
        KeyAssignment(CodeType.KEYBOARD, Keycode.ESCAPE),
        KeyAssignment(CodeType.MOUSE_BUTTON, Mouse.LEFT_BUTTON),
        KeyAssignment(CodeType.MOUSE_BUTTON, Mouse.MIDDLE_BUTTON),
        KeyAssignment(CodeType.MOUSE_BUTTON, Mouse.RIGHT_BUTTON),
        None,
        None,
        None,
        None,
    ],
]

pixpower = digitalio.DigitalInOut(board.NEOPIX_POWER)
pixpower.switch_to_output(True, digitalio.DriveMode.PUSH_PULL)
pixels = NeoPixel(board.NEOPIX, 1, auto_write=True)
pixels[0] = (0, 0, 2)

key_matrix = KeyMatrix()
rotary_encoder = RotaryEncoder()
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
while True:
  try:
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayoutUS(keyboard)
    mouse = Mouse(usb_hid.devices)
    pixels[0] = (0, 2, 2)

    key_map_layer = 0
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
          if key_event == KeyEvent.PRESS:
            print(f"""pressed : {i}""")
            pressed_keys[i] = KEY_MAP_LAYERS[key_map_layer][i]
            key_assignment = pressed_keys[i]
            if key_assignment is None:
              pass
            elif key_assignment.type == CodeType.LAYER_MOMENTRY:
              key_map_layer = 1
            elif key_assignment.type == CodeType.KEYBOARD:
              keyboard.press(key_assignment.code)
            elif key_assignment.type == CodeType.MOUSE_MOVE:
              mouse.move(**key_assignment.code)
            elif key_assignment.type == CodeType.MOUSE_BUTTON:
              mouse.press(key_assignment.code)
          elif key_event == KeyEvent.LONG_PRESS:
            # print(f"""pressed : {i}""")
            key_assignment = pressed_keys[i]
            if key_assignment is None:
              pass
            elif key_assignment.type == CodeType.LAYER_MOMENTRY:
              pass
            elif key_assignment.type == CodeType.KEYBOARD:
              print(f"""pressed : {i}""")
              keyboard.press(key_assignment.code)
            elif key_assignment.type == CodeType.MOUSE_MOVE:
              print(f"""pressed : {i}""")
              mouse.move(**key_assignment.code)
          elif key_event == KeyEvent.RELEASE:
            print(f"""released: {i}""")
            key_assignment = pressed_keys[i]
            pressed_keys[i] = None
            if key_assignment is None:
              pass
            elif key_assignment.type == CodeType.LAYER_MOMENTRY:
              key_map_layer = 0
            elif key_assignment.type == CodeType.KEYBOARD:
              keyboard.release(key_assignment.code)
            elif key_assignment.type == CodeType.MOUSE_BUTTON:
              mouse.release(key_assignment.code)

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
    pixels[0] = (0, 0, 2)
    time.sleep(3)
