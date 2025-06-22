#!/usr/bin/env python
"""
Makes a wall calendar with images.
"""


import argparse
import calendar
from datetime import datetime
import itertools
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
import sys
import tkinter as tk


# Static data items are stored here.
DATA = {"huge_font":  ImageFont.truetype('times.ttf', 300),
        "title_font": ImageFont.truetype('times.ttf', 80),
        "base_font":  ImageFont.truetype('times.ttf', 50),
        "small_font": ImageFont.truetype('times.ttf', 30),
        "smaller_font": ImageFont.truetype('times.ttf', 15),
        "box_width": 146,
        "box_height": 90,
        "root_width": 1050,
        "root_height": 800,
        }


def build_parser():
    """
    Collect command line arguments.
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-i', '--images_filename',
                        default='rachel_welch.json',
                        help='JSON file with image data. '
                        ' Default: %(default)s.')
    parser.add_argument('-y', '--year', default=datetime.now().year, type=int,
                        help='The year to draw. '
                        'default: %(default)s')
    parser.add_argument('-q', '--quiet',
                        default=False, action='store_true',
                        help="Don't display messages. "
                        'default: %(default)s')
    return parser


class RenderMonth():
    """
    Render an image for a specific month.
    """
    def __init__(self, args, year, month, holidays):
        self.args = args
        self.holidays = holidays
        self.im = Image.new('RGB', (DATA['root_width'], DATA['root_height']), (256, 256, 256))
        self.draw = ImageDraw.Draw(self.im)
        cal = calendar.Calendar(firstweekday=list(calendar.day_name).index('Sunday'))
        self.month_name = calendar.month_name[month]
        if not self.args.quiet:
            print(self.month_name)
        self.month_cal = cal.monthdays2calendar(year, month)
        if not self.args.quiet:
            for week in self.month_cal:
                print(week)

    def save(self):
        """
        Save the image as a JPG file.
        """
        self.im.save(f'{self.month_name}.jpg', "JPEG", optimize=True, quality=80)


    def show(self):
        """
        Show the image in gimp. This is for use in the debugger.
        """
        if not self.args.quiet:
            self.im.show()


    def draw_calendar(self):
        """
        Draw the calendar
        """
        self.normalize_holidays()
        self.draw_lines()
        self.draw_month()
        self.draw_dates()
        self.draw_days_of_week()


    def normalize_holidays(self):
        """
        For the holidays that are relative, convert them to absolute days.
        """
        day_names = list(calendar.day_name)           # Monday is 1st day
        day_names = [day_names[-1]] + day_names[0:-1] # Sunday is 1st day
        # Reconstruct self.holidays to have absolute days.
        # Make it a dict where the day# is the key, value is the holiday name.
        holidays = {}
        for (name, month, day) in self.holidays:
            if isinstance(day, list):
                # Relative days
                (week, dow) = day
                if week > 0:
                    week -= 1   # Convert to 0 based index
                # Need to count the number of valid Mondays.
                if self.month_cal[0][day_names.index(dow)][0] == 0:
                    # This DOW is not in the first week.
                    if week >= 0:
                        week += 1
                day = self.month_cal[week][day_names.index(dow)][0]
            holidays[day] = name
        self.holidays = holidays


    def draw_days_of_week(self):
        """
        Draw the days of the week column headers.
        """
        y_coord = 115
        x_coord = 10
        W, H = (DATA['box_width'], 100)
        for (_, dow_number) in self.month_cal[0]:
            day_name = calendar.day_name[dow_number]
            _, _, w, h = self.draw.textbbox((0, 0), day_name, font=DATA["small_font"])
            self.draw.text((x_coord + (W-w)/2, y_coord), day_name, font=DATA['small_font'], fill='green')
            x_coord += DATA['box_width']
            

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
                    self.draw.text((x_coord, y_coord), f'{day}', font=DATA['base_font'], fill='red')
                    if day in self.holidays:
                        self.draw.text((x_coord - 18, y_coord + 50), self.holidays[day],
                                       font=DATA['smaller_font'], fill='navy')                        
                x_coord += DATA['box_width']
            y_coord += DATA['box_height']

    def draw_month(self):
        """
        Draw the month name at the top.
        """
        W, H = (self.im.width, 100)
        _, _, w, h = self.draw.textbbox((0, 0), self.month_name, font=DATA['title_font'])
        self.draw.text(((W-w)/2, (H-h)/2), self.month_name, font=DATA['title_font'], fill='blue')


    def draw_lines(self):
        """
        Draw the vertical and horizontal lines.
        """
        def calc_y_bottom():
            """
            Months have 4, 5, or 6 weeks. This calculation is done to
            have the bottom of the vertical lines line up properly.
            2015/2 has 4 weeks, 2025/6 has 5 weeks, 2025/3 has 6 weeks.
            """
            if n_weeks == 4:
                return (DATA['box_height'] + 12) * (n_weeks + 1) + 1            
            if n_weeks == 5:
                return (DATA['box_height'] + 10) * (n_weeks + 1) + 1
            if n_weeks == 6:
                return (DATA['box_height'] + 8) * (n_weeks + 1) + 5
            raise Exception(f'Invalid n_weeks: {n_weeks}')

        n_weeks = len(self.month_cal)

        # Vertical lines
        y_top = 149
        y_bottom = calc_y_bottom()

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


    def draw_title_page(self, year, title_text):
        """
        Draw the calendar title page showing the year.
        """
        W, H = (self.im.width, self.im.height)
        _, _, w, h = self.draw.textbbox((0, 0), str(year), font=DATA["huge_font"])
        self.draw.text(((W-w)/2, (H-h)/3), str(year), font=DATA['huge_font'], fill='blue')

        _, _, w, h = self.draw.textbbox((0, 0), title_text, font=DATA["title_font"])
        self.draw.text(((W-w)/2, (H-h)/3*2), title_text, font=DATA['title_font'], fill='green')

        self.im.save(f'title.jpg', "JPEG", optimize=True, quality=80)


class MakeCalendar():
    """
    Make the whole wall calendar.
    """
    def __init__(self, args):
        self.args = args
        self.load_json()
        self.load_holidays()

        root = tk.Tk()
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        root.destroy()


    def load_json(self):
        with open(self.args.images_filename) as jin:
            self.json = json.load(jin)

    def load_holidays(self):
        with open('holidays.json') as jin:
            self.holidays = json.load(jin)

    def resize(self, image_path):
        """
        Resize an image to fit in the drawing image - self.im.
        """
        image = Image.open(image_path)
        scale = min(DATA['root_width'] / image.width,
                    DATA['root_height'] / image.height)
        resized = image.resize((round(scale * image.width),
                                round(scale * image.height)), Image.LANCZOS)
        im = Image.new('RGB', (DATA['root_width'], DATA['root_height']), (256, 256, 256))
        position = (int((im.width - resized.width) / 2),
                    int((im.height - resized.height) / 2))
        im.paste(resized, position)
        im.save(image_path.name, "JPEG", optimize=True, quality=80)


    def render(self):
        """
        Run RenderMonth for each month and prepare the images.
        """
        for month in range(1, 13):
            render = RenderMonth(self.args, self.args.year, month,
                                 [holiday for holiday in self.holidays
                                  if holiday[1] == month])
            render.draw_calendar()
            render.save()
        #### render = RenderMonth(self.args, self.args.year, 1)
        # draw_title_page also saves the JPG.
        render.draw_title_page(self.args.year, self.json['title_text'])

        # debug: make sure all of the image files are there.
        self.images = []
        for month in range(1, 13):
            month_name = calendar.month_name[month]
            image_path = Path(self.json['directory']) / self.json['images'][month]
            self.resize(image_path)
            self.images.append(image_path.name)
            if not self.args.quiet:
                print(image_path.name, f'{Path(image_path.name).exists()}')
        # Collect the title.jpg file, mohth.jpg files and the
        # scaled image files and call
        # magick concatenating them together with output going to a PDF file.
        cmd = ['magick', 'title.jpg'] + \
              list(
                  list(
	              itertools.chain.from_iterable(
		          zip([str(image) for image in self.images],
                              [f'{month}.jpg' for month in calendar.month_name[1:]])))) + \
              [f'{self.args.year}.pdf']


        self.jpg_files = [file for file in cmd if file.endswith('.jpg')]
        if not self.args.quiet:
            print(cmd)
        ret = subprocess.call(cmd)
        if ret != 0:
            raise RuntimeError(f'Got a subprocess.call error {ret}, command={" ".join(cmd)}')


    def cleanup(self):
        """
        Remove the files that were created in this directory.
        """
        [Path(path).unlink() for path in self.jpg_files]


def main(args):
    """
    Starting point.
    """
    make_calendar = MakeCalendar(args)
    make_calendar.render()
    make_calendar.cleanup()


if __name__ == '__main__':
    sys.exit(main(build_parser().parse_args()))
