###########################################
## 
## Animal Class for thermal laser
## SD Team 10: Robert Bara, Zari Grandy, Ezra Galapo, Tyiana Smith
## 
## Date:    2/3/2022
## Version: 2.1
##
## Description:
##  This python program allows for the thermal laser plantar test to run by prompting the user if
##  they would like to perform a test. The class creates an animal, performs a laser test, stores the withdrawal
##  times, as well as performs analysis such as standard dev, average, and variance calculations
##
## Usage:
##  Running: python3 animal_class.py (run it here, eventually build a make file-Rob)
##
########################################


############ Includes ##################
from datetime import date
from os import stat
from re import S
from sre_constants import MAXGROUPS             # Import date class from datetime module
from statistics import stdev    # Import statistics to utilize mean, standard deviation, and variance calculations
from statistics import variance
from statistics import mean
from enum import Enum
#import RPi.GPIO as GPIO        # Import General-Purpose In/Out for RPI4 to control laser and photodiode
from time import time           # Import time to calculate withdrawal time
########################################

############ animal Class #################
class animal:
    ##############################
    #Constructor for animal
    ##############################
    def __init__(self,name,group):
        self.name=name            #animal is named from user input
        self.time=[]              #create a list of all the animal's withdrawal times
        self.date = date.today()  #stores the corresponding test date
        self.group=group
        self.avg=0                #Initialize the average to be 0
        self.standardDev=0        #Initialize the standard deviation to be 0
        self.trialVariance=0      #Initialize the variance to be 0
        self.numOfTrials=0
        return
    
    #############################
    #Class Functions:
    #############################
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
        self.standardDev=stdev(sample)
        return self.standardDev
    
    #Getter for the Variance of the animal's response times
    def getVar(self):
        sample=self.time
        self.trialVariance=variance(sample)
        return self.trialVariance

    #Method for inserting a new withdrawl time into the list
    def insertTime(self,new_time):
        self.time.append(new_time)
        self.numOfTrials+=1
        return


    #Method for performing a trial and saving the data
    def trial(self):
        #Run a trial and insert withdrawal time into a list for exporting
        t_1=animal.timer()
        t_1=float(t_1) #Ensure the time is a valid time with decimals
        #Was the trial valid enough for the user?
        valid_trial=input("Keep trial? (Yes/No): ")
        if valid_trial != "y":
            #perform a retrial
            self.trial()
        else:        
            #When a valid trial is ran, 
            self.insertTime(t_1) #place withdrawal time into list
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

        #Print the animal's information and date
        print("Animal's Name:",self.name,"\tGroup:",self.group,"\tTest Date:",self.date)
        print("----------------------------------------------------------------------------")
        #Print the times for each trial
        for i in self.time:
            print("Trial",trialNum,":","%s seconds" % i)
            trialNum+=1
        #Print the animal's average time, standard deviation, variance
        print("\nAnalysis")

        if self.numOfTrials<=1:
            #If there is only 1 trial, dont update analysis
            self.avg=0
            self.standardDev=0
            self.trialVariance=0
            print("***Not enough trial data to perform analysis***")
        else:
            #Otherwise print the animal's analysis
            print("Average:", self.avg)
            print("Variance:", self.trialVariance)
            print("Standard Deviation:", self.standardDev,"\n")
        return 
    

#####################################################################
# Create a class to run a test and store all the animals information 
#####################################################################
class testAnimals:
    def __init__(self) -> None:
        pass
    #Print the results of the Passed in Group number
    def printGroup(self, saveAnimals, group):
        print("\n--------------------------------------")
        print("Group",group,"Results:")
        print("--------------------------------------\n")
        #If the group's number matches the group argument, print Animal's information
        for i in saveAnimals:
            if(i.group==group): 
                i.printTime() 
        return
    #Prints the results of all groups in orderS
    def printAllGroups(self, saveAnimals):
        numOfGroups=self.maxGroup(saveAnimals)
        for i in range(numOfGroups+1):
            self.printGroup(saveAnimals,i)
        return
    #Function determines how many groups are there    
    def maxGroup(self,saveAnimals):
        numOfGroups=0
        for i in saveAnimals:
            if(i.group>numOfGroups):
                numOfGroups=i.group
        return numOfGroups

    #This function prints today's Test Animal's results
    def printTodaysResults(self, saveAnimals):
        print("\n--------------------------------------")
        print("Test Results:")
        print("--------------------------------------\n")
        #Print every Animal's information
        for i in saveAnimals:
            i.printTime() 
        
        return

    def exportGroup(self,saveAnimals,group):
        
        return
    
    #Prompts the user for name and number to construct animal
    def promptAnimalInfo():
        #Create a animal with their information
        #Prompt for name of Animal
        name=input("Enter subject's Name: ")
        #Prompt for a valid integer group number
        while True:
            try:
                group = int(input("Enter subject's Group number: "))
                break
            except ValueError:
                print("Please enter Group number as an integer")  
            continue
        #Return Current Animal's name and number
        return name,group

    ###############################################################################
    #     This method is what starts the entire system to even run a test         #
    #     Think of it like main, it is a driver function                          #
    ###############################################################################    
    def startExperiment(self):
        saveAnimals=[]  #Create a list to store all animal's information
       #Prompt user to start program
        print("\n*******Welcome to the Plantar Thermal Laser test.*******")
        beginProgram=input("Would you like to run a trial? (Yes/No): ")
        print(beginProgram)

        #Determine valid response, if so create a animal as an object
        while beginProgram == "y":
            #Create an animal data structure
            name,group=testAnimals.promptAnimalInfo()
            curr_animal=animal(name,group)
            #Begin Testing a animal
            trialNum=1 #Keeps track of trial of current animal
            runTrial=1 #Flag to determine which animal is being tested on
            #Run as many trials as wanted for this animal
            while (runTrial==1):
                #Perform a Trial, get withdrawal time
                print("Trial ",trialNum,":")
                curr_animal.trial()

                #Prompt to perform another trial
                nextTrial=input("Run another trial for this animal?(Yes/No) ")
                if nextTrial == "y": #Keep testing current animal
                    trialNum+=1
                    runTrial=1 
                if nextTrial == "n": #Stop testing current animal
                    trialNum=0
                    runTrial=0
        #Print animal's information after testing 
            curr_animal.printTime()
        
            #Ask user to test another animal
            testAnotheranimal=input("\nTest a new animal?(Yes/No)")
            if testAnotheranimal == "y": 
                saveAnimals.append(curr_animal)
                beginProgram="y" #Jump back to start of loop and create new animal
            if testAnotheranimal == "n": 
                saveAnimals.append(curr_animal)
                self.printTodaysResults(saveAnimals)
                #Testing printing per group
                #self.printGroup(saveAnimals,0)
                #self.printGroup(saveAnimals,1)
                #self.printAllGroups(saveAnimals)
                beginProgram="n" #Exit loop
                        
        #Exit program when testing is stopped
        if beginProgram == "n":     
            print("*****Ending Testing*****")
        return saveAnimals

#########################################
#           Driver Function             #
#########################################
def main():
    #create a test and start the experiment
    test=testAnimals()
    saveAnimals=test.startExperiment() 
    #exit program
    return 0

##Main definition##
if __name__ == "__main__":
    main()    
