import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)

#Main function
def main():
    #starts program initializing the paw placement to false
    print "Program Started"
    first_placed=False
    t_0=time() #recording the initial time using Python's built in function
    while True:
        #GPIO pin 11 is hooked up to the PhotoDiode
        #When the photodiode's is covered, it has a high resistance and the signal generated to GPIO(11) is low (0V) 
        if GPIO.input(11)==0: 
            placed=True #record the state that the animal has placed it's paw over the diode
            if first_placed is False:
                print "Paw Placed"
                first_placed=True
        #If GPIO(11) has a high voltage sent, then the animal's paw is removed
        else:
            placed=False
        #Determining a valid paw withdrawal
        if first_placed is True and placed is False:
            t_1=time()-t_0 #Calculate the withdrawal time by calculating the difference
            print "Paw Placed time: %s" % t_1 #output the paw withdrawal time in terminal
            break #Exit the program

