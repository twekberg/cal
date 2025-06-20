# cal

# Introduction

Draws a wall calendar. The title page (first) shows the year and a
title. The rest of the pages show image, month calendar pages for all
12 months. The images are listed in a JSON file with these keys::

    - directory - fully specified directory containing the images.
	- title_text - text to show in the title page.
	- images: a list of image file names in the directory. There should be 12
	- images. Any extra are ignored.

# Usage

    $ ./make_calendar.py -h
    usage: make_calendar.py [-h] [-i INPUT_FILENAME] [-y YEAR] [-q]

    Complete program that makes a wall calendar with images.

    options:
      -h, --help            show this help message and exit
      -i INPUT_FILENAME, --input_filename INPUT_FILENAME
                            JSON file with image data. Default: rachel_welch.json.
      -y YEAR, --year YEAR  The year to draw. default: 2025
      -q, --quiet           Don't show the images. Only create JPG files. default:
                            False
Uses a venv that contains PIL for rendering the graphics. I happen to
have a venv that contains PIL so I use that.

The output for the calendar is year.pdf, whatever year is
specified. Use Adobe Acrobat to display and print the wall calendar.

# TODO

  - The images are scaled and centered on the page so they print
    correctly. Because of this, the current directory contains 12 JPG
    files for the scalled images. In addition, there is a JPG file for
    each month and title.jpg for the title page. There should be
    cleanup to remove these files, as either using a --cleanup
    parameter or doing that after creating the PDF file.
  - Think about adding a feature to specially note holidays. (Since I'm
    retired, every day is a holiday for me.)
  - Create a venv for this program and document it here.
