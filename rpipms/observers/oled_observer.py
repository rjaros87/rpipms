# -*- coding: utf-8 -*-

from datetime import datetime
from luma.core.render import canvas

from rpipms.oled_ssd1306_device import OledSsd1306Device
from rpipms.plan_tower_observer import PlanTowerObserver


class OledObserver(PlanTowerObserver):
    device = None
    config = None

    def __init__(self):
        self.device = OledSsd1306Device(self.config).device

    def configure(self, configure):
        self.config = configure

    def pm1_0(self, value):
        return str(value['pm1.0'])

    def pm2_5(self, value):
        return str(value['pm2.5'])

    def pm10(self, value):
        return str(value['pm10'])

    def notify(self, data):
        with canvas(self.device) as draw:
            font_color = "white"
            d_width = self.device.width
            d_height = self.device.height
            dh_width = d_width / 2

            if type(data) is dict:
                # 128 x 64
                text = "PM measured in ug/m3"
                text_size = draw.textsize(text)
                draw.text((0, 0), text, fill=font_color)
                draw.line((0, text_size[1] + 1, d_width, text_size[1] + 1), fill=font_color)

                standard = data['standard']
                atmospheric = data['atmospheric']

                axis_size = draw.textsize("PM1.0 ")  # only for count text size

                row_start_pos = text_size[1] + 5
                row_end_pos = row_start_pos + 3 * axis_size[1]
                first_col_size = axis_size[0] + 5
                second_cold_pos = dh_width + 15

                draw.line((axis_size[0], row_start_pos, axis_size[0], row_end_pos), fill=font_color)
                draw.line((second_cold_pos, row_start_pos, second_cold_pos, row_end_pos), fill=font_color)

                draw.text((1, row_start_pos), "PM1.0 ", fill=font_color)
                draw.text((first_col_size, row_start_pos), self.pm1_0(standard), fill=font_color)
                draw.text((second_cold_pos + 10, row_start_pos), self.pm1_0(atmospheric), fill=font_color)

                draw.text((1, row_start_pos + 11), "PM2.5 ", fill=font_color)
                draw.text((first_col_size, row_start_pos + axis_size[1]), self.pm2_5(standard), fill=font_color)
                draw.text((second_cold_pos + 10, row_start_pos + axis_size[1]), self.pm2_5(atmospheric),
                          fill=font_color)

                draw.text((1, row_start_pos + 22), "PM10  ", fill=font_color)
                draw.text((first_col_size, row_start_pos + 2 * axis_size[1]), self.pm10(standard), fill=font_color)
                draw.text((second_cold_pos + 10, row_start_pos + 2 * axis_size[1]), self.pm10(atmospheric),
                          fill=font_color)

                draw.text((0, d_height - axis_size[1]), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), fill=font_color)
            else:
                text = "Waiting for \nPlanTower..."
                text_size = draw.textsize(text)
                cx = d_width / 2 - int(text_size[0] / 2)
                cy = d_height / 2 - int(text_size[1] / 2)
                draw.multiline_text((cx, cy), text, fill=font_color)
