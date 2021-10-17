"""
programma scaricato dal sito Skyfield.
Riferimento:  https://rhodesmill.org/skyfield/
Il programma calcola la posizione di Marte nel cielo.
"""

from skyfield.api import load, wgs84
from skyfield.positionlib import position_of_radec

# Create a timescale and ask the current time.
ts = load.timescale()
t = ts.now()

# Load the JPL ephemeris DE421 (covers 1900-2050).
planets = load('de421.bsp')
earth, mars = planets['earth'], planets['mars']

# What's the position of Mars, viewed from Earth?
astrometric = earth.at(t).observe(mars)
ra, dec, distance = astrometric.radec()

print('Mars actual position')
print(ra)
print(dec)
print(distance)
print()
print()
print('Next, angular distance of the moon from the Sun along ecliptic')


"""
A seguire, un altro programma scarticato dallo stesso sito.
Il programma calcola l'angolo tra Luna e Sole lungo l'eclittica,
differenza tra le longitudini eclittiche di Sole e Luna
"""

from skyfield.api import load
from skyfield.framelib import ecliptic_frame

ts = load.timescale()
t=ts.now()
#t = ts.utc(2021, 10, 11, 16, 4)# year, month, day, hour, minutes

eph = load('de421.bsp')
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

e = earth.at(t)
_, slon, _ = e.observe(sun).apparent().frame_latlon(ecliptic_frame)
_, mlon, _ = e.observe(moon).apparent().frame_latlon(ecliptic_frame)
phase = (mlon.degrees - slon.degrees) % 360.0

print(type(phase))
if phase>0:
    print('phase >0')
else:
    print('phase<=0')
print('{0:.1f}'.format(phase))

"""
Quello che segue è un esempio
"""
from skyfield.api import Angle
ra, dec = Angle(hours=5.5877286), Angle(degrees=-5.38731536)

print('RA {:.8f} hours'.format(ra.hours))
print('Dec {:+.8f} degrees'.format(dec.degrees))

dec=str(dec.degrees)
print(type(dec))
print(dec)
dec=float(dec)
print(dec/2)

"""
ts = load.timescale()
t = ts.utc(2021, 2, 26, 15, 19)

planets = load('de421.bsp')  # ephemeris DE421
#moon = planets['Moon Barycenter']
earth = planets['Earth']
astrometric = earth.at(t).observe(moon)
ra, dec, distance = astrometric.radec()
print(Geoid.subpoint(astrometric))
"""
# A new set of instructions trying to get ISS and Moon coordinates

from skyfield.api import load, wgs84
#from orbit import ISS

#same function used in Astro Pi program, only some different naming
def convert(angle):
    """
    Convert a `skyfield` Angle to an EXIF-appropriate
    representation (rationals)
    e.g. 98° 34' 58.7 to "98/1,34/1,587/10"

    Return a tuple containing a boolean and the converted angle,
    with the boolean indicating if the angle is negative.
    """
    sign, degrees, minutes, seconds = angle.signed_dms()
    coord_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, coord_angle



stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'
satellites = load.tle_file(stations_url)

by_name = {sat.name: sat for sat in satellites}
satellite = by_name['ISS (ZARYA)']

"""
Similar instructions for the moon
"""
t=ts.now()

geocentric = satellite.at(t)
subpoint = wgs84.subpoint(geocentric)
#testing:
print('ISS')
print('Latitude:')
print(subpoint.latitude)
print('Longitude:')
print(subpoint.longitude)
# Convert Skyfield Angle format to ordinary format
south, exif_latitude = convert(subpoint.latitude)
west, exif_longitude = convert(subpoint.longitude)

# Set the EXIF tags specifying the current location-MODIFIED
lat_value = exif_latitude
lat_sign = "S" if south else "N"
long_value = exif_longitude
long_sign = "W" if west else "E"
#testing:
print('ISS latitude converted:')
print(lat_sign, lat_value)
print('ISS longitude converted:')
print(long_sign, long_value)

"""
Similar instructions for the Moon
"""







