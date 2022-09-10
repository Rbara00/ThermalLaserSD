#!/usr/bin/python3
###########################################
## 
## Test Class for thermal laser
## SD Team 10: Robert Bara, Zari Grandy, Ezra Galapo, Tyiana Smith
## 
## Author: Robert Bara
## Date:    9/6/2022
## Version: 1.3
##
## Description:
##  This python file performs a thermal laser test for a medium sized animal such as a cat,
##  the program prompts the user through the terminal for commands and activates the laser 
##  in the system to gather withdrawal times for each animal. The data is then stored to the
##  animal and the average, standard deviation, and variance are calculated for each animal.
##  The results are then exported to excel where the group average and standard deviation are 
##  plotted against each group.
##
## Usage:
##  Python3 laser_test.py       or      ./laser_test.py
##
########################################

from test_class import*

#########################################
#           Driver Function             #
#########################################
def main():
    #create a test and start the experiment
    test=testAnimals()
    workbookName=test.startExperiment()
    test.graphResults(workbookName)
    print(workbookName,"contains results and group analysis")
    #exit program
    return 0

##Main definition##
if __name__ == "__main__":
    main()    