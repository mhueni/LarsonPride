import badge
import binascii
import time
import ugfx

larson_modes = ('ff0000', '00ff00', '0000ff', 'ffffff', 'pride')
larson_mode = 0
larson_n = 0
larson_i = 1
larson_fade = 0.3
larson_seq = [ 0, 0, 0, 0, 0, 0 ]

def larson(idx,val):
    global larson_mode,larson_modes
    color = list(larson_pride(idx,val) if larson_modes[larson_mode] == 'pride' else larson_color(larson_modes[larson_mode],val))
    return (color[1], color[0], color[2], color[3])

def larson_color(color,val):
    return list(int(val * x) for (x) in binascii.unhexlify(color + '00'))

def larson_pride(idx,val):
    return [
        list(int(val * x) for (x) in binascii.unhexlify("75078710")),
        list(int(val * x) for (x) in binascii.unhexlify("004dff10")),
        list(int(val * x) for (x) in binascii.unhexlify("00802610")),
        list(int(val * x) for (x) in binascii.unhexlify("ffed0010")),
        list(int(val * x) for (x) in binascii.unhexlify("ff8c0010")),
        list(int(val * x) for (x) in binascii.unhexlify("e4030310")),
    ][idx]

def larson_fade_inc(pressed, inc):
    global larson_fade
    if pressed:
        new_value = larson_fade + inc
        if new_value > 0 and new_value < 1:
            larson_fade = new_value

def larson_mode_change(pressed, inc):
    global larson_mode
    global larson_modes
    if pressed:
        larson_mode = int(larson_mode + inc) % len(larson_modes)

def noop():
    pass

badge.init()
ugfx.init()
ugfx.input_init()
ugfx.input_attach(ugfx.JOY_UP, lambda pressed: larson_fade_inc(pressed, -0.1))
ugfx.input_attach(ugfx.JOY_DOWN, lambda pressed: larson_fade_inc(pressed, 0.1))
ugfx.input_attach(ugfx.JOY_LEFT, lambda pressed: larson_mode_change(pressed, 1))
ugfx.input_attach(ugfx.JOY_RIGHT, lambda pressed: larson_mode_change(pressed, -1))
ugfx.input_attach(ugfx.BTN_A, lambda pressed: noop())
ugfx.input_attach(ugfx.BTN_B, lambda pressed: noop())
ugfx.input_attach(ugfx.BTN_START, lambda pressed: noop())
ugfx.input_attach(ugfx.BTN_SELECT, lambda pressed: appglue.start_app(""))
ugfx.clear(ugfx.WHITE)
ugfx.flush()
ugfx.clear(ugfx.BLACK)
ugfx.string(10,10,'F**K YOU GANDALF',"PermanentMarker22",ugfx.WHITE)
ugfx.flush()

while True:
    for x in range(0,6):
        larson_seq[x] = round(larson_seq[x] - larson_fade, 1) if larson_seq[x] > larson_fade else 0.0
    larson_seq[larson_n] = 1.0
#    print(larson_seq)
    led_colors = ''.join([''.join(["{0:02x}".format(int(led)) for led in larson(idx,val)]) for idx,val in enumerate(larson_seq)])
    badge.leds_send_data(binascii.unhexlify(led_colors),24)
    larson_n = larson_n + larson_i
    larson_i = -larson_i if larson_n in (0,5) else larson_i
#    ugfx.flush()
    time.sleep(0.1)
