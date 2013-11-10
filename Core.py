NationQuantity = 3
RoundLimit = 5
Round = int
Turn = int
NationName = "NationName"
LeaderName = "LeaderName"
print("Turn = "+str(Turn)+" Round = "+str(Round)+" NationName = "+NationName+" LeaderName = "+LeaderName)

for Round in range(1,RoundLimit+1):
    for Turn in range(1,NationQuantity+1):
        print("Round "+str(Round)+", Turn "+str(Turn))
        # (What to do in turn)
