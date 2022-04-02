import time

import board
import digitalio
from neopixel import NeoPixel


class KnobStatus():
    IDLE = 0
    CW_BEGINNING = 1
    CW_CANDIDATE = 2
    CCW_BEGINNING = 3
    CCW_CANDIDATE = 4


DIO_HIGH = True
DIO_LOW = False


print("Hello, Octave!")

pixels = NeoPixel(board.NEOPIXEL, 1, auto_write=True)
pixels[0] = (0, 0, 1)

# Turns off the USER LED
led_pins = [board.LED_RED, board.LED_GREEN, board.LED_BLUE]
led_ios = [digitalio.DigitalInOut(pin) for pin in led_pins]
for led_io in led_ios:
    led_io.switch_to_input(digitalio.Pull.UP)


row_pins = [board.D6, board.D5, board.D3, board.D7]
row_ios = [digitalio.DigitalInOut(pin) for pin in row_pins]
for row_io in row_ios:
    row_io.switch_to_output(DIO_HIGH, digitalio.DriveMode.OPEN_DRAIN)

col_pins = [board.D2, board.D1, board.D0, board.D4]
col_ios = [digitalio.DigitalInOut(pin) for pin in col_pins]
for col_io in col_ios:
    col_io.switch_to_input(digitalio.Pull.UP)

knob_a = digitalio.DigitalInOut(board.D8)
knob_a.switch_to_input(digitalio.Pull.UP)
knob_b = digitalio.DigitalInOut(board.D10)
knob_b.switch_to_input(digitalio.Pull.UP)


def select_row(row):
    # Once deselect all rows
    for row_io in row_ios:
        row_io.value = DIO_HIGH
    if 0 <= row <= len(row_ios):
        row_ios[row].value = DIO_LOW


keys_state = [{'is_pressed': False}
              for _ in range(len(row_ios) * len(col_ios))]
previous_knob_signals = None
knob_state = KnobStatus.IDLE
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

    knob_signals = [knob_a.value, knob_b.value]
    if knob_signals != previous_knob_signals:
        #   0     1     2     3     0'
        # [H,H] [L,H] [L,L] [H,L] [H,H] => CW
        # [H,H] [H,L] [L,L] [L,H] [H,H] => CCW
        # print(f"""knob_signals: {knob_signals[0]}, {knob_signals[1]}""")
        if knob_signals == [True, True]:
            if knob_state == KnobStatus.CW_CANDIDATE:
                print(f"""rotated : CW""")
            elif knob_state == KnobStatus.CCW_CANDIDATE:
                print(f"""rotated : CCW""")
            knob_state = KnobStatus.IDLE
        elif knob_signals == [False, True]:
            if knob_state == KnobStatus.IDLE:
                knob_state = KnobStatus.CW_BEGINNING
            elif knob_state == KnobStatus.CW_CANDIDATE:
                knob_state = KnobStatus.CW_BEGINNING
            elif knob_state == KnobStatus.CCW_BEGINNING:
                knob_state = KnobStatus.CCW_CANDIDATE
        elif knob_signals == [True, False]:
            if knob_state == KnobStatus.IDLE:
                knob_state = KnobStatus.CCW_BEGINNING
            elif knob_state == KnobStatus.CW_BEGINNING:
                knob_state = KnobStatus.CW_CANDIDATE
            elif knob_state == KnobStatus.CCW_CANDIDATE:
                knob_state = KnobStatus.CCW_BEGINNING
        # elif knob_signals == [False, False]:
        #     if knob_state == KnobStatus.CW_BEGINNING:
        #         knob_state = KnobStatus.CW_CANDIDATE
        #     elif knob_state == KnobStatus.CCW_BEGINNING:
        #         knob_state = KnobStatus.CCW_CANDIDATE
    previous_knob_signals = knob_signals

    # time.sleep(0.01)
