# Imports
import os
import time

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
NationQuantity = input("How many will be playing?: ")
RoundLimit = input("The maximum number of rounds?: ")

# Create array of nations based on keyboard input
NationArray = []
for Turn in range(0,NationQuantity):
    NationArray.append(Nation())

# Get nation and leader name from keyboard input
NationArray[0].NationName = raw_input('Type the name of your nation: ')
NationArray[0].LeaderName = raw_input("What is your name, mighty leader of "+NationArray[0].NationName+"?: ")

# Display leader and nation name
print(" NationName = "+NationArray[0].NationName+" LeaderName = "+NationArray[0].LeaderName)

# Rounds and turns loops
for Round in range(1,RoundLimit+1):
    for Turn in range(1,NationQuantity+1):

        # Calculate and display resources for nation
        NationArray[Turn-1].Resources = 5 + NationArray[Turn-1].Production + ((NationArray[Turn-1].Technology + NationArray[Turn-1].Trade) / 10) + NationArray[Turn-1].Resources - ((NationArray[Turn-1].Resources**2) / 1000) - (2 * NationArray[Turn-1].Overspent)
        print("R"+str(Round)+"T"+str(Turn)+": "+str(NationArray[Turn-1].NationName)+" may spend "+str(NationArray[Turn-1].Resources)+" resources.")

        # End of turn, pause for 1 second
        time.sleep(1)

os.system("pause") # Doesn't close out until clicked
