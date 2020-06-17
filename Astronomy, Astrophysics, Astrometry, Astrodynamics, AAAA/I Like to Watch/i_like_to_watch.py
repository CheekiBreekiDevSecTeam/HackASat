from skyfield.api import EarthSatellite
from skyfield.api import load
from skyfield.api import Topos


line1 = '1 13337U 98067A   20087.38052801 -.00000452  00000-0  00000+0 0  9995'
line2 = '2 13337  51.6460  33.2488 0005270  61.9928  83.3154 15.48919755219337'

ts = load.timescale()

satellite = EarthSatellite(line1, line2, 'CheekiBreekiSat', ts)

# The image was taken on March 26th, 2020, at 21:54:06
t = ts.utc(2020, 3, 26, 21, 54, 06)

#flag located at the base of the Washington Monument
monument = Topos(longitude_degrees = -77.035278, latitude_degrees=38.889484)

geocentric = satellite.at(t)
#print(geocentric.position.km)


difference = satellite - monument
topocentric = difference.at(t)

alt, az, distance = topocentric.altaz()


# Convert elevation to KML tilt
print(90 - alt.degrees, 'deg')
# Satellite-relative azimuth
print(az.degrees - 180, 'deg')
print(int(distance.m), 'm')

