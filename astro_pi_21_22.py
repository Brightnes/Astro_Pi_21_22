"""
No more than 3 GB of data.
Edit 0.07 brightness value- get exif tags value from photos
mind check variable values through funtions
"""

from sense_hat import SenseHat
from gpiozero import MotionSensor # Comment out if I do not use  PIR
from pathlib import Path
from datetime import datetime, timedelta
from time import sleep
import csv
from logzero import logger, logfile
from orbit import ISS
from skyfield.api import load
from picamera import PiCamera

# Variables definitions and settings
earth_twilight=0
ISS_shadowing=0
envir_light=0
moving_creatures_nearby=0
i=0 # For loop numbering purpose
count_back = 5 # see doing_stuff function

# Function definitions

def brightness_check():
    # Not the camera, the light sensor
    sense.color.gain = 16
    light = sense.color.clear
    if light < 64:
        # Dark
        envir_light=0
    else:
        # Light
        envir_light=1

def chck4twilight(camera):
    # if ISS in shadow and brightness of photo above 0.07, say it's twilight, else not twilight (day or late night)
    global ISS_shadowing
    
    if ISS_shadowing == 1 and camera.exif_tags["BrightnessValue"]>=0.07:
        earth_twilight = 1
    else:
        earth_twilight = 0
    


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
        header = ("Date/time", "Loop number", "Mag field x", "Mag field y","Mag field z", "Acceler x", "Acceler y", "Acceler z", "Latitude", "Longitude")
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

def capture(camera, im):
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
    camera.capture(im)

def doing_stuff():
    global i
    try:
        index =i+1
        logger.info(f"Loop number {index} started")
        location = ISS.coordinates()
        lat = location.latitude.degrees
        long = location.longitude.degrees
        acceler = sh.get_accelerometer_raw()
        sleep(0.02)
        acceler = sh.get_accelerometer_raw()
        mag_value = sh.get_compass_raw()
        sleep(0.02)
        mag_value = sh.get_compass_raw()
        for el in mag_value:
            mag_value[el]=round(mag_value[el],3)

        for el in acceler:
            acceler[el]=round(acceler[el],3)
        row = (datetime.now(), index, mag_value["x"], mag_value["y"], mag_value["z"], acceler["x"], acceler["y"], acceler["z"], lat, long)# Add entries if needed
        add_csv_data(data_file, row)
        photo = f"{base_folder}/image_{index:04d}.jpg"
        capture(camera,photo)# Check if photo numbering is ok.
        #camera.close()# I guess opening and closing the camera at each shot is better.
        #(base_folder/"image.jpg").unlink() # Uncomment for life in space
        i +=1

        sleep(60)# edit to get more photos
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')

def doing_other_stuff():
    global i
    try:
        for a in range(4):
            index =i+1
            logger.info(f"Loop number {index} started")
            location = ISS.coordinates()
            lat = location.latitude.degrees
            long = location.longitude.degrees
            acceler = sh.get_accelerometer_raw()
            sleep(0.02)
            acceler = sh.get_accelerometer_raw()
            mag_value = sh.get_compass_raw()
            sleep(0.02)
            mag_value = sh.get_compass_raw()
            for el in mag_value:
                mag_value[el]=round(mag_value[el],3)
            for el in acceler:
                acceler[el]=round(acceler[el],3)
            row = (datetime.now(),index, mag_value["x"], mag_value["y"], mag_value["z"], acceler["x"], acceler["y"], acceler["z"], lat, long)# Add entries if needed
            add_csv_data(data_file, row)
            photo = f"{base_folder}/image_{index:04d}.jpg"
            capture(camera,photo)# Check if photo numbering is ok.
            #camera.close()# I guess opening and closing the camera at each shot is better.
            #(base_folder/"image.jpg").unlink() # Uncomment for life in space
            i +=1
            sleep(60)# edit to get more photos
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')

def doing_some_other_stuff():
    global i
    try:
        index =i+1
        logger.info(f"Loop number {index} started")
        location = ISS.coordinates()
        lat = location.latitude.degrees
        long = location.longitude.degrees
        acceler = sh.get_accelerometer_raw()
        sleep(0.02)
        acceler = sh.get_accelerometer_raw()
        mag_value = sh.get_compass_raw()
        sleep(0.02)
        mag_value = sh.get_compass_raw()
        for el in mag_value:
            mag_value[el]=round(mag_value[el],3)
        for el in acceler:
            acceler[el]=round(acceler[el],3)
        row = (datetime.now(),index, mag_value["x"], mag_value["y"], mag_value["z"], acceler["x"], acceler["y"], acceler["z"], lat, long)# Add entries if needed
        add_csv_data(data_file, row)
        i +=1
        sleep(60)# edit to get more photos
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e})')

# Object name definitions
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
#camera.resolution=camera.MAX_RESOLUTION# Give this instruction a try
camera.framerate = 15


# Part of program to repeat in a loop over 3 hours of execution

# Create a `datetime` variable to store the start time
start_time = datetime.now()
# Create a `datetime` variable to store the current time
# (these will be almost the same at the start)
now_time = datetime.now()
# Run a loop for 2 minutes
while (now_time < start_time + timedelta(minutes=174)):# properly edit timedelta value
    dark_or_shining()
    #camera.start_preview(alpha=200)
    # Camera warm-up time
    sleep(2)
    chck4twilight(camera)
    if ISS_shadowing == 0:
        doing_stuff()
    elif ISS_shadowing == 1 and earth_twilight == 1:
        doing_other_stuff()
    else:
        doing_some_other_stuff()
    sleep(1)
    #camera.stop_preview()
    # Update the current time
    now_time = datetime.now()








