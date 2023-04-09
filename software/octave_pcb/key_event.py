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
