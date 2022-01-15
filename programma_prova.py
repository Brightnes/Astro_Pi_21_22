"""
No more than 3 GB of data.
In case of darkness, photos are not deleted, they are overwritten instead.
Mind check variable values through functions.
Check 0.09 brightness value on HQ camera dark photos (from ISS samples or taken on Earth).
"""

from sense_hat import SenseHat
from pathlib import Path
from datetime import datetime, timedelta
from time import sleep
import csv
from logzero import logger, logfile
from orbit import ISS
from skyfield.api import load
from picamera import PiCamera
import PIL.ExifTags
import PIL.Image
from random import randint

# Variables definitions and settings
earth_nightime="Null"# A silly value initialization
wavy_clouds_in_photo="Null"# A silly value initialization
i=1 # For loop numbering purpose
pic=1 # For photo numbering purpose

# Function definitions

def chck4night(num):
    # if brughtness value of actual and last photos is less than 0.09, say it's night on earth, else day or twilight
    
    foto_prec = PIL.Image.open(f"{base_folder}/image_{num-1:04d}.jpg")
    exif_prec = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in foto_prec._getexif().items()
                if k in PIL.ExifTags.TAGS
                }
            
    foto_now = PIL.Image.open(f"{base_folder}/image_{num:04d}.jpg")
    exif_actl = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in foto_now._getexif().items()
                if k in PIL.ExifTags.TAGS
                }
    
    if (exif_prec["BrightnessValue"]<=0.09 and exif_actl["BrightnessValue"]<=0.09):
        earth_night = True
    else:
        earth_night = False
    return earth_night
        
        
def dark_or_shining():
    t = timescale.now()
    if ISS.at(t).is_sunlit(ephemeris):
        ISS_shadowing = True
    else:
        ISS_shadowing = False
    return ISS_shadowing



def create_csv(data_file):
    with open(data_file, 'w', buffering=1) as f:
        writer = csv.writer(f)
        header = ("Date/time", "Loop number", "Pic number", "ISS_shadowing_now", "earth_nightime", "Wavy clouds in precedent photo detected", "Mag field x", "Mag field y","Mag field z", "Acceler x", "Acceler y", "Acceler z", "Latitude", "Longitude")
        writer.writerow(header)


def add_csv_data(data_file, data):
    with open(data_file, 'a', buffering=1) as f:
        writer = csv.writer(f)
        writer.writerow(data)
        

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

def search4wav (photo_number):
    #this function will be a bit silly at first; it will be edited to account for use of coral hardware
    #write here a set of instructions
    #to use the coral ML hardware;it should output a confidence value for presence of wavy clouds in photo
    wave_clouds_in_photo=randint(0,100)#final code will get rid of randint and use the coral hardware output
    if wave_clouds_in_photo >= 80:
        photo_with_wavy_clouds=True
    else:
        photo_with_wavy_clouds=False
        
    return photo_with_wavy_clouds
        

def doing_stuff(a, b):
    global i, pic, wavy_clouds_in_photo
    try:
        logger.info(f"Loop number {i} started")
        location = ISS.coordinates()
        lat = location.latitude.degrees
        long = location.longitude.degrees
        logger.info("Loop {} coordinates computed".format(i))
        acceler = sense.get_accelerometer_raw()
        sleep(0.02)
        acceler = sense.get_accelerometer_raw()
        logger.info("Loop {} acceleration values measured".format(i))
        mag_value = sense.get_compass_raw()
        sleep(0.02)
        mag_value = sense.get_compass_raw()
        logger.info("Loop {} mag values measured".format(i))
        for el in mag_value:
            mag_value[el]=round(mag_value[el],3)

        for el in acceler:
            acceler[el]=round(acceler[el],3)
        logger.info("Loop {} mag, accel values rounded to 0.001".format(i))
        if pic >= 2:
            wavy_clouds_in_photo = search4wav(pic-1)
        #maybe it's better to move photo capture call before writing data to csv file
        #so we can have coral hardware work on actual photo
        row = (datetime.now(), i, pic, a, b, wavy_clouds_in_photo, mag_value["x"], mag_value["y"], mag_value["z"], acceler["x"], acceler["y"], acceler["z"], lat, long)# Add entries if needed
        add_csv_data(data_file, row)
        logger.info("Loop {} data line added to csv file".format(i))
        photo = f"{base_folder}/image_{pic:04d}.jpg"
        capture(camera,photo)# Check if photo numbering is ok.
        logger.info("Loop {} photo saved with photo number {}".format(i,pic))
        #(base_folder/"image.jpg").unlink() # Uncomment for life in space
        pic +=1
        sleep(30)# edit to get more photos
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

while (now_time < start_time + timedelta(minutes=10)):# properly edit timedelta value
    ISS_shadowing_now = dark_or_shining()# Try move this function call at the end, setting up ISS_shadowing_now at start
    #camera.start_preview(alpha=200)
    # Camera warm-up time
    sleep(2)
    doing_stuff(ISS_shadowing_now, earth_nightime )
    sleep(1)
    #camera.stop_preview()
    # Update the current time
    now_time = datetime.now()
    i +=1
    if pic >=3:
        earth_nightime = chck4night(pic-1)
        if earth_nightime:
            pic -= 1

camera.close()
logger.info("Program finished")

