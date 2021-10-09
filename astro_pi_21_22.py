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

try:
    logger.info(f"Loop number {i+1} started")
    location = ISS.coordinates()
    lat = location.latitude.degrees
    long = location.longitude.degrees
    row = (datetime.now(),lat, long, sense.temperature, sense.humidity)# Mind updating with roundings
    add_csv_data(data_file, row)
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    camera.capture(f"{base_folder}/image.jpg")
    #(base_folder/"image.jpg").unlink() # Uncomment for life in space

    
    sleep(60)
except Exception as e:
    logger.error(f'{e.__class__.__name__}: {e})')


i +=1 # Update loop numbering

