"""
No more than 3 GB of data.
Edit 0.07 brightness value- get exif tags value from photos
mind check variable values through functions
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

# Variables definitions and settings
earth_nightime="Null"# A silly value initialization
i=1 # For loop numbering purpose
pic=1 # For photo numbering purpose

# Function definitions

def chck4night(num):
    # if ISS in shadow and brightness of photo above 0.07, say it's night down on earth, else day or twilight
    
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
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Date/time", "Loop number", "Pic number", "ISS_shadowing_now", "earth_nightime", "Mag field x", "Mag field y","Mag field z", "Acceler x", "Acceler y", "Acceler z", "Latitude", "Longitude")
        writer.writerow(header)


def add_csv_data(data_file, data):
    with open(data_file, 'a') as f:
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

def doing_stuff(a, b):
    global i, pic
    try:
        logger.info(f"Loop number {i} started")
        location = ISS.coordinates()
        lat = location.latitude.degrees
        long = location.longitude.degrees
        acceler = sense.get_accelerometer_raw()
        sleep(0.02)
        acceler = sense.get_accelerometer_raw()
        mag_value = sense.get_compass_raw()
        sleep(0.02)
        mag_value = sense.get_compass_raw()
        for el in mag_value:
            mag_value[el]=round(mag_value[el],3)

        for el in acceler:
            acceler[el]=round(acceler[el],3)
        row = (datetime.now(), i, pic, a, b, mag_value["x"], mag_value["y"], mag_value["z"], acceler["x"], acceler["y"], acceler["z"], lat, long)# Add entries if needed
        add_csv_data(data_file, row)
        photo = f"{base_folder}/image_{pic:04d}.jpg"
        capture(camera,photo)# Check if photo numbering is ok.
        #camera.close()# I guess opening and closing the camera at each shot is better.
        #(base_folder/"image.jpg").unlink() # Uncomment for life in space
        pic +=1
        sleep(10)# edit to get more photos
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

while (now_time < start_time + timedelta(minutes=4)):# properly edit timedelta value
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
"""
# a first check
ephemeris = load('de421.bsp')
timescale = load.timescale()

for test in range (4):
    ISS_shadowing_now = dark_or_shining()
    if ISS_shadowing_now == 0:
        print("Sun shining onboard")
    if ISS_shadowing_now == 1:
        print("Night time on board")
    sleep(3)
    
# a second check
# Compute light conditions at utc times. Say 5 utc, it's 6 in Italy
#from skyfield.api import wgs84
stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'
satellites = load.tle_file(stations_url)
by_name = {sat.name: sat for sat in satellites}


eph = load('de421.bsp')
satellite = by_name['ISS (ZARYA)']
ts=load.timescale()

two_hours = ts.utc(2021, 12, 3, 17, range(0, 120, 5))# if it's 7 am in Italy, set 6
sunlit = satellite.at(two_hours).is_sunlit(eph)

for ti, sunlit_i in zip(two_hours, sunlit):
    print('{}  {} is in {}'.format(
        ti.utc_strftime('%Y-%m-%d %H:%M'),
        satellite.name,
        'sunlight' if sunlit_i else 'shadow',
    ))
"""