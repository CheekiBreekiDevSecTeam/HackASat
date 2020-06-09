from pwn import *
from skyfield.api import Topos, load
from skyfield.api import EarthSatellite
from skyfield.api import utc
from datetime import datetime
from skyfield.api import load, JulianDate

# Please use the following time to find the correct satellite:(2020, 3, 18, 9, 13, 51.0)
# Please use the following Earth Centered Inertial reference frame coordinates to find the 
# satellite:[2361.3051812424737, 6348.7859486091065, -67.66795583043648]


def find_satelite(x,y,z,tmt,ts):
	
	with open("stations.txt") as active:


		sat_name = active.readline()
		while sat_name:
			line1 = active.readline()
			line2 = active.readline()
			#print(sat_name,line1,line2)

			satellite = EarthSatellite(line1,line2,sat_name,ts)
			geocentric = satellite.at(tmt)
				

			sat_pos = geocentric.position.km

			if (sat_pos[0] == x and sat_pos[1] == y and sat_pos[2] == z):
				return satellite
			
			sat_name = active.readline().rstrip()

def creatTimeObj(p,ts):
	print(p.recvuntil('coordinate at the time of:('))

	d1 = p.recvuntil(')')[:-1].decode()
	print(d1)
	d1 = d1.replace(",","").split()
	d1 = [float(v) for v in d1]
	tmt = ts.utc(d1[0], d1[1], d1[2], d1[3], d1[4], d1[5])
	return tmt

try:
    p = remote('where.satellitesabove.me','5021')
except IndexError:
    print("[-]Error:")
    sys.exit()

p.recvuntil('Ticket please:\n')
p.sendline('  ticket{delta27590sierra:GAN9H5pLgBJuQ7wGvtA_2JHECniuzTk3DzzDH092MFEUZ-xUDjrNGy7e2VBucLv23w}  ')
p.recvuntil('Please use the following time to find the correct satellite:(')


ts = load.timescale()
d = p.recvuntil(')')[:-1].decode()
d = d.replace(",","").split()
d = [float(v) for v in d]


p.recvuntil('satellite:[')
x = float(p.recvuntil(',')[:-1])
y = float(p.recvuntil(',')[:-1])
z = float(p.recvuntil(']')[:-1])

print(x,y,z)

tmt = ts.utc(d[0], d[1], d[2], d[3], d[4], d[5])
sat = find_satelite(x,y,z,tmt,ts)
dir(sat)

for i in range(3):
	tmt = creatTimeObj(p,ts)
	p.send(str(sat.at(tmt).position.km[0]) + '\n')

	tmt = creatTimeObj(p,ts)
	p.send(str(sat.at(tmt).position.km[1]) + '\n')

	tmt = creatTimeObj(p,ts)
	p.send(str(sat.at(tmt).position.km[2]) + '\n')
	print(p.recvuntil('\n'))

p.interactive()