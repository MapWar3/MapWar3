import os
import cPickle
execfile('NationClass.py') #load the class so we can use it
with open('nationfile.dat', 'rb') as file: #load files
    NationArray = cPickle.load(file)



# Rounds and turns loops
for Round in range(1,RoundLimit+1):
    for Turn in range(1,NationQuantity+1):
        if (Round == 1) and (Turn > 1):
            print(NationArray[Turn-1].LeaderName+random.choice(StartedSynonyms)+NationArray[Turn-1].NationName+".")

        # Calculate and display resources for nation
        NationArray[Turn-1].resourcecompute()
        print("R"+str(Round)+"T"+str(Turn)+": "+str(NationArray[Turn-1].NationName)+" may spend "+str(NationArray[Turn-1].Resources)+" resources.")

        # End of turn, pause for the set sleeptime
        time.sleep(SleepTime)

os.system("pause") # Prevents program from closing automatically
