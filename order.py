import os
import cPickle
import time
import random

execfile('NationClass.py') #load the class so we can use it
execfile('processor.py') #load the processor file
execfile('settings.py') #get round limit and stuff

execfile('Initializer.py') #init file

with open('nationfile.dat', 'rb') as file: #load files
    NationArray = cPickle.load(file)

for Round in range(1,RoundLimit+1):
    for Turn in range(1,NationQuantity+1):
        processturn(NationArray)
        # End of turn, pause for the set sleeptime
        time.sleep(SleepTime)