import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)

def main():
    print "Program Started"
    first_placed=False
    t_0=time()
    while True:
        if GPIO.input(11)==0:
            placed=True
            if first_placed is False:
                print "Paw Placed"
                first_placed=True
        else:
            placed=False
        if first_placed is True and placed is False:
            t_1=time()-t_0
            print "Paw Placed time: %s" % t_1
            break
