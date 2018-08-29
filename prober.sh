#!/bin/bash

#DTC 2 Section 14, Team 4
#Written by: Drew Kersnar

for a in {10..10} # <- adjust the range of a here
do
	for b in {106..106} # <- adjust the range of b here
	do
		for c in {7..8} # <- adjust the range of c here
		do
			for d in {0..255} # <- adjust the range of d here
			do
				ping "$a"."$b"."$c"."$d" &
				sleep .01
				PID=$!
				kill -9 $PID
			done
		done
	done
done
arp -a >/home/pi/CatConnect/ArpOutput.txt