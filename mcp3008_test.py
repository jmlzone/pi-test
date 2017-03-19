#!/usr/bin/python
 
import spidev
import time
import os
 
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts
 
# Define delay between readings
delay = 5
 
while True:
    print "--------------------------------------------"
    for ch in range (0, 8):
        val = ReadChannel(ch)
        volts = ConvertVolts(val,2)
        # Print out results
        print " %d : %d  (%f)" % (ch, val, volts)

    # Wait before repeating loop
    time.sleep(delay)
