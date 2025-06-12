# cal
Draw a month for a wall calendar.

Use this a basis to print 12 months of a wall calendar.

Uses a venv that contains PIL.

Renders the page to the default program that displays PNG files.
I have that set to use gimp.

Usage:

 ./pil_calendar -h
 usage: pil_calendar.py [-h] [-a {calendar,demo}] [-y YEAR] [-m MONTH]

Example of PIL rendering. It renders to a file, when shown is brought
up with Gimp.

The advantage of using PIL is that a LARGE font can be used (100 pts).
tkinter can only support fonts up to a maximum of 30 pts.

options:
  -h, --help            show this help message and exit
  -a {calendar,demo}, --action {calendar,demo}
                        Type of action to perform. default: calendar
  -y YEAR, --year YEAR  The year to draw. default: 2025
  -m MONTH, --month MONTH
                        The month to draw. default: 6
