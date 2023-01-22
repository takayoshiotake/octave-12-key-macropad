import storage

from octave_pcb.key_matrix import KeyMatrix

key_matrix = KeyMatrix()
are_keys_pressed = key_matrix.scan_matrix()
key_matrix.deinit()
is_usb_drive_enabled = are_keys_pressed[11]

if is_usb_drive_enabled:
  storage.remount("/", readonly=False)
  m = storage.getmount("/")
  m.label = "OCTAVE_CP"
  storage.remount("/", readonly=True)
  storage.enable_usb_drive()
else:
  storage.disable_usb_drive()
