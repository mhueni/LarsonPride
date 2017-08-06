import badge
import binascii
import time
import ugfx
import hashlib

LARSON_FADE_STEPS = 0.05
larson_modes = ('ff0000', '00ff00', '0000ff', 'ffffff', 'pride')
pride_colors = ("750787", "004dff", "008026", "ffed00", "ff8c00", "e40303")
current_mode = 0
current_led = 0
direction = 1
larson_fade = 0.3
leds = [0, 0, 0, 0, 0, 0]

def home(pushed):
    if(pushed):
        print("go home")
        appglue.home()

def larson(led_pos, val):
    global current_mode, larson_modes
    color = larson_modes[current_mode]
    if (color == 'pride'):
        color = pride_colors[led_pos]
    led_colors = [int(val * x) for (x) in binascii.unhexlify(color + '00')]
    return (led_colors[1], led_colors[0], led_colors[2], led_colors[3])


def larson_fade_inc(inc):
    global larson_fade
    new_value = round(larson_fade + inc, 2)
    if new_value > 0 and new_value < 1:
        larson_fade = new_value


def larson_fade_more(pressed):
    if pressed:
        larson_fade_inc(LARSON_FADE_STEPS)


def larson_fade_less(pressed):
    if pressed:
        larson_fade_inc(-LARSON_FADE_STEPS)


def larson_mode_change(inc):
    global current_mode
    global larson_modes
    current_mode = int(current_mode + inc) % len(larson_modes)


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
        leds[x] = round(leds[x] - larson_fade, 1) if leds[x] > larson_fade else 0.0
    leds[current_led] = 1.0
    #    print(larson_seq)
    led_colors = ''.join(
        [''.join(["{0:02x}".format(int(led)) for led in larson(idx, val)]) for idx, val in enumerate(leds)])
    badge.leds_send_data(binascii.unhexlify(led_colors), 24)
    current_led = current_led + direction
    direction = -direction if current_led in (0, 5) else direction
    #    ugfx.flush()
    time.sleep(0.1)
