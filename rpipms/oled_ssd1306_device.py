from luma.core.serial import i2c
from luma.oled.device import ssd1306


class OledSsd1306Device:
    config = {
        'address': 0x3C,
        'port': 1
    }

    device = None

    def __init__(self, config=None):
        if type(config) is dict:
            for key in config:
                self.config[key] = config[key]

        # TODO: https://luma-oled.readthedocs.io/en/latest/hardware.html#tips-for-connecting-the-display
        # TODO: we need get OLED address and port from RPi (depends on RPi model/version) - bash command to check
        serial = i2c(port=self.config['port'], address=self.config['address'])
        self.device = ssd1306(serial)
