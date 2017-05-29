import serial
import time


class PlanTowerDevice(object):
    MODE_WAKEUP = bytearray([0x42, 0x4d, 0xe4, 0x00, 0x01, 0x01, 0x74])
    MODE_SLEEP = bytearray([0x42, 0x4d, 0xe4, 0x00, 0x00, 0x01, 0x73])

    MODE_ACTIVE = bytearray([0x42, 0x4d, 0xe1, 0x00, 0x01, 0x01, 0x71])
    MODE_PASSIVE = bytearray([0x42, 0x4d, 0xe1, 0x00, 0x00, 0x01, 0x70])

    # default config for PM7003
    config = {
        'data_length': 32,
        'serial_port': '/dev/ttyAMA0',
        'baudrate': 9600,
        'start_sequence': "\x42\x4d",
        'data_position': {
            'standard': {
                'pm1.0_position': 4,
                'pm2.5_position': 6,
                'pm10_position': 8
            },
            'atmospheric': {
                'pm1.0_position': 10,
                'pm2.5_position': 12,
                'pm10_position': 14
            }
        }
    }

    def __init__(self, config=None):
        if type(config) is dict:
            for key in config:
                self.config[key] = config[key]

        self.port = serial.Serial(self.config['serial_port'], baudrate=self.config['baudrate'], timeout=2)
        self.data_length = self.config['data_length']

    def parse_field(self, pos):
        # 256 * MSB + LSB
        return 0x100 * ord(self.raw_data[pos]) + ord(self.raw_data[pos + 1])

    def parse_fields(self):
        standard = self.config['data_position']['standard']
        atmospheric = self.config['data_position']['atmospheric']

        return {
            'standard': {
                'pm1.0': self.parse_field(standard['pm1.0_position']),
                'pm2.5': self.parse_field(standard['pm2.5_position']),
                'pm10': self.parse_field(standard['pm10_position'])
            },
            'atmospheric': {
                'pm1.0': self.parse_field(atmospheric['pm1.0_position']),
                'pm2.5': self.parse_field(atmospheric['pm2.5_position']),
                'pm10': self.parse_field(atmospheric['pm10_position'])
            }
        }

    def execute_command(self, command):
        self.port.write(command)

    def read(self):
        self.raw_data = self.port.read(self.data_length)
        try:
            head_index = self.raw_data.index(self.config['start_sequence'])
        except:
            return  # No valid data or PlanTower not ready

        if head_index > 0:
            # Adjust wrong position in serial data
            self.port.read(head_index)
            self.raw_data = self.port.read(self.data_length)

        time.sleep(1.0)
        return self.parse_fields()
