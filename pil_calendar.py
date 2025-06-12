#!/usr/bin/env python
"""
Example of PIL rendering. It renders to a file, when shown is brought
up with Gimp.

The advantage of using PIL is that a LARGE font can be used (100 pts). 
tkinter can only support fonts up to a maximum of 30 pts.
"""

# https://www.geeksforgeeks.org/python-pil-imagedraw-draw-text/


import argparse
import calendar
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import sys


def build_parser():
    """
    Collect command line arguments.
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-a', '--action', default='calendar',
                        choices=['calendar', 'demo'],
                        help='Type of action to perform. '
                        'default: %(default)s')
    parser.add_argument('-y', '--year', default=datetime.now().year, type=int,
                        help='The year to draw. '
                        'default: %(default)s')
    parser.add_argument('-m', '--month', default=datetime.now().month, type=int,
                        help='The month to draw. '
                        'default: %(default)s')
    return parser


class Render():
    def __init__(self, args):
        self.args = args
        self.im = Image.new('RGB', (1050, 800), (256, 256, 256))
        self.draw = ImageDraw.Draw(self.im)
        cal = calendar.Calendar(firstweekday=list(calendar.day_name).index('Sunday'))
        self.month_name = calendar.month_name[args.month]
        print(self.month_name)
        self.month_cal = cal.monthdays2calendar(args.year, args.month)
        for week in self.month_cal:
            print(week)
        self.title_font = ImageFont.truetype('times.ttf', 80)
        self.base_font = ImageFont.truetype('times.ttf', 50)
        self.small_font = ImageFont.truetype('times.ttf', 30)

        self.box_width = 146
        self.box_height = 90



    def demo(self):
        self.draw.ellipse((100, 400, 150, 500), fill=(255, 0, 0),
                          outline=(0, 0, 0))
        self.draw.rectangle((200, 400, 300, 500), fill='white',
                            outline=(255, 255, 255))
        self.draw.line((350, 400, 450, 500), fill=(255, 255, 0), width=10)

        font_size = 100
        font = ImageFont.truetype('times.ttf', font_size)

        text = 'LAUGHING IS THE\n BEST MEDICINE'

        # drawing text size
        self.draw.text((5, 5), text, font = font, align ="left") 

        self.draw.text((5, 200), text, fill ="red", font = font, align ="right")


    def show(self):
        self.im.show()


    def draw_calendar(self):
        """
        Draw the calendar
        """
        self.draw_lines()
        self.draw_month()
        self.draw_dates()
        self.draw_days_of_week()

    def draw_days_of_week(self):
        """
        Draw the days of the week near the top.
        """
        y_coord = 115
        x_coord = 10
        W, H = (self.box_width, 100)
        for (_, dow_number) in self.month_cal[0]:
            day_name = calendar.day_name[dow_number]
            _, _, w, h = self.draw.textbbox((0, 0), day_name, font=self.small_font)
            self.draw.text((x_coord + (W-w)/2, y_coord), day_name, font=self.small_font, fill='green')
            x_coord += self.box_width
            

    def draw_dates(self):
        """
        Draw the numbered dates.
        """
        y_coord = 170
        for week in self.month_cal:
            # Ignore DOW
            x_coord = 30
            for (day, _) in week:
                if day:
                    self.draw.text((x_coord, y_coord), f'{day}', font=self.base_font, fill='red')
                x_coord += self.box_width
            y_coord += self.box_height

    def draw_month(self):
        """
        Draw the month name at the top.
        """
        W, H = (self.im.width, 100)
        _, _, w, h = self.draw.textbbox((0, 0), self.month_name, font=self.title_font)
        self.draw.text(((W-w)/2, (H-h)/2), self.month_name, font=self.title_font, fill='blue')


    def draw_lines(self):
        n_weeks = len(self.month_cal)
        box_width = 146
        box_height = 90

        # Vertical lines
        y_top = 149
        y_bottom = (box_height + 10) * (n_weeks + 1) + 1
        for x in range(10, 1050, 145):
            self.draw.line((x, y_top, x, y_bottom), width=3, fill ="black")

        # Horizontal lines
        x_left = 10
        x_right = 1023
        for y in range(150, 800, 90):
            self.draw.line((x_left, y, x_right, y), width=3, fill ="black")
            n_weeks -= 1
            if n_weeks < 0:
                break


def main(args):
    """
    Starting point.
    """
    render = Render(args)
    if args.action == 'calendar':
        render.draw_calendar()
    else:
        render.demo()
    render.show()

if __name__ == '__main__':
    sys.exit(main(build_parser().parse_args()))
