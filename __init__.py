import ugfx, badge, appglue

try:
    from . import LarsonScanner, PoliceScanner
except:
    import LarsonScanner, PoliceScanner

LARSON_LIB = '/lib/larson_pride/' # change to /lib/larson_pride for public release
LARSON_NAMESPACE = 'larson_pride'
LARSON_VERSION = 'v42'
LARSON_FADE_STEPS = 0.02
LARSON_BRIGHTNESS_STEPS = 0.04

try:
    name = badge.nvs_get_str('owner', 'name', 'Christopher')
except:
    name = "Emulator"


def settings_get_color_map(default = 0):
    return settings_get('color_map', default)

def settings_set_color_map(val):
    return settings_set('color_map', val)


def settings_get_decay(default = 127):
    return round(settings_get('decay', default) / 255, 2)

def settings_set_decay(val):
    return settings_set('decay', int(val * 255))


def settings_get_brightness(default = 31):
    return round(settings_get('brightness', default) / 255, 2)

def settings_set_brightness(val):
    return settings_set('brightness', int(val * 255))


def settings_get(key, default = 0):
    try:
        value = badge.nvs_get_u8(LARSON_NAMESPACE, key, default)
        print('get', key, value, 'default', default)
        return value
    except:
        return default

def settings_set(key, val):
    print('set', key, val)
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
        if (scanner.brightness < 0.1):
            scanner.change_brightness(0.01)
        else:
            scanner.change_brightness(LARSON_BRIGHTNESS_STEPS)
        settings_set_brightness(scanner.brightness)


def dec_brightness(pressed):
    if pressed:
        if (scanner.brightness < 0.1):
            scanner.change_brightness(-0.01)
        else:
            scanner.change_brightness(-LARSON_BRIGHTNESS_STEPS)
        settings_set_brightness(scanner.brightness)


def larson_mode_next(pressed):
    global current_color_map
    if pressed:
        current_color_map = (current_color_map + 1) % len(color_maps)
        settings_set_color_map(current_color_map)
        show_scanner()


def larson_mode_prev(pressed):
    global current_color_map
    if pressed:
        current_color_map = (current_color_map - 1 + len(color_maps)) % len(color_maps)
        settings_set_color_map(current_color_map)
        show_scanner()


def inc_decay(pressed):
    if pressed:
        scanner.change_decay(LARSON_FADE_STEPS)
        settings_set_decay(scanner.decay)


def dec_decay(pressed):
    if pressed:
        scanner.change_decay(-LARSON_FADE_STEPS)
        settings_set_decay(scanner.decay)


def show_scanner():
    global current_color_map, scanner
    image = color_images[current_color_map]
    scanner = color_maps[image]
    scanner.brightness = settings_get_brightness() if 0 < settings_get_brightness() < 1 else 0.1
    scanner.decay = settings_get_decay() if 0 < settings_get_decay() < 1 else 0.6
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
    'sha2017.png'   : LarsonScanner.LarsonScanner(LarsonScanner.LarsonScanner.user_colors(name)),
    'pride.png'     : LarsonScanner.LarsonScanner(LarsonScanner.LarsonScanner.pride_colors), # pride
    'mfzh17.png'    : LarsonScanner.LarsonScanner(('EC1C2400','009EE000','FFFFFF00','EC1C2400','009EE000','FFFFFF00')),
    'kitt.png'      : LarsonScanner.LarsonScanner(list('FF000000' for _ in range(6))), # red
    'hackzh.png'    : LarsonScanner.LarsonScanner(list('00FF0000' for _ in range(6))), # green
    'ohm2013.png'   : LarsonScanner.LarsonScanner(list('0000FF00' for _ in range(6))), # blue
    'karr.png'      : LarsonScanner.LarsonScanner(list('FFFF0000' for _ in range(6))), # yellow
    'gunter.png'    : LarsonScanner.LarsonScanner(list('FFFFFF00' for _ in range(6))), # white
    'police.png'    : PoliceScanner.PoliceScanner()}   # police lights

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

ugfx.string(190,7,"STILL","Roboto_BlackItalic24",ugfx.BLACK)
ugfx.string(170,32,name,"PermanentMarker22",ugfx.BLACK)
length = ugfx.get_string_width(name,"PermanentMarker22")
ugfx.line(170, 54, 184 + length, 54, ugfx.BLACK)
ugfx.line(180 + length, 34, 180 + length, 54, ugfx.BLACK)
ugfx.string(180,57,"Anyway","Roboto_BlackItalic24",ugfx.BLACK)
ugfx.string(177, 88, "Mode: A/B, Tail: L/R","Roboto_Regular12",ugfx.BLACK)
ugfx.string(177, 101, "Brightness: UP/DOWN","Roboto_Regular12",ugfx.BLACK)
ugfx.string(215, 116, "Larson Pride","Roboto_Regular10",ugfx.BLACK)
ugfx.string(279, 116, LARSON_VERSION,"Roboto_Regular10",ugfx.BLACK)

ugfx.flush()

current_color_map = settings_get_color_map()
show_scanner()

while True:
    scanner.draw()
    scanner.wait()
