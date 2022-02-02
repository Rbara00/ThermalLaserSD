#Cat Class for Thermal Plantar Test

#Includes
# Import date class from datetime module
from datetime import date

#import RPi.GPIO as GPIO
from time import time

#Cat Class
class cat:
    #Constructor for cat
    def __init__(self,name):
        self.name=name     #cat is named from user input
        self.time=[]     #create a list of all the cat's withdrawal times
        self.date = date.today() #stores the corresponding test date        
        
    
    #Method for printing withdrawal times stored within list 
    def printTime(self):
        trialNum=1
        print("\nCat:",self.name,"\tTest Date:",self.date)
        print("--------------------------------------")
        for i in self.time:
            print("Trial",trialNum,":",i)
            trialNum+=1
    
    #Method for inserting a new withdrawl time into the list
    def insertTime(self,new_time):
        self.time.append(new_time)
    
    #Method for performing a trial and saving the data
    def trial(self):
        #Run a trial and insert withdrawal time into a list for exporting
        t_1=cat.timer()

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
        
        #REMOVE THIS LINE IN FUTURE THIS IS JUST FOR PROGRAMMING AT HOME
        t_1=input("")
        
        print("\tPaw Placed time: %s seconds" % t_1)
        return t_1
    
        
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



#Main function
def main():
    #Prompt user to start program
    print("\n*******Welcome to the Plantar Thermal Laser test.*******")
    beginProgram=input("Would you like to run a trial? (Yes/No): ")
    print(beginProgram)
    
    #Determine valid response, if so create a cat as an object
    while beginProgram == "y":
        #Create a cat with their information
        name=input("Enter subject's name: ")
        cat1=cat(name)
        #Begin Testing a cat
        trialNum=1 #Keeps track of trial of current cat
        runTrial=1 #Flag to determine which cat is being tested on
        #Run as many trials as wanted for this cat
        while (runTrial==1):
            #Perform a Trial, get withdrawal time
            print("Trial ",trialNum,":")
            cat1.trial()

            #Prompt to perform another trial
            nextTrial=input("Run another trial for this cat?(Yes/No) ")
            if nextTrial == "y": #Keep testing current cat
                trialNum+=1
                runTrial=1 
            if nextTrial == "n": #Stop testing current cat
                trialNum=0
                runTrial=0
        #Ask user to test another cat
        cat1.printTime()
        testAnotherCat=input("\nTest a new Cat?(Yes/No)")
        if testAnotherCat == "y": beginProgram="y" #Jump back to start of loop and create new cat
        if testAnotherCat == "n": beginProgram="n" #Exit loop
                    
    #Exit program when testing is stopped
    if beginProgram == "n": print("*****Ending Testing*****")
    return 0
if __name__ == "__main__":
    main()    
