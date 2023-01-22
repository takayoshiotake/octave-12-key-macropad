import board
import digitalio


class RotaryEncoder:

  class Status():
    IDLE = 0
    CW_BEGINNING = 1
    CW_CANDIDATE = 2
    CCW_BEGINNING = 3
    CCW_CANDIDATE = 4

  def __init__(self):
    self.io_a = digitalio.DigitalInOut(board.GPIO3)
    self.io_a.switch_to_input(digitalio.Pull.UP)
    self.io_b = digitalio.DigitalInOut(board.GPIO2)
    self.io_b.switch_to_input(digitalio.Pull.UP)

    self.previous_signals = None
    self.state = RotaryEncoder.Status.IDLE

  def deinit(self):
    self.io_a.deinit()
    self.io_b.deinit()

  def detect_direction(self):
    detected_direction = 0
    signals = [self.io_a.value, self.io_b.value]
    if signals != self.previous_signals:
      #   0     1     2     3     0'
      # [H,H] [L,H] [L,L] [H,L] [H,H] => CW
      # [H,H] [H,L] [L,L] [L,H] [H,H] => CCW
      if signals == [True, True]:
        if self.state == RotaryEncoder.Status.CW_CANDIDATE:
          detected_direction = 1
        elif self.state == RotaryEncoder.Status.CCW_CANDIDATE:
          detected_direction = -1
        self.state = RotaryEncoder.Status.IDLE
      elif signals == [False, True]:
        if self.state == RotaryEncoder.Status.IDLE:
          self.state = RotaryEncoder.Status.CW_BEGINNING
        elif self.state == RotaryEncoder.Status.CW_CANDIDATE:
          self.state = RotaryEncoder.Status.CW_BEGINNING
        elif self.state == RotaryEncoder.Status.CCW_BEGINNING:
          self.state = RotaryEncoder.Status.CCW_CANDIDATE
      elif signals == [True, False]:
        if self.state == RotaryEncoder.Status.IDLE:
          self.state = RotaryEncoder.Status.CCW_BEGINNING
        elif self.state == RotaryEncoder.Status.CW_BEGINNING:
          self.state = RotaryEncoder.Status.CW_CANDIDATE
        elif self.state == RotaryEncoder.Status.CCW_CANDIDATE:
          self.state = RotaryEncoder.Status.CCW_BEGINNING
        elif signals == [False, False]:
          if self.state == RotaryEncoder.Status.CW_BEGINNING:
            self.state = RotaryEncoder.Status.CW_CANDIDATE
          elif self.state == RotaryEncoder.Status.CCW_BEGINNING:
            self.state = RotaryEncoder.Status.CCW_CANDIDATE
    self.previous_signals = signals
    return detected_direction
