import ugfx, badge, appglue

try:
    from . import LarsonScanner
except:
    import LarsonScanner

LARSON_VERSION = "v41"
LARSON_NAMESPACE = 'larson_pride'
LARSON_FADE_STEPS = 0.02
LARSON_BRIGHTNESS_STEPS = 0.05

try:
    name = badge.nvs_get_str('owner', 'name', 'Christopher')
except:
    name = "Emulator"


def settings_get_color_map(default = 0):
    return settings_get('color_map', default)

def settings_set_color_map(val):
    return settings_set('color_map', val)


def settings_get_decay(default = 0.6):
    return settings_get('decay', default)

def settings_set_decay(val):
    return settings_set('decay', val)


def settings_get_brightness(default = 0.1):
    return settings_get('brightness', default)

def settings_set_brightness(val):
    return settings_set('brightness', val)


def settings_get(key, default = 0):
    try:
        return badge.nvs_get_u8(LARSON_NAMESPACE, key, default)
    except:
        return default

def settings_set(key, val):
    try:
        return badge.nvs_set_u8(LARSON_NAMESPACE, key, val)
    except:
        pass
    return settings_get(key)


def home(pushed):
    if(pushed):
        appglue.home()


def inc_brightness(pressed):
    if pressed:
        scanner.change_brightness(LARSON_BRIGHTNESS_STEPS)
        settings_set_brightness(scanner.brightness)


def dec_brightness(pressed):
    if pressed:
        scanner.change_brightness(-LARSON_BRIGHTNESS_STEPS)
        settings_set_brightness(scanner.brightness)


def larson_mode_next(pressed):
    global current_color_map
    if pressed:
        current_color_map = (current_color_map + 1) % len(color_maps)
        scanner.colors = color_maps[current_color_map]
        settings_set_color_map(current_color_map)


def larson_mode_prev(pressed):
    global current_color_map
    if pressed:
        current_color_map = (current_color_map - 1 + len(color_maps)) % len(color_maps)
        scanner.colors = color_maps[current_color_map]
        settings_set_color_map(current_color_map)


def inc_decay(pressed):
    if pressed:
        scanner.change_decay(LARSON_FADE_STEPS)
        settings_set_decay(scanner.decay)


def dec_decay(pressed):
    if pressed:
        scanner.change_decay(-LARSON_FADE_STEPS)
        settings_set_decay(scanner.decay)


def noop(pressed):
    pass


# colors as RGB in hex
color_maps = {
    '/lib/sha2017_colors/shrug.png' : LarsonScanner.LarsonScanner.user_colors(name),
    '/lib/sha2017_colors/shrug.png' : LarsonScanner.LarsonScanner.pride_colors,
    'resources/kitt.png' : list('FF0000' for _ in range(6)), # red
    'resources/goliath.png' : list('00FF00' for _ in range(6)), # green
    list('0000FF' for _ in range(6)), # blue
    'resources/karr.png' : list('FFFF00' for _ in range(6)), # yellow
    ['FF0000', 'DD0011', '990022', '220099', '1100DD', '0000FF']}   # police lights

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

scanner = LarsonScanner.LarsonScanner()
current_color_map = settings_get_color_map()
scanner.colors = color_maps[current_color_map]
scanner.decay = settings_get_decay()
scanner.brightness = settings_get_brightness()

while True:
    scanner.draw()
    scanner.wait()
