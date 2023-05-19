## LEFT
import board
from kmk.modules.split import SplitSide
from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (board.GP10,
                board.GP11,
                board.GP12,
                board.GP13,
                board.GP14,
                board.GP15,
                board.GP16
                )
    row_pins = (board.GP17,
				board.GP18,
                board.GP19)
    diode_orientation = DiodeOrientation.COL2ROW
    led_key_pos=[
        0,2
        ]
    brightness_limit = 1.0
    num_pixels = 3


"""
UART0_TX Pin is GPIO 0 (GP0)
UART0_RX Pin is GPIO 1 (GP1)
"""
