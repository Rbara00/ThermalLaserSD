import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)
GPIO.setup(13,GPIO.OUT)
try:
    while True:      
        if GPIO.input(11) == 0:
                print "Paw Placed"

        else:
            print "Paw Not Found"
    
    flag==0   
    while True:    
        if GPIO.input(11)==0 and flag==0:
                flag==1
                TIMER_START==time 
        endif
        
        if GPIO.input(11)>0 and flag == 1:
                flag==0
                TIMER_END=time
                print "TIME TO WITHDRAW== TIMER_END-TIMER_START"
        endif
finally:
    GPIO.cleanup()

