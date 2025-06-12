#!/usr/bin/env python
"""
This module renders the graphics for a single month of the calendar,
suitable for combining with the other 11 months as a wall calendar.
 setfirstweekday(6) ro make Sunday the first day of the week.
"""

# TODO:
# Look at times.ttf in c:/WIndows/fonts to see why it is smaller.
# datetime(args.year, args.month, 1).strftime('%b')
# returns 'May' for 2025/05.


import argparse
from calendar import Calendar
from datetime import datetime
import os
import os.path
from PIL import ImageFont
from graphics import Rectangle, Text, Line, Point, GraphWin
#from graphics import *
from tkinter import Tk, font

FONT_WIDTH = 10
FONT_HEIGHT = 50
BOX_WIDTH = 25
BOX_HEIGHT = 50
FONT_SIZE = 36


def build_parser():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__.strip())
    parser.add_argument('-y', '--year', default=2025, type=int,
                        help='The year to draw. '
                        'default: %(default)s')
    parser.add_argument('-m', '--month', default=5, type=int,
                        help='The month to draw. '
                        'default: %(default)s')

    return parser


class Box():
    """
    Code to render a box for an episode.
    """
    def __init__(self, win, text, xy, _width, _height):
        self.win = win
        self.text = text
        self.xy = xy

    def draw(self):
        """
        Draw a rectangle for an episode.
        """
        xy2 = Point(self.xy.getX() + BOX_WIDTH, self.xy.getY() + BOX_HEIGHT)
        Rectangle(self.xy, xy2).draw(self.win)
        Text(Point(self.xy.getX() + BOX_WIDTH/3, self.xy.getY() + FONT_HEIGHT/2), \
             self.text).draw(self.win)
        #Text(Point(self.xy.getX() + BOX_WIDTH/2, self.xy.getY() + FONT_HEIGHT/2), \
        #     self.text).draw(self.win)
        Line(Point(self.xy.getX() + BOX_WIDTH, self.xy.getY()),
             Point(xy2.getX() - BOX_WIDTH, xy2.getY())).draw(self.win)


class Show():
    """
    Display a line for a show.
    """

    def __init__(self, win, xy, text, count=24):
        """
        text - show title + season
        count - number of boxes to display
        """
        self.win = win
        self.xy = xy
        self.text = text
        self.count = count

    def draw(self):
        """
        Draw a line for a show.
        """
        x = self.xy.getX()
        y = self.xy.getY()
        Text(Point(x + len(self.text) * FONT_WIDTH / 2, y + FONT_HEIGHT/2), self.text).draw(self.win)
        y += FONT_HEIGHT + 2
        for count in range(1, self.count):
            Box(self.win, f'{count}', Point(x, y), BOX_WIDTH, BOX_HEIGHT).draw()
            x += BOX_WIDTH


# see for loop
shows = [
    ('Tracker', 'Sunday', 2, 'CBS - Oct 13'),
    ('NCIS', 'Monday', 21, 'CBS - Oct 14'),
    ('NCIS Origins', 'Monday', 1, 'CBS - Oct 14'),
    ('Elsbeth', 'Thursday', 3, 'CBS - Oct 17'),
    ('Ghosts', 'Thursday', 4, 'CBS - Oct 17'),
    ("George & Mandy's First Marriage", 'Thursday', 1, 'CBS'),
    ('Lower Decks', 'Thursday', 5, 'CBS'),
]

def getsize(text, font_size):
    font = ImageFont.truetype('times.ttf', font_size)
    # print(dir(font))
    # The PIL length is too small. Did some measurements with different
    # names of months and ran them through a least squares
    # regression. Here is the data:
    #   66	95	May
    #   76	100	April
    #   94	140	March
    #   104	163	August
    #   148	230	December
    #   154	244	September
    # This is the resultant equation:
    #   y = 1.72787x + -22.88197
    return font.getlength(text) * 1.72787 - 22.88197


def main(_args):
    """
    Top level function.
    """
    cal = Calendar(firstweekday=6)
    m = cal.monthdays2calendar(2025, 5)
    for week in m:
        print(week)

    win = GraphWin('Month', width=1000, height=700)

    # fonts=list(font.families())
    # for f_name in sorted(fonts):
    #     print(f_name)
    # print(len(fonts))
    text = 'Want to see this in its own window'
    txt = Text(Point(450, 100), text)
    txt.setFace('times roman')
    Line(Point(85, 120),
             Point(150+getsize(text, FONT_SIZE), 120)).draw(win)

    print(getsize(text, FONT_SIZE))
    # print(font.families()[1], dir(font.families()[1]))
    # print(dir(font))
    txt.setSize(FONT_SIZE)
    txt.draw(win)

    for (y_pos, text) in  zip(range(160, 500, 60),
                              ['March', 'April', 'May', 'August', 'September', 'December']):
        txt = Text(Point(450, y_pos), text)
        txt.setFace('times roman')
        txt.setSize(FONT_SIZE)
        pil_size = getsize(text, FONT_SIZE)
        Line(Point(85, y_pos),
             Point(85 + getsize(text, FONT_SIZE), y_pos)).draw(win)

        txt = Text(Point(450, y_pos), f'{text} {pil_size:6.2f}')
        txt.setFace('times roman')
        txt.setSize(FONT_SIZE)

        txt.draw(win)

    #print(help(txt))
    win.getMouse()
    win.close()

    exit()
    """
    Arial
    Times New Roman

    """
    win = GraphWin('Shows', width=950, height=700)
    win.setBackground('white')
    x = 180
    y = 15
    where = ' ' * 10 + os.path.join(os.getcwd(), __file__)
    Text(Point(x,y),where).draw(win)
    x = 10
    y = 35
    for (title, day, season, airs) in shows:
        text = f'{title} - {day} - Season {season} - {airs}'
        where = ''
        Show(win, Point(x, y), text).draw()
        y += BOX_HEIGHT + FONT_HEIGHT + 15
    x += 150
    y += 20
    when = 'Printed ' + str(datetime.now())
    Text(Point(x,y),when).draw(win)

    _ = win.getMouse()
    win.close()

if __name__ == '__main__':
    main(build_parser().parse_args())
