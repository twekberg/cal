#!/usr/bin/env python
"""
Modified from move-red-box.py.

The idea is to draw the graphics for TV shows I'm watching, noting when a
particular episode has been watched.

To change to another season for the shows, edit the shows list appropriately.
Then run this program and use the Snipping Tool to capture the image and paste
it into Gimp. Finally print.
"""

import argparse
from datetime import datetime
import os
import os.path
from graphics import Rectangle, Text, Line, Point, GraphWin
#from graphics import *

FONT_WIDTH = 10
FONT_HEIGHT = 16
BOX_WIDTH = 25
BOX_HEIGHT = 50


def build_parser():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__.strip())
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

def main(_args):
    """
    Top level function.
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
