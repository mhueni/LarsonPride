import ugfx, badge, appglue

try:
    from . import LarsonScanner
except:
    import LarsonScanner

LARSON_LIB = '/lib/larsonstage/' # change to /lib/larson_pride for public release
LARSON_NAMESPACE = 'larson_pride'
LARSON_VERSION = 'v41'
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
        color_image = color_images[current_color_map]
        show_image(color_image)
        scanner.colors = color_maps[color_image]
        settings_set_color_map(current_color_map)


def larson_mode_prev(pressed):
    global current_color_map
    if pressed:
        current_color_map = (current_color_map - 1 + len(color_maps)) % len(color_maps)
        color_image = color_images[current_color_map]
        show_image(color_image)
        scanner.colors = color_maps[color_image]
        settings_set_color_map(current_color_map)


def inc_decay(pressed):
    if pressed:
        scanner.change_decay(LARSON_FADE_STEPS)
        settings_set_decay(scanner.decay)


def dec_decay(pressed):
    if pressed:
        scanner.change_decay(-LARSON_FADE_STEPS)
        settings_set_decay(scanner.decay)


def show_image(image):
    try:
        ugfx.area(0, 0, 176, 128, ugfx.WHITE)
        ugfx.flush()
        badge.eink_png(0, 0, LARSON_LIB + image)
        ugfx.flush()
    except:
        pass



def noop(pressed):
    pass


# colors as RGB in hex
color_maps = {
    'shrug.png'      : LarsonScanner.LarsonScanner.user_colors(name),
    'pride.png'     : LarsonScanner.LarsonScanner.pride_colors,
    'kitt.png'      : list('FF0000' for _ in range(6)), # red
    'goliath.png'   : list('00FF00' for _ in range(6)), # green
    'blue.png'      : list('0000FF' for _ in range(6)), # blue
    'karr.png'      : list('FFFF00' for _ in range(6)), # yellow
    'police.png'    : ['FF0000', 'DD0011', '990022', '220099', '1100DD', '0000FF']}   # police lights

color_images = list(color_maps.keys())

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

ugfx.string(190,10,"STILL","Roboto_BlackItalic24",ugfx.BLACK)
ugfx.string(170,35,name,"PermanentMarker22",ugfx.BLACK)
length = ugfx.get_string_width(name,"PermanentMarker22")
ugfx.line(170, 57, 184 + length, 57, ugfx.BLACK)
ugfx.line(180 + length, 37, 180 + length, 57, ugfx.BLACK)
ugfx.string(180,60,"Anyway","Roboto_BlackItalic24",ugfx.BLACK)
ugfx.string(177, 88, "A/B: mode, L/R: tail size","Roboto_Regular10",ugfx.BLACK)
ugfx.string(177, 101, "UP/DOWN: brightness","Roboto_Regular10",ugfx.BLACK)
ugfx.string(215, 117, "Larson Pride","Roboto_Regular10",ugfx.BLACK)
ugfx.string(279, 117, LARSON_VERSION,"Roboto_Regular10",ugfx.BLACK)
ugfx.flush()

scanner = LarsonScanner.LarsonScanner()
current_color_map = settings_get_color_map()
scanner.colors = color_maps[color_images[current_color_map]]
scanner.decay = settings_get_decay()
scanner.brightness = settings_get_brightness()
show_image(color_images[current_color_map])

while True:
    scanner.draw()
    scanner.wait()
