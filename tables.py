###########################################
## 
## Tables Class for thermal laser
## SD Team 10: Robert Bara, Zari Grandy, Ezra Galapo, Tyiana Smith
## 
## Author: Robert Bara
## Date:    4/5/2022
## Version: 1.1
##
## Description:
##  This python file contains a class to construct a table which will hold store
##  an animal into a list avaliable at the given index which is based upon a group,
##  graphically the table can be drawn as:
##      [column index][list of cats]
##       group0     : cat1,cat2,cat3
##       group1     : cat1,cat2,cat3
##        ...
##       groupN     : N cats
## Usage:
##  This program is invoked by test_class and utilizes inputs from the animal_class
##
########################################

############ Includes ##################
import animal_class as animal
#############################################################
# Table Class
#############################################################
class resultTb:
    #constructor for a table of lists which hold a test animal as an element
    def __init__(self, size=100):
        self.size=size                              #dynamically allocated memory for the size of the table
        self.arr=[[] for i in range (self.size)]    #Creating the table as an array of lists
        self.filled=0                               #Keeps track of how man animals are "filled" in the table
        return
    #Takes an animal and inserts it into the results table based upon their group number
    def insert(self,curr_animal):
        group=curr_animal.getGroup()
        self.arr[group].append(curr_animal)
        self.filled+=1
        return
    #Prints all animals results within the passed in group number, in order of when they were stored into group
    def printIndex(self,group):
        #in the table at row with index corresponding to the group number, iterate across the list of animals
        for i in range(len(self.arr[group])):
            print(self.arr[group][i].printTime())   #Print the current counter's animal results
        return
    #print all results stored within the table in order of groups
    def printAll(self):
        for i in range(self.size):
            self.printIndex(i)
        return