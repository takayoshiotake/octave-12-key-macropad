import time

import board
import digitalio

DIGITALIO_HIGH = True
DIGITALIO_LOW = False


class KeyMatrix:
  def __init__(self):
    row_pins = [board.D6, board.D5, board.D3, board.D7]
    self.row_ios = [digitalio.DigitalInOut(pin) for pin in row_pins]
    for row_io in self.row_ios:
      row_io.switch_to_output(DIGITALIO_HIGH, digitalio.DriveMode.OPEN_DRAIN)

    col_pins = [board.D2, board.D1, board.D0, board.D4]
    self.col_ios = [digitalio.DigitalInOut(pin) for pin in col_pins]
    for col_io in self.col_ios:
      col_io.switch_to_input(digitalio.Pull.UP)

  def deinit(self):
    self.select_row(-1)
    for row_io in self.row_ios:
      row_io.deinit()
    for col_io in self.col_ios:
      col_io.deinit()

  def select_row(self, row):
    # Once deselect all rows
    for row_io in self.row_ios:
      row_io.value = DIGITALIO_HIGH
    if 0 <= row <= len(self.row_ios):
      self.row_ios[row].value = DIGITALIO_LOW

  def scan_matrix(self):
    are_keys_pressed = []
    for row in range(len(self.row_ios)):
      self.select_row(row)
      are_keys_pressed.extend(
          [True if col_io.value == DIGITALIO_LOW else False for col_io in self.col_ios]
      )
      time.sleep(0.001)
    return are_keys_pressed
