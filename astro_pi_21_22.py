"""
No more than 3 GB of data.
"""

from sense_hat import SenseHat
from gpiozero import MotionSensor # Comment out if I do not use  PIR
from pathlib import Path
from datetime import datetime
from time import sleeep
import csv
from logzero import logger, logfile
from orbit import ISS
from skyfield.api import load
from picamera import PiCamera

# Variables definitions and settings
ISS_shadowing=0
envir_light=0
moving_creatures_nearby=0
i=0 # For loop numbering purpose

# Function definitions

def brightness_check():
    sense.color.gain = 16
    light = sense.color.clear
    if light < 64:
        # Dark
        envir_light=0
    else:
        # Light
        envir_light=1


def grab_movement():
    # Inititating motion detection
    pir = MotionSensor(pin=12)
    pir.wait_for_motion() # Pause the script until the device is activated, or the timeout is reached.
    moving_creatures_nearby=1
    pir.wait_for_no_motion() # Pause the script until the device is deactivated, or the timeout is reached.
    moving_creatures_nearby=0

def create_csv(data_file):
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Date/time", "Latitude", "Longitude", "Temperature", "Humidity")
        writer.writerow(header)

def add_csv_data(data_file, data):
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)
        
def dark_or_shining():
    t = timescale.now()
    if ISS.at(t).is_sunlit(ephemeris):
        ISS_shadowing = 0
    else:
        ISS_shadowing = 1

def convert(angle):
    """
    Convert a `skyfield` Angle to an EXIF-appropriate
    representation (rationals)
    e.g. 98° 34' 58.7 to "98/1,34/1,587/10"

    Return a tuple containing a boolean and the converted angle,
    with the boolean indicating if the angle is negative.
    """
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle

def capture(camera, image):
    """Use `camera` to capture an `image` file with lat/long EXIF data."""
    point = ISS.coordinates()

    # Convert the latitude and longitude to EXIF-appropriate representations
    south, exif_latitude = convert(point.latitude)
    west, exif_longitude = convert(point.longitude)

    # Set the EXIF tags specifying the current location
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    # Capture the image
    camera.capture(image)

def doing_stuff(index):
    try:
        index +=1
        logger.info(f"Loop number {index} started")
        location = ISS.coordinates()
        lat = location.latitude.degrees
        long = location.longitude.degrees
        row = (datetime.now(),lat, long, round(sense.temperature,4), round(sense.humidity,4))# Add entries if needed
        add_csv_data(data_file, row)
        camera.start_preview()
        # Camera warm-up time
        sleep(2)
        camera.capture(f"{base_folder}/image_{index:04d}.jpg")# Check if photo numbering is ok.
        camera.close()# I guess opening and closing the camera at each shot is better.
        #(base_folder/"image.jpg").unlink() # Uncomment for life in space

        sleep(60)
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')


# Object names definitions
sense = SenseHat()
camera = PiCamera()

# Program main setup stuff

base_folder = Path(__file__).parent.resolve()
data_file = base_folder/'data.csv'
logfile(base_folder/"events.log")
create_csv(data_file)
ephemeris = load('de421.bsp')
timescale = load.timescale()
camera.resolution = (2592, 1944)
camera.framerate = 15


# Part of program to repeat in a loop over 3 hours of execution

# Create a `datetime` variable to store the start time
start_time = datetime.now()
# Create a `datetime` variable to store the current time
# (these will be almost the same at the start)
now_time = datetime.now()
# Run a loop for 2 minutes
while (now_time < start_time + timedelta(minutes=174)):# properly edit timedelta value
    doing_stuff(i)
    sleep(1)
    # Update the current time
    now_time = datetime.now()
    i +=1 # Update loop numbering

