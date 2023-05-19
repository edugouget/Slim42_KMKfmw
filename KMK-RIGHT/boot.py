import supervisor
import board
import digitalio
import storage
import usb_cdc
import usb_hid

from kb import KMKKeyboard
from kmk.scanners import DiodeOrientation

print("Desbloqueado para gravação USB")
storage.enable_usb_drive()
storage.remount("/", readonly=False, disable_concurrent_write_protection=True)
m = storage.getmount("/")
m.label = "KMK-RIGHT"
"""
usb_cdc.enable(console=True, data=True)

# If this key is held during boot, don't run the code which hides the storage and disables serial
# This will use the first row/col pin. Feel free to change it if you want it to be another pin
col = digitalio.DigitalInOut(KMKKeyboard.col_pins[0])
row = digitalio.DigitalInOut(KMKKeyboard.row_pins[0])

if KMKKeyboard.diode_orientation == DiodeOrientation.COLUMNS:
    col.switch_to_output(value=True)
    row.switch_to_input(pull=digitalio.Pull.DOWN)
else:
    col.switch_to_input(pull=digitalio.Pull.DOWN)
    row.switch_to_output(value=True)


if not row.value:
    storage.disable_usb_drive()
    # Equivalent to usb_cdc.enable(console=False, data=False)
    usb_cdc.disable()
    #usb_hid.enable((usb_hid.Device.KEYBOARD,),boot_device=1)
    storage.remount("/", False)
    print("Bloqueado para gravação USB")
else:
    print("Desbloqueado para gravação USB")
    storage.enable_usb_drive()
    storage.remount("/", readonly=False, disable_concurrent_write_protection=True)
    m = storage.getmount("/")
    m.label = "KMK-RIGHT"

row.deinit()
col.deinit()
"""
