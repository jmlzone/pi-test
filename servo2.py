#!/usr/bin/python
#
# copyleft 2016 James Lee jml@jmlzone.com
#
# hardware setup infomation
# board pin 11 is ued for this demo
import RPi.GPIO as GPIO 
import time
servoPin = 16 # was 11
def setServoByWidth(pwm,pw):
    pp = (pw * 100.0)/period # pulse percentage
    #print "Set PWM percentage %f" % pp
    pwm.ChangeDutyCycle(pp)

def setServoByAngle(pwm,angle):
    # 0 degrees = 0.6 ms
    # 180 degrees = 2.6 ms
    deg0 = 0.6
    deg180 = 2.6
    span = deg180-deg0
    if(angle >=0 and angle <=180) :
        ap=angle/180.0
        pw=(ap*span) + deg0;
        setServoByWidth(pwm,pw)


# main program starts here
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPin,GPIO.OUT)
period = 20.0 # ms = 50 hz
frequency = 1000/period # 50 hz
pwm=GPIO.PWM(servoPin,frequency)
# 90 degrees is 1.5 ms per spec
pw = 1.5 #ms
# full cycle is 20ms
# a 10 ms pulse would be 50%
pp = (pw * 100.0)/period # pulse percentage
print "Set PWM percentage %f" % pp
time.sleep(0.01)
pwm.start(pp)
time.sleep(0.01)
pwm.ChangeDutyCycle(7.5)

#while true :

for loop in range (1,10) :
    for angle in range (30,120):
        setServoByAngle(pwm,angle)
        time.sleep(0.1)
        for angle in range (120,30,-1):
            setServoByAngle(pwm,angle)
        time.sleep(0.1)

setServoByAngle(pwm,90)
time.sleep(1.0)
pwm.stop()
GPIO.cleanup()
