# Imports
import os

# Initial settings
NationQuantity = 3
RoundLimit = 5
Round = int
Turn = int

# Get nation and leader name from keyboard input
NationName = raw_input('Type the name of your nation: ')
LeaderName = raw_input("What is your name, mighty leader of "+NationName+"?: ")

# Display leader and nation name
print(" NationName = "+NationName+" LeaderName = "+LeaderName)

# Rounds and turns loops
for Round in range(1,RoundLimit+1):
    for Turn in range(1,NationQuantity+1):
        print("Round "+str(Round)+", Turn "+str(Turn))
        # (What to do in turn)

os.system("pause") # Doesn't close out until clicked
