from pwn import *
from skyfield.api import Topos, load

from skyfield.api import EarthSatellite
from skyfield.api import Topos, load
from skyfield.api import utc


from datetime import datetime


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))

def flit_alt(alt):
	if alt < 90:
		alt = 180 - alt
	else:
		alt = alt - 180

	return alt

def get_sat(satName):
	with open("active.txt") as active:
		line = active.readline()
		while line:
			line = line.rstrip()  # remove '\n' at end of line
			if satName == line:
				l1 = active.readline().rstrip()
				l2 = active.readline().rstrip()
				return (l1,l2)
			line = active.readline()


def get_servo(lat, lng, sat_name, timestamp):
	ts = load.timescale()
	lines = get_sat(sat_name)
	line1 = lines[0]
	line2 = lines[1]

	current_time = timestamp

	my_position = Topos(lat , lng)
	satellite = EarthSatellite(line1,line2,sat_name,ts)
	difference = satellite - my_position

	data = ""
	for i in range(720):

		dt_object = datetime.utcfromtimestamp(current_time)
		dt_object = dt_object.replace(tzinfo=utc)
		t = ts.utc(dt_object)

		topocentric = difference.at(t)

		alt, az, distance = topocentric.altaz()

		alt_d = alt.degrees
		az_d = az.degrees

		if(az_d > 180):
			alt_d = flit_alt(alt_d)
			az_d = az_d - 180

		if(az_d < 0):
			alt_d = flit_alt(alt_d)
			az_d = 180 + az_d


		# print(current_time,az_d,alt_d)

		data += str(current_time) +', ' + str(translate(az_d,0,180,2457,7372)) + ", " + str(translate(alt_d,0,180,2457,7372)) + '\n'
		current_time += 1
	return data

try:
    p = remote('trackthesat.satellitesabove.me','5031')
except IndexError:
    print("[-]Error:")
    sys.exit()
# Track-a-sat control system
# Latitude: -26.0829
# Longitude: -65.9666
# Satellite: GLOBALSTAR M096
# Start time GMT: 1586968272.603556
# 720 observations, one every 1 second
# Waiting fo
p.recvuntil('Ticket please:\n')
p.sendline('  ticket{uniform58986november:GDS409WNhyYdMl6CmoZRm83zSEH1DTqnruxRF1Vp-DVe9iMX0T7I9a4dTsogNRRwVA}  ')
p.recvuntil('Track-a-sat control system')
p.recvuntil('Latitude: ')
lat = float(p.recvuntil('\n')[:-1])
p.recvuntil('Longitude: ')
lng = float(p.recvuntil('\n')[:-1])
p.recvuntil('Satellite: ')
sat = p.recvuntil('\n')[:-1].decode()
print(sat)
p.recvuntil('Start time GMT: ')
tm = float(p.recvuntil('\n')[:-1])

print(lat,lng, sat,tm)
p.send(get_servo(lat,lng, sat,tm))
p.send('\n')
p.interactive()
#print(get_servo(52.5341,85.18, 'PERUSAT 1',1586789933.820023))