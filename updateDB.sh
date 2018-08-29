# This code updates the list of users, devices, and MAC addresses for CatConnect.
# The data is pulled from the 'wordpress' database which stores submissions from the plugin 'Form Maker' by WebDorado F0rm Builder Team 
# The updated list outputs to the file 'users.txt' which is located in  '/var/lib/mysql/wordpress'
# Created by: Beth Mallon during Spring Quarter 2018 for DTC 2 at Northwestern for the project 'CatConnect' by Team 4, Section 14

#!/bin/bash

sudo rm /var/lib/mysql/wordpress/users.txt 

sudo mysql --password=owl wordpress<<EOFMYSQL
select element_value from wp_formmaker_submits INTO OUTFILE 'users.txt'; # copies all the text from the column 'element_value' in the wordpress database table called 'wp_formmaker_submits' into a text file called 'users.txt'
EOFMYSQL 