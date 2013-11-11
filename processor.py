import random

execfile('NationClass.py') #load the class so we can use it
with open('nationfile.dat', 'rb') as file: #load files
    NationArray = cPickle.load(file)


# Rounds and turns loops
def processturn(NationArray):
    if (Round == 1) and (Turn > 1):
        print(NationArray[Turn-1].LeaderName+random.choice(StartedSynonyms)+NationArray[Turn-1].NationName+".")

    # Calculate and display resources for nation
    NationArray[Turn-1].resourcecompute()
    print("R"+str(Round)+"T"+str(Turn)+": "+str(NationArray[Turn-1].NationName)+" may spend "+str(NationArray[Turn-1].Resources)+" resources.")


#os.system("pause") # Prevents program from closing automatically
