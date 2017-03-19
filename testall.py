#!/usr/bin/python
######################################################################
# To request a particular module, send;
#
# #NN   # and two ID digits, no CR LF
#
# The module will reply with fixed field something like;
#
# *NN_CCCCC(space)TTT.TT(space)HH.H(space)LLLLL<cr><Lf> where;
#
# *NN is it responding with the module ID
# CCCCC is the one second timer in the PIC that rolls over at 65535
# TTT.TT is the temperature in degrees F
# HH.H is the relative humidity
# LLLLL is the light (0 to 65535)
#
# Let's use 4800 Baud, N 8 1
#
#
# The unit might take 5 seconds to reply because it will be in a low
# power mode and will go out to make a measurement only on request.
#
# They will all wake up on activity. It is only the one being that
# will stay on longer through the measurement.
#
# I will build one of these up and send it to you along with a
# programming cable so you can change it around if you would like.
#
######################################################################

import time
import os
import RPi.GPIO as GPIO
import serial
import spidev
import Adafruit_DHT
import urllib2

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
TXRX = 18
TX=1
RX=0
GPIO.setup(TXRX, GPIO.OUT)
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
 
def getSensorData(DHTpin):
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, DHTpin)
    
    #Convert from Celius to Farenheit
    if humidity is not None and  temperature is not None:
        temperatureF = 9/5.0 * temperature + 32
    else:
        humidity = None
        temperatureF = None
   
    # return dict
    return (humidity, temperatureF)

# Define delay between readings
delay = 5

ser = serial.Serial(
              
               port='/dev/ttyAMA0',
               baudrate = 4800,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=6
           )
SeqId = 0;

while True:
    print "--------------------------------------------"
    humidity0, temperatureF0 = getSensorData(4)
    if humidity0 is not None and  temperatureF0 is not None:
        print "Sensor 0: SeqId=%d, Temp=%2.1f, Humidity=%d" % (SeqId, temperatureF0, humidity0)
    humidity1, temperatureF1 = getSensorData(17)
    if humidity1 is not None and  temperatureF1 is not None:
        print "Sensor 1:           Temp=%2.1f, Humidity=%d" % (temperatureF1, humidity1)
    for ch in range (0, 8):
        val = ReadChannel(ch)
        volts = ConvertVolts(val,2)
        # Print out results
        print " %d : %d  (%f)" % (ch, val, volts)
    GPIO.output(TXRX, TX)
    print "TX"
    ser.write("this is just a test")
    ser.flush()
    #time.sleep(5)
    ser.flushInput()
    GPIO.output(TXRX, RX)
    print "RX"
    x=ser.readline()
    # should wait 6 second (timeout) for data
    GPIO.output(TXRX, TX)
    print x
    if len(x) > 0 and x.startswith('*') :
        id,t,h,l = x.split(' ')
    #time.sleep(5)
    # Wait before repeating loop
    SeqId += 1
    time.sleep(delay)

 
