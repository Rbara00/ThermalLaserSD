import RPi.GPIO as GPIO
from time import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)
GPIO.setup(13,GPIO.OUT)
GPIO.output(13,GPIO.LOW)
    
print("Program Started")
first_placed=False
while first_placed is False:
    print("Searching for Paw")
    if GPIO.input(11)==0:
        first_placed=True
        GPIO.output(13,GPIO.HIGH)
        print("Paw Placed")
        continue
        
t_0=time()
while True:
    if GPIO.input(11)==0:
        placed=True
        
    else:
        placed=False
    if first_placed is True and placed is False:
        t_1=time()-t_0
        print "Paw Placed time: %s seconds" % t_1
        GPIO.output(13,GPIO.LOW)
        break
GPIO.cleanup()
