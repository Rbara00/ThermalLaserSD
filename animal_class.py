###########################################
## 
## Animal Class for thermal laser
## SD Team 10: Robert Bara, Zari Grandy, Ezra Galapo, Tyiana Smith
## 
## Author: Robert Bara
## Date:    4/5/2022
## Version: 2.4
##
## Description:
##  This python file contains the class functions to create an animal data type, obtain data, and analyze the
##  data for the thermal laser plantar test on test animals.
##
## Usage:
##  This program is invoked by test_class.py
##
########################################

############ Includes ##################
from datetime import date   
from os import stat
from re import S
from sre_constants import MAXGROUPS             # Import date class from datetime module
from statistics import pstdev    # Import statistics to utilize mean, standard deviation, and variance calculations
from statistics import pvariance
from statistics import mean
#import RPi.GPIO as GPIO        # Import General-Purpose In/Out for RPI4 to control laser and photodiode
from time import time
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
    # Getter Functions for animal's attributes
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

    #Method for performing a trial and saving the data
    def trial(self):

        ############################################################################
        #Setup GPIO Board for RPI
       # GPIO.setmode(GPIO.BOARD)
       # GPIO.setup(13,GPIO.OUT)
       # GPIO.output(13,GPIO.LOW)
        ############################################################################

        #Run a trial and insert withdrawal time into a list for exporting
        t_1=animal.timer()

        ############################################################################
        #Clear the GPIO Pins, overide laser to be off
       # GPIO.setmode(GPIO.BOARD)
       # GPIO.setup(13,GPIO.OUT)
       # GPIO.output(13,GPIO.LOW)
        ############################################################################

        t_1=float(t_1) #Ensure the time is a valid time with decimals
        #Was the trial valid enough for the user?
        valid_trial=self.validInput(input("Keep trial? (Yes/No/Quit): "))
        if valid_trial==0:
            #perform a retrial
            self.trial()
        if valid_trial==1:        
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
        return
        
    #Method for recording withdrawal time
    def timer():
       # GPIO.setmode(GPIO.BOARD)
       # GPIO.setup(11,GPIO.IN)  #PhotoDiode Signal Pin
       # GPIO.setup(13,GPIO.OUT) #Output to the Laser
       # GPIO.output(13,GPIO.LOW) #Initialize to off
    
        print("\tProgram Started")
        
        #--------------------------------------------------------------
        
        t_1=input("") #REMOVE THIS LINE IN FUTURE THIS IS JUST FOR PROGRAMMING AT HOME
        
        print("\tPaw Placed time: %s seconds" % t_1)
        return t_1
        #--------------------------------------------------------------
        
        first_placed=False
        print("Searching for Paw")
        while first_placed is False:
            GPIO.output(13,GPIO.LOW)
            if GPIO.input(11)==0:
                first_placed=True
                GPIO.output(13,GPIO.HIGH) #Turn on the Laser
                print("Paw Placed")
                continue
        
        t_0=time()
        while True:
            if GPIO.input(11)==0:
                placed=True
               
            else:
                placed=False
                GPIO.output(13,0)

            if first_placed is True and placed is False:
                t_1=time()-t_0
                print("Paw Placed time: %s seconds" % t_1)
                GPIO.output(13,GPIO.LOW) #Turn off the laser
            
                break
        GPIO.output(13,GPIO.LOW)    #Possibly could comment out
        GPIO.cleanup()              #Could possibly comment out
        return t_1

    # Function for printing withdrawal times stored within list 
    def printTime(self):
        trialNum=1      #Counter for the current Trial
        #Print the animal's information and date
        print("Animal's Name:",self.name,"\tGroup:",self.group,"\tTest Date:",self.date,"\t Test Times:",self.startTime,"-",self.endTestTime)
        print("----------------------------------------------------------------------------")
        
        #Print the times for each trial
        for i in self.time:
            print("Trial",trialNum,":","%s seconds" % i)
            trialNum+=1
        #Print the animal's average time, standard deviation, variance
        print("\nAnalysis")
        
        #If there is only 1 trial, dont update analysis
        if self.numOfTrials<=1:
            self.avg=self.getTimeAt(0)  #Average will be the only valid trial
            self.standardDev=0          #Standard Dev and Variance would be 0 due to insufficient trials
            self.trialVariance=0
            print("***Not enough trial data to perform analysis***")
        #Otherwise if there are multiple valid trials, print analysis
        else:
            #Print the animal's analysis
            print("Average:", self.avg)
            print("Variance:", self.trialVariance)
            print("Standard Deviation:", self.standardDev,"\n")
        return 
    #Checks yes, no, or when to quit program
    def validInput(self,user_input):
        while True:
            if(user_input.lower()=="y") or user_input.lower()=="yes" or user_input=="1":
                output=1
                break
            if(user_input.lower()=="n") or user_input.lower()=="no" or user_input=="0":
                output=0
                break
            if(user_input.lower()=="q") or user_input.lower()=="quit" or user_input=="-1":
                output=-1
                break
            #Prompt for a new input if invalid
            user_input=input("Please Enter a Valid Input (Yes/No/Quit)")
        return output
