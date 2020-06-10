import sys
from pwn import * 
import scipy.misc
from numpy import asarray
import statistics


first = ["25,9","34,63","37,30","46,112","68,94","74,37","75,115","83,13","91,96","122,21"]

second = ["22,48","30,118","47,37","52,68","63,85","69,30","69,119","92,65","99,96","119,27"]

third = ["7,40","27,62","33,84","34,7","66,26","88,50","90,108","114,13","120,100","123,61"]

fourth = ["13,13","22,74","38,37","38,71","58,117","80,76","92,57","98,119","103,101","121,96"]

fifth = ["19,45","21,106","43,55","54,84","62,19","62,116","86,71","96,47","107,112","117,85"]

#with open('stars5','r') as f:
#	stars = []
#	for line in f: # read rest of lines
#		stars.append([int(x) for x in line.split()])
# print(stars[24][8])
# print(statistics.mean(stars[0]))
#p_stars = []
#for i in range(0,len(stars)):
	# print(len(stars[i]))
#	for j in range(0,len(stars[i])):
#		if stars[i][j] == 255:
			# print("Pixel value = ",stars[i][j])
#			print(""+str(i)+","+str(j))
#			p_stars.append(""+str(i)+","+str(j)+'\n')
# print(p_stars)
# ar = asarray(stars)
# print(ar)
# scipy.misc.imsave('stars5.png', ar)

p = remote('stars.satellitesabove.me','5013')

p.recvuntil('Ticket please:\n')
p.sendline('  ticket{romeo92831romeo:GFx16QR4gMD1CZhnM5aLJMz0lCstnZacPbnx5EReQO5kLuk1FVQo6J4rofa685DJyQ}  ')
log.info("Connected")
p.recvuntil('(Finish your list of answers with an empty line)\n')
log.info("Send")
# p.recvuntil('(Finish your list of answers with an empty line)\n')
for i in first:
	p.sendline(i)
	print(i)
p.send('\n')
p.recvuntil('(Finish your list of answers with an empty line)\n')
log.info("Passed first")
for i in second:
	p.sendline(i)
	print(i)
p.send('\n')
p.recvuntil('(Finish your list of answers with an empty line)\n')
log.info("Passed second")
for i in third:
	p.sendline(i)
	print(i)
p.send('\n')
p.recvuntil('(Finish your list of answers with an empty line)\n')
log.info("Passed third")
for i in fourth:
	p.sendline(i)
	print(i)
p.send('\n')
p.recvuntil('(Finish your list of answers with an empty line)\n')
log.info("Passed fourth")
for i in fifth:
	p.sendline(i)
	print(i)
p.send('\n')
log.info("[+]Passed fifth")
log.warning(p.recvall())
# print("[+]Connection OK")
# p.send(p_stars)
# p.send('\n')
# print("Finished")
