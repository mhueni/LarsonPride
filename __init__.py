import badge
import binascii
import time
import ugfx
import hashlib

LARSON_FADE_STEPS = 0.05
larson_modes = ('nickname', 'ff0000', '00ff00', '0000ff', 'ffffff', 'pride')
larson_mode = 0
larson_n = 0
larson_i = 1
larson_fade = 0.3
larson_seq = [0, 0, 0, 0, 0, 0]

def home(pushed):
    if(pushed):
        print("go home")
        appglue.home()

def larson(idx, val):
    global badge, larson_mode, larson_modes
    color = larson_modes[larson_mode]
    if (color == 'pride'):
        color = ("750787", "004dff", "008026", "ffed00", "ff8c00", "e40303")[idx]
    if (color == 'nickname'):
        nickname = badge.nvs_get_str("owner", "name", "")
        nickname_colors = list(map(int,hashlib.sha256("mhu3ni").digest()))
        color = (nickname_colors[0:3], nickname_colors[3:6], nickname_colors[6:9], nickname_colors[9:12])[idx]
    led_colors = list(int(val * x) for (x) in binascii.unhexlify(color + '00'))
    return (led_colors[1], led_colors[0], led_colors[2], led_colors[3])


def larson_fade_inc(inc):
    global larson_fade
    new_value = round(larson_fade + inc, 1)
    if new_value > 0 and new_value < 1:
        larson_fade = new_value


def larson_fade_more(pressed):
    if pressed:
        larson_fade_inc(LARSON_FADE_STEPS)


def larson_fade_less(pressed):
    if pressed:
        larson_fade_inc(-LARSON_FADE_STEPS)


def larson_mode_change(inc):
    global larson_mode
    global larson_modes
    larson_mode = int(larson_mode + inc) % len(larson_modes)


def larson_mode_next(pressed):
    if pressed:
        larson_mode_change(1)


def larson_mode_prev(pressed):
    if pressed:
        larson_mode_change(-1)


def noop(pressed):
    pass


badge.init()
ugfx.init()
ugfx.input_init()
ugfx.input_attach(ugfx.JOY_UP, larson_fade_more)
ugfx.input_attach(ugfx.JOY_DOWN, larson_fade_less)
ugfx.input_attach(ugfx.JOY_LEFT, larson_mode_next)
ugfx.input_attach(ugfx.JOY_RIGHT, larson_mode_prev)
ugfx.input_attach(ugfx.BTN_A, noop)
ugfx.input_attach(ugfx.BTN_B, noop)
ugfx.input_attach(ugfx.BTN_START, noop)
ugfx.input_attach(ugfx.BTN_SELECT, home)
ugfx.clear(ugfx.WHITE)
ugfx.flush()
ugfx.string(190,25,"STILL","Roboto_BlackItalic24",ugfx.BLACK)
ugfx.string(170,50,"Proud","PermanentMarker22",ugfx.BLACK)
length = ugfx.get_string_width("Proud","PermanentMarker22")
ugfx.line(170, 72, 184 + length, 72, ugfx.BLACK)
ugfx.line(180 + length, 52, 180 + length, 70, ugfx.BLACK)
ugfx.string(180,75,"Anyway","Roboto_BlackItalic24",ugfx.BLACK)
ugfx.string(20, 110, "UP: brighter, DOWN: darker, L/R: switch mode","Roboto_Regular12",ugfx.BLACK)
ugfx.string(275, 115, "v26","Roboto_Regular12",ugfx.BLACK)
try:
    badge.eink_png(0,40,'/lib/sha2017_colors/shrug.png')
except:
    ugfx.string(100,50,"Error loading shrug.png","Roboto_Regular12",ugfx.BLACK)

ugfx.flush()

while True:
    for x in range(0, 6):
        larson_seq[x] = round(larson_seq[x] - larson_fade, 1) if larson_seq[x] > larson_fade else 0.0
    larson_seq[larson_n] = 1.0
    #    print(larson_seq)
    led_colors = ''.join(
        [''.join(["{0:02x}".format(int(led)) for led in larson(idx, val)]) for idx, val in enumerate(larson_seq)])
    badge.leds_send_data(binascii.unhexlify(led_colors), 24)
    larson_n = larson_n + larson_i
    larson_i = -larson_i if larson_n in (0, 5) else larson_i
    #    ugfx.flush()
    time.sleep(0.1)
