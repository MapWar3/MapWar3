DebugVar = input("Debug mode? (1 = yes, 0 = no): ")

BR = 5.0 #Base resources pr. turn
TEM = 0.1 #Tech multiplier
TRM = 0.1 #Trade multiplier
RDE = 2.0 #Resource decay exponential factor
RDC = 0.001 #Resource decay constant factor
OPM = 2.0 #Overspending penalty multiplier

StartedSynonyms = [" established ", " founded ", " created "]

if DebugVar:
    NationQuantity, RoundLimit = 5, 5
else:
    NationQuantity = input("How many nations will be playing?: ")
    RoundLimit = input("The maximum number of rounds?: ")

if DebugVar: # Sets wait time after turn based on debug mode on/off
    SleepTime = 0
else:
    SleepTime = 1
