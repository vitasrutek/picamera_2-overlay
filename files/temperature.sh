#! /bin/bash
 
# Read Temperature
tempread=`cat /sys/bus/w1/devices/28-00000b991594/w1_slave`
# Format
temp=`echo "scale=2; "\`echo ${tempread##*=}\`" / 1000" | bc`
 
# Output
echo $temp
