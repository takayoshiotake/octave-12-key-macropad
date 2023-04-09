import collections
import math
import random
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

from octave_pcb.key_event import KeyEvent, KeyEventPlanner
from octave_pcb.key_matrix import KeyMatrix


class CodeType:
  KEYBOARD = 0
  MOUSE_MOVE = 1
  MOUSE_BUTTON = 2
  CONSUMER_CONTROL = 3
  LAYER_MOMENTRY = 4


KeyAssignment = collections.namedtuple('KeyAssignment', ['type', 'code'])
LambdaAssignment = collections.namedtuple('LambdaAssignment', ['on_press', 'on_release'])


SCAN_KEY_MATRIX_INTERVAL = 0.01
PIXELS_INTERVAL = 0.05
PIXELS_PATTEN_COUNT = 3

pixels_pattern = 0
pixels_frame_count = 0
pixels_target = [[0.0, 0.0, 0.0] for _ in range(12)]
pixels_current = [[0.0, 0.0, 0.0] for _ in range(12)]


def next_pixels_pattern():
  global pixels_pattern
  global pixels_frame_count
  pixels_pattern = (pixels_pattern + 1) % PIXELS_PATTEN_COUNT
  pixels_frame_count = 0


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
        KeyAssignment(CodeType.CONSUMER_CONTROL, ConsumerControlCode.VOLUME_DECREMENT),
        KeyAssignment(CodeType.CONSUMER_CONTROL, ConsumerControlCode.VOLUME_INCREMENT),
        KeyAssignment(CodeType.CONSUMER_CONTROL, ConsumerControlCode.REWIND),
        KeyAssignment(CodeType.CONSUMER_CONTROL, ConsumerControlCode.FAST_FORWARD),
        KeyAssignment(CodeType.KEYBOARD, Keycode.SHIFT),
        KeyAssignment(CodeType.KEYBOARD, Keycode.CONTROL),
        LambdaAssignment(next_pixels_pattern, None),
        None,
    ],
]


def update_pixels_according_to_key_presses(pixels, are_keys_pressed):
  for i in range(len(pixels)):
    if are_keys_pressed[i]:
      pixels[i] = [
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
    elif pixels[i] != (0, 0, 0):
      pixels[i] = (
          math.floor(pixels[i][0] * 0.8),
          math.floor(pixels[i][1] * 0.8),
          math.floor(pixels[i][2] * 0.8))


def update_pixels_transition(pixels):
  global pixels_frame_count
  global pixels_target
  global pixels_current
  if pixels_frame_count % 60 == 0:
    pixels_target[0][random.randint(0, 2)] = 0.5
    pixels_target[0][random.randint(0, 2)] = 0
    pixels_target[0][random.randint(0, 2)] = 0
    pixels_target[0][random.randint(0, 2)] = 1
  pixels_current[0][0] = pixels_current[0][0] * 0.97 + pixels_target[0][0] * 0.03
  pixels_current[0][1] = pixels_current[0][1] * 0.97 + pixels_target[0][1] * 0.03
  pixels_current[0][2] = pixels_current[0][2] * 0.97 + pixels_target[0][2] * 0.03
  for i in range(len(pixels)):
    pixels[i] = (
        math.floor(pixels_current[0][0] * 32),
        math.floor(pixels_current[0][1] * 32),
        math.floor(pixels_current[0][2] * 32))
  pixels_frame_count += 1
  pixels_frame_count = pixels_frame_count % 60


def update_pixels_random(pixels):
  global pixels_frame_count
  global pixels_target
  global pixels_current
  for i in range(len(pixels)):
    if pixels_frame_count % 60 == 0:
      pixels_target[i][random.randint(0, 2)] = 0.5
      pixels_target[i][random.randint(0, 2)] = 0
      pixels_target[i][random.randint(0, 2)] = 0
      pixels_target[i][random.randint(0, 2)] = 1
    pixels_current[i][0] = pixels_current[i][0] * 0.9 + pixels_target[i][0] * 0.1
    pixels_current[i][1] = pixels_current[i][1] * 0.9 + pixels_target[i][1] * 0.1
    pixels_current[i][2] = pixels_current[i][2] * 0.9 + pixels_target[i][2] * 0.1
    pixels[i] = (
        math.floor(pixels_current[i][0] * 32),
        math.floor(pixels_current[i][1] * 32),
        math.floor(pixels_current[i][2] * 32))
  pixels_frame_count += 1
  pixels_frame_count = pixels_frame_count % 60


if __name__ == '__main__':
  key_matrix = KeyMatrix()
  key_event_planners = [KeyEventPlanner() for _ in range(len(key_matrix.row_ios) * len(key_matrix.col_ios))]

  cpu_pixpower = digitalio.DigitalInOut(board.NEOPIX_POWER)
  cpu_pixpower.switch_to_output(True, digitalio.DriveMode.PUSH_PULL)
  cpu_pix = NeoPixel(board.NEOPIX, 1, auto_write=True)
  cpu_pix[0] = (0, 0, 2)

  pixels = NeoPixel(board.GPIO20, 12, auto_write=False)
  pixels.show()
  pixels_target = [[0.0, 0.0, 0.0] for _ in range(12)]
  pixels_current = [[0.0, 0.0, 0.0] for _ in range(12)]
  pixels_frame_count = 0
  pixels_pattern = 0

  # Sleep for a bit to avoid a race condition on some systems
  time.sleep(1)

  while True:
    try:
      keyboard = Keyboard(usb_hid.devices)
      keyboard_layout = KeyboardLayoutUS(keyboard)
      mouse = Mouse(usb_hid.devices)
      consumer_control = ConsumerControl(usb_hid.devices)
      cpu_pix[0] = (0, 2, 2)

      key_map_layer = 0
      pressed_keys = [None for _ in range(len(key_event_planners))]

      scan_key_matrix_timing = time.monotonic()  # For debounce
      pixels_timing = time.monotonic()  # For animation
      while True:
        current_time = time.monotonic()

        if current_time >= scan_key_matrix_timing:
          are_keys_pressed = key_matrix.scan_matrix()
          for i, key_event_planner in enumerate(key_event_planners):
            key_event = key_event_planner.make_event(
                current_time, are_keys_pressed[i])
            if key_event == KeyEvent.PRESS:
              # print(f"""pressed : {i}""")
              pressed_keys[i] = KEY_MAP_LAYERS[key_map_layer][i]
              key_assignment = pressed_keys[i]
              if key_assignment is None:
                pass
              elif isinstance(key_assignment, KeyAssignment):
                if key_assignment.type == CodeType.LAYER_MOMENTRY:
                  key_map_layer = 1
                elif key_assignment.type == CodeType.KEYBOARD:
                  keyboard.press(key_assignment.code)
                elif key_assignment.type == CodeType.MOUSE_MOVE:
                  mouse.move(**key_assignment.code)
                elif key_assignment.type == CodeType.MOUSE_BUTTON:
                  mouse.press(key_assignment.code)
                elif key_assignment.type == CodeType.CONSUMER_CONTROL:
                  consumer_control.press(key_assignment.code)
              elif isinstance(key_assignment, LambdaAssignment) and key_assignment.on_press is not None:
                key_assignment.on_press()
            elif key_event == KeyEvent.LONG_PRESS:
              # print(f"""pressed : {i}""")
              key_assignment = pressed_keys[i]
              if key_assignment is None:
                pass
              elif isinstance(key_assignment, KeyAssignment):
                if key_assignment.type == CodeType.LAYER_MOMENTRY:
                  pass
                elif key_assignment.type == CodeType.KEYBOARD:
                  # print(f"""pressed : {i}""")
                  keyboard.press(key_assignment.code)
                elif key_assignment.type == CodeType.MOUSE_MOVE:
                  # print(f"""pressed : {i}""")
                  mouse.move(**key_assignment.code)
            elif key_event == KeyEvent.RELEASE:
              # print(f"""released: {i}""")
              key_assignment = pressed_keys[i]
              pressed_keys[i] = None
              if key_assignment is None:
                pass
              elif isinstance(key_assignment, KeyAssignment):
                if key_assignment.type == CodeType.LAYER_MOMENTRY:
                  key_map_layer = 0
                elif key_assignment.type == CodeType.KEYBOARD:
                  keyboard.release(key_assignment.code)
                elif key_assignment.type == CodeType.MOUSE_BUTTON:
                  mouse.release(key_assignment.code)
                elif key_assignment.type == CodeType.CONSUMER_CONTROL:
                  consumer_control.release()
              elif isinstance(key_assignment, LambdaAssignment) and key_assignment.on_release is not None:
                key_assignment.on_release()
          scan_key_matrix_timing += SCAN_KEY_MATRIX_INTERVAL
          if scan_key_matrix_timing <= current_time:
            scan_key_matrix_timing = current_time + SCAN_KEY_MATRIX_INTERVAL

        if current_time >= pixels_timing:
          should_show_pixels = True
          if pixels_pattern == 0:
            prev_pixels = [pixel for pixel in pixels]
            update_pixels_according_to_key_presses(pixels, are_keys_pressed)
            should_show_pixels = not all(map(lambda i: pixels[i] == prev_pixels[i], range(12)))
          elif pixels_pattern == 1:
            update_pixels_transition(pixels)
          elif pixels_pattern == 2:
            update_pixels_random(pixels)

          if should_show_pixels:
            pixels.show()
          pixels_timing += PIXELS_INTERVAL
          if pixels_timing <= current_time:
            pixels_timing = current_time + PIXELS_INTERVAL

    except Exception:
      cpu_pix[0] = (0, 0, 2)
      time.sleep(3)
