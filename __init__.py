import ugfx, badge, appglue

from . import LarsonScanner

LARSON_VERSION = "v4.6"
LARSON_FADE_STEPS = 0.01
LARSON_BRIGHTNESS_STEPS = 0.05

try:
    name = badge.nvs_get_str('owner', 'name', 'Christopher')
except:
    name = "Emulator"

# colors as RGB in hex
current_color_map = 0
colors = {'user': LarsonScanner.LarsonScanner.user_colors(name),
          'red': ("FF0000", "FF0000", "FF0000", "FF0000", "FF0000", "FF0000"),
          'green': ('00FF00', '00FF00', '00FF00', '00FF00', '00FF00', '00FF00'),
          'blue': ('0000FF', '0000FF', '0000FF', '0000FF', '0000FF', '0000FF'),
          'pride': LarsonScanner.LarsonScanner.pride_colors}
color_maps = list(colors.keys())
print(colors)

def home(pushed):
    if(pushed):
        appglue.home()


def inc_brightness(pressed):
    if pressed:
        scanner.change_brightness(LARSON_BRIGHTNESS_STEPS)


def dec_brightness(pressed):
    if pressed:
        scanner.change_brightness(-LARSON_BRIGHTNESS_STEPS)


def larson_mode_next(pressed):
    global current_color_map
    if pressed:
        current_color_map += 1
        if current_color_map >= len(color_maps):
            current_color_map = 0
        scanner.colors = colors[color_maps[current_color_map]]


def larson_mode_prev(pressed):
    global current_color_map
    if pressed:
        current_color_map -= 1
        print(current_color_map)
        if current_color_map < 0:
            current_color_map = len(color_maps)-1
        print(current_color_map)
        scanner.colors = colors[color_maps[current_color_map]]


def inc_decay(pressed):
    scanner.change_decay(LARSON_FADE_STEPS)


def dec_decay(pressed):
    scanner.change_decay(-LARSON_FADE_STEPS)


def noop(pressed):
    pass

scanner = LarsonScanner.LarsonScanner()

badge.init()
badge.leds_init()
ugfx.init()
ugfx.input_init()
ugfx.input_attach(ugfx.JOY_UP, inc_brightness) # TODO rename to _up
ugfx.input_attach(ugfx.JOY_DOWN, dec_brightness)
ugfx.input_attach(ugfx.JOY_LEFT, dec_decay) # same here
ugfx.input_attach(ugfx.JOY_RIGHT, inc_decay)
ugfx.input_attach(ugfx.BTN_A, larson_mode_next)
ugfx.input_attach(ugfx.BTN_B, larson_mode_prev)
ugfx.input_attach(ugfx.BTN_START, home)
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
ugfx.string(270, 117, LARSON_VERSION,"Roboto_Regular10",ugfx.BLACK)
try:
    badge.eink_png(0,40,'/lib/sha2017_colors/shrug.png')
except:
    ugfx.string(100,50,"Error loading shrug.png","Roboto_Regular12",ugfx.BLACK)

ugfx.flush()

while True:
    scanner.draw()
    scanner.wait()
