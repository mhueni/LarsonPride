import badge, binascii, hashlib, time

class LarsonScanner:
    pride_colors = ("75078700", "004dff00", "00802600", "ffed0000", "ff8c0000", "e4030300")

    def __init__(self, colors=pride_colors):
        self.colors = colors
        self.direction = -1
        self.brightness = 1.0
        self.current_led = 5        # use 5 if direction is -1, and 0 if direction is 1!
        self.decay = 0.8
        self.speed = 0.1        # duration for sleeps in seconds, as for time.sleep()

        self.leds_intensity = [1.0 for x in range(6)]

    def change_brightness(self, value):
        self.brightness += float(value)
        self.brightness = round(self.brightness, 2)
        self.brightness = max(self.brightness, 0.0)     # ensure >= 0.0
        self.brightness = min(self.brightness, 1.0)     # ensure <= 1.0

    def change_decay(self, value):
        self.decay += float(value)
        self.decay = round(self.decay, 2)
        self.decay = max(self.decay, 0.0)             # ensure >= 0.0
        self.decay = min(self.decay, 1.0)             # ensure <= 1.0

    def get_GRBW(self, led_pos, brightness):
        color = self.colors[led_pos]

        led_colors = [int(brightness * x) for x in binascii.unhexlify(color + '00')]
        return (led_colors[1], led_colors[0], led_colors[2], led_colors[3])     # grbw

    def draw(self):
        # Zero make the move of curent_led and check for direction
        # move works as follows:
        # 0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4 ....
        self.current_led += self.direction
        if self.current_led in [0, 5]:
            self.direction = -self.direction

        # First calc intensity on each led
        for x, intensity in enumerate(self.leds_intensity):
            new_intensity = intensity * self.decay
            self.leds_intensity[x] = round(new_intensity, 3)
        # But head led gets full intensity. (brightness is later)
        self.leds_intensity[self.current_led] = 1.0

        # print(self.leds_intensity)

        # Second apply brightness
        leds = []
        for x, intensity in enumerate(self.leds_intensity):
            leds.append(intensity * self.brightness)

        # print(leds)

        # Now we have intensify & brightness, let's apply colors.
        leds_as_grbw = []
        for index, value in enumerate(leds):
            leds_as_grbw.extend(self.get_GRBW(index, value))

        badge.leds_send_data(bytes(leds_as_grbw), 24)

    def user_colors(name):
        name_digest = binascii.hexlify(hashlib.sha1(name).digest())
        name_colors = (name_digest[30:36], name_digest[24:30], name_digest[18:24], name_digest[12:18], name_digest[6:12], name_digest[0:6])
        return list(c.decode() for c in name_colors)

    def wait(self):
        time.sleep(self.speed)


def test_demo():
    scanner = LarsonScanner()

    while True:
        scanner.draw()

if __name__ == '__main__':
    test_demo()
