#Must have NationNames.txt and LeaderNames.txt in the same directory as this program to run

# Imports and initial stuff
import os
import random
import time
random.seed()

# Nation class
class Nation:
    Production = 0
    Technology = 0
    Trade = 0
    Resources = 0
    Overspent = 0
    NationName = str
    LeaderName = str

# Initial settings
Round = int
Turn = int
SleepTime = float
DebugVar = input("Debug mode? (1 = yes, 0 = no): ")
NationQuantity = input("How many will be playing?: ")
RoundLimit = input("The maximum number of rounds?: ")

# Sets wait time after turn based on debug mode on/off
if DebugVar == 1:
    SleepTime = 0.1
else:
    SleepTime = 1

# Load nationnames from NationNames.txt
text_file = open("NationNames.txt", "r")
NationNameDatabase = text_file.read().split("\n")
text_file.close()
if NationNameDatabase[len(NationNameDatabase)-1] == "":
    NationNameDatabase.pop(len(NationNameDatabase)-1)
NationNameQuantity = len(NationNameDatabase)

# Load leadernames from LeaderNames.txt
text_file = open("LeaderNames.txt", "r")
LeaderNameDatabase = text_file.read().split("\n")
text_file.close()
if LeaderNameDatabase[len(LeaderNameDatabase)-1] == "":
    LeaderNameDatabase.pop(len(LeaderNameDatabase)-1)
LeaderNameQuantity = len(LeaderNameDatabase)

if DebugVar == 1: # Show loaded nation and leader names if debug mode is on.
    print NationNameDatabase
    print LeaderNameDatabase

# Create array of nations based on keyboard input
NationArray = []
for Turn in range(0,NationQuantity):
    NationArray.append(Nation())

# Get nation and leader name from keyboard input
NationArray[0].NationName = raw_input('Type the name of your nation: ')
NationArray[0].LeaderName = raw_input("What is your name, mighty leader of "+NationArray[0].NationName+"?: ")

# Set random AI nation and leader names
for Turn in range(1,NationQuantity):
    NationArray[Turn].NationName = NationNameDatabase[random.randint(0,NationNameQuantity-1)]
    NationArray[Turn].LeaderName = LeaderNameDatabase[random.randint(0,LeaderNameQuantity-1)]

# Display leader and nation name
print("You established "+NationArray[0].NationName+".")

# Rounds and turns loops
for Round in range(1,RoundLimit+1):
    for Turn in range(1,NationQuantity+1):
        if (Round == 1) and (Turn > 1):
            print(NationArray[Turn-1].LeaderName+" established "+NationArray[Turn-1].NationName+".")

        # Calculate and display resources for nation
        NationArray[Turn-1].Resources = 5 + NationArray[Turn-1].Production + ((NationArray[Turn-1].Technology + NationArray[Turn-1].Trade) / 10) + NationArray[Turn-1].Resources - ((NationArray[Turn-1].Resources**2) / 1000) - (2 * NationArray[Turn-1].Overspent)
        print("R"+str(Round)+"T"+str(Turn)+": "+str(NationArray[Turn-1].NationName)+" may spend "+str(NationArray[Turn-1].Resources)+" resources.")

        # End of turn, pause for 1 second
        time.sleep(SleepTime)

os.system("pause") # Doesn't close out until clicked
