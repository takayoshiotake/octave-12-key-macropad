import collections
import math
import time

import board
import digitalio
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
from neopixel import NeoPixel

from octave_pcb.key_matrix import KeyMatrix

SCAN_KEY_MATRIX_INTERVAL = 0.01
LED_INTERVAL = 0.05


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
  LAYER_ALTERNATE = 4
  LAYER_SWITCH = 5
  CONSUMER_CONTROL = 6


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
        KeyAssignment(CodeType.KEYBOARD, Keycode.SHIFT),
        KeyAssignment(CodeType.KEYBOARD, Keycode.CONTROL),
        KeyAssignment(CodeType.KEYBOARD, Keycode.ESCAPE),
        KeyAssignment(CodeType.LAYER_MOMENTRY, None),
    ],
    [
        KeyAssignment(CodeType.KEYBOARD, Keycode.F9),
        KeyAssignment(CodeType.KEYBOARD, Keycode.F10),
        KeyAssignment(CodeType.KEYBOARD, Keycode.F11),
        KeyAssignment(CodeType.KEYBOARD, Keycode.F12),
        KeyAssignment(CodeType.CONSUMER_CONTROL,
                      ConsumerControlCode.VOLUME_DECREMENT),
        KeyAssignment(CodeType.CONSUMER_CONTROL,
                      ConsumerControlCode.VOLUME_INCREMENT),
        KeyAssignment(CodeType.CONSUMER_CONTROL, ConsumerControlCode.REWIND),
        KeyAssignment(CodeType.CONSUMER_CONTROL,
                      ConsumerControlCode.FAST_FORWARD),
        KeyAssignment(CodeType.KEYBOARD, Keycode.SHIFT),
        KeyAssignment(CodeType.KEYBOARD, Keycode.CONTROL),
        KeyAssignment(CodeType.KEYBOARD, Keycode.ESCAPE),
        None,
    ],
    # # Switch
    # [
    #     KeyAssignment(CodeType.MOUSE_MOVE, {'x': -1}),
    #     KeyAssignment(CodeType.MOUSE_MOVE, {'y': 1}),
    #     KeyAssignment(CodeType.MOUSE_MOVE, {'y': -1}),
    #     KeyAssignment(CodeType.MOUSE_MOVE, {'x': 1}),
    #     KeyAssignment(CodeType.KEYBOARD, Keycode.LEFT_ARROW),
    #     KeyAssignment(CodeType.KEYBOARD, Keycode.DOWN_ARROW),
    #     KeyAssignment(CodeType.KEYBOARD, Keycode.UP_ARROW),
    #     KeyAssignment(CodeType.KEYBOARD, Keycode.RIGHT_ARROW),
    #     KeyAssignment(CodeType.MOUSE_BUTTON, Mouse.LEFT_BUTTON),
    #     KeyAssignment(CodeType.MOUSE_BUTTON, Mouse.RIGHT_BUTTON),
    #     KeyAssignment(CodeType.LAYER_SWITCH, None),
    #     KeyAssignment(CodeType.LAYER_SWITCH, None),
    # ],
    # [
    #     None,
    #     None,
    #     None,
    #     None,
    #     None,
    #     None,
    #     None,
    #     None,
    #     None,
    #     None,
    #     None,
    #     None,
    # ],
]

pixpower = digitalio.DigitalInOut(board.NEOPIX_POWER)
pixpower.switch_to_output(True, digitalio.DriveMode.PUSH_PULL)
pixels = NeoPixel(board.NEOPIX, 1, auto_write=True)
pixels[0] = (0, 0, 2)
pixels_under_keys = NeoPixel(board.GPIO20, 12, auto_write=False)
pixels_under_keys.show()

key_matrix = KeyMatrix()

time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
while True:
  try:
    consumer_control = ConsumerControl(usb_hid.devices)
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayoutUS(keyboard)
    mouse = Mouse(usb_hid.devices)
    pixels[0] = (0, 2, 2)

    key_map_layer = 0
    key_event_planners = [KeyEventPlanner()
                          for _ in range(len(key_matrix.row_ios) * len(key_matrix.col_ios))]
    pressed_keys = [None for _ in range(len(key_event_planners))]
    scan_key_matrix_timing = time.monotonic()  # For debounce
    led_timing = time.monotonic()  # For debounce
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
            elif key_assignment.type == CodeType.LAYER_ALTERNATE:
              # xxx
              KEY_MAP_LAYERS[0], KEY_MAP_LAYERS[1] = KEY_MAP_LAYERS[1], KEY_MAP_LAYERS[0]
            elif key_assignment.type == CodeType.LAYER_SWITCH:
              # xxx
              KEY_MAP_LAYERS[0], KEY_MAP_LAYERS[2] = KEY_MAP_LAYERS[2], KEY_MAP_LAYERS[0]
              KEY_MAP_LAYERS[1], KEY_MAP_LAYERS[3] = KEY_MAP_LAYERS[3], KEY_MAP_LAYERS[1]
            elif key_assignment.type == CodeType.KEYBOARD:
              keyboard.press(key_assignment.code)
            elif key_assignment.type == CodeType.MOUSE_MOVE:
              mouse.move(**key_assignment.code)
            elif key_assignment.type == CodeType.MOUSE_BUTTON:
              mouse.press(key_assignment.code)
            elif key_assignment.type == CodeType.CONSUMER_CONTROL:
              consumer_control.press(key_assignment.code)
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
            elif key_assignment.type == CodeType.CONSUMER_CONTROL:
              consumer_control.release()

        scan_key_matrix_timing += SCAN_KEY_MATRIX_INTERVAL
        if scan_key_matrix_timing <= current_time:
          scan_key_matrix_timing = current_time + SCAN_KEY_MATRIX_INTERVAL

      if current_time >= led_timing:

        for i in range(len(pixels_under_keys)):
          if are_keys_pressed[i]:
            pixels_under_keys[i] = [
                (255, 0, 0),
                (255, 128, 0),
                (255, 255, 0),
                (128, 255, 0),
                (0, 255, 0),
                (0, 255, 128),
                (0, 255, 255),
                (0, 128, 255),
                (0, 0, 255),
                (128, 0, 255),
                (255, 0, 255),
                (255, 0, 128),
            ][i]
          elif pixels_under_keys[i] != (0, 0, 0):
            pixels_under_keys[i] = (
                math.floor(pixels_under_keys[i][0] * 0.8),
                math.floor(pixels_under_keys[i][1] * 0.8),
                math.floor(pixels_under_keys[i][2] * 0.8))

        pixels_under_keys.show()

        led_timing += LED_INTERVAL
        if led_timing <= current_time:
          led_timing = current_time + LED_INTERVAL

  except Exception:
    pixels[0] = (0, 0, 2)
    time.sleep(3)
