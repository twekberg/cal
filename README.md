# cal

# Introduction

Draws a wall calendar. The title page (first) shows the year and a
title. The rest of the pages show image, month calendar pages for all
12 months. The images are listed in a JSON file with these keys::

    - directory - fully specified directory containing the images.
	- title_text - text to show in the title page.
	- images - a list of image file names in the directory. There should be 12
	  images. Any extra are ignored.

# Create A Virtualenv And Install Dependencies

Run these commands:

    python -m venv cal-env
    See note
    source cal-env/bin/activate
    pip install pip -U # Latest pip
    pip install -r requirements.txt


Note:

if the cal-env/bin directory doesn't exist, run the following commands
to activate the venv.
  
    dos2unix cal-env/Scripts/activate
    source cal-env/Scripts/activate

# Usage

    $ ./make_calendar.py -h
    usage: make_calendar.py [-h] [-i INPUT_FILENAME] [-y YEAR] [-q]

    Makes a wall calendar with images.

    options:
      -h, --help            show this help message and exit
      -i INPUT_FILENAME, --input_filename INPUT_FILENAME
                            JSON file with image data. Default: rachel_welch.json.
      -y YEAR, --year YEAR  The year to draw. default: 2025
      -q, --quiet           Don't display messages. default: False

The output for the calendar is year.pdf, whatever year is
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


# TODO

  - Think about adding a feature to specially note holidays. (Since I'm
    retired, every day is a holiday for me.)
