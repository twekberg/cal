#!/usr/bin/env python
"""
Build a wall calendar with images for a whole year.
"""


import argparse
import calendar
from datetime import datetime
import json
from pathlib import Path
import sys
import tkinter as tk

from pil_calendar import main as pil_calendar_main


def build_parser():
    """
    Collect command line arguments.
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-y', '--year', default=datetime.now().year, type=int,
                        help='The year to draw. '
                        'default: %(default)s')
    parser.add_argument('-i', '--input_filename',
                        default='rachel_welch.json',
                        help='JSON file with image data. '
                        ' Default: %(default)s.')
    return parser


class Render_12():
    def __init__(self, args):
        self.args = args
        self.load_json()

        root = tk.Tk()
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        root.destroy()


    def load_json(self):
        with open(self.args.input_filename) as jin:
            self.json = json.load(jin)

    def run_pil_calendar(self, month):
        class Args():
            def __init__(self, month, year):
                self.batch = True
                self.title_page = False
                self.year = year
                self.month = month

        args = Args(month, self.args.year)
        pil_calendar_main(args)
        args.title_page = True
        pil_calendar_main(args)


    def render(self):
        
        for month in range(1, 13):
            self.run_pil_calendar(month)
        # debug: make sure all of the image files are there.
        # Remove when done
        for month in range(1, 13):
            month_name = calendar.month_name[month]
            image_filename = Path(self.json['directory']) / self.json['images'][month]
            print(image_filename.name, f'{image_filename.exists()}')
        # TODO
        #scale the images to full screen. Use self.screen_width and self.screen_height.
        # collect the title.jpg file, mohth.jpg files and the
        # scaled image files and call
        #   magick names str(args.year).pdf

def main(args):
    """
    Starting point.
    """
    render_12 = Render_12(args)
    render_12.render()
    


if __name__ == '__main__':
    sys.exit(main(build_parser().parse_args()))
