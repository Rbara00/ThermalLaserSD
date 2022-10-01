###########################################
## 
## Animal Class for thermal laser
## SD Team 10: Robert Bara, Zari Grandy, Ezra Galapo, Tyiana Smith
## 
## Author: Robert Bara
## Date:    10/1/2022
## Version: 3
##
## Description:
##  This python file contains the class functions to create an animal data type, obtain data, and analyze the
##  data for the thermal laser plantar test on test animals.
##
## Usage:
##  This program is invoked by laser_test_GUI.py
##
########################################

############ Includes ##################
from datetime import date   
from os import stat
from re import S
from sre_constants import MAXGROUPS             # Import date class from datetime module
from statistics import pstdev, pvariance, mean    # Import statistics to utilize mean, standard deviation, and variance calculations
#import RPi.GPIO as GPIO        # Import General-Purpose In/Out for RPI4 to control laser and photodiode
from time import time
from time import sleep
from tkinter import*
from tkinter import messagebox

############ animal Class #################
class animal:
    ##############################
    #Constructor for animal
    ##############################
    def __init__(self,name,group):
        self.name=name            #animal is named from user input
        self.time=[]              #create a list of all the animal's withdrawal times
        self.date = date.today()  #stores the corresponding test date
        self.startTime=0          #stores the timestamp when testing is starting for cat
        self.endTestTime=0        #stores the timestamp when testing is over for the cat
        self.group=group          #stores the cat's group number
        self.avg=0                #Initialize the average to be 0
        self.standardDev=0        #Initialize the standard deviation to be 0
        self.trialVariance=0      #Initialize the variance to be 0
        self.numOfTrials=0        #Counter for how many trials were performed for animal
        return
    
    ##########################################
    # Class Functions:
    ##########################################
    #Getter for the animal's name
    def getName(self):
        return self.name
    #Getter for the test date corresponding to the animal
    def getDate(self):
        return self.date
    #Getter for the animal's group number
    def getGroup(self):
        return self.group
    #Getter for the animal's number of trials completed
    def getNumOfTrials(self):
        return self.numOfTrials    
    #Getter for the average withdrawal time
    def getAvg(self):
        sample=self.time
        self.avg=mean(sample)
        return self.avg
    #Getter for time at specifed trial
    def getTimeAt(self,index):
        return self.time[index] 
    #Getter for the Standard Deviation of the animal's response times
    def getStdev(self):
        sample=self.time
        self.standardDev=pstdev(sample)
        return self.standardDev
    #Getter for the Variance of the animal's response times
    def getVar(self):
        sample=self.time
        self.trialVariance=pvariance(sample)
        return self.trialVariance

    ###################################################################################
    # Functions for turning on laser system and inserting withdrawal time into database
    ###################################################################################
    #Method for inserting a new withdrawl time into the list
    def insertTime(self,new_time):
        self.time.append(new_time)
        self.numOfTrials+=1
        return

    #Trial function with prompt from GUI
    def trial_gui(self,placed_label):
        ############################################################################
        #Setup GPIO Board for RPI
       # GPIO.setmode(GPIO.BOARD)
       # GPIO.setup(13,GPIO.OUT)
       # GPIO.output(13,GPIO.LOW)
        ############################################################################

        #Run a trial and insert withdrawal time into a list for exporting
        t_1=self.timer(placed_label)

        ############################################################################
        #Clear the GPIO Pins, overide laser to be off
       # GPIO.setmode(GPIO.BOARD)
       # GPIO.setup(13,GPIO.OUT)
       # GPIO.output(13,GPIO.LOW)
        ############################################################################

        t_1=float(t_1) #Ensure the time is a valid time with decimals
    
        #Check if the laser timed out
        if (t_1==-10):
            error_msg=messagebox.showerror("Time Out","Error: No reaction detected within 10 Seconds")
            valid_trial=False
        #If a value was returned, ask if this is a valid trial
        else:
            valid_trial=messagebox.askyesno("Valid Trial","Keep Trial?\nName: " + self.name +" Time: "+str(t_1)+" seconds")
        #If trial is discarded, return back to the test menu
        if valid_trial==False:
                placed_label.config(text="Photodiode Status:")
                return
        if valid_trial==True:        
            #When a valid trial is ran, 
            self.insertTime(t_1) #place withdrawal time into list
            if self.numOfTrials>1:
            #Update the analysis
                self.avg=self.getAvg()
                self.standardDev=self.getStdev()
                self.trialVariance=self.getVar()
            else:
                #If there is only 1 trial, dont update analysis
                self.avg=self.getTimeAt(0) #Average is the only valid trial
                self.standardDev=0
                self.trialVariance=0
        placed_label.config(text="Photodiode Status:")
        return
        
    #Method for recording withdrawal time with laser
    def timer(self,placed_label):
       # GPIO.setmode(GPIO.BOARD)
       # GPIO.setup(11,GPIO.IN)  #PhotoDiode Signal Pin
       # GPIO.setup(13,GPIO.OUT) #Output to the Laser
       # GPIO.output(13,GPIO.LOW) #Initialize to off

        first_placed=False
        time_out=10
        placed_label.config(text="Photodiode Status: Searching for Paw")
        #--------------------------------------------------------------       
        #t_0=time()
        #while time()<t_0+10:
        #t_1=input("") #REMOVE THIS LINE IN FUTURE THIS IS JUST FOR PROGRAMMING AT HOME
        #    t_1=time()
        #print("\tPaw Placed time: %s seconds" % t_1)
        #return t_1-t_0
        #--------------------------------------------------------------
        
        #Check if the photo diode is not covered, when it is covered, turn on the laser
        while first_placed is False:
            if GPIO.input(11)==0:           #When the Photodiode is first covered
                first_placed=True
                GPIO.output(13,GPIO.HIGH)   #Turn on the Laser
                t_0=time()                  #Get initial time as laser starts
                continue
        
        #Update GUI Label
        placed_label.config(text="Photodiode Status: Paw Placed, Laser on")

        #Check if the paw is removed and the photo diode becomes uncovered, if so turn off the laser
        #If nothing happens within 10 seconds, turn off the laser and break from the loop
        while True and time()<t_0+time_out:
            if GPIO.input(11)==0:   #check if the photodiode is covered
                placed=True
            else:                   #check if the photodiode is uncovered
                placed=False
                GPIO.output(13,0)   #Turn off the Laser

            #Check if the photodiode reading is valid, if it is, return the withdrawal time and turn off the laser
            if first_placed is True and placed is False:
                t_1=time()-t_0
                GPIO.output(13,0) #Turn off the laser
                break
        #If the timer timed out, then set t_1 to go to the error message
        if((time()>t_0+time_out) and (bool(t_1) is False)):
                t_1=-10
        #Update GUI Label
        placed_label.config(text="Photodiode Status: Paw Removed Laser off")
        
        GPIO.output(13,GPIO.LOW)    #Possibly could comment out
        GPIO.cleanup()              #Could possibly comment out
        return t_1
