# cal

# Introduction

Draws a wall calendar. The title page (first) shows the year and a
title. The rest of the pages show image and month calendar pages for all
12 months.

# JSON files

There are 2 JSON data files:

  * holidays.json - defines various holidays and important days.
  * images_filename - specifies a list of images to be on the even
    pages of the calendar. Page 1 is the title page. When you bind the
    pages along the long edge, you create a wall calendar with images
    on the top and the month calendars on the bottom. See the
    Constructing Calendar
    section for more details.
  
  
  The file holidays.json is assumed. The images_filename file either
  defaults to 'rachel_welch.json' or is passed as the --images_filename parameter to specify a
  different file.

## holidays.json

This file is a list of date specifiers for important events on
certains dates of the calendar. Each specifier is a triple
consisting of the name of the event, followed by the month number
when the event occurs. The event name is shown on the calendar. The
third element of the triple is an integer 
or a list. For Pi day, holiday specifier is ["Pi Day", 3, 14]. Other events
which occur at a fixed day, like News Years Day and Halloween, follow
this form. 

Instead of an integer, the third element of a holiday specifier can be tuple
list consisting of an integer week number and a capitalized day of the
week. Thanksgiving Day is the 4th Thursday of the week in November, so
its holiday specifier is ["Thanksgiving Day", 11, [4, "Thursday"]]. Memorial
Day is the last Monday in May, so its holiday date specifier is
["Memorial Day", 5, 
[-1, "Monday"]]. The -1 counts from the end of the month.

Most dates can be specified in this manner. An exception is the United
States Tax Day. Look up 'Tax Day' in wikipedia to see this how to
determine when annual taxes are due.

The holiday events are for the
United States.
If you are in a different country your holiday events
may differ.
This is why the holiday events are specified in a JSON file.

## images_filename

This file is used to specify images that are to be a part of the wall calendar.
It is a dictionary with the following keys

  - directory - fully specified directory containing the images.
  - title_text - text to show in the title page.
  - images - a list of image file names in the directory. There should be 12
	images. Any extra are ignored.

I created rachel_welch.json to create a calendar with images of Rachel
Welch. If you have images of bunnies or fall scenes you can create you
own calendar by creating a JSON file for them and passing that name as
the --images_filename parameter.

# Create A Virtualenv And Install Dependencies

Run these commands:

    python -m venv cal-env
    See note
    source cal-env/bin/activate
    pip install pip -U # Latest pip
    pip install -r requirements.txt


Note:

If the cal-env/bin directory doesn't exist, run the following commands
to activate the venv.
  
    dos2unix cal-env/Scripts/activate
    source cal-env/Scripts/activate

# Usage

    $ ./make_calendar.py -h
    usage: make_calendar.py [-h] [-i IMAGES_FILENAME] [-y YEAR] [-q]

    Makes a wall calendar with images.

    options:
      -h, --help            show this help message and exit
      -i IMAGES_FILENAME, --images_filename IMAGES_FILENAME
                            JSON file with image data. Default: rachel_welch.json.
      -y YEAR, --year YEAR  The year to draw. default: 2025
      -q, --quiet           Don't display messages. default: False

# Constructing Calendar

The primary output for the make_calendar.py is year.pdf, whatever year is
specified. Use Adobe Acrobat to display and print the wall
calendar. Be sure to print it double-sided.

To make the wall calendar, stack the pages so that the title page is
 at the top. Punch 5 holes above the year. Use a 3 hole punch and a
 hand punch 2 more holes 5.5 cm from either side of the center hole. Punch 1 hole
 below title. I ordered this from Amazon to join the pages:

    Loose Leaf Binder Office Book Rings 1-Inch
    https://www.amazon.com/dp/B07RN4QGW2?ref=ppx_yo2ov_dt_b_fed_asin_title

Use 5 of them to join the pages together. Use the single hole to hang
it from a wall. When showing a month, an image will appear at the top
and the calendar for a month at the bottom.
