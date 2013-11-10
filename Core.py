# Imports and initial stuff
import os
import random
import time

# Initial settings
Round = int
Turn = int
SleepTime = float
DebugVar = input("Debug mode? (1 = yes, 0 = no): ")
if DebugVar: #aint nobody got time for typing in numbers
    NationQuantity, RoundLimit = 5,5
else:
    NationQuantity = input("How many will be playing?: ")
    RoundLimit = input("The maximum number of rounds?: ")

# Load settings from Settings.txt
execfile('settings.py')

if DebugVar:
    print("BR = "+str(BR)+", TEM = "+str(TEM)+", TRM = "+str(TRM)+", RDE = "+str(RDE)+", RDC = "+str(RDC)+", OPM = "+str(OPM))

# Nation class
class Nation:  # To initialize, type: x = Nation()
    def __init__(self, production=0, technology=0, trade=0, resources=0, overspent=0, name='', leader=''):
        self.Production = production # Now you can say something like Bob.production
        self.Technology = technology
        self.Trade = trade
        self.Resources = resources
        self.Overspent = overspent
        self.NationName = name
        self.LeaderName = leader
    def resourcecompute(self):
        self.Resources += int(round(BR + self.Production + self.Technology*TEM + self.Trade*TRM - self.Resources**RDE*RDC - self.Overspent*OPM, 0))
    def resourceprint(self):
        pass # Osmotischen will work on this later.

if DebugVar: # Sets wait time after turn based on debug mode on/off
    SleepTime = 0
else:
    SleepTime = 1

# Load nationnames from NationNames.txt
with open("NationNames.txt", "r") as namefile: # This closes the file after indented block
    NationNameDatabase = [name.strip() for name in namefile.readlines()] # List of every line in file with \n removed
NationNameQuantity = len(NationNameDatabase)

# Load leadernames from LeaderNames.txt
with open("LeaderNames.txt", "r")as namefile:
    LeaderNameDatabase = [name.strip() for name in namefile.readlines()]
LeaderNameQuantity = len(LeaderNameDatabase)

if DebugVar: # Show loaded nation and leader names if debug mode is on.
    print NationNameDatabase
    print LeaderNameDatabase

# Create list of nations based on entered number of nations
NationArray = []
for i in range(0,NationQuantity):
    NationArray.append(Nation())

# Get nation and leader name from keyboard input
if DebugVar:
    NationArray[0].NationName = 'testnation'
    NationArray[0].LeaderName = 'testleader'
else:
    NationArray[0].NationName = raw_input('What is the name of your potential global future utopia?: ')
    NationArray[0].LeaderName = raw_input("What is your name, mighty leader of "+NationArray[0].NationName+"?: ")

# Set random AI nation and leader names
for i in range(1,NationQuantity): #using random.choice(list)
    NationArray[i].NationName = random.choice(NationNameDatabase)
    NationArray[i].LeaderName = random.choice(LeaderNameDatabase)

    # Checks for nation name duplicates and tries to avoid them
    if NationQuantity <= NationNameQuantity:
        for k in range(0,NationQuantity):
            if (i != k) and (NationArray[i].NationName == NationArray[k].NationName):
                NationArray[i].NationName = random.choice(NationNameDatabase)
                if DebugVar:
                    print("Nation name of "+NationArray[i].NationName+" was changed.")
    
    # Checks for leadername duplicates and tries to avoid them
    if NationQuantity < LeaderNameQuantity:
        for k in range(0,NationQuantity):
            if (i != k) and (NationArray[i].LeaderName == NationArray[k].LeaderName):
                NationArray[i].LeaderName = random.choice(LeaderNameDatabase)
                if DebugVar:
                    print("Leader name of "+NationArray[i].LeaderName+" was changed.")

# Suggest adding more names to files if there are too few names for their game
if NationQuantity > NationNameQuantity:
    if NationQuantity > LeaderNameQuantity:
        print("You play with more nations than there are names for in the LeaderNames.txt and NationNames.txt files. Consider adding more names to them. :)")
    else:
        print("You play with more nations than there are names for in the NationNames.txt file. Consider adding more names to it. :)")
elif NationQuantity > LeaderNameQuantity:
    print("You play with more nations than there are names for in the LeaderNames.txt file. Consider adding more names to it. :)")

# Word Bank
StartedSynonyms = [" established ", " started ", " founded ", " created ", " formed ", " chose ", " got ", " initiated ", " commenced ", " organized ", " developed ", " set up "]
# Display leader and nation name
print(NationArray[0].LeaderName+StartedSynonyms[random.randint(0,len(StartedSynonyms)-1)]+NationArray[0].NationName+".")

# Rounds and turns loops
for Round in range(1,RoundLimit+1):
    for Turn in range(1,NationQuantity+1):
        if (Round == 1) and (Turn > 1):
            print(NationArray[Turn-1].LeaderName+StartedSynonyms[random.randint(0,len(StartedSynonyms)-1)] +NationArray[Turn-1].NationName+".")

        # Calculate and display resources for nation
        NationArray[Turn-1].resourcecompute()
        print("R"+str(Round)+"T"+str(Turn)+": "+str(NationArray[Turn-1].NationName)+" may spend "+str(NationArray[Turn-1].Resources)+" resources.")

        # End of turn, pause for the set sleeptime
        time.sleep(SleepTime)

os.system("pause") # Prevents program from closing automatically
