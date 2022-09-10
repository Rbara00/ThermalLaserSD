import RPi.GPIO as GPIO
from time import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)
GPIO.setup(13,GPIO.OUT)
GPIO.output(13,GPIO.LOW)

#starts program initializing the paw placement to false and waits for change in resistance on the photodiode
print("Program Started")
first_placed=False

#Waiting for the paw to be placed over the diode
while first_placed is False:
    print("Searching for Paw")    
    #GPIO pin 11 is hooked up to the PhotoDiode
    #When the photodiode's gets covered, it has a high resistance and the signal generated to GPIO(11) is low (0V)
    if GPIO.input(11)==0:
        first_placed=True #If the photodiode has a high resistance then the paw covers the diode
        GPIO.output(13,GPIO.HIGH) #The Laser is hooked up to GPIO(13), since the paw covers the diode, start the laser
        print("Paw Placed")
        continue
#record the initial time using Python's built in function once the laser begins       
t_0=time()
while True:
    if GPIO.input(11)==0: #when GPIO(11) is lwo, paw covers photdiode
        placed=True
        
    else:
        placed=False #When the paw does not cover the photodiode, signal is high with low resistance
    #Checking for a valid paw response
    if first_placed is True and placed is False:
        t_1=time()-t_0 #Stop Timer and calculate the difference as the withdrawal time
        print "Paw Placed time: %s seconds" % t_1 #output the withdrawal time in seconds
        GPIO.output(13,GPIO.LOW) #Power the Laser off
        break #Stop program (This should be changed to run again by asking the user if they want to run another trial)
GPIO.cleanup() #This is here to reset the GPIO for the next test

