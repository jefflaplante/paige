#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os
import time
import traceback
import logging
from pprint import pformat
import argparse

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')

if os.path.exists(libdir):
    sys.path.append(libdir)

from PIL import Image,ImageDraw,ImageFont

# from waveshare_epd import epd7in5_V2
from waveshare_epd import epd2in13_V2 as epd

import display

# Update e-paper display
def update_display(image, epd):
    logging.info("Updating e-paper display")
    epd.display(epd.getbuffer(image))
    epd.sleep()
    epd.Dev_exit()

# Parse log level to option from CLI options
def parse_log_level():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", 
        "--log", 
        default="info",
        help=(
            "Provide logging level. "
            "Example --log debug', default='info'")
    )

    options = parser.parse_args()

    levels = {
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG
    }

    level = levels.get(options.log.lower())
    if level is None:
        raise ValueError(
            f"log level given: {options.log}"
            f" -- must be one of: {' | '.join(levels.keys())}")
    
    return level

def main():
    try:
        logging.basicConfig(level=parse_log_level())

        logging.info("Updating display")

        # Gather data to send to display creator
        d = {
            "first_name" : "Paige",
            "last_name" : "LaPlante"
        }

        # Initialize the display driver
        e = epd.EPD()
        e.init()

        # Generate a new display image
        img = display.draw((epd.EPD_WIDTH, epd.EPD_HEIGHT), d)

        # Write out image to disk as a jpeg
        img.save('display.jpg', "JPEG")

        # Update e-paper display
        update_display(img, e)

    except IOError as err:
        logging.info(err)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd.epdconfig.module_exit()
        exit()

if __name__ == "__main__":
    main()
