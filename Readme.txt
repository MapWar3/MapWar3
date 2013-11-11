Map War 3

To start the program, run Core.py. The program is currently in development.
The program requires Settings.txt, NationNames.txt and LeaderNames.txt in the same directory as Core.py to run.
Those three files can be edited to change the game, but be careful not to break the format.

What is to be done?
- Map
- Interface
- Division into single player and multi player
- Pick technology rates (5% to 25%) every 5 turns, input for player, random for AIs

The structure of the program is not quite right imo. currently, you have a list of nations, the first of which is the player. then, you compute the income for each turn and round sequentually. this isn't very flexible.

i suggest that the nations be stored as a file after initialization. then, through a gui, the player can create a turn file. ai can create a turn file too, it just doesn't need to be through a gui. (for development purposes, a player's turn file can be created without a gui too of course). then, a processor takes the turn files and applies them to the nation files. we might also decide to add a world file later (a data structure containing all the zones and cities). in that case, it would be initialized along with the nations and modified by the proecessor also.

to get from where we are to where we should be, let us rewrite the core.py file into two separate files. the first part will initialize the nations and create nation files. the second part is the processor (although since we don't have turn files yet, the only thing it has to process is resource amounts.) We'll also create a turnfile creator that...creates turn files. a turn file might store data like what zones are taken and what cities are constructed and what trades are established/broken. the ai will run on an ai.py that uses the turnfile creator to create turns. the gui that the player uses will also use the turnfile creator to create turns. then it is run through the processor.

edit: i've done most of the restructuring as detailed above. i added an order.py. where as processor processes a single turn, order.py will iterate through the rounds and turns and at each round, calls processor. if three is anything that happens once a round rather than once a turn, then there can be a turn_processor which runs every turn and a round_processor which runs every round.


