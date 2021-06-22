import os
import logging
from datetime import datetime

import qrcode
from PIL import Image,ImageDraw,ImageFont
from netifaces import AF_INET
import netifaces as ni

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')

# Return a datetime object by parsing date string from forecast data
def get_datetime(date_str):
    datetime_object = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return datetime_object

# Return the string name of the week from the passed in date
def get_day_name(date):
     return date.strftime("%A")

# Generate QR Code
def generate_qr_code(input_data):
    logging.info("Generating QR code")

    qr = qrcode.QRCode(
        version=1,
        box_size=1,
        border=0)
    qr.add_data(input_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

# Get a display font to write with
def get_font(size):
    font_file = os.path.join(picdir, 'Font.ttc')
    f = ImageFont.truetype(font_file, size)
    return f

# Return icon image based on forecast category
def get_icon(forecast):
    if forecast['category'] == 'Rain':
        pouring = Image.open(os.path.join(picdir, 'weather-pouring.jpg'))
        return pouring
    elif forecast['category'] == "Clouds":
        cloudy = Image.open(os.path.join(picdir, 'weather-cloudy.jpg'))
        return cloudy
    elif forecast['category'] == "Snow":
        snow = Image.open(os.path.join(picdir, 'weather-snowy.jpg'))
        return snow
    else:
        sunny= Image.open(os.path.join(picdir, 'weather-sunny.jpg'))
        return sunny

# Adjust time from open weather to account for timezone offset
def time_adjust(timestamp, timezone):
    t = timestamp + timezone
    d = datetime.utcfromtimestamp(t)
    time = d.strftime("%H:%M")
    return time

# Draw data to the display image
def _draw_data(image, d):
    logging.info("Drawing current weather widgets")

    # Date and time
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    current_day = now.strftime("%a")
    current_date_str = now.strftime("%b %d")

    logging.info(f"Current date: {now}")

    my_ip = ni.ifaddresses('wlan0')[AF_INET][0]['addr']
    qr = generate_qr_code(f'http://{my_ip}')

    title = f"{d['first_name']} {d['last_name']}"

    # Drawing utility
    draw = ImageDraw.Draw(image)

    # Element padding
    pad = 10

    # Title
    draw.text((pad, pad), title, font = get_font(16), fill = 0)

    # IP & QR Code for IP
    draw.text((145, pad), my_ip, font = get_font(10), fill = 0)
    image.paste(qr, (215, pad))

    # ---

    # Today's Date
    draw.text((30, 50), f"{current_day}, {current_date_str}", font = get_font(24), fill = 0)

    # ---

    x_offset = 0
    y_offset = 0

    # Update time
    x_offset += 60
    y_offset += 100

    draw.text((x_offset, y_offset), f"updated: {current_time} ", font = get_font(16), fill = 0)

    # ---

    # Divider Line
    y_offset += -15
    draw.line(((pad + 20) , y_offset, (image.width - pad - 20), y_offset), fill = 0, width = 3)

    return image

# Create and draw the widgets onto a new display image
def draw(dims, data):
    # Create a new image to draw our display on
    display_image = Image.new('1', dims, 255)  # 255: white

    # Draw data to the display image
    display_image = _draw_data(display_image, data)

    return display_image
