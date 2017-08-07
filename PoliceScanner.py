import badge, binascii, hashlib, time

class PoliceScanner():
    police_colors = ("FF000000", "FF000000", "FF000000", "0000FF00", "0000FF00", "0000FF00")

    def __init__(self, colors=police_colors):
        self.colors = colors
        self.side = -1
        self.brightness = 1.0
        self.cycle = 0              # keep track of blinking state: 0: on; 1,2,3: just decay;  4: on; 5,6,7: just decay, then change side
        self.decay = 0.8
        self.speed = 0.05  # duration for sleeps in seconds, as for time.sleep()

        self.leds_intensity = [1, 1, 1, 0, 0, 0]

    def change_brightness(self, value):
        self.brightness += float(value)
        self.brightness = round(self.brightness, 2)
        self.brightness = max(self.brightness, 0.0)  # ensure >= 0.0
        self.brightness = min(self.brightness, 1.0)  # ensure <= 1.0

    def change_decay(self, value):
        self.decay += float(value)
        self.decay = round(self.decay, 2)
        self.decay = max(self.decay, 0.0)  # ensure >= 0.0
        self.decay = min(self.decay, 1.0)  # ensure <= 1.0

    def get_GRBW(self, led_pos, brightness):
        color = self.colors[led_pos]

        led_colors = [int(brightness * x) for x in binascii.unhexlify(color)]
        return (led_colors[1], led_colors[0], led_colors[2], led_colors[3])  # grbw

    def draw(self):
        # First calc intensity on each led
        pass
        for x, intensity in enumerate(self.leds_intensity):
            new_intensity = intensity * self.decay
            self.leds_intensity[x] = round(new_intensity, 3)

        # But side leds gets full intensity every second cycle. (brightness is later)
        if self.cycle == 3:
            self.side *= -1
            if self.side > 0:
                self.leds_intensity[3:6] = [1.0, 1.0, 1.0]
            else:
                self.leds_intensity[0:3] = [1.0, 1.0, 1.0]

        self.cycle = (self.cycle + 1) % 4



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
        name_digest = binascii.hexlify(hashlib.sha256(name).digest())
        name_colors = (name_digest[0:6], name_digest[6:12], name_digest[12:18], name_digest[18:24], name_digest[24:30],
                       name_digest[30:36])
        return list(c.decode() for c in name_colors)

    def wait(self):
        time.sleep(self.speed)


def test_demo():
    scanner = PoliceScanner()

    while True:
        scanner.draw()


if __name__ == '__main__':
    test_demo()
