###########################################
## 
## Cat Class for thermal laser
## SD Team 10: Robert Bara, Zari Grandy, Ezra Galapo, Tyiana Smith
## 
## Date:    2/3/2022
## Version: 1.3
##
## Description:
##  This python program allows for the thermal laser plantar test to run by prompting the user if
##  they would like to perform a test. The class creates a cat, performs a laser test, stores the withdrawal
##  times, as well as performs analysis such as standard dev, average, and variance calculations
##
## Usage:
##  Running: (run it here, eventually build a make file-Rob)
##
########################################


############ Includes ##################
from ast import Num
from datetime import date
from os import stat             # Import date class from datetime module
from statistics import stdev    # Import statistics to utilize mean, standard deviation, and variance calculations
from statistics import variance
from statistics import mean
#import RPi.GPIO as GPIO        # Import General-Purpose In/Out for RPI4 to control laser and photodiode
from time import time           # Import time to calculate withdrawal time
########################################

############ Cat Class #################
class cat:
    ##############################
    #Constructor for cat
    ##############################
    def __init__(self,name):
        self.name=name            #cat is named from user input
        self.time=[]              #create a list of all the cat's withdrawal times
        self.date = date.today()  #stores the corresponding test date
        self.avg=0                #Initialize the average to be 0
        self.standardDev=0        #Initialize the standard deviation to be 0
        self.trialVariance=0      #Initialize the variance to be 0
        self.numOfTrials=0
    
    #############################
    #Class Functions:
    #############################
    #Getter for the average withdrawal time
    def getAvg(self):
        sample=self.time
        self.avg=mean(sample)
        return self.avg
    
    #Getter for time at specifed trial
    def getTimeAt(self,index):
        return self.time[index] 
    
    #Getter for the Standard Deviation of the cat's response times
    def getStdev(self):
        sample=self.time
        self.standardDev=stdev(sample)
        return self.standardDev
    
    #Getter for the Variance of the cat's response times
    def getVar(self):
        sample=self.time
        self.trialVariance=variance(sample)
        return self.trialVariance

    #Method for inserting a new withdrawl time into the list
    def insertTime(self,new_time):
        self.time.append(new_time)
        self.numOfTrials+=1


    #Method for performing a trial and saving the data
    def trial(self):
        #Run a trial and insert withdrawal time into a list for exporting
        t_1=cat.timer()
        t_1=float(t_1) #Ensure the time is a valid time with decimals
        #Was the trial valid enough for the user?
        valid_trial=input("Keep trial? (Yes/No): ")
        if valid_trial != "y":
            #perform a retrial
            self.trial()
        else:        
            #When a valid trial is ran, 
            self.insertTime(t_1) #place withdrawal time into list

        return
        
    #Method for recording withdrawal time
    def timer():
        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(11,GPIO.IN)
        #GPIO.setup(13,GPIO.OUT)
        #GPIO.output(13,GPIO.LOW)
    
        print("\tProgram Started")
        
        #--------------------------------------------------------------
        #REMOVE THIS LINE IN FUTURE THIS IS JUST FOR PROGRAMMING AT HOME
        t_1=input("")
        
        print("\tPaw Placed time: %s seconds" % t_1)
        return t_1
        #--------------------------------------------------------------
        
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
                print("Paw Placed time: %s seconds" % t_1)
                GPIO.output(13,GPIO.LOW)
                break
        GPIO.cleanup()
        return t_1

    #Method for printing withdrawal times stored within list 
    def printTime(self):
        trialNum=1

        #Print the Cat's information and date
        print("\nCat:",self.name,"\tTest Date:",self.date)
        print("--------------------------------------")
        #Print the times for each trial
        for i in self.time:
            print("Trial",trialNum,":","%s seconds" % i)
            trialNum+=1
        #Print the cat's average time, standard deviation, variance
        print("\nAnalysis")

        if self.numOfTrials>1:
            #Update the analysis
            self.avg=self.getAvg()
            self.standardDev=self.getStdev()
            self.trialVariance=self.getVar()
        else:
            #If there is only 1 trial, dont update analysis
            self.avg=0
            self.standardDev=0
            self.trialVariance=0
            print("***Not enough trial data to perform analysis***")

        print("Average:", self.avg)
        print("Variance:", self.trialVariance)
        print("Standard Deviation:", self.standardDev)
        return 

    #def printAllCats(testCats):
     #   for i in testCats:

      #      curr_cat=cat(testCats[i])
       #     curr_cat.printTime()
        #return
    
    ###############################################################################
    #     This method is what starts the entire system to even run a test         #
    #     Think of it like main, it is a driver function                          #
    ###############################################################################
    def start_testing():
        #Prompt user to start program
        print("\n*******Welcome to the Plantar Thermal Laser test.*******")
        beginProgram=input("Would you like to run a trial? (Yes/No): ")
        print(beginProgram)
        
        testCats=[]
        #Determine valid response, if so create a cat as an object
        while beginProgram == "y":
            #Create a cat with their information
            name=input("Enter subject's name: ")
            curr_cat=cat(name)
            #Begin Testing a cat
            trialNum=1 #Keeps track of trial of current cat
            runTrial=1 #Flag to determine which cat is being tested on
            #Run as many trials as wanted for this cat
            while (runTrial==1):
                #Perform a Trial, get withdrawal time
                print("Trial ",trialNum,":")
                curr_cat.trial()

                #Prompt to perform another trial
                nextTrial=input("Run another trial for this cat?(Yes/No) ")
                if nextTrial == "y": #Keep testing current cat
                    trialNum+=1
                    runTrial=1 
                if nextTrial == "n": #Stop testing current cat
                    trialNum=0
                    runTrial=0
        #Print cat's information after testing 
            curr_cat.printTime()
        
            #Ask user to test another cat
            testAnotherCat=input("\nTest a new Cat?(Yes/No)")
            if testAnotherCat == "y": 
                testCats.append(curr_cat)
                beginProgram="y" #Jump back to start of loop and create new cat
            if testAnotherCat == "n": 
                testCats.append(curr_cat)
                beginProgram="n" #Exit loop
                        
        #Exit program when testing is stopped
        if beginProgram == "n": 
            #cat.printAllCats(testCats)
            print("*****Ending Testing*****")

        return
        #########################################################

################Driver Function#########################
def main():
    #call the driver to begin the testing
    cat.start_testing()

    #exit program
    return 0

##Main definition##
if __name__ == "__main__":
    main()    
