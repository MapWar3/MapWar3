# Imports and initial stuff
import os
import random
import time

# Nation class
class Nation:  #to initialize, type: x = Nation()
    TTM = 0.1 #tech trade multiplier
    DE = 2.0 #decay exponential factor
    DC = 0.001 #decay constant factor
    OP = 2.0 #overpsending penalty
    def __init__(self, production=0, technology=0, trade=0, resources=0, overspent=0, name='', leader=''):
        self.Production = production #now you can say something like Bob.production
        self.Technology = technology
        self.Trade = trade
        self.Resources = resources
        self.Overspent = overspent
        self.NationName = name
        self.LeaderName = leader
    def resourcecompute(self):
        self.Resources += int(5+self.Production + (self.Technology+self.Trade)*Nation.TTM - self.Resources**Nation.DE*Nation.DC-self.Overspent*Nation.OP)
    def resourceprint(self):
        pass #will work on this later.
        
# Initial settings
Round = int
Turn = int
SleepTime = float
DebugVar = input("Debug mode? (1 = yes, otherwise no): ")
NationQuantity = input("How many will be playing?: ")
RoundLimit = input("The maximum number of rounds?: ")

# Sets wait time after turn based on debug mode on/off
if DebugVar: #1 is boolean true, so if DebugVar==1: is the same as if DebugVar:
    SleepTime = 0.1
else:
    SleepTime = 1

# Load nationnames from NationNames.txt
with open("NationNames.txt", "r") as namefile: #this closes the file after indented block
    NationNameDatabase = [name.strip() for name in namefile.readlines()]
NationNameQuantity = len(NationNameDatabase)

# Load leadernames from LeaderNames.txt
with open("LeaderNames.txt", "r")as namefile:
    LeaderNameDatabase = [name.strip() for name in namefile.readlines()] #list of every line in file with \n removed
LeaderNameQuantity = len(LeaderNameDatabase)

if DebugVar: # Show loaded nation and leader names if debug mode is on.
    print NationNameDatabase
    print LeaderNameDatabase

# Create array of nations based on keyboard input
NationArray = []
for Turn in range(0,NationQuantity):
    NationArray.append(Nation())

# Get nation and leader name from keyboard input
NationArray[0].NationName = raw_input('What is the name of your potential global future utopia?: ')
NationArray[0].LeaderName = raw_input("What is your name, mighty leader of "+NationArray[0].NationName+"?: ")

# Set random AI nation and leader names
for Turn in range(1,NationQuantity): #using random.choice(list)
    NationArray[Turn].NationName = random.choice(NationNameDatabase)
    NationArray[Turn].LeaderName = random.choice(LeaderNameDatabase)

# Display leader and nation name
print("You established "+NationArray[0].NationName+".")

# Rounds and turns loops
for Round in range(1,RoundLimit+1):
    for Turn in range(1,NationQuantity+1):
        if (Round == 1) and (Turn > 1):
            print(NationArray[Turn-1].LeaderName+" established "+NationArray[Turn-1].NationName+".")

        # Calculate and display resources for nation
        NationArray[Turn-1].resourcecompute()
        print("R"+str(Round)+"T"+str(Turn)+": "+str(NationArray[Turn-1].NationName)+" may spend "+str(NationArray[Turn-1].Resources)+" resources.")

        # End of turn, pause for 1 second
        time.sleep(SleepTime)

os.system("pause") # Doesn't close out until clicked