# CatConnect

Spring Quarter 2018

DTC Section 14, Team 4

Drew Kersnar, Beth Mallon, Jean Selep, Jack Wiig


The purpose of CatConnect is to detect if employees are currently in the office and to mark them "here" or "not here". The client specified that they would prefer an automatic system that requires no daily input to track: something that would run in the background.

Our solution, CatConnect, takes advantage of the fact that all of the client's employees connect to their Wi-Fi network to track presence in the background. If the person's device or devices are connected to the Wi-Fi network, then they are in the office.

To make this happen, we created the following programs:
- prober.sh
- reader.py
- filter.py
- updateDB.sh

... and the following text files (not included, but generated):
- ArpOutput.txt
- MACList.txt
- here.csv
- notHere.csv
- /var/lib/mysql/wordpress/users.txt

... and we are running the following programs:
- WordPress (includes Apache, MySQL, PHP) with plugins:
	- wpDataTables
	- Form Maker

------
PROGRAM / FILE EXPLANATION:
The files are explained in order of relevance from start to finish of the process.

prober.sh - this program runs once a minute, at HR:MN:00, and pings all of the devices within a specified range on the Wi-Fi network. The range is specified in the file and can be easily changed to encompass all of the IP addresses on the network. Each ping lasts 0.01 seconds, so it can run 100 pings per second, or 6000 per minute. At the end of the pinging process, the file calls ARP on all of the addresses and outputs it to the file ArpOutput.txt.

ArpOutput.txt - this file stores the results of the arp call on the IP addresses that were previously pinged. If something does not respond to the ping, it returns <incomplete> with the associated IP address, but if it returns successfully, it returns a MAC address (that looks like: 55:55:55:55:55:55). All of the MAC addresses that prober.sh has detected are in this file, but there is a lot of garbage text also in the file that we want to get rid of.

reader.py - this program runs once a minute, at HR:MN:30, and filters out just MAC addresses from the file ArpOutput.txt. This program reads through all of the text in ArpOutput.txt and filters out anything that has five colons (:), which will only return the MAC addresses in ArpOutput.txt. reader.py writes these MAC addresses one per line to the file MACList.txt. At this point, all of the scanned MAC addresses within the range have been output to a file that just contains the MAC Addresses and nothing else.

updateDB.sh - this program runs once a minute, at HR:MN:30, and updates the file /var/lib/mysql/wordpress/users.txt. CatConnect runs a website on the local IP address of the Raspberry Pi. The website is powered by WordPress, and runs the plugins wpDataTables, which allow for the creation of dynamic data tables, and Form Maker, which allows submission of data from the website. Form Maker writes to a database file stored in /var/lib/mysql/wordpress. The updateDB.sh program copies the data from the database into a text file users.txt, which is stored in /var/lib/mysql/wordpress.

/var/lib/mysql/wordpress/users.txt - this file stores the contents of the database in a text file that can be accessed by other programs. The file will be generated from the website, and updated with updateDB.sh

filter.py - this program runs once a minute, at HR:MN:00, and uses the list of MAC addresses and list of users, converts them to into data structures, and then applies the filter. People are marked in the office if any of their devices' MAC addresses are picked up by the scanner. If a person is in the office, all of the connected devices are displayed in the "Device(s)" section of here.csv. If a person is not in the office, their name is marked in notHere.csv.

here.csv - this file is a table format text file that has two columns: "Name" and "Device(s)". This file lists all of the users in the office in rows, with their name in the first column and their device(s) in the second column. Devices are separated by commas in quotes. Rows are separated by new line characters, and columns are separated by commas.

notHere.csv - this file is a table format text file that has one column for names. This file lists all of the users who are not in the office, one per row.

------
PLUGIN EXPLANATION:

wpDataTables - allows for displaying constantly updating data tables. Every time the page is loaded, the information in the table is read from the file associated with the table. This provides constantly updating information at the refresh of a page.

Form Maker - allows for submission of information to a database. This plugin lets people submit information from the website to the local storage on the Raspberry Pi, to be processed after the fact.
