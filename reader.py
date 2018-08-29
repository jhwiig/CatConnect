#DTC 2 Section 14, Team 4
#Written by: Drew Kersnar

#Reads from the ArpOutput.txt file, seperates out the MAC addresses, and sends them to MACList.txt

file = open("/home/pi/CatConnect/ArpOutput.txt","r")
data = file.readlines()
macs = []


for line in data:
	elements = line.split()
	for element in elements:
		numColon = 0
		for char in element:
			if char == ":":
				numColon+=1
		if numColon == 5:
			macs.append(element)

file.close()
file = open("/home/pi/CatConnect/MACList.txt","w")

for mac in macs:
	file.write(mac)
	file.write("\n")
file.close()