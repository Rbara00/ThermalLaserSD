#!/usr/bin/python3
###########################################
## 
## Test Class for thermal laser
## SD Team 10: Robert Bara, Zari Grandy, Ezra Galapo, Tyiana Smith
## 
## Author: Robert Bara
## Date:    9/6/2022
## Version: 2.5
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
##  Python3 laser_test_GUI.py       or      ./laser_test_GUI.py
##
########################################

#Imports
from cProfile import label
from cmath import exp
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from tkinter.ttk import Notebook
from tkinter import ttk
from tokenize import group
from unicodedata import name
import animal_classGUI as animal
import export_classGUI as export
from export_classGUI import*
import tablesGUI as resultTb
from datetime import datetime
import RPi.GPIO as GPIO        # Import General-Purpose In/Out for RPI4 to control laser and photodiode

#Glocal variable definitions to pass data between button callback functions
global currName
global numOfGroups
global currGroup
global mytext
mytext=("Name: " + "  Group: " + "  Trial: " + "  Withdrawal Time: "+"  Start Time: " + "  End Time: ")
trialNum=0
numOfGroups=0

#########################################
#     Functions for running a test      #
#########################################
#Prompts the user for name and number to construct animal
def promptAnimalInfo():
    #initailize changing global values
    global currName
    global currGroup
    global curr_animal
    global numOfGroups

    #Prompt for a valid integer group number
    currName=simpledialog.askstring("Thermal Laser Plantar Test", " Please Enter the Subject's Name: ")
    while True:
        try:
            currGroup = int(simpledialog.askinteger("Thermal Laser Plantar Test","Enter subject's Group number, minimum of 1: "))
            if currGroup>=1:
                break
        except ValueError:
            simpledialog.askinteger("Thermal Laser Plantar Test","Please Enter a group number, minimum of 1")
        continue
    #Update number of groups based on max group number
    if currGroup>numOfGroups:
        numOfGroups=currGroup
    #create animal based on name and group
    curr_animal=animal.animal(currName,currGroup)

#This method is what starts the entire system to run a test
def startExperiment():
    global curr_animal
    #Begin Testing a animal
    curr_animal.startTime=datetime.now().strftime("%H:%M:%S")  #get the timestamp when testing is beginning
    
    #Starts and Stops the Laser based on Photodiode state
    curr_animal.trial_gui(placed_label)                             
    
    #Print animal's information after testing 
    curr_animal.endTestTime=datetime.now().strftime("%H:%M:%S")  #get the timestamp when testing is over for current cat
    global mytext
    mytext=("Name: " + currName + "  Group: " + str(curr_animal.getGroup()) + "  Trial: " + str(curr_animal.getNumOfTrials()) + "  Withdrawal Time: " 
            + str(curr_animal.getTimeAt(curr_animal.getNumOfTrials()-1)) +"\nStart Time: " + str(curr_animal.startTime) + "  End Time: " + 
            str(curr_animal.endTestTime))

#########################################
#    Callback Functions for Buttons     #
#########################################
#Begins the Test
def Button_1():    
    global l4
    global mytext
    #get info from user to name animal and assign group
    promptAnimalInfo()
    #Update Labels
    mytext=mytext=("Name: " + currName + "  Group: " + str(curr_animal.getGroup()) + "  Trial: " + "  Withdrawal Time: " 
                    +"\nStart Time: " + "  End Time: ")
    l4.configure(text=mytext)
    #Switches to Testing Menu
    menus.add(frame2,text='Laser Test Menu')
    menus.hide(0)

#Exits the Program
def Button_2():
    quit()

#Begin the laser for testing
def Button_3():
    startExperiment()
    #Update label with last known results
    global l4
    l4.configure(text=mytext)

#Prompts to test a new animal or not
def Button_4():
    results.insert(curr_animal) #Insert the last animal into results
    promptAnimalInfo()          #Prompt for new animal
    #Update Labels
    mytext=mytext=("Name: " + currName + "  Group: " + str(curr_animal.getGroup()) + "  Trial: " + "  Withdrawal Time: " 
                    +"  Start Time: " + "  End Time: ")
    l4.configure(text=mytext)

#Saves the spreadsheet and exits the program
def Button_5():
    results.insert(curr_animal) #Insert the last animal into results
    #Create an exporting object
    lasertest=export()
    #Prompt user for filename and exports data into Excel Sheet based upon Group Number
    wb1=lasertest.exportResults(results,numOfGroups)
    #Generates Bar Graphs from Data
    wb1=lasertest.graphResults(wb1)
    #Exits the program
    quit()

#########################################
#           Driver Function             #
#########################################
# Creating menus 
# Creating menus 
root = Tk()
root.title("Thermal Laser Plantar Test")
root.geometry("800x500")
root.resizable(True,True)
#root.iconbitmap(os.path.join(os.path.dirname(os.path.abspath(__file__)),('lemay.ico')))
results=resultTb.resultTb()

#Create a notebook to store menus as tabs
menus=Notebook(root)
menus.pack()

#Format Menus
style = ttk.Style()
style.theme_create( "MyStyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {"configure": {"padding": [5, 5] },}})

style.theme_use("MyStyle")

#Setup GPIO Board for RPI, insuring that the laser is off as soon as the python script begins 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.OUT)
GPIO.output(13,GPIO.LOW)

# setup frame 1 as start menu and frame 2 as test menu
frame1=Frame(menus,width=800,height=500,bg="#7F7FFF")
frame2=Frame(menus,width=800,height=500,bg='red4')
frame1.pack()
frame1.pack_propagate(0)
frame2.pack()
frame2.pack_propagate(0)

# Add frames as tabs to GUI and hide the Test menu so only the main menu appears
menus.add(frame1,text='Main Menu')
menus.add(frame2,text='Laser Test Menu')
menus.hide(1)

# Labels and Buttons for main menu
l1=  Label(frame1, text="Welcome to the Thermal Laser Test", bg="#7F7FFF",fg="yellow", font=("Times",25,"bold","underline")).pack(pady=(100,0))
l2=  Label(frame1, text="Would you like to Run a Test?", bg="#7F7FFF",fg="yellow", font=("Times",20,"bold")).pack()
B1 = Button(frame1, text = "Start Test",height=3,width=25,command = Button_1).pack(side="left", anchor="e",expand=True)  
B2 = Button(frame1, text = "Exit",height=3,width=25,command = Button_2).pack(side="right", anchor="w",expand=True)  

#Labels and buttons for Test menu
l3=  Label(frame2, text="Place Animal onto System, then click 'Start' to begin a Test", bg="red4",fg="yellow", font=("Times",20,"bold","underline"))
l3.place(relx=0.05,rely=.1)
l4=  Label(frame2, text=mytext, font=("Times",15,"bold"),bg="red4",fg="yellow")
l4.pack(anchor="center", expand=True)

#PhotoDiode Label
placed_label=Label(frame2,text="Photodiode Status:",font=("Times",15,"bold"),bg="red4",fg="white")
placed_label.place(relx=.3,rely=.3)

B3 = Button(frame2, text = "Start Laser Test",height=2,width=25,command=Button_3).place(relx=0.1,rely=0.7)  
B4 = Button(frame2, text = "Select New Animal",height=2,width=25,command = Button_4).place(relx=0.35,rely=0.7)  
B5=  Button(frame2, text = "Exit",height=2,width=25,command = Button_5).place(relx=0.6,rely=0.7) 

#define function if the user hits the "x" at the top of the window
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit without saving?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

#Run the GUI indefinetly until the user stops the test
frame1.mainloop()
