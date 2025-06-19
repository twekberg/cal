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
from PIL import Image
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


    def resize(self, image_path):
        image = Image.open(image_path)
        scale = min(self.im.width / image.width, self.im.height / image.height)
        resized = img.resize((round(scale * image.width),
                              round(scale * image.height), Image.LANCZOS))
        position = ((self.im.width - resized.width) / 2,
                    (self.im.height - resized.height) / 2)
        im.paste(position, resized)
        
    def render(self):
        """
        Run 
        """
        for month in range(1, 13):
            self.run_pil_calendar(month)
        # debug: make sure all of the image files are there.
        self.images = []
        for month in range(1, 13):
            month_name = calendar.month_name[month]
            image_path = Path(self.json['directory']) / self.json['images'][month]
            self.images.append(image_path)
            print(image_path.name, f'{image_path.exists()}')
        # TODO
        scale the images to full screen. Use self.screen_width and self.screen_height.
        # collect the title.jpg file, mohth.jpg files and the
        # scaled image files and call
        #   magick names str(args.year).pdf
        list(
            list(
	        itertools.chain.from_iterable(
		    zip(['Title'] + [f'{month}.jpg'
				     for month in calendar.month_name[1:]],
		        self.images))))
def main(args):
    """
    Starting point.
    """
    render_12 = Render_12(args)
    render_12.render()
    


if __name__ == '__main__':
    sys.exit(main(build_parser().parse_args()))
