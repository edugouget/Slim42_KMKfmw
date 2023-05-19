## RIGHT
print("Starting")

from kb import KMKKeyboard
import board
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmK.handlers.sequences import send_string, simple_key_sequence
from kmk.modules.split import Split, SplitSide, SplitType

keyboard = KMKKeyboard()

print("RGB")
from kmk.extensions.RGB import RGB
pixel_pin = board.GP7 ######### GP7
num_pixels = 21
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
BLACK = (0, 0, 0)
rgb2 = RGB(pixel_pin=board.GP23, num_pixels=1, hue_default = 255, sat_default=0, val_default=1)
rgb = RGB(pixel_pin=pixel_pin, num_pixels=num_pixels, hue_default = 0, sat_default=0, val_default=17)
keyboard.extensions.append(rgb2)
keyboard.extensions.append(rgb)

def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*255
    v = mx*255
    h = h*255/360
    return int(h), int(s), int(v)

print("Layers")
#from kmk.modules.layers import Layers
from kmk.modules.layers import Layers as _Layers
class Layers(_Layers):
    last_top_layer = 0
    LADO = 1 # 0-Left 1-Right
    cor_map = [
        [0 , 1 , 2 , 3 , 4 , 5,
         6 , 7 , 8 , 9 , 10 ,11,
         12, 13, 14, 15, 16, 17,
                     18, 19, 20],
        
        [15, 16, 17, 18, 19, 20,
         9 , 10 ,11, 12, 13, 14,
         3 , 4 , 5,  6 , 7 , 8 ,
         0 , 1 , 2 ]
        ]
    cor_camada = [
        [#### LEFT
        [# COLEMAK
         RED,CYAN,CYAN,CYAN,CYAN,CYAN,
         BLACK,CYAN,CYAN,CYAN,CYAN,CYAN,
         RED,CYAN,CYAN,CYAN,CYAN,CYAN,
                 YELLOW,YELLOW,YELLOW
         ],
        [# QWERT
         RED,CYAN,CYAN,CYAN,CYAN,CYAN,
         BLACK,CYAN,CYAN,CYAN,CYAN,CYAN,
         RED,CYAN,CYAN,CYAN,CYAN,CYAN,
                 PURPLE,PURPLE,PURPLE
         ],
        [# FN1
         RED,BLACK,BLACK,BLUE,YELLOW,GREEN,
         BLACK,BLUE,CYAN,YELLOW,YELLOW,GREEN,
         RED,CYAN,CYAN,CYAN,BLUE,BLUE,
                    BLUE,BLUE,BLUE
         ],
        [# FN2
         RED,CYAN,CYAN,CYAN,CYAN,CYAN,
         BLACK,GREEN,GREEN,GREEN,GREEN,GREEN,
         RED,CYAN,CYAN,BLUE,BLUE,BLACK,
                     GREEN,GREEN,GREEN
         ],
        [# NUMPAD / EXCEL
         RED,CYAN,CYAN,CYAN,RED,RED,
         BLACK,CYAN,CYAN,CYAN,RED,RED,
         RED,CYAN,CYAN,CYAN,CYAN,BLACK,
                        RED,RED,RED
         ],
        [# GAME
         RED,CYAN,CYAN,CYAN,CYAN,CYAN,
         BLACK,CYAN,CYAN,CYAN,CYAN,CYAN,
         RED,CYAN,CYAN,CYAN,CYAN,CYAN,
                       CYAN,CYAN,CYAN
         ]],
        
        [ #### RIGHT
        [ # COLEMAK
         CYAN,CYAN,CYAN,CYAN,CYAN,RED,
         CYAN,CYAN,CYAN,CYAN,CYAN,CYAN,
         CYAN,CYAN,CYAN,CYAN,CYAN,CYAN,
         YELLOW,YELLOW,YELLOW
         ],
        [ # QWERTY
         CYAN,CYAN,CYAN,CYAN,CYAN,RED,
         CYAN,CYAN,CYAN,CYAN,CYAN,CYAN,
         CYAN,CYAN,CYAN,CYAN,CYAN,CYAN,
         PURPLE,PURPLE,PURPLE
         ],
        [ #FN1
         CYAN,CYAN,GREEN,GREEN,RED,RED,
         GREEN,GREEN,GREEN,GREEN,GREEN,CYAN,
         RED,RED,CYAN,CYAN,RED,RED,
         BLUE,BLUE,BLUE
         ],
        [ #FN2
         GREEN,GREEN,GREEN,GREEN,RED,RED,
         BLACK,BLACK,BLACK,BLACK,BLACK,CYAN,
         BLACK,BLACK,BLACK,RED,BLACK,BLACK,
         GREEN,GREEN,GREEN
         ],
         [ # NUMPAD / EXCEL
         CYAN, RED,  CYAN,BLUE,RED,  RED,
         RED,  RED,  RED, BLUE,BLACK,CYAN,
         BLACK,BLACK,CYAN,CYAN,CYAN, CYAN,
         RED,  RED,  RED
         ],
        [ # GAME
         CYAN,RED,CYAN,BLUE,CYAN,CYAN,
         RED, RED,RED, BLUE,CYAN,RED,
         CYAN,CYAN,CYAN,CYAN,CYAN,CYAN,
         CYAN,CYAN,CYAN
         ]
            ]
        ]
    def after_hid_send(self, keyboard):
        if keyboard.active_layers[0] != self.last_top_layer:
            if rgb.enable:
                self.last_top_layer = keyboard.active_layers[0]
                tmp = 0
                for x in self.cor_camada[self.LADO][self.last_top_layer]:
                    h, s, v = rgb_to_hsv(x[0],x[1],x[2])
                    if tmp != 6 or (tmp == 6 and self.LADO == 1):
                        if (h+s) == 0:
                            rgb.set_hsv(0, 0, 0, self.cor_map[self.LADO][tmp])
                        else:
                            rgb.set_hsv(h, s, rgb.val, self.cor_map[self.LADO][tmp])
                    tmp += 1
                rgb2.set_hsv(h, s, 3, 0)
            else:
                rgb2.set_hsv(0, 0, 0, 0)

#############################
from kmk.modules.modtap import ModTap
modtap = ModTap()
print("Modtap")
keyboard.modules.append(modtap)

print("Media keys")
from kmk.extensions.media_keys import MediaKeys
keyboard.extensions.append(MediaKeys())
#############################
print("Tap Dance")
from kmk.modules.tapdance import TapDance
tapdance = TapDance()
tapdance.tap_time = 750
keyboard.modules.append(tapdance)
#############################
print("LED Caps")
import digitalio
from kmk.extensions.lock_status import LockStatus
from kmk.extensions.LED import LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True
leds = LED(led_pin=[board.GP26])
class LEDLockStatus(LockStatus):
    def set_lock_leds(self):
        if self.get_caps_lock():
            leds.set_brightness(50, leds=[0])
            #rgb.set_hsv(0, 255, 100, 6)
            #rgb2.set_hsv(0, 255, 2, 0)
        else:
            leds.set_brightness(0, leds=[0])
            #rgb.set_hsv(0, 0, 0, 6)
            #rgb2.set_hsv(0, 0, 0, 0)
    def after_hid_send(self, sandbox):
        super().after_hid_send(sandbox)  # Critically important. Do not forget
        #if self.report_updated:
        self.set_lock_leds()
keyboard.extensions.append(leds)
keyboard.extensions.append(LEDLockStatus())
############################# SPLIT #############################
print("Split")
split = Split(
    #split_target_left=True,
    data_pin = board.GP1,
    data_pin2 = board.GP0,
    split_side = SplitSide.RIGHT,
    use_pio=True
)
keyboard.modules.append(split)

################################################################
print("Modulo Layers")
keyboard.modules.append(Layers())

def flattenList(nestedList):
    if not(bool(nestedList)):
        return nestedList
    if isinstance(nestedList[0], list):
        return flattenList(*nestedList[:1]) + flattenList(nestedList[1:])
    return nestedList[:1] + flattenList(nestedList[1:])
ESPERA = KC.MACRO_SLEEP_MS(500)
CTRLALTDEL = KC.LCTL(KC.LALT(KC.DEL))
WOW3 = simple_key_sequence((send_string("senha3"), ESPERA , KC.ENTER))
WOW4 = simple_key_sequence((send_string("login2"), ESPERA, KC.TAB ,ESPERA, send_string("senha3") , ESPERA , KC.ENTER))
WOW6 = simple_key_sequence((send_string("senha1"), ESPERA , KC.ENTER)) # senha1
WOW7 = simple_key_sequence((send_string("login1"), ESPERA , KC.ENTER, ESPERA , send_string("senha1"), ESPERA , KC.ENTER))
WOW8 = simple_key_sequence((send_string("senha2"), KC.ENTER)) #
NOME = send_string("nome1")
CPF = send_string("id")

NOME1 = send_string("nome2")
NOME2 = send_string("nome3")
NOME3 = send_string("nome4")
NOME4 = send_string("nome5")

end1 = send_string("Address1")
end2 =send_string("Address2")
end3 =send_string("Address3")
end4 =send_string("Address4")
ENDERECO = simple_key_sequence((end1, KC.INT1, end2))
ENDERECO2 = simple_key_sequence((end3, KC.INT1, end4))

ESPERA1 = KC.MACRO_SLEEP_MS(300)
ESPERA2 = KC.MACRO_SLEEP_MS(100)
TAB = simple_key_sequence((KC.TAB,ESPERA2))
SEL_NOME = simple_key_sequence((KC['E'],ESPERA,KC['E'],ESPERA,KC['E'],ESPERA,KC['E'],ESPERA,KC['E'],ESPERA,KC['E'],ESPERA,KC['E']))
EMAIL = send_string('email1')
EMAILH = send_string('email2')

EMAIL1 = send_string('xx@gmail.com')
EMAIL2 = send_string('yyy@gmail.com')
EMAIL3 = send_string('zzt@gmail.com')
TELEFONE = send_string('tel')

"""from random import randint
INICIO = ''+chr(ord('0') + randint(0, 4))
FIM = ''+chr(ord('9') - randint(0, 4))
HPR1 = simple_key_sequence((send_string('065'),ESPERA2,KC[FIM],TAB,send_string('Entrada'),TAB,TAB,TAB,TAB,TAB,send_string('170'),ESPERA2,KC[INICIO],TAB,send_string('Saida')))
HPR2 = simple_key_sequence((send_string('065'),ESPERA2,KC[FIM],TAB,send_string('Entrada'),TAB,TAB,TAB,TAB,TAB,send_string('160'),ESPERA2,KC[INICIO],TAB,send_string('Saida')))
CHEKL = simple_key_sequence((TAB, ESPERA1 , SEL_NOME , ESPERA1 , TAB,KC['B'], TAB, KC['U'], TAB, ESPERA1,KC['H'],ESPERA1,KC['H'],ESPERA1,TAB,KC['N'],ESPERA1,TAB,KC.SPACE,KC.ENTER,ESPERA1,TAB,EMAIL))
#MEXC1 = simple_key_sequence((KC.LALT(), ESPERA1 , send_string('JDGGR')))
"""

PCOM = send_string(".com")
PCOMBR = send_string(".com.br")
#TD1 = KC.TD(HPR1, HPR2, CHEKL)
TD2 = KC.TD(CTRLALTDEL, WOW3, WOW4, EMAILH)
TD3 = KC.TD(WOW6, WOW7, WOW8)
TD4 = KC.TD(NOME, CPF, EMAIL, ENDERECO2)
TD5 = KC.TD(PCOM, PCOMBR)
COLEMAK = KC.TO(0)
QWERTY =  KC.TO(1)
FN1    =  KC.MO(2)
FN2    =  KC.MO(3)
NUMPAD =  KC.TO(4)
GAME   =  KC.TO(5)
WPTRSCR = KC.LSFT(KC.LWIN(KC.S))

RGB_TOG = KC.RGB_TOG
RGB_VAI = KC.RGB_VAI
RGB_VAD = KC.RGB_VAD

print("Combos")
from kmk.modules.combos import Combos, Chord, Sequence
combos = Combos()
keyboard.modules.append(combos)

combos.combos = [
    Chord((KC.A, KC.J), EMAIL),
    Chord((KC.R, KC.J), TELEFONE),
    Chord((KC.A, KC.L), NOME),
    Chord((KC.A, KC.U), CPF),
    Chord((KC.A, KC.Y), ENDERECO2),
    Chord((KC.A, KC.M), NOME1),
    Chord((KC.A, KC.N), NOME2),
    Chord((KC.A, KC.E), NOME3),
    Chord((KC.A, KC.I), NOME4),
    Chord((KC.R, KC.M), EMAIL1),
    Chord((KC.R, KC.N), EMAIL2),
    Chord((KC.R, KC.E), EMAIL3),
]

print("Ok")
keyboard.keymap = [
   [ # COLEMAK
     KC.GRV  , KC.Q    , KC.W    , KC.F    , KC.P    , KC.B    , KC.SPC      , KC.ENT      , KC.J    , KC.L    , KC.U    , KC.Y    , KC.SCLN , KC.LBRC ,
     KC.LSFT , KC.A    , KC.R    , KC.S    , KC.T    , KC.G    , FN1         , FN2         , KC.M    , KC.N    , KC.E    , KC.I    , KC.O    , KC.QUOT ,
     KC.LCTL , KC.Z    , KC.X    , KC.C    , KC.D    , KC.V    , KC.LGUI     , KC.RALT     , KC.K    , KC.H    , KC.COMM , KC.DOT  , KC.SLSH , KC.INT1  ],
    [ # QWERTY
     KC.GRV  , KC.Q    , KC.W    , KC.E    , KC.R    , KC.T    , KC.SPC      , KC.ENT      , KC.Y    , KC.U    , KC.I    , KC.O    , KC.P    , KC.LBRC ,
     KC.LSFT , KC.A    , KC.S    , KC.D    , KC.F    , KC.G    , FN1         , FN2         , KC.H    , KC.J    , KC.K    , KC.L    , KC.SCLN , KC.QUOT ,
     KC.LCTL , KC.Z    , KC.X    , KC.C    , KC.V    , KC.B    , KC.LGUI     , KC.RALT     , KC.N    , KC.M    , KC.COMM , KC.DOT  , KC.SLSH , KC.INT1  ],
    [ # FN1
     KC.ESC  , KC.NO     , KC.NO   , KC.MPLY , KC.VOLU , KC.BRIU , KC.SPC      , KC.ENT      , KC.F10  , KC.F11  , KC.MINS , KC.EQL  , KC.DEL  , KC.BSPC ,
     KC.LALT , TD4     , WPTRSCR , KC.MUTE , KC.VOLD , KC.BRID , KC.TRNS     , KC.TRNS     , KC.N6   , KC.N7   , KC.N8   , KC.N9   , KC.N0   , KC.NUBS ,
     KC.TAB  , RGB_TOG , RGB_VAI   , RGB_VAD   , TD3     , TD2     , KC.LGUI     , KC.RALT     , KC.PGUP , KC.PGDN , KC.LEFT , KC.RGHT , KC.UP   , KC.DOWN  ],
    [ # FN2
     KC.ESC  , KC.F1   , KC.F2   , KC.F3   , KC.F4   , KC.F5   , KC.SPC      , KC.ENT      , COLEMAK , QWERTY  , NUMPAD  , GAME    , KC.DEL  , KC.BSPC ,
     KC.CAPS , KC.N1   , KC.N2   , KC.N3   , KC.N4   , KC.N5   , KC.TRNS     , KC.TRNS     , KC.NO   , KC.NO   , KC.NO   , KC.NO   , KC.NO   , KC.NUBS ,
     KC.TAB  , KC.RBRC , KC.BSLS , KC.HOME , KC.END  , KC.NO   , KC.LGUI     , KC.RALT     , KC.NO   , KC.NO   , KC.NO   , TD5     , KC.NO   , KC.NO    ],
    [ # NUMPAD / EXCEL
     KC.ESC  , KC.N1   , KC.N2   , KC.N3   , KC.MINS , KC.EQL  , KC.SPC      , KC.ENT      , KC.HOME , KC.UP   , KC.END  , KC.PGUP , KC.DEL  , KC.BSPC ,
     KC.LSFT , KC.N4   , KC.N5   , KC.N6   , KC.PPLS , KC.INT1 , FN1         , FN2         , KC.LEFT , KC.DOWN , KC.RGHT , KC.PGDN , KC.NO   , KC.NUBS ,
     KC.LCTL , KC.N7   , KC.N8   , KC.N9   , KC.N0   , KC.NO   , KC.LGUI     , KC.RALT     , KC.NO   , KC.NO   , KC.COMM , KC.DOT  , KC.SLSH , KC.INT1  ],
    [ # GAME
     KC.ESC  , KC.Q    , KC.W    , KC.E    , KC.R    , KC.N1   , KC.SPC      , KC.ENT      , KC.HOME , KC.UP   , KC.END  , KC.PGUP , KC.N8   , KC.NO   ,
     KC.LSFT , KC.A    , KC.S    , KC.D    , KC.F    , KC.N2   , FN1         , FN2         , KC.LEFT , KC.DOWN , KC.RGHT , KC.PGDN , KC.N9   , KC.RCTL ,
     KC.LCTL , KC.Z    , KC.X    , KC.C    , KC.V    , KC.N3   , KC.LGUI     , KC.RALT     , KC.N4   , KC.N5   , KC.N6   , KC.N7   , KC.N0   , KC.RSFT  ]
]



if __name__ == '__main__':
    keyboard.go()
