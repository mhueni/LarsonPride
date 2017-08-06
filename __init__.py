import ugfx, badge, binascii, time, appglue

LARSON_VERSION = "v36"
LARSON_FADE_STEPS = 0.05
LARSON_BRIGHTNESS_STEPS = 0.02
larson_modes = ('pride', 'ff0000', '00ff00', '0000ff', 'ffffff')
pride_colors = ("750787", "004dff", "008026", "ffed00", "ff8c00", "e40303")
current_mode = 0
current_led = 0
direction = 1
larson_fade = 0.3
larson_brightness = 0.1
larson_settings_string = ""
leds = [0, 0, 0, 0, 0, 0]
try:
    name = badge.nvs_get_str('owner', 'name', 'Hacker1337')
except:
    name = "Emulator"


def home(pushed):
    if(pushed):
        appglue.home()


def larson(led_pos, val):
    global current_mode, larson_modes
    color = larson_modes[current_mode]
    if (color == 'pride'):
        color = pride_colors[led_pos]
    led_colors = [int(val * larson_brightness * x) for (x) in binascii.unhexlify(color + '00')]
    return (led_colors[1], led_colors[0], led_colors[2], led_colors[3])


def larson_brightness_inc(inc):
    global larson_brightness
    new_value = round(larson_brightness + inc, 2)
    if 0 < new_value < 1:
        larson_brightness = new_value
    display_settings()


def larson_brightness_up(pressed):
    if pressed:
        larson_brightness_inc(LARSON_BRIGHTNESS_STEPS)


def larson_brightness_down(pressed):
    if pressed:
        larson_brightness_inc(-LARSON_BRIGHTNESS_STEPS)


def larson_fade_inc(inc):
    global larson_fade
    new_value = round(larson_fade + inc, 2)
    if new_value > 0 and new_value < 1:
        larson_fade = new_value
    display_settings()


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
    display_settings()


def larson_mode_next(pressed):
    if pressed:
        larson_mode_change(1)


def larson_mode_prev(pressed):
    if pressed:
        larson_mode_change(-1)


def noop(pressed):
    pass


def display_settings():
    global larson_settings_string
    ugfx.string(2, 2, larson_settings_string,"Roboto_Regular10",ugfx.WHITE)
    ugfx.flush()
    larson_settings_string = "mode={:d}/brightness={:0.2f}/tail={:0.2f}".format(current_mode, larson_brightness, 1-larson_fade);
    ugfx.string(2, 2, larson_settings_string,"Roboto_Regular10",ugfx.BLACK)
    ugfx.flush()


badge.init()
badge.leds_init()
ugfx.init()
ugfx.input_init()
ugfx.input_attach(ugfx.JOY_UP, larson_brightness_up)
ugfx.input_attach(ugfx.JOY_DOWN, larson_brightness_down)
ugfx.input_attach(ugfx.JOY_LEFT, larson_fade_less)
ugfx.input_attach(ugfx.JOY_RIGHT, larson_fade_more)
ugfx.input_attach(ugfx.BTN_A, larson_mode_next)
ugfx.input_attach(ugfx.BTN_B, larson_mode_prev)
ugfx.input_attach(ugfx.BTN_START, noop)
ugfx.input_attach(ugfx.BTN_SELECT, home)

ugfx.clear(ugfx.BLACK)
ugfx.flush()
ugfx.clear(ugfx.WHITE)
ugfx.flush()

ugfx.string(190,25,"STILL","Roboto_BlackItalic24",ugfx.BLACK)
ugfx.string(170,50,name,"PermanentMarker22",ugfx.BLACK)
length = ugfx.get_string_width(name,"PermanentMarker22")
ugfx.line(170, 72, 184 + length, 72, ugfx.BLACK)
ugfx.line(180 + length, 52, 180 + length, 70, ugfx.BLACK)
ugfx.string(180,75,"Anyway","Roboto_BlackItalic24",ugfx.BLACK)
ugfx.string(20, 110, "A/B: mode, UP/DOWN: brightness, L/R: +/- tail","Roboto_Regular12",ugfx.BLACK)
ugfx.string(275, 115, LARSON_VERSION,"Roboto_Regular12",ugfx.BLACK)
try:
    badge.eink_png(0,40,'/lib/sha2017_colors/shrug.png')
except:
    ugfx.string(100,50,"Error loading shrug.png","Roboto_Regular12",ugfx.BLACK)
ugfx.flush()
display_settings()

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
    time.sleep(0.1)
